# German Debug battle-tool subsystem

This record corrects the earlier over-broad classification that treated the entire 0x08010800..0x080139E3 span as Debug-only.

## Debug-only tool block A

- Start: **0x08010800**
- End exclusive: **0x080132F0**
- Size: **10,992 bytes (0x2AF0)**
- SHA-256: **c82b583df905cded349e3d5edc41f899d64175f2c848ae76cc7086d05dcb87f2**

This contains the large animation/audio/battle-state development UI and associated test helpers.

## Shared sprite/helper block

After the large Debug tool block, both Retail and Debug contain the same semantic helper sequence.

Retail:
- 0x0801041C..0x080109F7
- 1,500 bytes
- SHA-256: b159eaa8d62c47cfcbef24546a7b75595dbc7996ca7aff14d64a3a3693b6749f

Debug:
- 0x080132F0..0x080138CB
- 1,500 bytes
- SHA-256: 6ad77a398be92d0eae95f4cebde9069cc52d66af998b417cf8657e0f6c00aa55

| Function | Retail | Debug |
| --- | --- | --- |
| oac_poke_opponent | 0x0801041C | 0x080132F0 |
| sub_8010278 | 0x0801044C | 0x08013320 |
| sub_80102AC | 0x08010480 | 0x08013354 |
| nullsub_37 | 0x080104DC | 0x080133B0 |
| unref_sub_801030C | 0x080104E0 | 0x080133B4 |
| sub_8010320 | 0x080104F4 | 0x080133C8 |
| sub_8010384 | 0x08010558 | 0x0801342C |
| sub_8010494 | 0x08010668 | 0x0801353C |
| sub_8010520 | 0x080106F4 | 0x080135C8 |
| sub_801053C | 0x08010710 | 0x080135E4 |
| sub_8010574 | 0x08010748 | 0x0801361C |
| sub_80105A0 | 0x08010774 | 0x08013648 |
| oac_poke_ally_ | 0x08010780 | 0x08013654 |
| sub_80105DC | 0x080107B0 | 0x08013684 |
| nullsub_86 | 0x080107BC | 0x08013690 |
| sub_80105EC | 0x080107C0 | 0x08013694 |
| dp11b_obj_instanciate | 0x080107E8 | 0x080136BC |
| dp11b_obj_free | 0x080108E8 | 0x080137BC |
| objc_dp11b_pingpong | 0x08010984 | 0x08013858 |
| nullsub_41 | 0x080109D0 | 0x080138A4 |
| sub_8010800 | 0x080109D4 | 0x080138A8 |

## Debug-only tool block B

Immediately before BattleMainCB1, Debug contains one additional auto-input helper:

- debug_sub_80138CC
- Start: **0x080138CC**
- End exclusive: **0x080139E4**
- Size: **280 bytes (0x118)**
- SHA-256: **d2d1d17bf6cc53d9dac48843ba154fef9033a8182598500188bfa1601962ca76**

It can synthesize A-button input for player-side battlers in the Debug automated battle path.

## BattleMainCB1 rejoin

- Retail: **0x080109F8**
- Debug: **0x080139E4**
- Address displacement at rejoin: **+0x2FEC**

The Retail pointer 0x080109F9 and Debug pointer 0x080139E5 are directly embedded in each profile's CB2_HandleStartBattle routine.
