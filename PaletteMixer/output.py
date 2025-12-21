from __future__ import annotations

import numpy as np
import shutil
from collections import defaultdict
from math import atan2, ceil, sqrt
from pathlib import Path
from PIL import Image, ImageDraw
from typing import List, Dict

from classes import ProcessedColor

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

