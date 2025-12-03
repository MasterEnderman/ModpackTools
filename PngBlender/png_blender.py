from pathlib import Path
from PIL import Image
import numpy as np
import json
import re


class TextureColorBlender:
    """
    Blends texture and color images using a sophisticated averaging and normalization approach.
    """
    
    def __init__(self, settings_path: str):
        """
        Initialize the blender with a settings file path.
        
        Args:
            settings_path: Path to the JSON settings file
        """
        self.settings_path = Path(settings_path)
        self.load_settings()
        
    def load_settings(self):
        """
        Load settings from JSON file.
        Expected format:
        {
            "paths": {
                "textures": "path/to/textures",
                "colors": "path/to/colors",
                "output": "path/to/output"
            },
            "blends": {
                "texture1": ["color1", "#FF0000(red)", "#00FF00"],
                "texture2": ["color1", "#00FF00"]
            }
        }
        """
        if not self.settings_path.exists():
            raise FileNotFoundError(f"Settings file not found: {self.settings_path}")
        
        with open(self.settings_path, 'r') as f:
            settings = json.load(f)
        
        # Load paths
        paths = settings.get('paths', {})
        self.textures_dir = Path(paths.get('textures', './textures'))
        self.colors_dir = Path(paths.get('colors', './colors'))
        self.output_dir = Path(paths.get('output', './output'))
        
        # Load blend mappings
        self.blends = settings.get('blends', {})
        
        print(f"Settings loaded from: {self.settings_path}")
        print(f"  Textures directory: {self.textures_dir}")
        print(f"  Colors directory: {self.colors_dir}")
        print(f"  Output directory: {self.output_dir}")
        print(f"  Blend configurations: {len(self.blends)}")
        
    def parse_hex_color(self, color_string: str) -> tuple:
        """
        Parse hex color string with optional name in brackets.
        
        Args:
            color_string: String like "#FF0000" or "#FF0000(red)"
            
        Returns:
            Tuple of (hex_code, custom_name) where custom_name is None if not specified
            
        Raises:
            ValueError: If hex code is invalid
        """
        # Pattern to match hex color with optional name in brackets
        pattern = r'^#([0-9A-Fa-f]{3}|[0-9A-Fa-f]{6})(?:\(([^)]+)\))?$'
        match = re.match(pattern, color_string)
        
        if not match:
            raise ValueError(f"Invalid hex color format: '{color_string}'. Expected format: #RRGGBB or #RRGGBB(name)")
        
        hex_code = match.group(1)
        custom_name = match.group(2)  # None if not specified
        
        return hex_code, custom_name
    
    def hex_to_rgb(self, hex_code: str) -> tuple:
        """
        Convert hex color code to RGB tuple.
        
        Args:
            hex_code: Hex color string without # (e.g., "FF0000" or "F00")
            
        Returns:
            Tuple of (R, G, B) values
        """
        # Handle both 3-digit and 6-digit hex codes
        if len(hex_code) == 3:
            hex_code = ''.join([c*2 for c in hex_code])
        
        r = int(hex_code[0:2], 16)
        g = int(hex_code[2:4], 16)
        b = int(hex_code[4:6], 16)
        
        return (r, g, b)
    
    def create_color_array(self, shape: tuple, hex_code: str) -> np.ndarray:
        """
        Create a color array filled with the specified hex color.
        
        Args:
            shape: Shape of the array to create (matching texture dimensions)
            hex_code: Hex color string (without #)
            
        Returns:
            Numpy array filled with the color
        """
        rgb = self.hex_to_rgb(hex_code)
        
        # Create array with the same shape as texture
        if len(shape) == 2:
            # Grayscale texture - use average of RGB values
            gray_value = sum(rgb) / 3
            color_array = np.full(shape, gray_value, dtype=np.float32)
        else:
            # RGB texture
            color_array = np.zeros(shape, dtype=np.float32)
            color_array[:, :, 0] = rgb[0]
            color_array[:, :, 1] = rgb[1]
            color_array[:, :, 2] = rgb[2]
        
        return color_array
    
    def load_png(self, filepath: Path) -> np.ndarray:
        """
        Load a PNG file and return as numpy array.
        
        Args:
            filepath: Path to the PNG file
            
        Returns:
            Numpy array of the image
        """
        img = Image.open(filepath)
        # Convert to RGB if it has an alpha channel, or if it's in a different mode
        if img.mode != 'RGB' and img.mode != 'L':
            img = img.convert('RGB')
        return np.array(img)
    
    def load_or_create_color(self, color_name: str, texture_shape: tuple) -> tuple:
        """
        Load a color from file or create from hex code.
        
        Args:
            color_name: Either a filename or a hex color code (starting with #)
            texture_shape: Shape of the texture for creating solid color arrays
            
        Returns:
            Tuple of (color_array, display_name, filename_safe_name)
            
        Raises:
            ValueError: If hex color format is invalid
        """
        if color_name.startswith('#'):
            # It's a hex color code
            try:
                hex_code, custom_name = self.parse_hex_color(color_name)
                color_array = self.create_color_array(texture_shape, hex_code)
                
                # Display name shows the full specification
                display_name = color_name
                
                # Filename uses custom name if provided, otherwise hex code
                if custom_name:
                    filename_safe_name = self.sanitize_filename(custom_name)
                else:
                    filename_safe_name = f"hex_{hex_code}"
                
                return color_array, display_name, filename_safe_name
                
            except ValueError as e:
                raise ValueError(f"Error parsing hex color '{color_name}': {e}")
        else:
            # It's a file name
            color_path = self.colors_dir / f"{color_name}.png"
            
            if not color_path.exists():
                print(f"Warning: Color file not found: {color_path}")
                return None, None, None
            
            color_array = self.load_png(color_path)
            display_name = color_name
            filename_safe_name = color_name
            return color_array, display_name, filename_safe_name
    
    def calculate_average(self, texture_array: np.ndarray) -> float:
        """
        Calculate the average color value of the texture across all pixels.
        
        Args:
            texture_array: Numpy array of texture image
            
        Returns:
            Average value as float
        """
        return float(np.mean(texture_array))
    
    def blend_images(self, texture_array: np.ndarray, color_array: np.ndarray, texture_avg: float) -> np.ndarray:
        """
        Blend texture and color pixel by pixel: if texture is 255, keep it; else add texture + color - average.
        
        Args:
            texture_array: Numpy array of texture image
            color_array: Numpy array of color image
            texture_avg: Average value of the texture
            
        Returns:
            Blended numpy array (may contain values outside 0-255 range)
        """
        # Convert to float for calculations
        texture = texture_array.astype(np.float32)
        color = color_array.astype(np.float32)
        
        # Create result array - process each pixel
        result = np.where(
            texture == 255,
            255,
            texture + color - texture_avg
        )
        
        return result
    
    def normalize_all_blends(self, blended_data: list) -> list:
        """
        Normalize all blended images through multiple passes.
        
        Args:
            blended_data: List of tuples (texture_array, blended_array, output_path)
            
        Returns:
            List of tuples with normalized arrays
        """
        if not blended_data:
            return []
        
        # Extract all blended arrays for global min/max calculation
        all_blended = [data[1] for data in blended_data]
        
        # Find global min and max across all blends
        global_min = min(np.min(arr) for arr in all_blended)
        global_max = max(np.max(arr) for arr in all_blended)
        
        print(f"\nGlobal statistics before normalization:")
        print(f"  Min value: {global_min:.2f}")
        print(f"  Max value: {global_max:.2f}")
        
        normalized_data = []
        
        for texture_array, blended_array, output_path in blended_data:
            result = blended_array.copy()
            
            # Pass 1: If min is negative, subtract min from all values (double subtraction = adding absolute value)
            if global_min < 0:
                result = result - global_min
            
            # Pass 2: If max > 255, normalize: value + 255 - max
            if global_max > 255:
                result = result + 255 - global_max
            
            # Pass 3: Restore 255 values where original texture was 255
            result = np.where(texture_array == 255, 255, result)
            
            # Pass 4: Final clamp to ensure no value exceeds 255
            result = np.clip(result, 0, 255)
            
            # Convert to uint8
            result = result.astype(np.uint8)
            
            normalized_data.append((result, output_path))
        
        return normalized_data
    
    def save_png(self, array: np.ndarray, output_path: Path):
        """
        Save numpy array as PNG file.
        
        Args:
            array: Numpy array to save
            output_path: Path where to save the PNG
        """
        # Handle both grayscale and RGB images
        if array.ndim == 2:
            img = Image.fromarray(array, mode='L')
        else:
            img = Image.fromarray(array, mode='RGB')
        img.save(output_path, 'PNG')
    
    def sanitize_filename(self, name: str) -> str:
        """
        Sanitize a string to be used as a filename.
        
        Args:
            name: String to sanitize
            
        Returns:
            Sanitized string safe for filenames
        """
        # Replace problematic characters
        name = name.replace('/', '_').replace('\\', '_').replace(':', '_')
        name = name.replace('<', '_').replace('>', '_').replace('|', '_')
        name = name.replace('"', '_').replace('?', '_').replace('*', '_')
        return name
    
    def process_all(self):
        """
        Process all texture-color combinations based on settings and export as PNG files.
        """
        if not self.blends:
            print("No blend configurations found in settings file.")
            return
        
        # Store all blended data for global normalization
        blended_data = []
        total_combinations = sum(len(colors) for colors in self.blends.values())
        
        print(f"\nWill generate {total_combinations} output file(s)\n")
        
        # Process each texture with its specified colors
        for texture_name, color_names in self.blends.items():
            texture_path = self.textures_dir / f"{texture_name}.png"
            
            if not texture_path.exists():
                print(f"Warning: Texture file not found: {texture_path}, skipping...")
                continue
            
            # Load texture
            texture_array = self.load_png(texture_path)
            
            # Calculate average for this texture once
            texture_avg = self.calculate_average(texture_array)
            print(f"Texture '{texture_name}' average value: {texture_avg:.2f}")
            
            for color_name in color_names:
                try:
                    # Load color from file or create from hex code
                    result = self.load_or_create_color(color_name, texture_array.shape)
                    
                    if result[0] is None:
                        continue
                    
                    color_array, display_name, filename_safe_name = result
                    
                    # Check if dimensions match
                    if texture_array.shape != color_array.shape:
                        print(f"Warning: Dimension mismatch between {texture_name} and {display_name}, skipping...")
                        continue
                    
                    # Blend them (initial blend, not normalized yet)
                    blended_array = self.blend_images(texture_array, color_array, texture_avg)
                    
                    # Create output filename: texture_color.png
                    output_filename = f"{texture_name}_{filename_safe_name}.png"
                    output_path = self.output_dir / output_filename
                    
                    # Store for later normalization
                    blended_data.append((texture_array, blended_array, output_path))
                    
                    print(f"  Blended: {texture_name} + {display_name}")
                    
                except ValueError as e:
                    print(f"Error processing color '{color_name}': {e}")
                    continue
        
        if not blended_data:
            print("\nNo valid texture-color combinations were processed.")
            return
        
        print(f"\nBlending complete. Starting normalization...")
        
        # Normalize all blends together
        normalized_data = self.normalize_all_blends(blended_data)
        
        # Save all normalized images
        print(f"\nSaving output files...")
        for idx, (normalized_array, output_path) in enumerate(normalized_data, 1):
            self.save_png(normalized_array, output_path)
            print(f"Saved [{idx}/{len(normalized_data)}]: {output_path.name}")
        
        print(f"\nProcessing complete! {len(normalized_data)} output files saved to {self.output_dir}")
