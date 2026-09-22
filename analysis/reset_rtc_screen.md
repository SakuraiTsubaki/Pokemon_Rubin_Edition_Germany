# German reset_rtc_screen module

The complete `reset_rtc_screen` text module has been bounded directly in the supplied German Retail Rev 0, Retail Rev 1 and Debug ROMs.

## Module boundary

| Profile | Start | End exclusive | Size | SHA-256 |
| --- | --- | --- | ---: | --- |
| Retail Rev 0 / Rev 1 | 0x0806A7C0 | 0x0806B21C | **2,652 bytes (0xA5C)** | `77007b88f74c8d930d9ca9a753bb307fee59a46903a68276d4a183e80057d9f9` |
| Debug | 0x0806EE9C | 0x0806FB44 | **3,240 bytes (0xCA8)** | `ba808e9fe207c8925504f661ae8ff1e6c19079a15eff92e50319d112e0f43914` |

Retail Rev 0 and Rev 1 are byte-identical across the complete module.

Debug is **588 bytes (0x24C)** larger. The accumulated Retail-to-Debug displacement changes from **+0x46DC** at entry to **+0x4928** at the following `party_menu` module.

## Entry anchor

The first function is source-correlated as `SpriteCB_ResetRtcCusor0`.

Common first 32 bytes:

`00 B5 03 1C 0A 4A 2E 20 19 5E 88 00 40 18 C0 00 80 18 0C 22 81 5E 30 22 98 5E 81 42 7B D0 19 86`

It reads the active reset-RTC selection from the task referenced by the cursor sprite and updates visibility, animation number and position.

## Retail/common runtime

The common body implements the complete reset-RTC UI and save flow:

- two animated cursor sprites;
- cursor palette setup/free;
- current/previous time display;
- day/hour/minute/second selection;
- RTC offset reset;
- save-file validation;
- reset confirmation;
- save write result;
- palette fade and soft reset.

The reset-time selector has five entries: day, hour, minute, second and OK.

## Debug growth

The Debug common body runs from **0x0806EE9C to 0x0806F8F8**, exactly **0xA5C bytes**, matching the Retail module size.

The final **0x24C bytes** are Debug-only:

| Function | Range | Size | SHA-256 |
| --- | --- | ---: | --- |
| `debug_sub_806F8F8` | 0x0806F8F8..0x0806F908 | 0x10 | `b9d46c8666dc6f80f76512bbb1f37a39d6138b241016bf33b02dd9058a03c673` |
| `debug_sub_806F908` | 0x0806F908..0x0806F99C | 0x94 | `3b79039f0fae18532c2e87e45a8e09cd5f8e5c50c615b1d315b4e27f75d5b52b` |
| `debug_sub_806F99C` | 0x0806F99C..0x0806F9B8 | 0x1C | `95685efd13811c1e99ec0d2275589c0f9c557ba76f15b42a506096e2de3f3fa5` |
| `debug_sub_806F9B8` | 0x0806F9B8..0x0806F9E4 | 0x2C | `33a72a98a81c617bdbff0da2962378a04404e79c7e9561848448f4086fad1c16` |
| `debug_sub_806F9E4` | 0x0806F9E4..0x0806FB44 | 0x160 | `69ffc50642ac5d2b7ba661e3045389c007b3426f49e56243afd2242a39b0b5c0` |

Combined Debug-only tail SHA-256:

`15903c364ae087117620114b83df44d784f8e2ded4f3177516fbd4c0db3aeccb`

The Debug-only functions expose reset-RTC screen entry, in-field clock editing, and RTC/game-time diagnostic display.

## Source-correlated inventory

The connected source contains **23 explicit function definitions**:

- **18 common**
- **5 Debug-only**

The five Debug names above happen to encode addresses that match this German Debug binary, but this project still treats those names as semantic source labels; the addresses are independently verified from the German ROM.

## Next-module anchor

`party_menu` begins immediately afterward:

- Retail Rev 0 / Rev 1: **0x0806B21C**
- Debug: **0x0806FB44**
- accumulated delta: **+0x4928**

Its first function is source-correlated as `CB2_PartyMenuMain`.

Retail entry begins:

`70 B5 81 B0 95 F7 52 FB 95 F7 76 FB`

Debug entry begins:

`70 B5 81 B0 90 F7 BE FE 90 F7 E2 FE`

Both immediately execute the party-menu sprite/OAM update path. The Debug form is larger later in the function because `party_menu` itself contains Debug-only link diagnostics; that later growth belongs to the next module, not to `reset_rtc_screen`.
