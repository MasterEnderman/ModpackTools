from typing import override, Optional
from abc import ABC, abstractmethod
from PIL import Image
import mixbox
import numpy as np

from errors import report_info


class BlendStrategy(ABC):
    """
    Base class for blend strategies.

    Applies a single layer to a base texture.

    Subclasses implement `_blend` to compute the blended RGB(A) result for
    every pixel. The public `apply` method wraps `_blend` with alpha-aware
    compositing: any pixel that is fully transparent in the base or the
    layer is left untouched (copied straight from the base) instead of
    being fed into the blend math, so transparent regions never bleed
    color into (or take color from) the visible parts of the image.
    """

    def apply(
        self,
        base: Image.Image,
        layer: Image.Image,
    ) -> Image.Image:
        """
        Apply a single layer to the base image, ignoring transparent pixels.
        """
        mask = self._transparency_mask(base, layer)
        blended = self._blend(base, layer, mask)

        if mask is None:
            return blended

        base_arr = np.asarray(base.convert(blended.mode), dtype=np.uint8)
        blended_arr = np.asarray(blended, dtype=np.uint8)

        out_arr = np.where(mask[..., None], base_arr, blended_arr)
        return Image.fromarray(out_arr.astype(np.uint8), mode=blended.mode)

    @abstractmethod
    def _blend(
        self,
        base: Image.Image,
        layer: Image.Image,
        mask: Optional[np.ndarray],
    ) -> Image.Image:
        """
        Compute the blended image for all pixels.

        `mask` (if not None) is a boolean HxW array that is True wherever
        the base or layer pixel is fully transparent. Implementations that
        aggregate statistics across the whole image (e.g. averages, min/max
        normalization) should exclude masked pixels from those statistics.
        """
        raise NotImplementedError

    @staticmethod
    def _transparency_mask(
        base: Image.Image,
        layer: Image.Image,
    ) -> Optional[np.ndarray]:
        """
        Build a boolean mask marking pixels that are fully transparent in
        either the base or the layer. Returns None if neither image has an
        alpha channel (nothing to mask).
        """
        base_alpha = BlendStrategy._alpha_channel(base)
        layer_alpha = BlendStrategy._alpha_channel(layer)

        if base_alpha is None and layer_alpha is None:
            return None

        transparent = np.zeros(base.size[::-1], dtype=bool)
        if base_alpha is not None:
            transparent |= base_alpha == 0
        if layer_alpha is not None:
            transparent |= layer_alpha == 0

        return transparent

    @staticmethod
    def _alpha_channel(image: Image.Image) -> Optional[np.ndarray]:
        if image.mode not in ("RGBA", "LA", "PA"):
            return None
        return np.asarray(image, dtype=np.uint8)[..., -1]


class NoOpBlendStrategy(BlendStrategy):
    """
    Placeholder strategy that returns the base image unchanged.
    """

    @override
    def _blend(
        self,
        base: Image.Image,
        layer: Image.Image,
        mask: Optional[np.ndarray],
    ) -> Image.Image:
        return base.copy()


class MultiplyBlend(BlendStrategy):
    @override
    def _blend(
        self,
        base: Image.Image,
        layer: Image.Image,
        mask: Optional[np.ndarray],
    ) -> Image.Image:
        base_arr = np.asarray(base, dtype=np.float32)
        layer_arr = np.asarray(layer, dtype=np.float32)

        result = (base_arr * layer_arr) / 255.0

        result = np.clip(result, 0, 255).astype(np.uint8)
        return Image.fromarray(result, mode=base.mode)


class MixBlend(BlendStrategy):
    def __init__(self, weight: float) -> None:
        if not 0.0 <= weight <= 1.0:
            raise ValueError("Mix weight must be between 0 and 1.")
        self._weight = weight

    @override
    def _blend(
        self,
        base: Image.Image,
        layer: Image.Image,
        mask: Optional[np.ndarray],
    ) -> Image.Image:
        base_arr = np.asarray(base, dtype=np.float32)
        layer_arr = np.asarray(layer, dtype=np.float32)

        result = base_arr * (1.0 - self._weight) + layer_arr * self._weight

        result = np.clip(result, 0, 255).astype(np.uint8)
        return Image.fromarray(result, mode=base.mode)


class MixboxBlend(BlendStrategy):
    """
    Perceptual color mixing using Mixbox.

    mixbox.lerp(a.rgb, b.rgb, weight) is applied per pixel. Pixels that are
    fully transparent in either image are skipped entirely (not just
    overwritten afterwards) since running mixbox.lerp over the whole image
    is the expensive part of this strategy.
    """

    def __init__(self, weight: float) -> None:
        if not 0.0 <= weight <= 1.0:
            raise ValueError("mixbox weight must be between 0 and 1.")
        self._weight = weight

    @override
    def _blend(
        self,
        base: Image.Image,
        layer: Image.Image,
        mask: Optional[np.ndarray],
    ) -> Image.Image:
        base_arr = np.asarray(base, dtype=np.uint8)
        layer_arr = np.asarray(layer, dtype=np.uint8)

        # Ensure RGB(A)
        if base_arr.shape[-1] < 3 or layer_arr.shape[-1] < 3:
            raise ValueError("Mixbox requires RGB or RGBA images.")

        height, width, channels = base_arr.shape
        out = base_arr.copy()

        for y in range(height):
            for x in range(width):
                if mask is not None and mask[y, x]:
                    continue

                a = base_arr[y, x][:3]
                b = layer_arr[y, x][:3]

                mixed = mixbox.lerp(a, b, self._weight)
                out[y, x][:3] = mixed

        return Image.fromarray(out, mode=base.mode)


class PenteractBlend(BlendStrategy):
    """
    Experimental procedural blend algorithm.

    Uses grayscale averaging, value normalization, and dynamic range
    remapping to generate a new color transformation. Transparent pixels
    (per `mask`) are excluded from the grayscale average and the min/max
    normalization passes so a large transparent region can't skew the
    stats used to color the visible pixels.
    """

    def __init__(self, average: Optional[int] = None) -> None:
        if average is not None and not 0 <= average <= 255:
            raise ValueError("Penteract average must be between 0 and 255.")
        self._average = average

    @override
    def _blend(
        self,
        base: Image.Image,
        layer: Image.Image,
        mask: Optional[np.ndarray],
    ) -> Image.Image:
        # Ensure RGB
        base_rgb = base.convert("RGB")
        layer_rgb = layer.convert("RGB")

        opaque = None if mask is None else ~mask

        # --- Step 1: grayscale average (opaque pixels only) ---
        gray_arr = np.asarray(base_rgb.convert("L"))
        if self._average is not None:
            avg_gray = self._average
        elif opaque is not None and opaque.any():
            avg_gray = int(np.mean(gray_arr[opaque]))
        else:
            avg_gray = int(np.mean(gray_arr))
        report_info(f"    - Penteract average: {avg_gray}")

        # --- Step 2: flatten images ---
        base_arr = np.asarray(base_rgb, dtype=np.int32)
        layer_arr = np.asarray(layer_rgb, dtype=np.int32)

        if base_arr.shape != layer_arr.shape:
            raise ValueError("Base and layer images must have same dimensions.")

        flat_base = base_arr.reshape(-1, 3)
        flat_layer = layer_arr.reshape(-1, 3)
        flat_opaque = None if opaque is None else opaque.reshape(-1)

        # --- Step 3: first pass ---
        result = np.where(
            flat_base == 255,
            255,
            flat_base + flat_layer - avg_gray,
        )

        # --- Step 4: normalize minimum (stats over opaque pixels only) ---
        stats_mask = np.ones(result.shape[0], dtype=bool) if flat_opaque is None else flat_opaque
        stats_view = result[stats_mask] if stats_mask.any() else result

        min_val = int(stats_view.min())
        if min_val < 0:
            report_info(f"    - Penteract minimum: {min_val}")
            result = np.where(result == 255, 255, result - min_val)
            stats_view = result[stats_mask] if stats_mask.any() else result

        # --- Step 5: normalize maximum (stats over opaque pixels only) ---
        max_val = int(stats_view.max())
        if max_val > 255:
            report_info(f"    - Penteract maximum: {max_val}")
            result = np.where(result == 255, 255, result + 255 - max_val)

        # --- Step 6: clamp ---
        result = np.clip(result, 0, 255)

        # --- Step 7: rebuild image ---
        out_arr = result.astype(np.uint8).reshape(base_arr.shape)

        return Image.fromarray(out_arr, mode="RGB")