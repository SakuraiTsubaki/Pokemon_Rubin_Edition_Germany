# German palette module

The complete `palette` text module has been bounded directly in the supplied German Retail Rev 0, Retail Rev 1 and Debug ROMs.

## Module boundary

| Profile | Start | End exclusive | Size | SHA-256 |
| --- | --- | --- | ---: | --- |
| Retail Rev 0 / Rev 1 | 0x08073DD4 | 0x08074F6C | **4,504 bytes (0x1198)** | `00253a220123b34da98a8f730bbd40566732cd88f3062ed8535393bf98915e22` |
| Debug | 0x0807B040 | 0x0807C1D8 | **4,504 bytes (0x1198)** | `68f011f71b92e1c424fe5767d750d9ff8a32ad2db28a8c1cd7510d4cc4f2a3ba` |

Retail Rev 0 and Rev 1 are byte-identical across the complete module. Debug adds no `palette` text, so the accumulated Retail-to-Debug displacement remains **+0x726C**.

## Entry anchor

The first function is `LoadCompressedPalette`.

Stable setup:

`70 B5 0C 1C 15 1C 24 04 24 0C 2D 04 0A 4E 31 1C`

It decompresses source palette data to the palette work buffer and copies the requested range into both the unfaded and faded palette buffers.

## Runtime palette buffers

The final functions reference the profile-specific palette buffers:

- unfaded: Retail **0x0202EAC8**, Debug **0x0202ED6C**
- faded: Retail **0x0202EEC8**, Debug **0x0202F16C**

Each buffer covers the complete 0x200-entry GBA palette domain.

## Fade system

The source-correlated module contains **32 explicit functions** and no Debug-only text.

It implements:

- compressed/uncompressed palette loading and filling;
- PLTT transfer;
- reset/readback;
- normal software fades;
- fast palette fades;
- hardware blend fades;
- blend-register updates;
- palette masking/blending for faded and unfaded buffers.

The fade runtime separates source/unfaded palette state from the displayed/faded palette state, allowing weather, transitions and battle/field effects to compose palette changes without destroying the original colors.

## Tail anchor

The final source-correlated function is `BlendPalettesUnfaded`. Its literal pool contains the two profile-specific palette-buffer addresses above and the hardware palette constant **0x040000D4 / 0x84000100** used by the nearby transfer/fade machinery.

The literal pool is included through the module end-exclusive address.

## Next-module anchor

`sound` begins immediately afterward:

- Retail Rev 0 / Rev 1: **0x08074F6C**
- Debug: **0x0807C1D8**
- accumulated delta: **+0x726C**

Its first function is `InitMapMusic`.

Common code:

`00 B5 03 49 00 20 08 70 00 F0 80 F8 01 BC 00 47`

The following literal is the profile-specific `gDisableMusic` byte:

- Retail: **0x03004AFC**
- Debug: **0x03004BD4**

The function clears the disable flag, calls `ResetMapMusic`, and returns. This independently anchors the palette/sound transition.
