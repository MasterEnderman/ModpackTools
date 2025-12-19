from itertools import combinations, chain
from typing import Dict, Set, List, Optional
from input import ColorDefinition

class ColorGenerator:
    """
    Generates ColorDefinition objects for all possible combinations of colors,
    generation by generation, excluding colors already defined in the input YAML.
    Each generated color has exactly two parents (mixed_from tuple).
    """

    def __init__(self, existing_colors: Dict[str, ColorDefinition], max_depth: int):
        self.existing_colors = existing_colors
        self.max_depth = max_depth
        self.generations: Dict[int, List[ColorDefinition]] = {}

    def generate_all(self) -> List[ColorDefinition]:
        """
        Generate all possible colors, including all generations.

        Returns:
            List of ColorDefinition objects.
        """
        self.generations[0] = [
            ColorDefinition(c.identifier, c.name, c.hex_value, c.mixed_from, 0)
            for c in self.existing_colors.values() if c.mixed_from is None
        ]

        for generation in range(1, self.max_depth + 1):
            self._generate_generation(generation)

        return list(chain.from_iterable(self.generations.values()))

    def _generate_generation(self, generation: int) -> None:
        """
        Generate all possible colors for a given generation.

        Args:
            generation: Generation ID.
        """
        if generation in self.generations:
            return

        self.generations[generation] = []

        for combo in combinations(chain.from_iterable(self.generations.values()), 2):
            tup = (combo[0].identifier, combo[1].identifier)
            yml = self._get_from_yaml(tup)

            if any(c.mixed_from and sorted(c.mixed_from) == sorted(tup) for c in self.generations[generation - 1]):
                continue

            self.generations[generation].append(
                ColorDefinition(
                    identifier=yml.identifier if yml else f"{combo[0].identifier}{'+' * generation}{combo[1].identifier}",
                    name=yml.name if yml else None,
                    hex_value=yml.hex_value if yml else None,
                    mixed_from=tup,
                    generation=generation,
                )
            )

    def _get_from_yaml(self, mixed_from: tuple[str, str]) -> Optional[ColorDefinition]:
        """
        Get a color definition from the input YAML.

        Args:
            identifier: Color identifier.

        Returns:
            ColorDefinition object, if found.
        """
        for color in self.existing_colors.values():
            if color.mixed_from and sorted(color.mixed_from) == sorted(mixed_from):
                return color

        return None
