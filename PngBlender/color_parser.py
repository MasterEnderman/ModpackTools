import re
from typing import Optional, Tuple


class ColorParser:
    """Parses hex color strings with optional custom names."""

    PATTERN = re.compile(r'^#([0-9A-Fa-f]{3}|[0-9A-Fa-f]{6})(?:\(([^)]+)\))?$')

    def parse(self, value: str) -> Tuple[str, Optional[str]]:
        """
        Parse a hex color string with optional name.

        Args:
            value: Hex color string, e.g. "#FF0000" or "#FF0000(red)".

        Returns:
            Tuple of (hex_code, custom_name). custom_name is None if not specified.

        Raises:
            ValueError: If the string is not a valid hex color.
        """
        match = self.PATTERN.match(value)
        if not match:
            raise ValueError(f"Invalid hex color: {value}")
        return match.group(1), match.group(2)
