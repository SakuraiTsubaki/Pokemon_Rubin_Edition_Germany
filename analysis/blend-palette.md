# German blend_palette module

The module contains one palette interpolation routine.

## Boundary

| Profile | Start | End exclusive | Size | SHA-256 |
| --- | --- | --- | ---: | --- |
| Retail Rev 0 / Rev 1 | 0x08041534 | 0x080415D4 | 160 bytes (0xA0) | 13150341e5969b2327aed9ed6452aa2d6da482e3527ee5fedaac3a123d5da778 |
| Debug | 0x080456B0 | 0x08045750 | 160 bytes (0xA0) | f98222f2d23d62a0b4c281964709531e1725a0bc394a8406ae481dc860cb070b |

Retail Rev 0 and Rev 1 are byte-identical. There is no Debug-only growth and the code remains at **+0x417C**.

## BlendPalette

`BlendPalette(palOffset, numEntries, coeff, blendColor)` reads each source color from `gPlttBufferUnfaded` and writes the blended result to `gPlttBufferFaded`.

For each 5-bit GBA RGB channel:

`out = source + ((target - source) * coeff >> 4)`

Therefore the coefficient is effectively a **/16 interpolation factor**:

- coeff 0 -> original unfaded color;
- coeff 16 -> target blend color.

The routine processes exactly `numEntries` consecutive 15-bit RGB555 entries starting at `palOffset`.

This low-level behavior is shared by fades and visual effects and should remain bit-exact for legacy rendering.

## Next module

The next linked module, `daycare`, begins at:

- Retail **0x080415D4**
- Debug **0x08045750**
- delta **+0x417C**
