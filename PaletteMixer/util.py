import sys
from typing import Optional

def calculate_max_color_count(
    base_color_count: int,
    max_depth: int,
) -> int:
    """
    Calculate the maximum possible number of colors that can be generated
    given a number of base colors and a maximum generation depth.

    Generation rules:
    - Generation 0: base colors
    - Each next generation consists of all unique, unordered combinations
      of two distinct colors from all previous generations.

    Args:
        base_color_count: Number of base (primary) colors.
        max_depth: Maximum generation depth.

    Returns:
        Total number of colors including all generations.
    """
    if base_color_count < 1:
        return 0

    total_colors = base_color_count

    for _ in range(1, max_depth + 1):
        new_colors = total_colors * (total_colors - 1) // 2
        total_colors += new_colors

    return total_colors

def resolve_output_size(
    requested_size: Optional[int],
    max_size: int,
) -> int:
    """
    Resolve the final output size based on user input and maximum allowed size.

    Args:
        requested_size: Size provided via CLI flag, if any.
        max_size: Maximum allowed size.

    Returns:
        Final validated output size.
    """
    if requested_size is not None:
        if requested_size < 1 or requested_size > max_size:
            print(
                f"Error: --size must be between 1 and {max_size}.",
                file=sys.stderr,
            )
            sys.exit(1)
        return requested_size

    print(f"Maximum possible output size: {max_size}")
    print("Press Enter to use the maximum size.")

    while True:
        value_str = input(f"Enter desired output size (1 - {max_size}): ").strip()

        # Accept empty input as max_size
        if value_str == "":
            return max_size

        try:
            value = int(value_str)
        except ValueError:
            print("Please enter a valid integer.")
            continue

        if 1 <= value <= max_size:
            return value

        print(f"Size must be between 1 and {max_size}.")
