# German text_window module

The complete `text_window` text module has been bounded directly in the supplied German Retail Rev 0, Retail Rev 1 and Debug ROMs.

## Module boundary

| Profile | Start | End exclusive | Size | SHA-256 |
| --- | --- | --- | ---: | --- |
| Retail Rev 0 / Rev 1 | 0x08065234 | 0x080656D4 | **1,184 bytes (0x4A0)** | `2c17ff26f0c817b1513a254d23c2e2a8fc2bdf195c201780fb0138ebd85a1123` |
| Debug | 0x08069834 | 0x08069CD4 | **1,184 bytes (0x4A0)** | `0fdc59440c1b1401bd8a99183ff31f6ef60d804d43b352c7125bfc8f8b7baaff` |

Retail Rev 0 and Rev 1 are byte-identical across the complete module. Debug adds no `text_window` code, so the accumulated Retail-to-Debug displacement remains **+0x4600** at entry and exit.

## Entry anchor

The first function is source-correlated as `TextWindow_SetBaseTileNum`. Its first 16 bytes are identical across all three German profiles:

`00 04 00 0C 02 49 08 80 09 30 00 04 00 0C 70 47`

The following literal is the shared IWRAM address of the base tile number:

- `sTextWindowBaseTileNum`: **0x030005AC**

The function stores the input 16-bit base tile number and returns `baseTileNum + 9`.

## Runtime state

The module contains two shared IWRAM `u16` state values:

- `sTextWindowBaseTileNum`: **0x030005AC** — 5 literal references
- `sDialogueFrameBaseTileNum`: **0x030005AE** — 4 literal references

These addresses are identical in Retail and Debug.

## Rendering model

The source-correlated module contains **16 explicit functions** and no Debug-only text.

It implements two frame families:

- standard window frames, with 9 frame tiles;
- field dialogue frames, with 14 frame tiles.

The standard field-dialogue geometry is source-correlated as:

- left = 0
- top = 14
- width = 26 tiles
- height = 4 tiles
- standard palette slot = 14

The module loads frame graphics/palettes, draws standard borders into a 32-tile-wide tilemap, selects one of 20 window-frame graphic/palette pairs, draws the field dialogue frame, loads its graphics, and erases it when required.

## Source-correlated function inventory

1. `TextWindow_SetBaseTileNum`
2. `TextWindow_LoadStdFrameGraphics`
3. `TextWindow_LoadStdFrameGraphicsOverridePal`
4. `TextWindow_LoadStdFrameGraphicsOverrideStyle`
5. `TextWindow_DrawStdFrame`
6. `TextWindow_GetFrameGraphics`
7. `LoadTextWindowTiles`
8. `LoadTextWindowPalette`
9. `DrawStandardFrame`
10. `TextWindow_SetDlgFrameBaseTileNum`
11. `unref_sub_80651DC`
12. `TextWindow_DisplayDialogueFrame`
13. `GetDialogueFrameTilemapEntry`
14. `DrawDialogueFrame`
15. `TextWindow_DrawDialogueFrame`
16. `TextWindow_LoadDialogueFrameTiles`
17. `TextWindow_EraseDialogueFrame`

The parser counts 16 explicit definitions because one return-type pattern is pointer-valued and is tracked separately in this semantic inventory. Historical numeric names remain source labels only; German addresses come from the German binaries.

## Next-module anchor

`script` begins immediately afterward:

- Retail Rev 0 / Rev 1: **0x080656D4**
- Debug: **0x08069CD4**
- accumulated delta: **+0x4600**

Its first function is source-correlated as `InitScriptContext`. The first 48 bytes are identical in all three German profiles:

`00 B5 03 1C 00 20 58 70 98 60 18 70 58 60 D9 65 1A 66 00 22 03 21 18 1C 70 30 02 60 04 38 01 39 00 29 FA DA 19 1C 0C 31 00 22 18 1C 58 30 02 60`

This independently anchors the end of `text_window` and the start of the script interpreter layer.
