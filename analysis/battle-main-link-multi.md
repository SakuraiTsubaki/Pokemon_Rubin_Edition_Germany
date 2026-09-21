# German battle_main link/multi and pre-core slice

This record supersedes the earlier boundary interpretation around 0x0801041C.

## Verified common link/multi slice

- Retail Rev 0 / Rev 1: 0x0800F200..0x0801041B
- German Debug: 0x0800F4C0..0x08010800
- Retail Rev 0 and Rev 1 are byte-identical over the complete slice.

Debug-only growth inside the common flow remains:

- sub_800F104: +48 bytes
- CB2_HandleStartMultiBattle: +44 bytes
- BattleMainCB2: +200 bytes

The accumulated Debug displacement at the end of c2_081284E0 is +0x3E4.

## Corrected continuation

Retail address 0x0801041C is **not BattleMainCB1**.

It begins a shared battle-sprite/helper block that is present in both Retail and Debug:

- Retail: 0x0801041C..0x080109F7
- Debug: 0x080132F0..0x080138CB
- Size: 1,500 bytes in each profile
- Retail Rev 0 / Rev 1 SHA-256: b159eaa8d62c47cfcbef24546a7b75595dbc7996ca7aff14d64a3a3693b6749f
- Debug SHA-256: 6ad77a398be92d0eae95f4cebde9069cc52d66af998b417cf8657e0f6c00aa55
- Address delta inside this shared block: +0x2ED4

The actual BattleMainCB1 addresses are:

- Retail: **0x080109F8**
- Debug: **0x080139E4**

These addresses are independently confirmed by the Thumb function pointers stored in CB2_HandleStartBattle:

- Retail literal: 0x080109F9
- Debug literal: 0x080139E5

The low bit is the Thumb-state bit.
