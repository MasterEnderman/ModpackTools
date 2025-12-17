from pathlib import Path
from PIL import Image
import numpy as np
from numpy.typing import NDArray


class ImageIO:
    """Responsible for loading and saving images as NumPy arrays."""

    def load(self, path: Path) -> NDArray[np.uint8]:
        """
        Load an image from a file.

        Args:
            path: Path to the image file.

        Returns:
            NumPy array of shape (H, W, 3) for RGB or (H, W) for grayscale.
        """
        img = Image.open(path)
        if img.mode not in ("RGB", "L"):
            img = img.convert("RGB")
        return np.array(img)

    def save(self, array: NDArray[np.uint8], path: Path) -> None:
        """
        Save a NumPy array as an image.

        Args:
            array: NumPy array to save.
            path: Path to save the image file.
        """
        if array.ndim == 2:
            img = Image.fromarray(array, "L")
        else:
            img = Image.fromarray(array, "RGB")
        img.save(path)
