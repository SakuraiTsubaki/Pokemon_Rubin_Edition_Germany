# German pokemon_summary_screen module

The complete `pokemon_summary_screen` text module has been bounded directly in the German Retail Rev 0, Retail Rev 1 and Debug ROMs.

## Boundary

| Profile | Start | End exclusive | Size | SHA-256 |
| --- | --- | --- | ---: | --- |
| Retail Rev 0 / Rev 1 | 0x0809D998 | 0x080A2224 | **18,572 bytes (0x488C)** | `7340ceeb3b69f3ff1fb65a3a64b0a29d89841b2decb3eac6d3ed0ee1ce66d94b` |
| Debug | 0x080AB1DC | 0x080AFAB4 | **18,648 bytes (0x48D8)** | `59eb2394e4ba40e321aa4f6654efa6d0ce358d3f6f85747dc6d6d11462ba2337` |

Retail Rev 0 and Rev 1 are byte-identical. Debug adds **0x4C bytes**, changing the accumulated Retail-to-Debug displacement from **+0xD844** to **+0xD890**.

## Runtime scope

The connected source contains **117 explicit functions**. The module implements the Pokémon summary screen: ordinary and PC modes, move-selection modes, screen/graphics loading, mon sprite and cry, info/skills/move/contest pages, trainer memo, move ordering, status/Pokérus display, markings, ball sprite and colored summary text.

Historical numeric source labels are semantic identifiers only. German addresses are established from the German binaries.

## Debug growth

The source has exactly two `#if DEBUG` executable blocks.

### Per-frame link receive display

The first function is `sub_809D844`.

Retail:
- **0x0809D998..0x0809D9B0**
- size **0x18**
- SHA-256 `8bfa5e539a0f88e0d017278123bb240fe32c14bd337a95b92fa59ce1cb4dd539`

Debug:
- **0x080AB1DC..0x080AB220**
- size **0x44**
- SHA-256 `a952d10abc36c12d19d21859467541ff4b57851534d6dec83158dece17ee382e`

The Debug function is **0x2C bytes larger**. Source correlation identifies the added path as the link-open check and receive-queue Debug display.

### Graphics-completion link display

The second Debug block is in the summary-screen initialization state machine after installing VBlank/main callbacks and enabling palette transfers. If link is open, it calls the Debug VRAM/link display helper.

After accounting for the first function's +0x2C, the remaining binary-proven module growth is exactly **0x20 bytes**, matching this second and only remaining Debug source guard.

Thus:

**0x2C + 0x20 = 0x4C**

No finer per-instruction interpretation is invented.

## Tail

The final function is source-correlated as `sub_80A20A8`.

- Retail: **0x080A21F8..0x080A2224**
- Debug: **0x080AFA88..0x080AFAB4**
- size **0x2C**

SHA-256:
- Retail: `9696dceaf51f770b406a676fb441b6ae3dbb275315a35ad88802dd35c5948e11`
- Debug: `436b6c9eb5c0bd0cc79f6b6c2e697a5c0e56a64e9b39b5c7bfc27dcfe520a3a5`

It waits for the field helper to complete and restores the task's saved callback.

The four bytes immediately before this function are a Thumb-function pointer from the previous helper and are not part of `sub_80A20A8`; this prevents an off-by-four tail boundary.

## Next module

`script_movement` begins immediately afterward:

- Retail: **0x080A2224**
- Debug: **0x080AFAB4**
- delta: **+0xD890**

The first function is `ScriptMovement_StartObjectMovementScript`.

Common prefix before the profile-specific branch:

`10 B5 81 B0 1C 1C 00 06 00 0E 09 06 09 0E 12 06 12 0E 6B 46`

It resolves the object event by local/map ID, ensures the shared script-movement task exists, and attaches the requested movement script.
