# German battle_main action handlers and complete module boundary

This slice closes the German battle_main module.

## Action-handler slice

| Profile | Start | End exclusive | Size | SHA-256 |
| --- | --- | --- | ---: | --- |
| Retail Rev 0 / Rev 1 | 0x080141BC | 0x08015324 | 4,456 bytes | 20e994944adc5b1f3405a34ac8d07ae2ee405f492b5071c19dd328f77ce4a1d9 |
| Debug | 0x08017244 | 0x080183AC | 4,456 bytes | e204ce288cf66d02e6ffee4d63b51bb5cf81c82c79b88d44bac49ed7cb93af6 |

Retail Rev 0 and Rev 1 are byte-identical throughout the complete slice.

Every Debug entry remains exactly +0x3088 from the Retail counterpart. There are no further Debug-only insertions before battle_main ends.

## Function map

| Function | Retail | Debug | Bytes | Role |
| --- | --- | --- | ---: | --- |
| HandleAction_UseMove | 0x080141BC | 0x08017244 | 1804 | select move/target, apply Follow Me/Lightning Rod redirection, enter move-effect battle script |
| HandleAction_Switch | 0x080148C8 | 0x08017950 | 172 | prepare switch nickname/script and increment battle-result switch count |
| HandleAction_UseItem | 0x08014974 | 0x080179FC | 792 | decode 16-bit item ID and choose ball/run/item/AI item script |
| TryRunFromBattle | 0x08014C8C | 0x08017D14 | 316 | Smoke Ball/Run Away/speed-based escape calculation |
| HandleAction_Run | 0x08014DC8 | 0x08017E50 | 348 | resolve link/local escape and wild-opponent flee behavior |
| HandleAction_WatchesCarefully | 0x08014F24 | 0x08017FAC | 72 | Safari watch-carefully action |
| HandleAction_SafariZoneBallThrow | 0x08014F6C | 0x08017FF4 | 96 | consume Safari Ball and enter ball script |
| HandleAction_ThrowPokeblock | 0x08014FCC | 0x08018054 | 196 | apply Pokeblock Safari flee-rate changes |
| HandleAction_GoNear | 0x08015090 | 0x08018118 | 196 | apply Safari catch/flee factor changes |
| HandleAction_SafriZoneRun | 0x08015154 | 0x080181DC | 60 | force Safari escape outcome |
| HandleAction_Action9 | 0x08015190 | 0x08018218 | 120 | prepare Safari action text/script and force second turn-order slot finished |
| HandleAction_Action11 | 0x08015208 | 0x08018290 | 44 | process fainted-mon actions or finish action |
| HandleAction_NothingIsFainted | 0x08015234 | 0x080182BC | 52 | advance turn action and clear transient hit-marker state |
| HandleAction_ActionFinished | 0x08015268 | 0x080182F0 | 188 | advance turn, clear special/transient move state and script stack |

## Action dispatch table

The original battle action table is present directly in the German ROMs.

- Retail table: 0x08207610
- Debug table: 0x082207A8
- Entries: 14
- Entry width: 32-bit Thumb function pointer
- Retail table SHA-256: 325dc01ec5a02fb745118e57fa04eec5b43626f086af1db21eee8944c29e700c
- Debug table SHA-256: 9f3eeb6e3a1f504da2c87f8c39c617441f6bfd011c8c7fbc26f13a6fa349de98

| ID | Handler | Retail pointer | Debug pointer |
| ---: | --- | --- | --- |
| 0 | HandleAction_UseMove | 0x080141BD | 0x08017245 |
| 1 | HandleAction_UseItem | 0x08014975 | 0x080179FD |
| 2 | HandleAction_Switch | 0x080148C9 | 0x08017951 |
| 3 | HandleAction_Run | 0x08014DC9 | 0x08017E51 |
| 4 | HandleAction_WatchesCarefully | 0x08014F25 | 0x08017FAD |
| 5 | HandleAction_SafariZoneBallThrow | 0x08014F6D | 0x08017FF5 |
| 6 | HandleAction_ThrowPokeblock | 0x08014FCD | 0x08018055 |
| 7 | HandleAction_GoNear | 0x08015091 | 0x08018119 |
| 8 | HandleAction_SafriZoneRun | 0x08015155 | 0x080181DD |
| 9 | HandleAction_Action9 | 0x08015191 | 0x08018219 |
| 10 | sub_801B594 (battle script action) | 0x0801B769 | 0x0801ECBD |
| 11 | HandleAction_Action11 | 0x08015209 | 0x08018291 |
| 12 | HandleAction_ActionFinished | 0x08015269 | 0x080182F1 |
| 13 | HandleAction_NothingIsFainted | 0x08015235 | 0x080182BD |

Action ID 10 points into battle_util and is now resolved as sub_801B594: a 44-byte handler that executes the current battle-script opcode when controller execution flags are idle.

## Outcome dispatch table

Immediately after the action table is the nine-entry outcome table.

- Retail: 0x08207648
- Debug: 0x082207E0

| ID | Handler | Retail pointer | Debug pointer |
| ---: | --- | --- | --- |
| 0 | BattleTurnPassed | 0x08011F9D | 0x08015025 |
| 1 | HandleEndTurn_BattleWon | 0x08013B6D | 0x08016BF5 |
| 2 | HandleEndTurn_BattleLost | 0x08013D39 | 0x08016DC1 |
| 3 | HandleEndTurn_BattleLost | 0x08013D39 | 0x08016DC1 |
| 4 | HandleEndTurn_RanFromBattle | 0x08013DB1 | 0x08016E39 |
| 5 | HandleEndTurn_FinishBattle | 0x08013E71 | 0x08016EF9 |
| 6 | HandleEndTurn_MonFled | 0x08013E1D | 0x08016EA5 |
| 7 | HandleEndTurn_FinishBattle | 0x08013E71 | 0x08016EF9 |
| 8 | HandleEndTurn_FinishBattle | 0x08013E71 | 0x08016EF9 |

Several outcome values deliberately alias the same finalization handler.

## Move-action constraints

HandleAction_UseMove confirms several original battle assumptions:

- move identifiers are held in 16-bit fields;
- each battler exposes four move slots;
- selected move slot is stored separately from the 16-bit move ID;
- target identity is an 8-bit battler index;
- double-battle random targeting assumes left/right positions on two sides;
- Lightning Rod redirect search is bounded by the active battler set;
- Follow Me uses a single target battler stored in the side timer;
- move effect selects the battle-script entry through a move-effect table.

## Item-action constraints

HandleAction_UseItem reconstructs the item ID from two command-buffer bytes, proving a 16-bit item ID path in the original battle action layer.

The original branching still assumes the original ball item range through Premier Ball, special run-away items, fixed AI item categories, and compact AI-used-item effect bits.

## Escape mechanics

TryRunFromBattle implements held-item always-run, Run Away ability, and the original speed/run-attempt formula. In a slower single battle the calculated escape value is playerSpeed * 128 / opponentSpeed + runTries * 30 and is compared against an 8-bit random value.

## Safari mechanics

The Safari handlers expose fixed counters/tables for Safari Ball consumption, Pokeblock flee-rate reduction, Go Near catch/flee adjustments, three-step counters, and a factor cap of 20.

## Complete battle_main module

| Profile | Start | End exclusive | Size | SHA-256 |
| --- | --- | --- | ---: | --- |
| Retail Rev 0 / Rev 1 | 0x0800E998 | 0x08015324 | 27,020 bytes (0x698C) | 8e23208aa7693b31725b31dffa051c7808b82351ab40c591be8c41c746fd387b |
| Debug | 0x0800EC0C | 0x080183AC | 38,816 bytes (0x97A0) | db5388b194b192cfe68ef6ddf3b01638c19a938ed1b687acdbf707400532ebf5 |

Retail Rev 0 and Rev 1 are byte-identical across the entire battle_main module.

The Debug module is 11,796 bytes larger due to the previously mapped Debug-only battle instrumentation and smaller Debug branches inside shared functions.

## Next module

The next source module begins at Retail 0x08015324 / Debug 0x080183AC. Link order identifies it as battle_util.
