from pathlib import Path
import json
from typing import Dict


class Settings:
    """Loads and holds paths and blend configurations from a JSON settings file."""

    def __init__(self, path: str):
        """
        Args:
            path: Path to the JSON settings file.
        """
        self.path: Path = Path(path)
        self.textures_dir: Path = Path("./textures")
        self.colors_dir: Path = Path("./colors")
        self.output_dir: Path = Path("./output")
        self.blends: Dict[str, list] = {}
        self.load()

    def load(self) -> None:
        """Load settings from JSON file."""
        if not self.path.exists():
            raise FileNotFoundError(f"Settings file not found: {self.path}")

        with self.path.open() as f:
            data: Dict = json.load(f)

        paths: Dict = data.get("paths", {})
        self.textures_dir = Path(paths.get("textures", "./textures"))
        self.colors_dir = Path(paths.get("colors", "./colors"))
        self.output_dir = Path(paths.get("output", "./output"))
        self.blends = data.get("blends", {})
