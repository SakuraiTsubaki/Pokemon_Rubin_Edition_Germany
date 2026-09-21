# German battle_util foundation

The first battle_util slice is now mapped directly from the supplied German ROMs.

## Exact slice

| Profile | Start | End exclusive | Size | SHA-256 |
| --- | --- | --- | ---: | --- |
| Retail Rev 0 / Rev 1 | 0x08015324 | 0x08015FD0 | 3,244 bytes | f1292d07e15d28e091d388c71f989ba613c06f45d5d2ec118cb625d41576d374 |
| Debug | 0x080183AC | 0x08019058 | 3,244 bytes | 8280b41942af994c9ae1979d2a785dc62b13c75e4bdba295b6d15fa59535a05e |

Retail Rev 0 and Rev 1 are byte-identical throughout this slice. Every Debug function entry remains exactly +0x3088 from Retail; battle_util contains no Debug conditional block in this range.

## Function map

| Function | Retail | Debug | Bytes | Role |
| --- | --- | --- | ---: | --- |
| GetBattlerForBattleScript | 0x08015324 | 0x080183AC | 132 | map battle-script bank selector to target/attacker/effect/scripting battler |
| PressurePPLose | 0x080153A8 | 0x08018430 | 200 | apply Pressure PP loss to one move and synchronize PP through the controller |
| PressurePPLoseOnUsingImprision | 0x08015470 | 0x080184F8 | 308 | apply Pressure PP loss for Imprison across opposing battlers |
| PressurePPLoseOnUsingPerishSong | 0x080155A4 | 0x0801862C | 276 | apply Pressure PP loss for Perish Song across battlers |
| MarkAllBattlersForControllerExec | 0x080156B8 | 0x08018740 | 112 | set controller-execution bits for all active battlers |
| MarkBattlerForControllerExec | 0x08015728 | 0x080187B0 | 80 | set controller-execution bits for one battler |
| sub_80155A4 | 0x08015778 | 0x08018800 | 80 | set per-link-player controller bits for one battler and clear a high pending bit |
| CancelMultiTurnMoves | 0x080157C8 | 0x08018850 | 108 | clear multi-turn/status3 state and Rollout/Fury Cutter counters |
| WasUnableToUseMove | 0x08015834 | 0x080188BC | 88 | test per-turn ProtectStruct failure and immobility flags |
| PrepareStringBattle | 0x0801588C | 0x08018914 | 36 | emit a battle-string command and mark battler controller busy |
| ResetSentPokesToOpponentValue | 0x080158B0 | 0x08018938 | 100 | rebuild sent-party bitfields from active battler party indexes |
| sub_8015740 | 0x08015914 | 0x0801899C | 132 | refresh sent-party bitfield for an opponent-side battler |
| sub_80157C4 | 0x08015998 | 0x08018A20 | 104 | propagate sent-party bit for player/opponent tracking |
| BattleScriptPush | 0x08015A00 | 0x08018A88 | 32 | push a battle-script pointer onto the battle-script stack |
| BattleScriptPushCursor | 0x08015A20 | 0x08018AA8 | 36 | push the current battle-script cursor |
| BattleScriptPop | 0x08015A44 | 0x08018ACC | 36 | pop the current battle-script cursor |
| TrySetCantSelectMoveBattleScript | 0x08015A68 | 0x08018AF0 | 516 | select a rejection script for disabled/Torment/Taunt/Imprison/Choice/zero-PP moves |
| CheckMoveLimitations | 0x08015C6C | 0x08018CF4 | 504 | build the four-bit unusable-move mask |
| AreAllMovesUnusable | 0x08015E64 | 0x08018EEC | 204 | detect mask 0xF and configure no-moves/Struggle behavior |
| IsImprisoned | 0x08015F30 | 0x08018FB8 | 160 | scan opposing battlers and their four move slots for Imprison overlap |

## Pressure and PP synchronization

The three Pressure helpers expose the original four-move layout directly. They search a battler's move slots, decrement the matching PP entry, and synchronize that one-byte PP value through the battle controller when the move is neither transformed nor treated as a mimicked slot.

Imprison and Perish Song perform the same concept across opposing/other active battlers with Pressure, so one use can consume additional PP according to the active battle layout.

## Controller-execution flags

MarkAllBattlersForControllerExec and MarkBattlerForControllerExec use different bit placement for link versus local battles. The link helper sub_80155A4 additionally allocates controller-execution bits per link player. This is part of the original four-battler/link synchronization model and must be audited before increasing active battler capacity.

## Battle-script stack

BattleScriptPush, BattleScriptPushCursor and BattleScriptPop recover the original stack cursor operations. Two of these are tiny leaf functions that begin without a PUSH prologue, so the German address map is based on control flow/literal boundaries rather than prologue scanning alone.

## Move-selection limitations

TrySetCantSelectMoveBattleScript and CheckMoveLimitations cover:

- Disable
- Torment
- Taunt
- Imprison
- Choice Band locking
- zero PP
- Encore mismatch
- empty move slots

The original move set is represented by exactly four slots. CheckMoveLimitations returns a bit mask over those four slots, and AreAllMovesUnusable explicitly tests **0xF** to mean all four moves are unavailable.

This is stronger evidence than a generic MAX_MON_MOVES constant alone: the original runtime decision path itself assumes a four-bit complete mask.

Move IDs in these helpers are 16-bit, while the selected move-slot index and unusable mask are byte-sized.

## Imprison

IsImprisoned walks opposing active battlers and compares the requested 16-bit move ID against each opponent's four move slots. This will need deliberate generalization only if the number of simultaneously selectable moves is ever changed; adding more move IDs alone does not require widening the move ID here beyond its existing 16-bit path.

## Action-table cross-module edge

The previously mapped battle action table's action ID 10 points into battle_util at Retail 0x0801B768 / Debug 0x0801ECBC (Thumb pointers 0x0801B769 / 0x0801ECBD). That handler lies later in this module and remains an explicit target for the next battle_util passes.

## Next function

The next function starts at Retail **0x08015FD0** / Debug **0x08019058** and is DoFieldEndTurnEffects, the field/side/weather end-turn state machine.
