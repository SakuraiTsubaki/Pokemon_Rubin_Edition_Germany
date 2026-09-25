# German script_movement module

The complete `script_movement` text module has been bounded directly in the German Retail Rev 0, Retail Rev 1 and Debug ROMs.

## Boundary

- Retail Rev 0 / Rev 1: **0x080A2224..0x080A2654**, size **0x430 = 1,072 bytes**, SHA-256 `2f2790d8621ae2fe724a8dfd52479b24a91c4f9eed2c68782c0753d5f9c88750`
- Debug: **0x080AFAB4..0x080AFEE4**, size **0x430**, SHA-256 `5325c59d58f13c5a416f9e2cc57e0f2731664b11be16e1f1f40bd054b3fc29f4`
- Retail Rev 0 and Rev 1 are byte-identical.
- no Debug-only text; delta remains **+0xD890**.

## Runtime scope

The source-correlated module contains **18 explicit functions** and no Debug-only code.

It implements script-driven object movement:
- object lookup by local/map ID;
- shared priority-50 movement task creation;
- up to 16 movement-script slots;
- held-movement dispatch;
- movement-script completion tracking;
- movement-script pointer storage;
- freezing/unfreezing object events when a script terminates.

The script terminator is source-correlated as **0xFE**.

## Entry

The first function is `ScriptMovement_StartObjectMovementScript`.

Common prefix:

`10 B5 81 B0 1C 1C 00 06 00 0E 09 06 09 0E 12 06 12 0E 6B 46`

It resolves the target object event, ensures the shared movement task is active, then attaches the supplied movement script.

## Tail

The final function is source-correlated as `sub_80A2490`.

- Retail: **0x080A25E0..0x080A2654**, size **0x74**, SHA-256 `0f3221843beaae8637a85ce0cabc224447f080f745aa2e91ef5f0079f7131066`
- Debug: **0x080AFE70..0x080AFEE4**, size **0x74**, SHA-256 `9917805dcfa0b391d9cff9c7080cccad65081f17107c6b286bf6d2e76df5e4b7`

It waits for any held movement to finish, consumes the next movement byte, freezes the object on 0xFE, or advances the script pointer after successfully assigning the next held movement.

## Next module

`fldeff_cut` begins immediately afterward.

Retail:
- start **0x080A2654**
- first function `SetUpFieldMove_Cut`

Debug:
- start **0x080AFEE4**
- first function `Debug_SetUpFieldMove_Cut`

The different entry functions are expected because the Debug-only Cut setup helper appears first in the source module.

Retail entry prefix:

`F0 B5 47 46 80 B4 52 20 69 F0 34 F8 00 06 00 0E 01 28`

Debug entry prefix:

`F0 B5 47 46 80 B4 52 20 70 F0 24 FC 00 06 00 0E 01 28`

Historical numeric labels remain semantic identifiers only; German addresses are independently established from the German binaries.
