from __future__ import annotations

from cli import CliParser
from generation import ColorGenerator
from input import InputLoader, InputParser, DependencyValidator
from util import calculate_max_color_count, resolve_output_size

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

    print(f"Base color count: {base_color_count}")

    max_size = calculate_max_color_count(
        base_color_count=base_color_count,
        max_depth=GRAPH_MAX_DEPTH,
    )

    # 5. Resolve final size
    final_size = resolve_output_size(
        requested_size=cli_args.size,
        max_size=max_size,
    )

    # 6. Generate colors
    generator = ColorGenerator(colors, max_depth=GRAPH_MAX_DEPTH)
    generated_colors = generator.generate_all()

    print(f"Generated {len(generated_colors)} colors:")
    for color in sorted(generated_colors[:final_size], key=lambda c: c.generation or 0):
        print(f"  - {color.identifier}: {color.mixed_from} -> {color.generation}")

if __name__ == "__main__":
    main()
