from pathlib import Path
from typing import Tuple, Optional
import numpy as np
from color_parser import ColorParser
from color_factory import ColorFactory
from image_io import ImageIO


class ColorSource:
    """Loads colors from files or creates solid colors from hex codes."""

    def __init__(self, colors_dir: Path, parser: ColorParser,
                 factory: ColorFactory, image_io: ImageIO):
        self.colors_dir = colors_dir
        self.parser = parser
        self.factory = factory
        self.image_io = image_io

    def load(self, name: str, shape: Tuple[int, int, int]) -> Tuple[Optional[np.ndarray], Optional[str]]:
        """
        Load a color as an array.

        Args:
            name: Filename or hex code
            shape: Shape to create solid color if hex

        Returns:
            Tuple of (array, display_name). None if file not found.
        """
        if name.startswith("#"):
            hex_code, custom_name = self.parser.parse(name)
            arr = self.factory.create_solid(shape, self.factory.hex_to_rgb(hex_code))
            return arr, custom_name or f"hex_{hex_code}"

        path = self.colors_dir / f"{name}.png"
        if not path.exists():
            return None, None

        return self.image_io.load(path), name
