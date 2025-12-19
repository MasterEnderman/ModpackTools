from __future__ import annotations

import argparse
import sys
from dataclasses import dataclass
from pathlib import Path
from typing import Optional


@dataclass(frozen=True)
class CliArguments:
    """
    Represents validated command-line arguments.

    Attributes:
        input_path: Path to the input.txt file.
        size: Chosen size parameter.
    """

    input_path: Path
    size: Optional[int]


class CliParser:
    """
    Parses command-line arguments only.
    """

    def parse(self) -> CliArguments:
        parser = argparse.ArgumentParser(
            description="Advanced color processing tool"
        )

        parser.add_argument(
            "input_file",
            type=Path,
            help="Path to the input YAML file"
        )

        parser.add_argument(
            "--size",
            type=int,
            required=False,
            help="Optional maximum output size"
        )

        args = parser.parse_args()

        if not args.input_file.exists():
            print(
                f"Error: input file not found: {args.input_file}",
                file=sys.stderr,
            )
            sys.exit(1)

        return CliArguments(
            input_path=args.input_file,
            size=args.size,
        )
