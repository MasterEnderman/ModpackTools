from __future__ import annotations

import numpy as np
from dataclasses import dataclass
from pathlib import Path
from typing import Optional, Tuple

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


@dataclass
class ColorDefinition:
    """
    Raw color definition parsed from input YAML.
    """

    identifier: str
    name: Optional[str]
    hex_value: Optional[str]
    mixed_from: Optional[Tuple[str, str]]
    generation: Optional[int]


@dataclass(frozen=True)
class ProcessedColor:
    identifier: str
    generation: int
    hex_value: str
    rgb: Tuple[int, int, int]
    lab: np.ndarray
    name: str
    mixed_from: Optional[Tuple[str, str]]
