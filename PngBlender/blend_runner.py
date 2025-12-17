from typing import Any
import numpy as np
from pathlib import Path
from settings import Settings
from image_io import ImageIO
from color_source import ColorSource
from texture_stats import TextureStats
from blend_pipeline import BlendPipeline
from filename_policy import FilenamePolicy


class BlendRunner:
    """Orchestrates the blending process using other components."""

    def __init__(self, settings: Settings, image_io: ImageIO,
                 color_source: ColorSource, texture_stats: TextureStats,
                 pipeline: BlendPipeline, filename_policy: FilenamePolicy):
        self.settings = settings
        self.image_io = image_io
        self.color_source = color_source
        self.texture_stats = texture_stats
        self.pipeline = pipeline
        self.filename_policy = filename_policy

    def run(self) -> None:
        """Process all textures and colors according to the settings."""
        for texture_name, color_names in self.settings.blends.items():
            texture_path: Path = self.settings.textures_dir / f"{texture_name}.png"
            if not texture_path.exists():
                continue

            texture: np.ndarray = self.image_io.load(texture_path)

            for color_name in color_names:
                color, cname = self.color_source.load(color_name, texture.shape)
                if color is None or cname is None:
                    continue

                result: np.ndarray = self.pipeline.blend(texture, color)

                fname: str = self.filename_policy.sanitize(cname)
                out: Path = self.settings.output_dir / f"{texture_name}_{fname}.png"
                self.image_io.save(result, out)
