# ΔE Palette Generator

A Python tool for generating visually distinct color palettes using **perceptual color distance (ΔE2000)**.
Developed for [The Road not taken](https://github.com/xkforce/The-Road-Not-Taken).

The program:

* Loads a list of base colors from a text file
* Optionally generates mixed colors by combining base colors
* Reduces the full candidate set to a target palette size using a max-distance algorithm
* Ensures strong visual contrast between colors
* Can enforce usage of all base colors in mixed palettes
* Can sort the final palette into a perceptual gradient
* Automatically assigns human-readable color names using the **color.pizza API**
* Outputs both a PNG preview and a text representation of the final palette

## Features

* 🎨 Perceptual palette reduction using **ΔE2000**
* 📏 Target palette size configurable via CLI
* 🧪 Optional color mixing (pairwise combinations)
* 🔀 Multiple color mix modes, including perceptual **mixbox** blending
* 🪢 Adjustable mix ratio for mixbox mode
* 🧠 Human-friendly color names (via color.pizza)
* 🧬 Guaranteed base color usage in mixed palettes (optional)
* 🌈 Optional perceptual gradient sorting of the final palette
* 📄 Simple, extensible text-based color input
* 🌓 PNG palette preview with uniform swatches

## Requirements

* Python 3.11+
* [`uv`](https://github.com/astral-sh/uv)

All Python dependencies are managed by `uv`.

## Input format

The program expects a file named `colors.txt` in the project root.

### Rules

* One color per line
* Hex values must start with `#` and be 6-digit RGB
* An optional color name may be provided in parentheses
* Lines starting with `//` are treated as comments and ignored
* Malformed lines are ignored with an informational message

### Example

```txt
// Base colors with optional names
#000000 (Black)
#FFFFFF (White)
#FF0000 (Red)
#00FF00 (Green)
#0000FF (Blue)
#FFFF00 (Yellow)
#00FFFF (Cyan)
#FF00FF (Magenta)
```

## Color combining

By default, the program generates additional **derived colors** by combining all unordered pairs of base colors:

* No self-pairs (e.g. `A + A`)
* No duplicate ordering (`A + B` is the same as `B + A`)

These derived colors are added to the candidate pool before palette reduction.

### Mix modes

The way two colors are combined is controlled via the `--mix-mode` flag:

| Mode       | Description                                   |
| ---------- | --------------------------------------------- |
| `average`  | Averages RGB components of both colors        |
| `add`      | Adds RGB components and clamps to 255         |
| `multiply` | Multiplies RGB components (normalized)        |
| `mixbox`   | Perceptual pigment-style mixing (recommended) |

When using `mixbox`, you can control the mixing ratio with `--mix-ratio`:

```bash
--mix-ratio 0.0   # 100% first color
--mix-ratio 0.5   # Even mix (default)
--mix-ratio 1.0   # 100% second color
```

### Disabling combination

To work **only with base colors**, disable color combining:

```bash
--no-combine
```

## Usage

Run the program with a target palette size:

```bash
uv run python palette.py --size 32
```

### Arguments

| Argument              | Description                                                   |
| --------------------- | ------------------------------------------------------------- |
| `--size`              | Desired number of colors in the final palette                 |
| `--no-combine`        | Disable generation of combined colors                         |
| `--mix-mode`          | Color mix mode: `average`, `add`, `multiply`, `mixbox`        |
| `--mix-ratio`         | Mix ratio for `mixbox` mode (0.0–1.0)                         |
| `--ensure-base-usage` | Ensure every base color is used at least once in mixed colors |
| `--sort-palette`      | Sort the final palette into a perceptual color gradient       |

### Examples

Generate a palette using base colors and perceptual mixing:

```bash
uv run python palette.py --size 32 --mix-mode mixbox
```

Generate a palette using only base colors:

```bash
uv run python palette.py --size 16 --no-combine
```

Ensure every base color appears in at least one mix:

```bash
uv run python palette.py --size 32 --ensure-base-usage
```

Sort the palette into a perceptual gradient:

```bash
uv run python palette.py --size 32 --sort-palette
```

## Output

After execution, two files are generated:

### `palette.png`

* Visual preview of the palette
* Each color rendered as a **32×32 pixel square**
* Colors arranged in a grid
* Order reflects palette sorting (if enabled)

### `palette.txt`

* One color per line (base colors)
* Mixed colors are represented as a block with their source colors listed below

**Base color example:**

```txt
#FF0000 Red
```

**Mixed color example:**

```txt
#487E8E Mysterious Blue
  - #3AB3DA (Light Blue)
  - #474F52 (Gray)
```

Each palette entry contains:

1. The hex color value
2. A human-readable color name
3. For mixed colors, the base colors used to create the mix (listed below the color)

## How it works (high-level)

1. Base colors are loaded from `colors.txt`
2. Optional pairwise color combinations are generated
3. All colors are converted from RGB to CIELAB
4. A greedy **max-min distance** algorithm selects colors that are maximally distinct
5. Distance is measured using **ΔE2000**, a perceptual color difference metric
6. Optionally, the palette is post-processed to ensure every base color is used in mixing
7. Optionally, the palette is sorted into a perceptual gradient
8. Base colors without names are resolved using the color.pizza API
9. Results are written to disk

This ensures that every added color contributes new, visually distinct information to the palette.

## Notes

* The color.pizza API is queried in batch
* Network access is required for color naming
* Informational warnings are printed for ignored input lines or missing mix candidates
