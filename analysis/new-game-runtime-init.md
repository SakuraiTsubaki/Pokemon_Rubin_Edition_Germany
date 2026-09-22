# German new-game runtime initialization

The complete `new_game` text module is bounded directly from the supplied German Retail, Rev 1 and Debug ROMs.

## Module boundary

| Profile | Start | End exclusive | Size | SHA-256 |
| --- | --- | --- | ---: | --- |
| Retail Rev 0 / Rev 1 | 0x08053040 | 0x0805329C | 604 bytes (0x25C) | ff8616201d0b9a71942cf375db42b9db673a2678deb42dcb3022ecdcfe76ec4c |
| Debug | 0x08057230 | 0x080575AC | 892 bytes (0x37C) | 7055ef8767b612ce44f42a93fb0a12d04e051f53dc23774664777cdb43b99b66 |

Retail Rev 0 and Rev 1 are byte-identical across the complete module.

Debug is exactly **288 bytes (0x120)** larger. The module starts at inherited delta **+0x41F0** and the next module begins at **+0x4310**.

The source correlates the growth with two Debug-only new-game helpers plus one Debug-only flag clear in the ordinary reset helper. The binary proves the total growth; per-helper byte attribution is intentionally not claimed until each Debug helper is statement-mapped.

## Retail function map

| Function | Retail start | Role |
| --- | --- | --- |
| write_word_to_mem | 0x08053040 | serialize 32-bit value little-endian into four bytes |
| copy_word_to_mem | 0x08053050 | copy four bytes |
| InitPlayerTrainerId | 0x0805306C | combine two 16-bit RNG results into trainer ID |
| SetDefaultOptions | 0x08053094 | initialize text/window/sound/battle/map options |
| ClearPokedexFlags | 0x080530B8 | clear owned/seen flags |
| ResetContestAndMuseumWinners | 0x080530E8 | clear contest/museum winner state |
| ZeroBattleTowerData | 0x08053124 | clear Battle Tower save data |
| WarpToTruck | 0x08053144 | set initial truck warp and enter map |
| ClearSav2 | 0x08053164 | zero SaveBlock2 then restore default options |
| sub_8052E4C | 0x0805318C | reset runtime/new-save working state |
| NewGameInitData | 0x080531AC | initialize complete new-game save/runtime state |

Historical source names are only semantic labels; the addresses above are German Retail binary locations.

## Trainer ID

`InitPlayerTrainerId` calls the already mapped main RNG twice and forms:

`trainerId = (Random() << 16) | Random()`

`write_word_to_mem` then stores the resulting 32-bit value little-endian in SaveBlock2's four-byte trainer-ID field at +0x0A.

## Default options

The German Retail new game initializes:

- text speed: MID;
- window frame: 0;
- sound: MONO;
- battle style: SHIFT;
- battle scenes: enabled;
- region-map zoom: disabled.

The source explicitly notes that L=A is not initialized here.

## NewGameInitData

The normal new-game path performs a broad schema reset rather than only clearing the player party.

Major operations include:

- optionally reset RTC when save status is 0 or 2;
- mark this as a different/new save file;
- zero player and enemy parties;
- reset Pokédex and Battle Tower;
- zero all of SaveBlock1;
- clear mail;
- clear SaveBlock2 specialSaveWarp;
- create player Trainer ID;
- reset play time;
- clear Pokédex owned/seen flags;
- initialize event flags/variables;
- clear TV, Gabby/Ty, Secret Bases and Berry Trees;
- set starting money to **3000**;
- reset game statistics, contests, museum winners and link battle records;
- reset Pokémon storage;
- clear Roamer state;
- clear registered item and bag;
- initialize PC items;
- clear Pokéblocks and decorations;
- initialize Easy Chat, Mauville old man, Dewford trend, Fan Club and Lottery;
- warp to the moving truck;
- run the map-flag reset event script.

This is the canonical legacy initialization boundary for any expanded save/runtime model.

## SaveBlock interaction

`ClearSav2` zeroes the full legacy SaveBlock2, then reapplies default options. `NewGameInitData` separately clears the full SaveBlock1.

A modern expanded format should therefore keep legacy SaveBlock1/2 reset logic isolated from new extension blocks; otherwise new-game initialization can accidentally erase extension metadata.

## Debug-only bootstrap

The Debug build includes additional new-game development helpers.

One helper cycles among four development warp targets.

The large Debug bootstrap begins at **0x08057508** and:

- sets the Debug inspection flag;
- calls normal `NewGameInitData`;
- sets money to **999999**;
- enables Pokémon/Pokédex/PokéNav/running-system flags;
- gives a level **99 Treecko**;
- optionally names it **KRÖTE**;
- invokes several development setup routines and initializes time-based events.

This is development tooling and must remain a separate Debug profile, not leak into the German Retail reconstruction.

## Debug growth

Total module growth:

`0x37C - 0x25C = 0x120 = 288 bytes`

Accumulated address displacement therefore changes:

`+0x41F0 -> +0x4310`

## Next module

`overworld` begins with `DoWhiteOut` at:

- Retail **0x0805329C**
- Debug **0x080575AC**
- delta **+0x4310**

The function identity is binary-proven by the sequence: run White Out script, halve SaveBlock1 money, heal party, reset overworld flags, warp to last heal location and enter the map.
