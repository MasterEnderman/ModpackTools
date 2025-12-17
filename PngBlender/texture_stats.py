import numpy as np


class TextureStats:
    """Calculates statistics on texture images."""

    def average(self, texture: np.ndarray) -> float:
        """
        Compute the average value of all pixels.

        Args:
            texture: Texture array

        Returns:
            Average pixel value (float)
        """
        return float(np.mean(texture))
