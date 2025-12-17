from __future__ import annotations

import argparse
import math
import mixbox
from dataclasses import dataclass
from enum import Enum
from pathlib import Path
from typing import List, Tuple

import numpy as np
import requests
from PIL import Image
import colour
import re


# ============================================================
# Mix modes
# ============================================================

class MixMode(str, Enum):
    AVERAGE = "average"
    ADD = "add"
    MULTIPLY = "multiply"
    MIXBOX = "mixbox"


# ============================================================
# Color model
# ============================================================

@dataclass(frozen=True)
class Color:
    hex_value: str
    rgb: Tuple[int, int, int]
    lab: np.ndarray
    name: str | None = None
    mixed_from: Tuple[str, str] | None = None
    mixed_from_name: Tuple[str, str] | None = None

    @staticmethod
    def _rgb_to_lab(rgb: Tuple[int, int, int]) -> np.ndarray:
        # Normalize RGB to 0–1
        rgb_norm = np.array(rgb) / 255.0

        # Convert sRGB → XYZ → Lab
        xyz = colour.sRGB_to_XYZ(rgb_norm)
        lab = colour.XYZ_to_Lab(xyz)

        return lab

    @staticmethod
    def from_hex(hex_value: str) -> Color:
        hex_value = hex_value.upper()
        r = int(hex_value[1:3], 16)
        g = int(hex_value[3:5], 16)
        b = int(hex_value[5:7], 16)

        rgb = (r, g, b)
        lab = Color._rgb_to_lab(rgb)

        return Color(hex_value, rgb, lab)

    @staticmethod
    def from_rgb(rgb: Tuple[int, int, int], mixed_from: Tuple[str, str] | None = None, mixed_from_name: Tuple[str, str] | None = None) -> Color:
        hex_value = f"#{rgb[0]:02X}{rgb[1]:02X}{rgb[2]:02X}".upper()
        lab = Color._rgb_to_lab(rgb)
        return Color(hex_value, rgb, lab, mixed_from=mixed_from, mixed_from_name=mixed_from_name)


# ============================================================
# Input
# ============================================================

class ColorLoader:
    COLOR_LINE_RE = re.compile(
        r"""
        ^
        \s*
        (?P<hex>\#[0-9A-Fa-f]{6})
        (?:\s*\((?P<name>[^)]+)\))?
        \s*$
        """,
        re.VERBOSE,
    )

    @staticmethod
    def load(path: Path) -> List[Color]:
        colors: List[Color] = []

        for lineno, raw_line in enumerate(path.read_text().splitlines(), start=1):
            line = raw_line.strip()

            if not line or line.startswith("//"):
                continue

            match = ColorLoader.COLOR_LINE_RE.match(line)
            if not match:
                print(f"[info] Ignoring malformed line {lineno}: {raw_line}")
                continue

            hex_value = match.group("hex").upper()
            name = match.group("name")

            color = Color.from_hex(hex_value)
            if name:
                color = Color(
                    hex_value=color.hex_value,
                    rgb=color.rgb,
                    lab=color.lab,
                    name=name,
                )

            colors.append(color)

        return colors


# ============================================================
# Color combining
# ============================================================

class ColorCombiner:
    @staticmethod
    def _mix_rgb(
        a: tuple[int, int, int],
        b: tuple[int, int, int],
        mode: MixMode,
        ratio: float,
    ) -> tuple[int, int, int]:

        if mode == MixMode.AVERAGE:
            return (
                (a[0] + b[0]) // 2,
                (a[1] + b[1]) // 2,
                (a[2] + b[2]) // 2,
            )

        if mode == MixMode.ADD:
            return (
                min(a[0] + b[0], 255),
                min(a[1] + b[1], 255),
                min(a[2] + b[2], 255),
            )

        if mode == MixMode.MULTIPLY:
            return (
                (a[0] * b[0]) // 255,
                (a[1] * b[1]) // 255,
                (a[2] * b[2]) // 255,
            )

        if mode == MixMode.MIXBOX:
            c = mixbox.lerp(a, b, ratio)
            return (c[0], c[1], c[2])

        raise ValueError(f"Unsupported mix mode: {mode}")

    @staticmethod
    def combine(colors: List[Color], mode: MixMode, ratio: float) -> List[Color]:

        combined: dict[str, Color] = {}

        for i in range(len(colors)):
            for j in range(i + 1, len(colors)):
                c1 = colors[i]
                c2 = colors[j]

                mixed_rgb = ColorCombiner._mix_rgb(
                    c1.rgb,
                    c2.rgb,
                    mode,
                    ratio,
                )

                color = Color.from_rgb(
                    mixed_rgb,
                    mixed_from=(c1.hex_value, c2.hex_value),
                    mixed_from_name=(c1.name, c2.name) if c1.name and c2.name else None,
                )
                combined[color.hex_value] = color

        return list(combined.values())


# ============================================================
# Palette selection (ΔE2000)
# ============================================================

class DeltaESelector:
    def __init__(
        self,
        base_colors: List[Color],
        candidates: List[Color]
    ) -> None:
        self.selected: List[Color] = base_colors[:]
        self.candidates: List[Color] = [
            c for c in candidates if c not in self.selected
        ]

    def _min_distance(self, color: Color) -> float:
        distances = [
            colour.delta_E(
                color.lab,
                sel.lab,
                method="CIE 2000"
            )
            for sel in self.selected
        ]
        return float(min(distances))

    def select(self, target_size: int) -> List[Color]:
        while len(self.selected) < target_size and self.candidates:
            best = max(
                self.candidates,
                key=lambda c: self._min_distance(c)
            )
            self.selected.append(best)
            self.candidates.remove(best)

        return self.selected


# ============================================================
# Color naming (color.pizza)
# ============================================================

class ColorNamer:
    API_URL = "https://api.color.pizza/v1/"

    @staticmethod
    def name(colors: List[Color]) -> List[Color]:
        hexes = ",".join(c.hex_value.lstrip("#") for c in colors)

        response = requests.get(
            ColorNamer.API_URL,
            params={"values": hexes, "list": "bestOf"},
            timeout=10
        )
        response.raise_for_status()

        data = response.json()["colors"]

        named: List[Color] = []
        for color, api_color in zip(colors, data):
            if color.name is not None:
                named.append(color)
                continue
            named.append(
                Color(
                    hex_value=color.hex_value,
                    rgb=color.rgb,
                    lab=color.lab,
                    name=api_color["name"],
                    mixed_from=color.mixed_from,
                    mixed_from_name=color.mixed_from_name,
                )
            )

        return named


# ============================================================
# Output
# ============================================================

class PaletteRenderer:
    TILE_SIZE = 32

    @staticmethod
    def render(colors: List[Color], path: Path) -> None:
        cols = math.ceil(math.sqrt(len(colors)))
        rows = math.ceil(len(colors) / cols)

        image = Image.new(
            "RGB",
            (cols * PaletteRenderer.TILE_SIZE,
             rows * PaletteRenderer.TILE_SIZE)
        )

        for idx, color in enumerate(colors):
            x = (idx % cols) * PaletteRenderer.TILE_SIZE
            y = (idx // cols) * PaletteRenderer.TILE_SIZE

            tile = Image.new(
                "RGB",
                (PaletteRenderer.TILE_SIZE, PaletteRenderer.TILE_SIZE),
                color.rgb
            )
            image.paste(tile, (x, y))

        image.save(path)


class PaletteWriter:
    @staticmethod
    def write(colors: List[Color], path: Path) -> None:
        with path.open("w") as f:
            for c in colors:
                line = f"{c.hex_value} {c.name}\n"

                if c.mixed_from and c.mixed_from_name:
                    for i in range(len(c.mixed_from)):
                        line += f"  - {c.mixed_from[i]} ({c.mixed_from_name[i]})\n"
                f.write(line)


# ============================================================
# Base usage enforcement
# ============================================================

class BaseUsageEnforcer:
    def __init__(
        self,
        base_colors: list[Color],
        mixed_colors: list[Color],
    ) -> None:
        self.base_colors = base_colors
        self.mixed_colors = mixed_colors

    def enforce(self, palette: list[Color]) -> list[Color]:
        # Early exits
        if not self.mixed_colors:
            return palette

        mixed_in_palette = [
            c for c in palette if c.mixed_from is not None
        ]
        if not mixed_in_palette:
            return palette

        missing = self._missing_base_colors(palette)
        if not missing:
            return palette

        print(f"[info] The following base colors are missing: {[c.name for c in missing]}.")
        print(f"[info] Ensuring base usage for {len(missing)} base color(s)...")

        # Remove last X removable colors
        removable = self._removable_colors(palette)
        to_remove = removable[-len(missing):]

        for c in to_remove:
            palette.remove(c)
            print(f"[info] Removed {c.name} from palette to make room for base colors.")

        # Add best candidates for each missing base color
        for base in missing:
            candidate = self._best_candidate_for_base(base, palette)
            if candidate is None:
                print(
                    f"[warn] No mixed color available for base {base.hex_value}!"
                )
                continue

            palette.append(candidate)

        return palette

    def _missing_base_colors(self, palette: list[Color]) -> list[Color]:
        missing: list[Color] = []

        for base in self.base_colors:
            base_hex = base.hex_value.lstrip("#").upper()

            used = any(
                c.mixed_from
                and any(
                    base_hex == h.lstrip("#").upper()
                    for h in c.mixed_from
                )
                for c in palette
            )

            if not used:
                missing.append(base)

        return missing

    def _removable_colors(self, palette: list[Color]) -> list[Color]:
        base_hexes = {b.hex_value for b in self.base_colors}

        # Only non-base colors are removable
        return [
            c for c in palette
            if c.hex_value not in base_hexes
        ]

    def _best_candidate_for_base(
        self,
        base: Color,
        palette: list[Color],
    ) -> Color | None:
        candidates = [
            c for c in self.mixed_colors
            if c.mixed_from
            and base.hex_value in c.mixed_from
            and c not in palette
        ]

        if not candidates:
            return None

        def min_distance(color: Color) -> float:
            return float(min(
                colour.delta_E(
                    color.lab,
                    sel.lab,
                    method="CIE 2000"
                )
                for sel in palette
            ))

        return max(candidates, key=min_distance)


# ============================================================
# Main
# ============================================================

def main() -> None:
    parser = argparse.ArgumentParser(
        description="Generate perceptually distinct color palettes using ΔE2000."
    )
    parser.add_argument("--size", type=int, required=True)
    parser.add_argument(
        "--no-combine",
        action="store_true",
        help="Disable generation of combined colors"
    )
    parser.add_argument(
        "--mix-mode",
        type=MixMode,
        choices=list(MixMode),
        default=MixMode.MIXBOX,
        help="Color mix mode"
    )
    parser.add_argument(
        "--mix-ratio",
        type=float,
        default=0.5,
        help="Mix ratio for mixbox mode (0.0–1.0)"
    )
    parser.add_argument(
        "--ensure-base-usage",
        action="store_true",
        help="Ensure every base color is used at least once in mixed colors"
    )

    args = parser.parse_args()

    base_colors = ColorLoader.load(Path("colors.txt"))

    if args.size < len(base_colors):
        raise ValueError(
            "Target size must be >= number of base colors"
        )
    
    if not 0.0 <= args.mix_ratio <= 1.0:
        raise ValueError("--mix-ratio must be between 0.0 and 1.0")

    if args.no_combine:
        all_colors = base_colors
        combined_colors = []
    else:
        combined_colors = ColorCombiner.combine(
            base_colors,
            args.mix_mode,
            args.mix_ratio,
        )
        all_colors = base_colors + combined_colors

    selector = DeltaESelector(
        base_colors=base_colors,
        candidates=all_colors
    )

    palette = selector.select(args.size)

    if args.ensure_base_usage and not args.no_combine:
        enforcer = BaseUsageEnforcer(
            base_colors=base_colors,
            mixed_colors=combined_colors,
        )
        palette = enforcer.enforce(palette)
        print(f"[info] Ensured base usage for {len(palette)} colors.")

    palette = ColorNamer.name(palette)

    PaletteRenderer.render(palette, Path("palette.png"))
    PaletteWriter.write(palette, Path("palette.txt"))

    print(f"[info] Generated palette with {len(palette)} colors.")


if __name__ == "__main__":
    main()
