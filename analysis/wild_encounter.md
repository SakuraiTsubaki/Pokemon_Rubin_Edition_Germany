# German wild_encounter module

The complete `wild_encounter` text module has been bounded directly in the supplied German Retail Rev 0, Retail Rev 1 and Debug ROMs.

## Module boundary

| Profile | Start | End exclusive | Size | SHA-256 |
| --- | --- | --- | ---: | --- |
| Retail Rev 0 / Rev 1 | 0x08084DCC | 0x08085ABC | **3,312 bytes (0xCF0)** | `957aab21eeb0e9a3f6fe29b2b0a8884ab46f3d1ca239c48f02ad38a548357413` |
| Debug | 0x08092138 | 0x08092E88 | **3,408 bytes (0xD50)** | `b9022adf9e727020045e3f601fa1073865d2cf5f4f510eae98c8e79708da6cdc` |

Retail Rev 0 and Rev 1 are byte-identical across the complete module.

Debug adds exactly **0x60 bytes**, changing the accumulated Retail-to-Debug text displacement from **+0xD36C** at entry to **+0xD3CC** at exit.

## Entry anchor

The first function is source-correlated as `DisableWildEncounters`:

`01 49 08 70 70 47 00 00`

The following literal is the profile-specific `gWildEncountersDisabled` byte:

- Retail: **0x0202FF7C**
- Debug: **0x02030228**

## Encounter runtime

The source-correlated module contains **32 explicit functions**, including two Debug-only functions.

It covers:

- Route 119 Feebas water-tile numbering and six Feebas spots;
- Feebas RNG seeding and the 50% Feebas encounter gate;
- land/water/fishing encounter-slot selection;
- wild level generation;
- current-map wild header lookup;
- wild nature selection;
- wild Pokémon creation;
- outbreak and roamer integration;
- encounter-rate dice rolls;
- standard field encounters;
- Rock Smash, Sweet Scent and fishing encounters;
- local wild/water species queries;
- Repel step countdown;
- Repel, flute and Cleanse Tag encounter filtering/modification.

## Debug growth

The two Debug-only functions account for the entire **0x60-byte** increase.

### FeebasDebug_GetTrueNumberOfWaterTilesInMapThird

- Debug: **0x08092344..0x0809236C**
- size **0x28**
- SHA-256 `4e4b5a83b8afa73f3f3b25eb73c5bf3491531398dbd0805fe22e2608dd957b42`

It returns the three Route 119 section water-tile totals used by the Debug build: **131, 167 and 149**.

### debug_sub_809283C

- Debug: **0x0809283C..0x08092874**
- size **0x38**
- SHA-256 `3c06b8bdc88b76b1777c7337fe0fc9144061ef10bf1505ebe5feb7d703f4e7a0`

It repeatedly runs the encounter-rate dice roll at rate 320 and returns the number of successful rolls.

Therefore:

**0x28 + 0x38 = 0x60**

## Tail anchor

The final function is source-correlated as `ApplyCleanseTagEncounterRateMod`.

- Retail: **0x08085A94..0x08085ABC**
- Debug: **0x08092E60..0x08092E88**
- size **0x28**

SHA-256:

- Retail: `dbb891d095b12726f53ac3658337ec1168a99ab0f35a94dd1eda1b70c189a1c6`
- Debug: `53f5e67a03e31cde8943aa20a7044fd19816594da491d2fe9b41a023480169b2`

Source semantics check the lead party Pokémon's held item and, for Cleanse Tag, multiply the encounter rate by 2/3.

## Next-module anchor

`field_effect` begins immediately afterward:

- Retail Rev 0 / Rev 1: **0x08085ABC**
- Debug: **0x08092E88**
- accumulated delta: **+0xD3CC**

The first function is source-correlated as `FieldEffectStart`.

Common prefix:

`30 B5 82 B0 04 1C 24 06 24 0E 20 1C`

The function adds the field-effect ID to the active list, fetches the effect script and interprets it through the field-effect command table until completion.
