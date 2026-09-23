# German field_screen_effect module

The complete `field_screen_effect` text module has been bounded directly in the supplied German Retail Rev 0, Retail Rev 1 and Debug ROMs.

## Module boundary

| Profile | Start | End exclusive | Size | SHA-256 |
| --- | --- | --- | ---: | --- |
| Retail Rev 0 / Rev 1 | 0x080817A0 | 0x08081D94 | **1,524 bytes (0x5F4)** | `dc3058ebd07b7a27a381d1b75b9f095c3bdc9d94e70d90076d608ca68cf6782d` |
| Debug | 0x08088B68 | 0x0808915C | **1,524 bytes (0x5F4)** | `131727fd66761d42156daeb30b806f7312f912673d8d4aa4d5cba54b5024c2a1` |

Retail Rev 0 and Rev 1 are byte-identical across the complete module. Connected source contains no Debug-only text, and the binary result matches: accumulated Retail-to-Debug displacement remains **+0x73C8** at entry and exit.

## Entry anchor

The first function is source-correlated as `SetFlashScanlineEffectWindowBoundary`.

Common function bytes:

`00 B5 A0 29 10 D8 00 2A 00 DA 00 22 FF 2A 00 DD FF 22 00 2B 00 DA 00 23 FF 2B 00 DD FF 23 49 00 09 18 10 02 18 43 08 80 01 BC 00 47`

It clamps a scanline number and left/right window boundaries and writes the packed WIN0H-style value into the destination scanline buffer.

## Runtime scope

The connected source contains **15 explicit functions** and no `#if DEBUG` code.

The module implements field screen effects centered on cave Flash and related transitions:

- single-scanline window-boundary packing;
- circle/radius scanline generation;
- Flash radius animation task;
- script-resume helper task;
- Flash-level transitions;
- scanline-buffer generation;
- palette preparation;
- alpha-blend progression;
- temporary display/blend/window register preservation and restoration;
- camera panning during the screen effect;
- special-variable-selected effect setup;
- map-music fade task.

The Flash radii source table is semantically correlated as:

`200, 72, 56, 40, 24, 0`

with maximum ordinary Flash level 4.

## Tail anchor

The final function is source-correlated as `task50_0807F0C8`.

- Retail Rev 0 / Rev 1: **0x08081D70..0x08081D94**
- Debug: **0x08089138..0x0808915C**
- size: **0x24 bytes**

SHA-256:

- Retail: `3c94a205e2b9de6a41b71323c3dd1c575fd09bd542c3e173a3602e163d90c8dc`
- Debug: `c68c8330ca0f2db300e043aeef5a6b859eedbfaab9e6c56a1722ba96364e026a`

It waits until BGM has stopped, then destroys itself and re-enables script execution.

Historical numeric naming is semantic only; the ranges above are German-ROM evidence.

## Next-module anchor

`battle_setup` begins immediately afterward:

- Retail Rev 0 / Rev 1: **0x08081D94**
- Debug: **0x0808915C**
- accumulated delta: **+0x73C8**

The first function is source-correlated as `Task_BattleStart`.

Common first 32 bytes:

`30 B5 00 06 05 0E A8 00 40 19 C0 00 04 49 44 18 00 21 60 5E 00 28 05 D0 01 28 0E D0 1D E0 00 00`

The task indexes the 0x28-byte task structure, reads the transition state, waits for field poison activity to finish, starts the battle transition, then hands control to the battle initializer when the transition completes. This independently anchors the module boundary.
