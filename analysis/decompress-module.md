# German decompression module

The complete module immediately after battle_controllers is now bounded and mapped.

## Exact module identity

| Profile | Start | End exclusive | Size | SHA-256 |
| --- | --- | --- | ---: | --- |
| Retail Rev 0 / Rev 1 | 0x0800D40C | 0x0800D858 | 1,100 bytes | 8214643be8cafdff49ca26dfa48cdbce01e99cedf26e6143d5e5754625190feb |
| Debug | 0x0800D628 | 0x0800DA74 | 1,100 bytes | b49b41f45d0812ec8342a6a77345cc789f9e0ed6ce76dbadd3855ecd1248a8fd |

Retail Rev 0 and Rev 1 are byte-identical across the complete module.

Every Debug function remains exactly +0x21C from Retail. No Debug-only code is inserted here.

## Function map

| Function | Retail | Debug | Size | Role |
| --- | --- | --- | ---: | --- |
| LZDecompressWram | 0x0800D40C | 0x0800D628 | 12 | thin wrapper around BIOS LZ77 WRAM decompression |
| LZDecompressVram | 0x0800D418 | 0x0800D634 | 12 | thin wrapper around BIOS LZ77 VRAM decompression |
| LoadCompressedObjectPic | 0x0800D424 | 0x0800D640 | 44 | decompress sprite sheet to EWRAM and load it |
| LoadCompressedObjectPicOverrideBuffer | 0x0800D450 | 0x0800D66C | 40 | decompress sprite sheet to caller buffer and load it |
| LoadCompressedObjectPalette | 0x0800D478 | 0x0800D694 | 52 | decompress object palette to EWRAM and load it |
| LoadCompressedObjectPaletteOverrideBuffer | 0x0800D4AC | 0x0800D6C8 | 48 | decompress object palette to caller buffer and load it |
| DecompressPicFromTable_2 | 0x0800D4DC | 0x0800D6F8 | 44 | decompress normal species image or fallback question-mark image |
| HandleLoadSpecialPokePic | 0x0800D508 | 0x0800D724 | 68 | select front/back context and forward to special Pokemon-picture loader |
| LoadSpecialPokePic | 0x0800D54C | 0x0800D768 | 168 | handle Unown forms, unknown-species fallback and Spinda spots |
| Unused_LZDecompressWramIndirect | 0x0800D5F4 | 0x0800D810 | 12 | unused pointer-indirect LZ77 WRAM wrapper |
| unref_sub_800D42C | 0x0800D600 | 0x0800D81C | 600 | repack compacted Pokemon tile objects into centered 8x8-tile canvases |

## Recovered behavior

### LZ77 wrappers

The first two functions call the GBA decompression services used for WRAM and VRAM destinations.

### Object graphics

The object-picture and object-palette loaders decompress into either:

- the standard EWRAM scratch area, or
- a caller-provided override buffer,

then construct the temporary sprite-sheet/palette descriptor passed into the graphics loader.

### Pokemon picture selection

DecompressPicFromTable_2 uses a fallback image when the species value is beyond the original egg boundary.

LoadSpecialPokePic additionally performs:

- Unown form selection from personality bits;
- front/back table selection;
- fallback handling for out-of-range species;
- post-decompression Spinda spot drawing.

These comparisons are important expansion constraints because the original code directly embeds the Generation III species boundary and Unown form mapping assumptions.

### Legacy tile repacker

The final 600-byte routine repacks compacted Pokemon graphics into centered 8x8-tile canvases.

It has dedicated behavior for object sizes 5, 6 and 7 and is explicitly layout-oriented rather than a generic LZ routine. This should be preserved as a compatibility path until all callers are mapped.

## Expansion significance

This module is one of the first graphics areas that will need deliberate modernization rather than blind table growth:

- species-out-of-range fallback logic must not classify future valid species as unknown;
- Unown form mapping is hard-coded around the original species ordering;
- front/back graphics tables are accessed by species-derived indexes;
- EWRAM scratch assumptions need auditing when larger or additional sprite assets are introduced.

No expansion changes have been applied yet; this commit records the German original behavior.

## Next boundary

The next module begins at:

- Retail: 0x0800D858
- Debug: 0x0800DA74

Module-order and call-pattern evidence identify it as battle background code.
