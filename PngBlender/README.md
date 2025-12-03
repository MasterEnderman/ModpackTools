# PngBlender

Merge 2 png files. Developed for [The Road not taken](https://github.com/xkforce/The-Road-Not-Taken).
Can be configured using the `settings.json`.

## Example Config

```json
{
    "paths": {
        "textures": "./textures",
        "colors": "./colors",
        "output": "./output"
    },
    "blends": {
        "brick": [
            "red",
            "#FF0000(bright_red)",
            "#00FF00",
            "#985694(purple_test)"
        ],
        "stone": [
            "#808080(gray)",
            "#A52A2A"
        ]
    }
}
```