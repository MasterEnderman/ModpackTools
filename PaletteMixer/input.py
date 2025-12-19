from __future__ import annotations

import sys
from dataclasses import dataclass
from pathlib import Path
from typing import Dict, Optional, Set, Tuple

import yaml

# =========================
# Phase 2: Input loading
# =========================

class InputLoader:
    """
    Responsible for reading and decoding the input YAML file.
    """

    def load(self, path: Path) -> Dict:
        """
        Load and parse the YAML input file.

        Args:
            path: Path to the YAML file.

        Returns:
            Parsed YAML content as a dictionary.

        Raises:
            SystemExit: If the file cannot be read or parsed.
        """
        try:
            with path.open("r", encoding="utf-8") as f:
                data = yaml.safe_load(f)
        except Exception as exc:
            print(
                f"Error reading YAML file: {exc}",
                file=sys.stderr,
            )
            sys.exit(1)

        if not isinstance(data, dict):
            print(
                "Error: top-level YAML structure must be a mapping.",
                file=sys.stderr,
            )
            sys.exit(1)

        return data


# =========================
# Phase 2: Parsed model
# =========================

@dataclass(frozen=True)
class ColorDefinition:
    """
    Raw color definition parsed from input YAML.
    """

    identifier: str
    name: Optional[str]
    hex_value: Optional[str]
    mixed_from: Optional[Tuple[str, str]]
    generation: Optional[int]


class InputParser:
    """
    Converts raw YAML data into validated ColorDefinition objects.
    """

    def parse(self, raw_data: Dict) -> Dict[str, ColorDefinition]:
        """
        Parse and validate color definitions.

        Args:
            raw_data: Raw YAML dictionary.

        Returns:
            Mapping of color identifiers to ColorDefinition objects.

        Raises:
            SystemExit: If validation fails.
        """
        colors = raw_data.get("colors")

        if not isinstance(colors, dict):
            print(
                "Error: 'colors' section missing or invalid.",
                file=sys.stderr,
            )
            sys.exit(1)

        result: Dict[str, ColorDefinition] = {}

        for identifier, entry in colors.items():
            if not isinstance(entry, dict):
                self._error(
                    f"Color '{identifier}' must be a mapping."
                )

            name = entry.get("name")
            hex_value = entry.get("hex")
            mixed_from = entry.get("mixed_from")

            if hex_value is None and mixed_from is None:
                self._error(
                    f"Color '{identifier}' must define 'hex' or 'mixed_from'."
                )

            mixed_tuple: Optional[Tuple[str, str]] = None
            if mixed_from is not None:
                if (
                    not isinstance(mixed_from, list)
                    or len(mixed_from) != 2
                    or not all(isinstance(x, str) for x in mixed_from)
                ):
                    self._error(
                        f"'mixed_from' in '{identifier}' must be a list of exactly two identifiers."
                    )
                mixed_tuple = (mixed_from[0], mixed_from[1])

            result[identifier] = ColorDefinition(
                identifier=identifier,
                name=name,
                hex_value=hex_value,
                mixed_from=mixed_tuple,
                generation=None,
            )

        return result

    @staticmethod
    def _error(message: str) -> None:
        print(f"Error: {message}", file=sys.stderr)
        sys.exit(1)


class DependencyValidator:
    """
    Validates dependency relationships between color definitions.
    """

    def validate(
        self,
        colors: Dict[str, ColorDefinition],
        max_depth: int,
    ) -> None:
        """
        Validate references, cycles, and maximum dependency depth.

        Args:
            colors: Mapping of color identifiers to definitions.
            max_depth: Maximum allowed dependency depth.

        Raises:
            SystemExit: If validation fails.
        """
        for identifier in colors:
            self._validate_color(
                identifier=identifier,
                colors=colors,
                visited=set(),
                depth=0,
                max_depth=max_depth,
            )

    def _validate_color(
        self,
        identifier: str,
        colors: Dict[str, ColorDefinition],
        visited: Set[str],
        depth: int,
        max_depth: int,
    ) -> None:
        if depth > max_depth:
            self._error(
                f"Maximum dependency depth exceeded at '{identifier}'. "
                f"Allowed depth is {max_depth}."
            )

        if identifier in visited:
            cycle = " -> ".join(list(visited) + [identifier])
            self._error(f"Circular dependency detected: {cycle}")

        color = colors[identifier]

        if color.mixed_from is None:
            return

        visited.add(identifier)

        for dependency in color.mixed_from:
            if dependency not in colors:
                self._error(
                    f"Color '{identifier}' references unknown color '{dependency}'."
                )

            self._validate_color(
                identifier=dependency,
                colors=colors,
                visited=visited.copy(),
                depth=depth + 1,
                max_depth=max_depth,
            )

    @staticmethod
    def _error(message: str) -> None:
        import sys

        print(f"Error: {message}", file=sys.stderr)
        sys.exit(1)
