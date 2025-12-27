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
    projections: bool
    size: Optional[int]


@dataclass
class ColorDefinition:
    """
    Raw color definition parsed from input YAML.
    """

    identifier: str
    parsed: bool
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
    parsed: bool
    mixed_from: Optional[Tuple[str, str]]


@dataclass(frozen=True)
class MixProjection:
    """
    Represents the result of virtually mixing two palette colors and
    projecting the result onto the closest existing palette color.
    """

    source_a: str
    source_b: str
    projected: str
    delta_e: float
