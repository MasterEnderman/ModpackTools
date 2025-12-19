from dataclasses import dataclass
from typing import Tuple
import numpy as np


@dataclass(slots=True)
class ProcessedColor:
    """
    Fully evaluated color representation.
    """
    identifier: str
    generation: int
    name: str

    hex_value: str
    rgb: Tuple[int, int, int]
    lab: np.ndarray
