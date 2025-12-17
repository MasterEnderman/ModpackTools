import numpy as np
from numpy.typing import NDArray


class BlendPipeline:
    """
    Responsible for blending a texture and a color according
    to the per-channel algorithm specified.
    """

    def blend(self, texture: NDArray[np.uint8], color: NDArray[np.uint8]) -> NDArray[np.uint8]:
        """
        Blend a texture with a color array.

        For each pixel:
        - If the texture pixel is white (255, 255, 255), the output pixel is white.
        - Otherwise, output = texture + color - average(texture)
        - After initial blending, normalize per channel:
            - Shift negative values up
            - Shift values >255 down
            - Restore white pixels
            - Clamp final values to [0, 255]

        Args:
            texture: Texture image array of shape (H, W, 3)
            color: Color array of shape (H, W, 3) or (H, W) for grayscale

        Returns:
            Blended and normalized image as uint8 array of shape (H, W, 3)
        """

        # If color is grayscale, expand to RGB
        if color.ndim == 2:
            color = np.stack([color]*3, axis=2)

        # Compute per-channel average of the texture
        avg_per_channel: NDArray[np.float32] = np.mean(texture, axis=(0, 1))

        # Initialize output array
        output: NDArray[np.float32] = np.zeros_like(texture, dtype=np.float32)

        # White mask
        white_mask: NDArray[np.bool_] = np.all(texture == 255, axis=2)

        # Initial blend per channel
        output[:, :, 0] = texture[:, :, 0] + color[:, :, 0] - avg_per_channel[0]
        output[:, :, 1] = texture[:, :, 1] + color[:, :, 1] - avg_per_channel[1]
        output[:, :, 2] = texture[:, :, 2] + color[:, :, 2] - avg_per_channel[2]

        # Normalize each channel independently
        for c in range(3):
            channel = output[:, :, c]
            min_val = channel.min()
            max_val = channel.max()

            if min_val < 0:
                channel += abs(min_val)
            if max_val > 255:
                channel -= (max_val - 255)

            output[:, :, c] = channel

        # Restore white pixels
        output[white_mask] = 255

        # Hard clamp to [0, 255] and convert to uint8
        output = np.clip(output, 0, 255)

        return output.astype(np.uint8)
