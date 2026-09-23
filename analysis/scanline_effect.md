# German scanline_effect module

The German ROM binaries directly bound this module as follows.

- Retail Rev 0 / Rev 1: `0x080899CC..0x08089EC4`, **0x4F8 bytes**, SHA-256 `96bc747002423e226b44f4b0cc7152350f42b579daa3437b32acb0fcb8995522`
- Debug: `0x08096D98..0x08097290`, **0x4F8 bytes**, SHA-256 `f21a414215e96ff73766c4f4a72d0895fb6dd8b2536768c411bf093e3663795c`
- Rev 0 / Rev 1 are byte-identical.
- Debug adds no text here; accumulated displacement remains **+0xD3CC**.

## Entry

The first function is source-correlated as `ScanlineEffect_Stop`.

Common first 34 bytes:

`10 B5 0B 4C 00 20 60 75 0A 49 4A 89 0A 48 10 40 48 81 4A 89 09 48 10 40 48 81 48 89 20 7E FF 28 03 D0`

It clears the scanline-effect state, stops DMA0 and destroys the wave task if active.

## Runtime

The source-correlated module has 9 functions: stop, clear, parameter setup, HBlank DMA initialization, 16/32-bit first-scanline copies, per-frame wave update, wave generation and wave initialization.

The implementation uses double-buffered per-scanline register values and swaps the active source buffer each frame.

## Tail

The final function is `ScanlineEffect_InitWave`.

- Retail: `0x08089D98..0x08089EC4`
- Debug: `0x08097164..0x08097290`
- size: **0x12C**
- Retail SHA-256: `2cb3c4a1583878673bc356e585587bc6aaf5b0307bf048245054fb1b77498e9d`
- Debug SHA-256: `daecf910e078672460d5f3678f5f7c946c50bb6ac6f583bfbbe67cd730d35b36`

## Next

`pokemon_menu` begins immediately afterward:

- Retail: **0x08089EC4**
- Debug: **0x08097290**
- delta: **+0xD3CC**

The first function is source-correlated as `sub_8089A70` and begins:

`00 B5 05 48 01 7A 80 22 11 43 01 72 00 20 00 21`

The following `gPaletteFade` literal is Retail **0x0202F388**, Debug **0x0202F62C**.
