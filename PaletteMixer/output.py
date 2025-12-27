from __future__ import annotations

import numpy as np
import shutil
from collections import defaultdict
from math import atan2, ceil, sqrt
from pathlib import Path
from PIL import Image, ImageDraw
from typing import List, Dict, Iterable

from classes import ProcessedColor, MixProjection

ICON_SIZE = 16
ICON_PATH = Path("resources/icons")


class PaletteImageExporter:
    """
    Responsible for exporting a palette of ProcessedColor objects
    into an image representation.
    """

    def __init__(self, swatch_size: int = 64) -> None:
        self.swatch_size = swatch_size

    @staticmethod
    def _hue_angle(lab: np.ndarray) -> float:
        # lab = [L*, a*, b*]
        a = lab[1]
        b = lab[2]
        return atan2(b, a)

    @staticmethod
    def _sort_colors(colors: List[ProcessedColor]) -> List[ProcessedColor]:
        """
        Sort colors by perceptual lightness and hue (Lab space).
        """

        if len(colors) <= 1:
            return colors

        return sorted(
            colors,
            key=lambda c: (
                PaletteImageExporter._hue_angle(c.lab),
                c.lab[0],
            ),
        )

    def export_png(
        self,
        colors: List[ProcessedColor],
        output_path: Path,
    ) -> None:
        """
        Export the given colors as a PNG palette image.
        """

        if not colors:
            raise ValueError("Cannot export an empty color palette")

        sorted_colors = self._sort_colors(colors)

        n = len(sorted_colors)
        cols = ceil(sqrt(n))
        rows = ceil(n / cols)

        width = cols * self.swatch_size
        height = rows * self.swatch_size

        image = Image.new("RGB", (width, height))
        draw = ImageDraw.Draw(image)

        for index, color in enumerate(sorted_colors):
            row = index // cols
            col = index % cols

            x0 = col * self.swatch_size
            y0 = row * self.swatch_size
            x1 = x0 + self.swatch_size
            y1 = y0 + self.swatch_size

            draw.rectangle(
                [x0, y0, x1, y1],
                fill=color.rgb,
            )

        output_path.parent.mkdir(parents=True, exist_ok=True)
        image.save(output_path, format="PNG")


class PaletteMarkdownExporter:
    """
    Exports a palette of ProcessedColor objects into a Markdown document.
    """

    def export(
        self,
        colors: List[ProcessedColor],
        output_path: Path,
    ) -> None:
        if not colors:
            raise ValueError("Cannot export an empty palette")

        lookup = {color.identifier: color for color in colors}
        grouped = self._group_by_generation(colors)
        markdown = self._render_markdown(grouped, lookup)

        output_path.parent.mkdir(parents=True, exist_ok=True)
        output_path.write_text(markdown, encoding="utf-8")

    @staticmethod
    def _group_by_generation(
        colors: List[ProcessedColor],
    ) -> Dict[int, List[ProcessedColor]]:
        groups: Dict[int, List[ProcessedColor]] = defaultdict(list)

        for color in colors:
            groups[color.generation].append(color)

        # Ensure deterministic ordering
        for generation in groups:
            groups[generation].sort(key=lambda c: c.name.lower())

        return dict(sorted(groups.items()))

    def _render_markdown(
        self,
        grouped: Dict[int, List[ProcessedColor]],
        lookup: Dict[str, ProcessedColor],
    ) -> str:
        lines: List[str] = []

        for generation, colors in grouped.items():
            count = len(colors)
            lines.append(
                f"# Generation {generation} ({count} color{'s' if count != 1 else ''})"
            )
            lines.append("")

            for color in colors:
                lines.extend(self._render_color(color, lookup))
                lines.append("")

        return "\n".join(lines).rstrip() + "\n"

    def _render_color(
        self,
        color: ProcessedColor,
        lookup: Dict[str, ProcessedColor],
    ) -> List[str]:
        lines: List[str] = []

        # 1️⃣ Export icon
        icon_path = self._export_color_icon(color)

        # 2️⃣ Heading with icon
        lines.append(f"## ![{color.name}]({icon_path}) {color.name}")

        # 3️⃣ Existing details
        lines.append(f"- **Hex:** `{color.hex_value}`")
        lines.append(f"- **RGB:** `{color.rgb}`")
        lines.append(
            f"- **Lab:** `({color.lab[0]:.2f}, {color.lab[1]:.2f}, {color.lab[2]:.2f})`"
        )

        if color.mixed_from is None:
            lines.append("- **Mixed from:** _Base color_")
        else:
            lines.append("- **Mixed from:**")
            for parent_id in color.mixed_from:
                parent = lookup.get(parent_id)
                if parent is None:
                    lines.append(f"  - ⚠ Unknown color `{parent_id}`")
                else:
                    # Export parent icon if not already
                    parent_icon = self._export_color_icon(parent)
                    lines.append(
                        f"  - ![{parent.name}]({parent_icon}) {parent.name} (`{parent.hex_value}`)"
                    )

        return lines

    def _export_color_icon(self, color: ProcessedColor) -> str:
        """
        Create a 16x16 PNG icon for a single color if it doesn't already exist.
        Returns the relative path to the icon.
        """
        # Ensure folder is prepared once
        if not hasattr(self, "_icons_prepared"):
            if ICON_PATH.exists():
                shutil.rmtree(ICON_PATH)
            ICON_PATH.mkdir(parents=True, exist_ok=True)
            self._icons_prepared = True

        icon_file = ICON_PATH / f"{color.identifier}.png"

        # Only generate if file doesn't exist
        if not icon_file.exists():
            img = Image.new("RGB", (ICON_SIZE, ICON_SIZE), color.rgb)
            img.save(icon_file, format="PNG")

        return icon_file.as_posix().removeprefix("resources/")

class PaletteMixProjectionExporter:
    """
    Exports virtual color-mix projections into a readable Markdown document.
    """

    def __init__(
        self,
        output_path: Path,
    ) -> None:
        self.output_path = output_path
        self.icon_dir = ICON_PATH

    def export(
        self,
        colors: Iterable[ProcessedColor],
        projections: Iterable[MixProjection],
    ) -> None:
        """
        Export mix projection data to Markdown.

        Parameters
        ----------
        colors:
            Mapping from color_id -> ProcessedColor
        projections:
            Iterable of MixProjection results
        """
        grouped = self._group_by_target(projections)
        summary = self._compute_summary(projections)

        lines: List[str] = []
        c = {c.identifier: c for c in colors}
        lines.extend(self._render_header(summary))
        lines.extend(self._render_targets(grouped, c))
        lines.extend(self._render_worst_cases(projections, c))

        self.output_path.parent.mkdir(parents=True, exist_ok=True)
        self.output_path.write_text("\n".join(lines), encoding="utf-8")

    def _group_by_target(
        self,
        projections: Iterable[MixProjection],
    ) -> Dict[str, List[MixProjection]]:
        grouped: Dict[str, List[MixProjection]] = defaultdict(list)

        for p in projections:
            grouped[p.projected].append(p)

        # sort each group by increasing ΔE
        for lst in grouped.values():
            lst.sort(key=lambda p: p.delta_e)

        return dict(grouped)

    def _compute_summary(
        self,
        projections: Iterable[MixProjection],
    ) -> dict:
        projections = list(projections)

        delta_es = [p.delta_e for p in projections]

        return {
            "palette_size": len(set(p.projected for p in projections)),
            "total_combinations": len(projections),
            "avg_delta_e": sum(delta_es) / len(delta_es) if delta_es else 0.0,
            "max_delta_e": max(delta_es) if delta_es else 0.0,
        }

    def _render_header(self, summary: dict) -> List[str]:
        return [
            "# 🔀 Color Mix Projections",
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

    def _render_targets(
        self,
        grouped: Dict[str, List[MixProjection]],
        colors: Dict[str, ProcessedColor],
    ) -> List[str]:
        lines: List[str] = []
        lines.append("## 🎯 Projection Targets")
        lines.append("")

        for target_id, projections in sorted(
            grouped.items(),
            key=lambda item: len(item[1]),
            reverse=True,
        ):
            target = colors[target_id]

            icon = self._icon_md(target)
            lines.append(f"### {icon} {target.name}")
            lines.append("")
            lines.append("| Mix | ΔE |")
            lines.append("|-----|----|")

            for p in projections:
                a = colors[p.source_a]
                b = colors[p.source_b]

                mix = (
                    f"{self._icon_md(a)} {a.name} + "
                    f"{self._icon_md(b)} {b.name}"
                )

                lines.append(f"| {mix} | {p.delta_e:.2f} |")

            lines.append("")

        return lines

    def _render_worst_cases(
        self,
        projections: Iterable[MixProjection],
        colors: Dict[str, ProcessedColor],
        limit: int = 10,
    ) -> List[str]:
        worst = sorted(projections, key=lambda p: p.delta_e, reverse=True)[:limit]

        lines = [
            "## 🚨 Largest Deviations",
            "",
            "| Mix | Projected To | ΔE |",
            "|----|-------------|----|",
        ]

        for p in worst:
            a = colors[p.source_a]
            b = colors[p.source_b]
            target = colors[p.projected]

            mix = f"{self._icon_md(a)} {a.name} + {self._icon_md(b)} {b.name}"
            proj = f"{self._icon_md(target)} {target.name}"

            lines.append(f"| {mix} | {proj} | {p.delta_e:.2f} |")

        lines.append("")
        return lines

    def _icon_md(self, color: ProcessedColor) -> str:
        icon_path = self.icon_dir / f"{color.identifier}.png"
        return f"![{color.name}]({icon_path.as_posix()})"
