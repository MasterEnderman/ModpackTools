# ΔE Palette Generator

A Python tool for generating visually distinct color palettes using **perceptual color distance (ΔE2000)**.
Developed for [The Road not taken](https://github.com/xkforce/The-Road-Not-Taken).

The program:

* Loads a list of base colors from a text file
* Optionally generates mixed colors by combining base colors
* Reduces the full candidate set to a target palette size using a max-distance algorithm
* Ensures strong visual contrast between colors
* Automatically assigns human-readable color names using the **color.pizza API**
* Outputs both a PNG preview and a text representation of the final palette

## Features

* 🎨 Perceptual palette reduction using **ΔE2000**
* 📏 Target palette size configurable via CLI
* 🧪 Optional color mixing (pairwise combinations)
* 🔀 Multiple color mix modes
* 📄 Simple text-based color input
* 🧠 Human-friendly color names (via color.pizza)
* 🖼 PNG palette preview with uniform swatches

## Requirements

* Python 3.11+
* [`uv`](https://github.com/astral-sh/uv)

All Python dependencies are managed by `uv`.

## Input format

The program expects a file named `colors.txt` in the project root.

### Rules

* One hex color per line
* Hex values must start with `#` and be 6-digit RGB
* Lines starting with `//` are treated as comments and ignored
* Empty lines are ignored

### Example

```txt
// Base colors
#000000
#FFFFFF
#FF0000
#00FF00
#0000FF
#FFFF00
#00FFFF
#FF00FF
```

## Color combining

By default, the program generates additional **derived colors** by combining all unordered pairs of base colors:

* No self-pairs (e.g. `A + A`)
* No duplicate ordering (`A + B` is the same as `B + A`)

These derived colors are added to the candidate pool before palette reduction.

### Mix modes

The way two colors are combined is controlled via the `--mix-mode` flag:

| Mode                | Description                            |
| ------------------- | -------------------------------------- |
| `average` (default) | Averages RGB components of both colors |
| `add`               | Adds RGB components and clamps to 255  |
| `multiply`          | Multiplies RGB components (normalized) |

Example (average mode):

```
R = (R₁ + R₂) / 2
G = (G₁ + G₂) / 2
B = (B₁ + B₂) / 2
```

### Disabling combination

If you want to work **only with the base colors**, you can disable color combining entirely using the `--no-combine` flag.

## Usage

Run the program with a target palette size:

```bash
uv run python palette.py --size 32
```

### Arguments

| Argument       | Description                                     |
| -------------- | ----------------------------------------------- |
| `--size`       | Desired number of colors in the final palette   |
| `--no-combine` | Disable generation of combined colors           |
| `--mix-mode`   | Color mix mode: `average`, `add`, or `multiply` |

### Examples

Generate a palette using base colors **and** averaged mixes:

```bash
uv run python palette.py --size 32
```

Generate a palette using **only base colors**:

```bash
uv run python palette.py --size 16 --no-combine
```

Generate a palette using additive color mixing:

```bash
uv run python palette.py --size 32 --mix-mode add
```

**Note:**
The target size must be **greater than or equal to** the number of base colors.

## Output

After execution, two files are generated:

### `palette.png`

* A visual preview of the palette
* Each color is rendered as a **32×32 pixel square**
* Colors are arranged in a grid

### `palette.txt`

* One color per line
* Format:

```txt
#FF5733 Red Orange
#1F3A5F Dark Blue
#A8C686 Light Green
```

Each line contains:

1. The hex color value
2. A human-readable color name (from color.pizza)

## How it works (high-level)

1. Base colors are loaded from `colors.txt`
2. Optional pairwise color combinations are generated
3. All colors are converted from RGB to CIELAB
4. A greedy **max-min distance** algorithm selects colors that are maximally distinct
5. Distance is measured using **ΔE2000**, a perceptual color difference metric
6. Selected colors are named using the color.pizza API
7. Results are written to disk

This ensures that every added color contributes new, visually distinct information to the palette.

## Notes

* The color.pizza API is queried in a single batch request
* Network access is required for color naming
* If naming fails, the program will raise an error