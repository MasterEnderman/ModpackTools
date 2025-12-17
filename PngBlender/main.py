from settings import Settings
from image_io import ImageIO
from color_parser import ColorParser
from color_factory import ColorFactory
from color_source import ColorSource
from texture_stats import TextureStats
from blend_pipeline import BlendPipeline
from filename_policy import FilenamePolicy
from blend_runner import BlendRunner

def main(settings_path: str):
    # Load settings
    settings = Settings(settings_path)

    # Initialize utility components
    image_io = ImageIO()
    color_parser = ColorParser()
    color_factory = ColorFactory()
    color_source = ColorSource(settings.colors_dir, color_parser, color_factory, image_io)
    texture_stats = TextureStats()
    pipeline = BlendPipeline()
    filename_policy = FilenamePolicy()

    # Create runner and execute blending
    runner = BlendRunner(
        settings=settings,
        image_io=image_io,
        color_source=color_source,
        texture_stats=texture_stats,
        pipeline=pipeline,
        filename_policy=filename_policy
    )

    runner.run()


if __name__ == "__main__":
    import sys

    if len(sys.argv) < 2:
        print("Usage: python main.py path/to/settings.json")
        sys.exit(1)

    main(sys.argv[1])
