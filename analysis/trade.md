# German trade module

The complete `trade` text module has been bounded directly in the supplied German ROMs.

## Module boundary

| Profile | Start | End exclusive | Size | SHA-256 |
| --- | --- | --- | ---: | --- |
| Retail Rev 0 / Rev 1 | 0x08047FFC | 0x0804E5FC | **26,112 bytes (0x6600)** | dcfc40527a81508441e9e0c457be2ae8554345218ca21f0b79f81423f555586c |
| Debug | 0x0804C1C8 | 0x080527C8 | **26,112 bytes (0x6600)** | 557436d7f90a9543e7ce0e1fdd05fae54f83ecbe2538d28258d4bc31fd10bef1 |

Retail Rev 0 and Rev 1 are byte-identical across the complete module.

There are no `DEBUG` compile-time insertions in this module, so the accumulated Retail→Debug text displacement remains **+0x41CC** throughout.

The module boundary is binary-proven: the final trade routine performs the battle-textbox BG load, and the next function at 0x0804E5FC is the Berry Blender pitch helper whose instruction stream reads blender field +0x56, subtracts 128, doubles it, and calls the m4a pitch-control routine.

## Source-correlated function inventory

The connected source provides the following distinct implementation names for this module. Historical `sub_804xxxx` numbers are names only and are **not** German addresses.

- 1. sub_8047CD8
- 2. sub_8047CE8
- 3. sub_8047D58
- 4. sub_8047E44
- 5. sub_8047EC0
- 6. sub_80484F4
- 7. sub_80489F4
- 8. sub_8048AB4
- 9. sub_8048B0C
- 10. sub_8048C70
- 11. nullsub_5
- 12. Trade_Memcpy
- 13. sub_8048D44
- 14. sub_8049088
- 15. sub_80490BC
- 16. sub_80491E4
- 17. sub_80492D8
- 18. sub_80494D8
- 19. sub_8049514
- 20. TradeMenuMoveCursor
- 21. sub_8049620
- 22. sub_8049680
- 23. sub_8049804
- 24. sub_8049860
- 25. sub_8049954
- 26. sub_804997C
- 27. sub_80499F0
- 28. sub_8049A20
- 29. sub_8049AC0
- 30. sub_8049BC0
- 31. sub_8049C8C
- 32. sub_8049CC4
- 33. DisplayMessageAndContinueTask
- 34. sub_8049D44
- 35. sub_8049D9C
- 36. sub_8049DC4
- 37. sub_8049DE0
- 38. sub_8049E9C
- 39. sub_8049ED4
- 40. sub_804A2B4
- 41. sub_804A33C
- 42. sub_804A41C
- 43. sub_804A51C
- 44. sub_804A6DC
- 45. sub_804A740
- 46. sub_804A80C
- 47. sub_804A840
- 48. sub_804A938
- 49. sub_804A940
- 50. sub_804A964
- 51. sub_804A96C
- 52. sub_804A96C_alt
- 53. sub_804A9F4
- 54. sub_804AA00
- 55. sub_804AA0C
- 56. sub_804AA88
- 57. sub_804AADC
- 58. sub_804AB30
- 59. sub_804ABF8
- 60. sub_804ACD8
- 61. sub_804ACF4
- 62. sub_804AE3C
- 63. sub_804AF10
- 64. sub_804AF84
- 65. sub_804AFB8
- 66. sub_804B058
- 67. sub_804B07C
- 68. sub_804B0BC
- 69. sub_804B0E0
- 70. sub_804B104
- 71. sub_804B128
- 72. sub_804B1BC
- 73. sub_804B210
- 74. sub_804B228
- 75. sub_804B24C
- 76. sub_804B2B0
- 77. sub_804B2D0
- 78. sub_804B41C
- 79. sub_804B790
- 80. sub_804BA18
- 81. sub_804BA64
- 82. sub_804BA94
- 83. sub_804BB78
- 84. sub_804BBCC
- 85. sub_804BBE8
- 86. sub_804C0F8
- 87. sub_804C164
- 88. SetTradeSceneStrings
- 89. sub_804C29C
- 90. sub_804D588
- 91. sub_804D63C
- 92. sub_804D6BC
- 93. sub_804D738
- 94. sub_804D7AC
- 95. sub_804D80C
- 96. GetInGameTradeSpeciesInfo
- 97. sub_804D8E4
- 98. _CreateInGameTradePokemon
- 99. sub_804DAD4
- 100. GetTradeSpecies
- 101. CreateInGameTradePokemon
- 102. sub_804DB84
- 103. sub_804DC18
- 104. sub_804DC88
- 105. sub_804E144
- 106. DoInGameTradeScene
- 107. sub_804E1A0
- 108. sub_804E1DC
- 109. sub_804E22C

## Trade-screen topology

The link-trade selection screen is built around exactly two six-slot parties:

- local party: logical selections **0..5**;
- remote party: **6..11**;
- Cancel: **12**.

The navigation table, party-icon arrays, level coordinates and box coordinates all encode this fixed **2 × 6 + 1** layout.

The working structure contains:

- `partyIcons[2][6]`;
- `partyCounts[2]`;
- several additional 2×6 status/selection arrays;
- **13** trade-menu option/activity entries;
- a `linkData[20]` array of 16-bit elements.

The send macro passes that link-data buffer to `SendBlock` with a length argument of **20**. The backing buffer is 20 halfwords; this analysis intentionally does not reinterpret the transport API's length unit without separately proving it.

## Pokémon records used by trade

The trade scene operates on the ordinary 0x64-byte `Pokemon` records already mapped in `pokemon_1` / `pokemon_2`.

Consequently trade inherits the same legacy limits:

- six party members per side;
- four moves per Pokémon;
- one-bit alternate-ability selection;
- Gen III personality/OT/checksum/encrypted BoxPokemon schema;
- mail and held-item fields in the existing save structures.

This makes trade protocol compatibility a separate concern from expanding the internal modern Pokémon model.

## Link trade save synchronization

The post-trade save state machine explicitly uses the `load_save` module's `specialSaveWarp` flag:

1. set special-save flag while hiding/synchronizing BG;
2. increment the Pokémon-trade game statistic;
3. run the save operation;
4. retry/poll until completion;
5. clear the special-save flag;
6. finalize link/save state before closing the link.

This connects the trade transaction boundary directly to the exact German SaveBlock2 +0x09 flag mapped in `load_save`.

## Link handshake markers

The trade scene uses explicit 16-bit markers in its link-data exchange, including **0xABCD** and **0xDCBA**, while waiting for the peers to advance through synchronization states.

Those values are protocol/state markers, not Pokémon data.

## German-specific trade presentation

The source has real `GERMAN` branches inside this module.

### Tilemap dirty/update behavior

German builds explicitly set the trade tilemap/work-buffer update flag in rendering paths where the English build's matching arrangement differs. A German-only wrapper around the common tilemap-copy helper performs the copy and then sets that update flag.

This is another concrete case where German localization changes rendering behavior rather than only replacing strings.

### Mail player-name padding

When constructing mail for an in-game trade, the German path pads the OT/player-name field using **space characters** after copying the localized OT name.

That is serialized/display-data behavior and must be retained for exact German compatibility.

## German in-game trades

The German source data defines three fixed in-game trades:

| Requested Pokémon | Received Pokémon | Received nickname | OT |
| --- | --- | --- | --- |
| Slakoth | Makuhita | **MAKIT** | **MAIK** |
| Pikachu | Skitty | **CONEC** | **MADINA** |
| Bellossom | Corsola | **CORASO** | **LIANA** |

The created Pokémon uses the player's offered Pokémon's **level**, but fixed trade data supplies the received species, six IVs, personality, OT ID/name/gender, alternate-ability flag, contest stats, sheen and held item/mail.

Its met location is set to **0xFE**, and stats are recalculated after all fixed fields are applied.

The German mail Easy Chat data is also localized independently rather than being identical to the English records.

## In-game trade construction

`_CreateInGameTradePokemon` creates the received Pokémon in `gEnemyParty[0]`, then overwrites the fixed in-game-trade fields.

Important fixed data-model assumptions:

- six explicit IV bytes;
- five contest condition values + sheen;
- fixed personality;
- fixed OT ID;
- optional second-ability bit;
- held item and optional mail.

`GetTradeSpecies` refuses Eggs by returning `SPECIES_NONE`.

## Trade evolution / provenance

The surrounding scene integrates the ordinary evolution and Pokédex systems after a trade. Because the received Pokémon remains a normal Gen III Pokémon record, trade evolution, held-item evolution and Pokédex updates continue through the already mapped legacy species/evolution registry.

A modern implementation should therefore separate:

1. transport/session protocol;
2. trade-screen presentation;
3. Pokémon-record serialization/adaptation;
4. post-trade evolution and Pokédex policy.

## Expansion direction

For a Gen-10-ready implementation:

- preserve the German 2×6 link-trade screen as a legacy UI;
- version or adapt exchanged Pokémon records instead of widening legacy 0x64-byte records in-place;
- keep the original link markers/session state for Ruby-compatible sessions;
- expose modern party/storage sizes behind an adapter;
- keep localized in-game trade records as data;
- preserve German-specific mail padding and render-update behavior in the legacy German profile.

## Next module

`berry_blender` begins at:

- Retail **0x0804E5FC**
- Debug **0x080527C8**
- delta **+0x41CC**

The first function is `Blender_ControlHitPitch`.
