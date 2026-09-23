# German field_fadetransition module

The complete `field_fadetransition` text module has been bounded directly in the supplied German Retail Rev 0, Retail Rev 1 and Debug ROMs.

## Module boundary

| Profile | Start | End exclusive | Size | SHA-256 |
| --- | --- | --- | ---: | --- |
| Retail Rev 0 / Rev 1 | 0x08080CA8 | 0x080817A0 | **2,808 bytes (0xAF8)** | `f96353b9c87675df5ce13131a1fca193b058f8dda2a2770fa1baedf49dc34068` |
| Debug | 0x0808805C | 0x08088B68 | **2,828 bytes (0xB0C)** | `1e8a0f4842a41da185180921af4747d6b63f0eb81bedae9b88edf0b01100a8dd` |

Retail Rev 0 and Rev 1 are byte-identical across the complete module.

Debug adds exactly **0x14 bytes**, changing the accumulated Retail-to-Debug displacement from **+0x73B4** at entry to **+0x73C8** at exit.

## Entry anchor

The first function is source-correlated as `palette_bg_fill_white`.

It starts with:

`00 B5 81 B0 04 48 00 90 04 49 05 4A 68 46`

and constructs the duplicated white value `0x7FFF7FFF`, targets the profile-specific faded palette buffer and fills the full **0x400-byte** palette.

The immediately following `palette_bg_fill_black` uses the same destination and size with a zero fill value.

Faded-palette destination literals:

- Retail Rev 0 / Rev 1: **0x0202EEC8**
- Debug: **0x0202F16C**

## Runtime scope

The source-correlated module contains **45 functions when the Debug-only function is included**.

Its responsibilities include:

- white/black palette fills for map transitions;
- map-pair fade direction selection;
- warp fade setup;
- player-control locking/unlocking around transitions;
- animated and non-animated door transition tasks;
- map-change sequencing;
- field/start-menu return sequencing;
- fall/warp/special-map transitions;
- cable-club/link warp sequencing;
- door-open/walk-through/door-close transition flow;
- map reload callbacks.

Historical numeric source labels are semantic identifiers only and are not German ROM addresses.

## Debug growth

The sole Debug-only executable function is source-correlated as `debug_sub_80888D8`.

German Debug range:

- **0x080888D8..0x080888EC**
- size **0x14 bytes**
- SHA-256 `ebf96fac7b416d1e95e002459d594edc90f429311a2468148935b698d33e3857`

Bytes:

`00 B5 CE F7 2B FD FF F7 C7 FE E1 F7 C5 FA 01 BC 00 47 00 00`

It consists of three calls followed by the standard return/alignment sequence. Source correlation identifies the calls as the Debug field helper, the ordinary fade/warp helper and field-control locking.

The **0x14-byte** function fully accounts for the entire Debug module growth.

## Tail anchor

The final function is source-correlated as `sub_8081334`.

- Retail: **0x08081768..0x080817A0**
- Debug: **0x08088B30..0x08088B68**
- size: **0x38 bytes**

SHA-256:

- Retail: `bb3a28ad81d2475c472a45c8aca141095b78c2e80ea28a2001b0294f1c0d12aa`
- Debug: `2ec098ec081f221e2158188eb5db786baed13fbce2bfa7049a60c889ccc0846e`

Source semantics lock field controls, fade the old map music and screen, stop rain sound, play the exit SE, set the field callback and create the final map-change task.

## Next-module anchor

`field_screen_effect` begins immediately afterward:

- Retail Rev 0 / Rev 1: **0x080817A0**
- Debug: **0x08088B68**
- accumulated delta: **+0x73C8**

The first function is source-correlated as `SetFlashScanlineEffectWindowBoundary`.

Common first 48 bytes:

`00 B5 A0 29 10 D8 00 2A 00 DA 00 22 FF 2A 00 DD FF 22 00 2B 00 DA 00 23 FF 2B 00 DD FF 23 49 00 09 18 10 02 18 43 08 80 01 BC 00 47 F0 B5 57 46`

It clamps a scanline/window boundary to the GBA screen/window range and writes the packed left/right value. The following `F0 B5 57 46` begins the multi-scanline boundary builder, providing an additional contiguous boundary anchor.
