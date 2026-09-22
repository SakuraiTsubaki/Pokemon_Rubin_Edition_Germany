# German Berry Blender module

The complete `berry_blender` text module is bounded directly in the supplied German ROMs.

## Module boundary

| Profile | Start | End exclusive | Size | SHA-256 |
| --- | --- | --- | ---: | --- |
| Retail Rev 0 / Rev 1 | 0x0804E5FC | 0x08052F68 | **18,796 bytes (0x496C)** | 62fbfcba5debf22f2b64ad53dd3c5eda741cf850c9c150d8795c7fa3b2090966 |
| Debug | 0x080527C8 | 0x08057158 | **18,832 bytes (0x4990)** | 7d7d9ca8ce896788f29041665b0b537b8c4ae462f7dc1cabecbfd46a2ac913e3 |

Retail Rev 0 and Rev 1 are byte-identical.

Debug is **36 bytes (0x24)** larger. The source has one `#if DEBUG` code insertion in normal Berry Blender result processing: it converts a development value to four hexadecimal digits and appends it to the Pokéblock result message. That block accounts for the complete binary size increase.

Therefore the accumulated text delta changes:

- module start: **+0x41CC**;
- after the Debug result-message block / module end: **+0x41F0**.

## Function inventory

- 1. Blender_ControlHitPitch
- 2. VBlankCB0_BerryBlender
- 3. VBlankCB1_BerryBlender
- 4. sub_804E2EC
- 5. sub_804E4FC
- 6. DoBerryBlending
- 7. sub_804E56C
- 8. sub_804E738
- 9. sub_804E794
- 10. sub_804E7C0
- 11. Blender_CopyBerryData
- 12. Blender_SetPlayerNamesLocal
- 13. sub_804E990
- 14. sub_804E9F8
- 15. sub_804F0F4
- 16. sub_804F16C
- 17. sub_804F1BC
- 18. sub_804F238
- 19. sub_804F2A8
- 20. sub_804F378
- 21. sub_804F81C
- 22. sub_804F844
- 23. sub_804F890
- 24. sub_804F8C8
- 25. sub_804F9F4
- 26. sub_804FB1C
- 27. sub_804FC48
- 28. sub_804FD30
- 29. sub_804FE70
- 30. sub_80500A8
- 31. sub_80501FC
- 32. sub_80502A4
- 33. Blender_GetPokeblockColor
- 34. sub_80504F0
- 35. unref_sub_80504FC
- 36. sub_8050508
- 37. unref_sub_8050514
- 38. Blender_CalculatePokeblock
- 39. BlenderDebug_CalculatePokeblock
- 40. sub_80508D4
- 41. sub_80508FC
- 42. sub_8050954
- 43. sub_8050CE8
- 44. sub_8050E30
- 45. sub_80510E8
- 46. sub_805123C
- 47. sub_8051414
- 48. sub_8051474
- 49. sub_80514A4
- 50. sub_80514F0
- 51. sub_8051524
- 52. sub_805156C
- 53. sub_8051650
- 54. sub_8051684
- 55. Blender_SetBankBerryData
- 56. unref_sub_80516F8
- 57. sub_805181C
- 58. sub_80518CC
- 59. sub_805194C
- 60. sub_805197C
- 61. sub_8051A1C
- 62. sub_8051A3C
- 63. sub_8051AC8
- 64. sub_8051AF4
- 65. sub_8051B18
- 66. sub_8051B40
- 67. sub_8051B8C
- 68. sub_8051C04
- 69. Blender_PrintBlendingResults
- 70. Blender_PrintMadePokeblockString
- 71. Blender_SortBasedOnPoints
- 72. Blender_SortScores
- 73. Blender_PrintBlendingRanking
- 74. debug_sub_80524BC
- 75. BlenderDebug_PrintBerryData
- 76. sub_80527BC
- 77. sub_8052918
- 78. sub_8052AF8
- 79. ShowBerryBlenderRecordWindow
- 80. sub_8052BD0

## Player topology

Berry Blender is built around **up to four players**.

Local/non-link play supplies named NPC opponents; the German opponent names are:

- **OPI**
- **KUMPEL**
- **TUSSI**

Four-player arrays are used for input/synchronization, selected berries, results, score ordering and arrow positions.

This is a distinct multiplayer topology from the two-party link-trade screen and should be generalized separately.

## German presentation rules

German code paths alter multiple pieces of presentation logic:

- localized NPC opponent names;
- German string-composition helpers for messages where player names are inserted;
- German berry-name concatenation;
- decimal **comma** for max-RPM output where English uses a period-style separated form;
- different horizontal alignment values for result-time/RPM text.

This module is another clear example where German localization is code + geometry + data, not only string replacement.

## Blender pitch / speed

`Blender_ControlHitPitch`, the module entry, computes the sound pitch from blender field +0x56:

`pitch = (value - 128) * 2`

and applies it to sound-effect player 2.

The Berry Blender therefore couples visual rotation speed/game state to live audio pitch.

## Pokéblock flavour model

`Blender_CalculatePokeblock` accumulates **six** per-berry values:

- five flavour values;
- smoothness.

The five flavours are processed cyclically by subtracting the next flavour, negative results are zeroed, then speed scales the positive results using:

`speedFactor = maxRPM / 333 + 100`

The resulting five flavours and feel are clamped to **255** before writing the Pokéblock.

The six final output bytes are:

- spicy;
- dry;
- sweet;
- bitter;
- sour;
- feel.

## Pokéblock colour rules

Colour selection uses the five flavour outputs, number of players and duplicate-berry checks.

Notable original behavior:

- all-zero result or too many negative flavour interactions -> Black;
- duplicate berries among players normally force Black;
- >3 positive flavours -> White;
- exactly 3 positive flavours -> Gray;
- any flavour >50 can produce Gold;
- one positive flavour maps to Red/Blue/Pink/Green/Yellow;
- two positive flavours map to the secondary colour set according to dominant flavour.

Black Pokéblocks take an additional random flavour pattern.

## Original out-of-bounds bug

The retail code path of `Blender_GetPokeblockColor` copies indices **0 through 5 inclusive** into a local array declared for five elements unless a separate `UBFIX` build option is enabled.

The supplied German retail binaries preserve the original behavior.

This is a compatibility bug and should not become part of the modern generalized Pokéblock implementation.

## Ranking

Player ranking is determined using the integer score:

`1,000,000 * BEST + 1,000 * GOOD + (1,000 - MISS)`

The resulting ordering is copied into the four-entry player-place array.

## Link synchronization

The Blender uses normal link block transport for berries and synchronized timing/results. One results step transmits the authoritative game-frame time and maximum RPM from player 0 so all participants converge on the same outcome.

This protocol should remain separate from the Pokéblock recipe calculation itself.

## Debug build addition

The Debug-only 0x24-byte result hook appends a hexadecimal development value to the normal made-Pokéblock message. It does not change the Pokéblock calculation algorithm.

## Expansion direction

For an expanded system:

- treat the four-player limit as a legacy minigame profile;
- keep the five-flavour + feel Pokéblock schema for Ruby compatibility;
- isolate the original OOB colour-calculation bug;
- keep locale-specific decimal punctuation and text layout in presentation data;
- keep recipe calculation deterministic and separate from link/session transport.

## Next module

`play_time` begins at:

- Retail **0x08052F68**
- Debug **0x08057158**
- new accumulated delta **+0x41F0**.

The entry is `PlayTimeCounter_Reset`, directly recognizable from zeroing the play-time state plus SaveBlock2 offsets +0x0E..+0x12.
