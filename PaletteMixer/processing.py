from __future__ import annotations

import mixbox
from itertools import combinations
from classes import ColorDefinition, ProcessedColor, MixProjection
from util import hex_to_rgb, rgb_to_hex
from colour import sRGB_to_XYZ, XYZ_to_Lab
from colour.difference import delta_E_CIE2000
import numpy as np


class PaletteProcessor:
    def __init__(self, colors: list[ColorDefinition]):
        self.colors = {c.identifier: c for c in colors}

    def resolve_hex_values(self) -> None:
        """
        Iterates by generation and assigns hex values using pymixbox.
        """
        for generation in sorted(
            {c.generation for c in self.colors.values() if c.generation}
        ):
            for color in self.colors.values():
                if color.generation != generation or color.generation == 0:
                    continue
                if color.hex_value is not None or color.mixed_from is None:
                    continue

                parent_a_id, parent_b_id = color.mixed_from
                parent_a = self.colors[parent_a_id]
                parent_b = self.colors[parent_b_id]

                if parent_a.hex_value is None or parent_b.hex_value is None:
                    raise RuntimeError(f"Parent hex missing for {color.identifier}")

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

        hexes = ",".join(
            c.hex_value.lstrip("#") for c in unresolved if c.hex_value is not None
        )
        url = "https://api.color.pizza/v1/"

        response = requests.get(
            url,
            params={"values": hexes, "list": "bestOf", "noduplicates": "true"},
            timeout=10,
        )
        response.raise_for_status()

        data = response.json()["colors"]

        for color_def, api_color in zip(unresolved, data):
            color_def.name = api_color["name"]

    def to_processed_colors(self) -> list[ProcessedColor]:
        """
        Converts fully-resolved ColorDefinitions into ProcessedColor objects.
        """
        processed: list[ProcessedColor] = []

        for c in self.colors.values():
            if c.hex_value is None or c.name is None:
                raise RuntimeError(f"Color {c.identifier} is not fully resolved")

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
                    parsed=c.parsed,
                    mixed_from=c.mixed_from,
                )
            )

        return processed

    def reduce_palette(
        self,
        processed: list[ProcessedColor],
        max_colors: int,
    ) -> list[ProcessedColor]:
        """
        Reduce palette size using farthest-point sampling (CIEDE2000),
        while keeping all user-defined colors AND ensuring mix-closure.
        """
        if len(processed) <= max_colors:
            return processed

        fixed = [c for c in processed if c.parsed]
        candidates = [c for c in processed if not c.parsed]

        if len(fixed) > max_colors:
            raise ValueError("Number of user-defined colors exceeds max palette size")

        selected = fixed.copy()

        lab_map = {c.identifier: c.lab for c in processed}

        # ---- Phase 1: geometric reduction ----
        while len(selected) < max_colors and candidates:
            best_candidate = None
            best_distance = -1.0

            for candidate in candidates:
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

        # ---- Phase 2: dependency closure ----
        selected_map = {c.identifier: c for c in selected}
        full_map = {c.identifier: c for c in processed}

        changed = True
        while changed:
            changed = False

            required_ids: set[str] = set()
            for c in selected:
                self._collect_dependencies(c, full_map, required_ids)

            missing = required_ids - selected_map.keys()
            if not missing:
                break

            # Remove least important generated colors (last added, highest generation)
            removable = sorted(
                (c for c in selected if not c.parsed),
                key=lambda c: (c.generation, selected.index(c)),
                reverse=True,
            )

            for missing_id in missing:
                if len(selected) >= max_colors and removable:
                    victim = removable.pop(0)
                    selected.remove(victim)
                    selected_map.pop(victim.identifier)

                dep = full_map[missing_id]
                selected.append(dep)
                selected_map[dep.identifier] = dep
                changed = True

        return selected

    def project_all_mixes(
        self,
        palette: list[ProcessedColor],
    ) -> list[MixProjection]:
        """
        Virtually mix all unordered pairs of palette colors and project each
        mix onto the closest existing palette color using ΔE (CIEDE2000).
        """

        if len(palette) < 2:
            return []

        projections: list[MixProjection] = []

        for a, b in combinations(palette, 2):
            if not a.parsed or not b.parsed:
                continue

            mixed_rgb = mixbox.lerp(a.rgb, b.rgb, 0.5)

            rgb_norm = [v / 255 for v in mixed_rgb]

            xyz = sRGB_to_XYZ(rgb_norm)
            mixed_lab = np.array(XYZ_to_Lab(xyz))

            best_id: str | None = None
            best_delta: float = float("inf")

            for candidate in palette:
                d = float(delta_E_CIE2000(mixed_lab, candidate.lab))
                if d < best_delta:
                    best_delta = d
                    best_id = candidate.identifier

            projections.append(
                MixProjection(
                    source_a=a.identifier,
                    source_b=b.identifier,
                    projected=best_id or "UNDEFINED",
                    delta_e=best_delta,
                )
            )

        return projections

    def _collect_dependencies(
        self,
        color: ProcessedColor,
        color_map: dict[str, ProcessedColor],
        acc: set[str],
    ) -> None:
        if not color.mixed_from:
            return

        for parent_id in color.mixed_from:
            if parent_id in acc:
                continue

            acc.add(parent_id)
            parent = color_map[parent_id]
            self._collect_dependencies(parent, color_map, acc)
