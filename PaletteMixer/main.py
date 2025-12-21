from __future__ import annotations

from pathlib import Path

from cli import CliParser
from generation import ColorGenerator
from input import InputLoader, InputParser, DependencyValidator
from util import calculate_max_color_count, resolve_output_size
from processing import PaletteProcessor
from output import PaletteImageExporter, PaletteMarkdownExporter

# =========================
# Main wiring
# =========================

GRAPH_MAX_DEPTH: int = 2


def main() -> None:
    # 1. Parse CLI (no prompting yet)
    cli_parser = CliParser()
    cli_args = cli_parser.parse()

    # 2. Load + parse YAML
    loader = InputLoader()
    raw_yaml = loader.load(cli_args.input_path)

    parser = InputParser()
    colors = parser.parse(raw_yaml)

    # 3. Validate dependencies
    validator = DependencyValidator()
    validator.validate(colors, max_depth=GRAPH_MAX_DEPTH)

    # 4. Calculate max size
    base_color_count = sum(
        1 for c in colors.values() if c.mixed_from is None
    )

    max_size = calculate_max_color_count(
        base_color_count=base_color_count,
        max_depth=GRAPH_MAX_DEPTH,
    )

    # 5. Resolve final size
    final_size = resolve_output_size(
        requested_size=cli_args.size,
        max_size=max_size + base_color_count,
    )

    # 6. Generate colors
    generator = ColorGenerator(colors, max_depth=GRAPH_MAX_DEPTH)
    generated_colors = generator.generate_all()

    # 7. Process colors
    processor = PaletteProcessor(generated_colors)

    processor.resolve_hex_values()
    processor.resolve_names()

    processed_palette = processor.to_processed_colors()
    processed_palette = processor.reduce_palette(
        processed_palette,
        max_colors=final_size,
        user_defined_ids=set(colors.keys()),
    )

    # 8. Export palette
    png_exporter = PaletteImageExporter(swatch_size=64)
    png_exporter.export_png(
        colors=processed_palette,
        output_path=Path("resources/palette.png"),
    )

    md_exporter = PaletteMarkdownExporter()
    md_exporter.export(
        colors=processed_palette,
        output_path=Path("resources/output.md"),
    )

    # 9. Print stats
    print(f"🎨 Final palette ({final_size} mixed and {base_color_count} base colors):")
    print(f"  - {base_color_count} defined base colors")
    print(f"  - {len(colors) - base_color_count} defined mixed colors")
    print(f"  - {len(generated_colors) - len(colors)} generated colors")
    print(f"  - {len(processed_palette)} total colors")

if __name__ == "__main__":
    main()
