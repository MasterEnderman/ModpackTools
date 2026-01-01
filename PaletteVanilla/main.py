#!/usr/bin/env python3
"""
Palette generation and reduction tool.

Directory structure:
- resources/input.yml
- resources/icons/
- resources/output.md
- main.py

Usage:
    uv run python main.py --size 16
"""

from __future__ import annotations

import argparse
import itertools
import pathlib
from dataclasses import dataclass, field
from colour import sRGB_to_XYZ, XYZ_to_Lab
from colour.difference import delta_E_CIE2000
from typing import Dict, List, Optional, Tuple

import math
import mixbox
import numpy as np
import requests
import shutil
import yaml
from PIL import Image, ImageDraw


# ---------------------------------------------------------------------------
# Constants & Paths
# ---------------------------------------------------------------------------

ROOT = pathlib.Path(__file__).parent
RESOURCES = ROOT / "resources"
ICON_DIR = RESOURCES / "icons"
INPUT_YAML = RESOURCES / "input.yml"
OUTPUT_MD = RESOURCES / "output.md"
OUTPUT_PNG = RESOURCES / "palette.png"

COLOR_PIZZA_API = "https://api.color.pizza/v1/"


# ---------------------------------------------------------------------------
# Utility functions
# ---------------------------------------------------------------------------


def clamp(v: float, lo: float = 0.0, hi: float = 1.0) -> float:
    """Clamp a float into a given range."""
    return max(lo, min(hi, v))


# ---------------------------------------------------------------------------
# Color class
# ---------------------------------------------------------------------------


@dataclass(slots=True)
class Color:
    """
    Represents a color and all derived metadata.

    This class is the single source of truth for:
    - color space conversions
    - ΔE computation
    - icon generation
    """

    key: str
    hex: str
    gen: int
    parsed: bool
    mixed_from: Tuple[str, ...] = field(default_factory=tuple)

    # runtime metadata
    resolved_name: Optional[str] = None

    # ------------------------------------------------------------------

    def rgb01(self) -> Tuple[float, float, float]:
        """Return RGB values in range [0,1]."""
        rgb_tuple = [v / 255 for v in self.rgb255()]
        return (rgb_tuple[0], rgb_tuple[1], rgb_tuple[2])

    def rgb255(self) -> Tuple[int, int, int]:
        """Return RGB values in range [0,255]."""
        hex_str = self.hex.lstrip("#")
        tup = tuple(int(hex_str[i : i + 2], 16) for i in (0, 2, 4))
        return (tup[0], tup[1], tup[2])

    # ------------------------------------------------------------------

    def lab(self) -> np.ndarray:
        """Return LAB values."""
        xyz = sRGB_to_XYZ(self.rgb01())
        return np.array(XYZ_to_Lab(xyz))

    # ------------------------------------------------------------------

    def mix(self, other: "Color") -> "Color":
        """
        Mix two colors using mixbox.
        """
        r1, r2 = self.rgb255(), other.rgb255()
        mixed = mixbox.lerp(r1, r2, 0.5)
        hex_color = "#{:02X}{:02X}{:02X}".format(*mixed)

        return Color(
            key=f"{self.key}+{other.key}",
            hex=hex_color,
            gen=max(self.gen, other.gen) + 1,
            mixed_from=(self.key, other.key),
            parsed=False,
        )

    # ------------------------------------------------------------------

    def write_icon(self, path: pathlib.Path, size: int = 16) -> None:
        """Write a n x n PNG icon for the color."""
        path.parent.mkdir(parents=True, exist_ok=True)
        img = Image.new("RGB", (size, size), self.rgb255())
        img.save(path, "PNG")

    # ------------------------------------------------------------------
    # Hashing & equality (identity-based)
    # ------------------------------------------------------------------

    def __hash__(self) -> int:
        """Allow Color to be used in sets and dict keys."""
        return hash(self.key)

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, Color):
            return NotImplemented
        return self.key == other.key


@dataclass(frozen=True)
class MixProjection:
    """
    Represents the result of virtually mixing two palette colors and
    projecting the result onto the closest existing palette color.
    """

    source_a: str
    source_b: str
    delta_e: float


# ---------------------------------------------------------------------------
# Parsing & palette creation
# ---------------------------------------------------------------------------


def load_colors(path: pathlib.Path) -> Dict[str, Color]:
    """Load base colors from YAML."""
    with path.open("r", encoding="utf-8") as f:
        raw = yaml.safe_load(f)

    colors: Dict[str, Color] = {}
    for key, data in raw["colors"].items():
        colors[key] = Color(
            key=key,
            hex=data["hex"],
            gen=data["gen"],
            mixed_from=tuple(data.get("mixed_from", [])),
            resolved_name=key.replace("_", " ").title(),
            parsed=True,
        )
    return colors


def build_full_palette(base: Dict[str, Color]) -> List[Color]:
    """
    Generate all possible color combinations.
    """
    palette = list(base.values())
    existing_mixes = [c.mixed_from for c in base.values()]

    for a, b in itertools.combinations(base.values(), 2):
        if (a.key, b.key) in existing_mixes or (b.key, a.key) in existing_mixes:
            continue
        palette.append(a.mix(b))

    return palette


# ---------------------------------------------------------------------------
# Palette reduction
# ---------------------------------------------------------------------------


def reduce_palette(
    palette: List[Color],
    max_size: int,
) -> List[Color]:
    """
    Reduce palette size using farthest-point sampling (CIEDE2000),
    while keeping all user-defined colors AND ensuring mix-closure.
    """
    if len(palette) <= max_size:
        return palette

    fixed = [c for c in palette if c.parsed]
    candidates = [c for c in palette if not c.parsed]

    if len(fixed) > max_size:
        raise ValueError("Number of user-defined colors exceeds max palette size")

    selected = fixed.copy()

    lab_map = {c.key: c.lab() for c in palette}

    while len(selected) < max_size and candidates:
        best_candidate = None
        best_distance = -1.0

        for candidate in candidates:
            min_dist = min(
                delta_E_CIE2000(
                    lab_map[candidate.key],
                    lab_map[sel.key],
                )
                for sel in selected
            )

            if min_dist > best_distance:
                best_distance = min_dist
                best_candidate = candidate

        if best_candidate:
            selected.append(best_candidate)
            candidates.remove(best_candidate)
    return selected


def project_all_mixes(
    palette: List[Color],
) -> Dict[str, List[MixProjection]]:
    """
    Virtually mix all unordered pairs of palette colors and project each
    mix onto the closest existing palette color using ΔE (CIEDE2000).
    """

    if len(palette) < 2:
        return {}

    projections: Dict[str, List[MixProjection]] = {}

    for a, b in itertools.combinations(palette, 2):
        if not a.parsed or not b.parsed:
            continue

        color = a.mix(b)
        mixed_lab = color.lab()

        best_id: Optional[str] = None
        best_delta: float = float("inf")

        for candidate in palette:
            if (
                candidate.mixed_from
                and a.key in candidate.mixed_from
                and b.key in candidate.mixed_from
            ):
                best_delta = 0.0
                best_id = candidate.key
                break
            d = float(delta_E_CIE2000(mixed_lab, candidate.lab()))
            if d < best_delta:
                best_delta = d
                best_id = candidate.key

        id = best_id or "UNDEFINED"
        projections[id] = projections.get(id, [])
        projections[id].append(
            MixProjection(
                source_a=a.key,
                source_b=b.key,
                delta_e=best_delta,
            )
        )

    return projections


# ---------------------------------------------------------------------------
# Markdown export
# ---------------------------------------------------------------------------


def export_markdown(
    colors: List[Color], projections: Dict[str, List[MixProjection]]
) -> None:
    """Export final palette to markdown."""

    def camel_case(s: str) -> str:
        return "".join(
            word.capitalize()
            for word in s.strip()
            .replace("’", "")
            .replace("ä", "ae")
            .replace("ö", "oe")
            .replace("ü", "ue")
            .split(" ")
        )

    temp_gen: int = -1

    delta_es = [p.delta_e for p in itertools.chain.from_iterable(projections.values())]
    lookup = {c.key: c for c in colors}

    summary = {
        "palette_size": len(colors),
        "total_combinations": len(delta_es) + len([c for c in colors if c.parsed]),
        "avg_delta_e": sum(delta_es) / len(delta_es) if delta_es else 0.0,
        "max_delta_e": max(delta_es) if delta_es else 0.0,
    }

    lines: List[str] = [
        "# 🔀 Vanilla Palette Color Mix Projections",
        "",
        "This document shows *virtual* 50/50 mix results projected onto the closest existing palette color.",
        "",
        "## 📊 Summary",
        "",
        f"- Palette size: **{summary['palette_size']} colors**",
        f"- Total mix combinations: **{summary['total_combinations']}**",
        f"- Average ΔE (CIEDE2000): **{summary['avg_delta_e']:.2f}**",
        f"- Worst-case ΔE: **{summary['max_delta_e']:.2f}**",
        "",
    ]

    shutil.rmtree(ICON_DIR, ignore_errors=True)
    for c in sorted(colors, key=lambda x: x.gen):
        icon_path = ICON_DIR / f"{c.key}.png"
        c.write_icon(icon_path)

        if c.gen != temp_gen:
            temp_gen = c.gen
            gen_count = len([c for c in colors if c.gen == temp_gen])
            lines.append(
                f"## Generation {c.gen} ({gen_count} color{'s' if gen_count != 1 else ''})\n"
            )

        name = c.resolved_name or c.key
        lines.append(
            f"### ![{camel_case(name)}]({icon_path.as_posix().split('resources/')[-1]}) {name}"
        )
        lines.append(f"- **Hex:** ` {c.hex} `")
        lines.append(f"- **RGB:** ` {c.rgb255()} `")
        lines.append(
            f"- **Lab:** ` ({c.lab()[0]:.2f}, {c.lab()[1]:.2f}, {c.lab()[2]:.2f}) `"
        )

        if c.gen == 0:
            lines.append("- **Mixed from:** _Base color_")
        else:
            lines.append("- **Mixed from:**")
            for parent_id in c.mixed_from:
                parent = lookup.get(parent_id)
                if parent is None:
                    lines.append(f"  - ⚠ Unknown color `{parent_id}`")
                else:
                    parent_name = camel_case(parent.resolved_name or parent.key)
                    parent_icon = ICON_DIR / f"{parent.key}.png"
                    parent_path = parent_icon.as_posix().split("resources/")[-1]
                    lines.append(
                        f"  - ![{parent_name}]({parent_path}) {parent_name} (` {parent.hex} `)"
                    )

        if c.key in projections:
            lines.append("\n**Projections:**\n```js")
            lines.append(f"// {camel_case(name)}")
            for combination in sorted(projections[c.key], key=lambda x: x.delta_e):
                delta = f"{combination.delta_e:.2f}"
                c_a = camel_case(
                    lookup[combination.source_a].resolved_name or combination.source_a
                )
                c_b = camel_case(
                    lookup[combination.source_b].resolved_name or combination.source_b
                )
                lines.append(
                    f"/* {delta.rjust(5)} */ {camel_case(name)}.addMix([{c_a}, {c_b}]);"
                )
            lines.append("```")

        lines.append("")

    OUTPUT_MD.write_text("\n".join(lines), encoding="utf-8")


# ---------------------------------------------------------------------------
# Color name resolution
# ---------------------------------------------------------------------------


def resolve_color_names(colors: List[Color]) -> None:
    """
    Resolve color names for all colors using a single color.pizza API call.
    """
    if not colors:
        return

    hex_values = ",".join(c.hex.lstrip("#") for c in colors)

    try:
        response = requests.get(
            COLOR_PIZZA_API,
            params={"values": hex_values, "list": "bestOf", "noduplicates": "true"},
            timeout=10,
        )
        response.raise_for_status()
        data = response.json()["colors"]

        for color, payload in zip(colors, data):
            color.resolved_name = color.resolved_name or payload.get("name", color.key)

    except Exception:
        # graceful fallback
        for color in colors:
            print(f"Warning: failed to resolve name for {color.key}")
            color.resolved_name = color.key


# ---------------------------------------------------------------------------
# Image export
# ---------------------------------------------------------------------------


def export_png(
    colors: List[Color],
    swatch_size: int = 64,
) -> None:
    """
    Export the given colors as a PNG palette image.
    """

    def hue_angle(lab: np.ndarray) -> float:
        # lab = [L*, a*, b*]
        a = lab[1]
        b = lab[2]
        return math.atan2(b, a)

    def sort_colors(colors: List[Color]) -> List[Color]:
        """
        Sort colors by perceptual lightness and hue (Lab space).
        """

        if len(colors) <= 1:
            return colors

        return sorted(
            colors,
            key=lambda c: (
                hue_angle(c.lab()),
                c.lab()[0],
            ),
        )

    if not colors:
        raise ValueError("Cannot export an empty color palette")

    sorted_colors = sort_colors(colors)

    n = len(sorted_colors)
    cols = math.ceil(math.sqrt(n))
    rows = math.ceil(n / cols)

    width = cols * swatch_size
    height = rows * swatch_size

    image = Image.new("RGB", (width, height))
    draw = ImageDraw.Draw(image)

    for index, color in enumerate(sorted_colors):
        row = index // cols
        col = index % cols

        x0 = col * swatch_size
        y0 = row * swatch_size
        x1 = x0 + swatch_size
        y1 = y0 + swatch_size

        draw.rectangle(
            [x0, y0, x1, y1],
            fill=color.rgb255(),
        )

    OUTPUT_PNG.parent.mkdir(parents=True, exist_ok=True)
    image.save(OUTPUT_PNG, format="PNG")


# ---------------------------------------------------------------------------
# Main entry point
# ---------------------------------------------------------------------------


def main() -> None:
    """CLI entry point."""
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--size",
        type=int,
        required=True,
        help="Maximum palette size",
    )
    args = parser.parse_args()

    base = load_colors(INPUT_YAML)
    full_palette = build_full_palette(base)

    reduced = reduce_palette(
        palette=full_palette,
        max_size=args.size,
    )

    resolve_color_names(reduced)

    projections = project_all_mixes(list(reduced))

    export_markdown(reduced, projections)
    export_png(reduced)


if __name__ == "__main__":
    main()
