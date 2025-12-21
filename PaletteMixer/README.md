# 🎨 Advanced Color Processor

Welcome to the **Advanced Color Processor**! This Python project allows you to generate, mix, process, and visualize complex color palettes from a simple YAML input. Developed for [The Road not taken](https://github.com/xkforce/The-Road-Not-Taken)! ✨

## 🛠️ Features

* Parse human-readable `input.yml` files with color definitions.
* Generate all possible color combinations up to a configurable **depth**.
* Mix colors using accurate color science (`pymixbox`) with 50/50 ratios.
* Calculate **RGB** and **Lab** values for all colors.
* Reduce palette size using **ΔE (CIEDE2000)** distance-based algorithm while keeping user-defined colors.
* Export results as:
  * **Markdown overview** (`output.md`) with generation info, mix ancestry, and all color values.
  * **Palette image** (`palette.png`) sorted in a perceptual gradient.

## 📁 Project Structure

```
src/
├── main.py           # Entry point
├── cli.py            # Command-line interface
├── input.py          # YAML file parsing
├── util.py           # Utility functions (hex ↔ rgb etc.)
├── processing.py     # PaletteProcessor class
├── output.py         # Image & Markdown exporters
└── classes.py        # Shared data classes
```

* `input.yml` → Your source color definitions.
* `output/palette.png` → Generated palette image.
* `output/output.md` → Markdown overview of the palette.

## ⚡ Quick Start

1️⃣ **Prepare your input** (`input.yml`):

```yaml
# Base color
ultramarine_blue:
  name: Ultramarine Blue
  hex: "#1F3A8A"

# Generated color
slate_indigo:
  mixed_from:
    - ultramarine_blue
    - neutral_gray
```

2️⃣ **Run the script**:

```bash
python main.py path/to/input.yml --size 20
```

* `--size` is optional; if not provided, the program will calculate the maximum number of colors and prompt you.

3️⃣ **View outputs**:

* `output/palette.png` 🖼️
* `output/output.md` 📄

## 🖌️ How It Works

1. **Parsing**: Loads the YAML file and validates unique identifiers.
2. **Color Generation**: Builds combinations across generations (primary, secondary, tertiary, …) using the defined mix rules.
3. **Processing**: Calculates RGB and Lab values for all colors, mixes colors, and fetches names for unnamed colors via the `color.pizza` API.
4. **Reduction**: Optionally reduces the palette size using a distance-based algorithm while keeping user-defined colors.
5. **Output**:
   * **Markdown**: Shows all colors by generation with hex, RGB, Lab, and ancestry.
   * **PNG Image**: Palette visualized in a gradient sorted by lightness and hue.

## 💡 Notes

* Colors are processed **generation-wise**, so lower generations are always resolved before higher ones.
* All generated colors are **fully resolved** before exporting, ensuring no optional fields remain.
* The pipeline ensures **deterministic output** for reproducibility.

## 📎 Links

* Input example: [`input.yml`](resources/input.yml)
* Generated palette image: [`palette.png`](resources/palette.png)
* Generated Markdown overview: [`output.md`](resources/output.md)

## 😺 Have Fun!

Enjoy exploring your generated palettes and mixing colors with science-backed accuracy! 🌈✨

Stay creative and colorful! 💖
