from __future__ import annotations

import argparse
import sys
from pathlib import Path

from classes import CliArguments


class CliParser:
    """
    Parses command-line arguments only.
    """

    def parse(self) -> CliArguments:
        parser = argparse.ArgumentParser(description="Advanced color processing tool")

        parser.add_argument("input_file", type=Path, help="Path to the input YAML file")

        parser.add_argument(
            "--size", type=int, required=False, help="Optional maximum output size"
        )

        parser.add_argument(
            "--project-mixes",
            action="store_true",
            help=(
                "Generate a virtual additional generation by projecting all possible "
                "mixes onto the closest existing palette color (ΔE)"
            ),
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
            projections=args.project_mixes,
            size=args.size,
        )
