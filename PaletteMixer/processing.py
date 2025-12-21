from __future__ import annotations

from classes import ColorDefinition, ProcessedColor


class PaletteProcessor:
    def __init__(self, colors: list[ColorDefinition]):
        self.colors = {c.identifier: c for c in colors}

    def resolve_hex_values(self) -> None:
        """
        Iterates by generation and assigns hex values using pymixbox.
        """
        import mixbox
        from util import hex_to_rgb, rgb_to_hex

        for generation in sorted({c.generation for c in self.colors.values() if c.generation}):
            for color in self.colors.values():
                if color.generation != generation or color.generation == 0:
                    continue
                if color.hex_value is not None or color.mixed_from is None:
                    continue

                parent_a_id, parent_b_id = color.mixed_from
                parent_a = self.colors[parent_a_id]
                parent_b = self.colors[parent_b_id]

                if parent_a.hex_value is None or parent_b.hex_value is None:
                    raise RuntimeError(
                        f"Parent hex missing for {color.identifier}"
                    )

                rgb_a = hex_to_rgb(parent_a.hex_value)
                rgb_b = hex_to_rgb(parent_b.hex_value)

                mixed_rgb = mixbox.lerp(rgb_a, rgb_b, 0.5)

                color.hex_value = rgb_to_hex((mixed_rgb[0], mixed_rgb[1], mixed_rgb[2]))

    def resolve_names(self) -> None:
        """
        Fetch missing names using color.pizza in a single request.
        """
        import requests

        unresolved = [c for c in self.colors.values() if c.name is None]
        if not unresolved:
            return

        hexes = ",".join(c.hex_value.lstrip("#") for c in unresolved if c.hex_value is not None)
        url = "https://api.color.pizza/v1/"

        response = requests.get(
            url,
            params={"values": hexes, "list": "bestOf"},
            timeout=10
        )
        response.raise_for_status()

        data = response.json()["colors"]

        for color_def, api_color in zip(unresolved, data):
            color_def.name = api_color["name"]

    def to_processed_colors(self) -> list[ProcessedColor]:
        """
        Converts fully-resolved ColorDefinitions into ProcessedColor objects.
        """
        from util import hex_to_rgb
        from colour import sRGB_to_XYZ, XYZ_to_Lab
        import numpy as np

        processed: list[ProcessedColor] = []

        for c in self.colors.values():
            if c.hex_value is None or c.name is None:
                raise RuntimeError(
                    f"Color {c.identifier} is not fully resolved"
                )

            rgb = hex_to_rgb(c.hex_value)
            rgb_norm = [v / 255 for v in rgb]

            xyz = sRGB_to_XYZ(rgb_norm)
            lab = np.array(XYZ_to_Lab(xyz))

            processed.append(
                ProcessedColor(
                    identifier=c.identifier,
                    generation=c.generation or 0,
                    hex_value=c.hex_value,
                    rgb=rgb,
                    lab=lab,
                    name=c.name,
                    mixed_from=c.mixed_from,
                )
            )

        return processed

    def reduce_palette(
        self,
        processed: list[ProcessedColor],
        max_colors: int,
        user_defined_ids: set[str],
    ) -> list[ProcessedColor]:
        """
        Reduce palette size using farthest-point sampling (CIEDE2000),
        while keeping all user-defined colors.
        """
        from colour.difference import delta_E_CIE2000

        if len(processed) <= max_colors:
            return processed

        # 1. Split palette
        fixed = [c for c in processed if c.identifier in user_defined_ids]
        candidates = [c for c in processed if c.identifier not in user_defined_ids]

        if len(fixed) > max_colors:
            raise ValueError(
                "Number of user-defined colors exceeds max palette size"
            )

        selected = fixed.copy()

        # Pre-cache Lab arrays for speed
        lab_map = {c.identifier: c.lab for c in processed}

        # 2. Iteratively add farthest colors
        while len(selected) < max_colors and candidates:
            best_candidate = None
            best_distance = -1.0

            for candidate in candidates:
                # Compute distance to closest selected color
                min_dist = min(
                    delta_E_CIE2000(
                        lab_map[candidate.identifier],
                        lab_map[sel.identifier],
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
