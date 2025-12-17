import numpy as np
from typing import Tuple


class ColorFactory:
    """Generates RGB arrays from hex colors."""

    def hex_to_rgb(self, hex_code: str) -> Tuple[int, int, int]:
        """
        Convert hex code to an RGB tuple.

        Args:
            hex_code: e.g., "FF0000" or "F00"

        Returns:
            Tuple of integers (R, G, B)
        """
        if len(hex_code) == 3:
            hex_code = "".join(c * 2 for c in hex_code)

        t = tuple(int(hex_code[i:i+2], 16) for i in (0, 2, 4))
        return (t[0], t[1], t[2])

    def create_solid(self, shape: Tuple[int, int, int], rgb: Tuple[int, int, int]) -> np.ndarray:
        """
        Create a solid color NumPy array.

        Args:
            shape: Shape of the array (H, W, 3)
            rgb: Tuple of (R, G, B)

        Returns:
            NumPy array of dtype float32 filled with the RGB color.
        """
        arr = np.zeros(shape, dtype=np.float32)
        arr[:, :, 0] = rgb[0]
        arr[:, :, 1] = rgb[1]
        arr[:, :, 2] = rgb[2]
        return arr
