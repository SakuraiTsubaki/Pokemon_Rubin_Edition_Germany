# German battle script switching, move-learning and reward core

This slice maps opcodes 0x4A through 0x5F. The recorded byte count for each opcode is the physical span until the next opcode entry; spans can include private helpers placed between command entries.

## Exact slice

| Profile | Start | End exclusive | Size | SHA-256 |
| --- | --- | --- | ---: | --- |
| Retail Rev 0 / Rev 1 | 0x080224B0 | 0x0802446C | 8,124 bytes | fd0fbc4f5136c719654a6aa60db0c86df7d57f0ba9dac8492e0e99b5fd288b49 |
| Debug | 0x08025A54 | 0x08027A10 | 8,124 bytes | ccbd097180e90153754f95259031b3551a4d33d0e22cdd7cca6e879342782303 |

Retail Rev 0 and Rev 1 are byte-identical across the full slice. No new Debug-only growth occurs; every opcode remains at **+0x35A4**.

## Opcode map

| Opcode | Function | Retail | Debug | Span to next opcode | Role |
| ---: | --- | --- | --- | ---: | --- |
| 0x4A | atk4A_typecalc2 | 0x080224B0 | 0x08025A54 | 592 | type-effectiveness/Levitate/Wonder Guard check without damage modulation |
| 0x4B | atk4B_returnatktoball | 0x08022700 | 0x08025CA4 | 80 | return attacker sprite to Poké Ball unless already fainted |
| 0x4C | atk4C_getswitchedmondata | 0x08022750 | 0x08025CF4 | 116 | request selected party Pokémon data for switching battler |
| 0x4D | atk4D_switchindataupdate | 0x080227C4 | 0x08025D68 | 404 | replace BattlePokemon data, restore species types/ability, apply Knock Off/Baton Pass state |
| 0x4E | atk4E_switchinanim | 0x08022958 | 0x08025EFC | 172 | mark Pokédex seen and emit switch-in animation |
| 0x4F | atk4F_jumpifcantswitch | 0x08022A04 | 0x08025FA8 | 616 | test trapping/rooting and party availability before switching |
| 0x50 | atk50_openpartyscreen | 0x08022C6C | 0x08026210 | 2180 | open/coordinate party selection across single/double/multi/link battle states |
| 0x51 | atk51_switchhandleorder | 0x080234F0 | 0x08026A94 | 520 | consume switch selection results and synchronize multi-battle switch metadata |
| 0x52 | atk52_switchineffects | 0x080236F8 | 0x08026C9C | 680 | Spikes, Truant initialization, switch-in ability/item effects and action cleanup |
| 0x53 | atk53_trainerslidein | 0x080239A0 | 0x08026F44 | 64 | emit trainer slide animation |
| 0x54 | atk54_playse | 0x080239E0 | 0x08026F84 | 60 | play 16-bit sound effect ID |
| 0x55 | atk55_fanfare | 0x08023A1C | 0x08026FC0 | 60 | play 16-bit fanfare/BGM ID |
| 0x56 | atk56_playfaintcry | 0x08023A58 | 0x08026FFC | 48 | emit fainting cry for selected battler |
| 0x57 | atk57 | 0x08023A88 | 0x0802702C | 56 | send battle outcome through controller command 55 |
| 0x58 | atk58_returntoball | 0x08023AC0 | 0x08027064 | 52 | return selected battler to ball |
| 0x59 | atk59_handlelearnnewmove | 0x08023AF4 | 0x08027098 | 472 | drive learn-new-move decision and update active battle copies |
| 0x5A | atk5A_yesnoboxlearnmove | 0x08023CCC | 0x08027270 | 892 | move-forgetting yes/no UI and summary-screen state machine |
| 0x5B | atk5B_yesnoboxstoplearningmove | 0x08024048 | 0x080275EC | 272 | stop-learning confirmation UI |
| 0x5C | atk5C_hitanimation | 0x08024158 | 0x080276FC | 144 | emit hit animation unless no-effect/substitute suppresses it |
| 0x5D | atk5D_getmoneyreward | 0x080241E8 | 0x0802778C | 384 | calculate trainer reward and add money to SaveBlock1 |
| 0x5E | atk5E | 0x08024368 | 0x0802790C | 180 | refresh battler move/PP slots from controller mon-data buffer |
| 0x5F | atk5F_swapattackerwithtarget | 0x0802441C | 0x080279C0 | 80 | swap attacker/target and toggle swap hit-marker |

## Switching pipeline

Opcodes 0x4B through 0x52 form the main switch pipeline:

- return the outgoing battler;
- fetch the chosen party mon;
- rebuild BattlePokemon data;
- restore species types and ability;
- preserve Baton Pass stat stages/status2 when applicable;
- remove a knocked-off item from the in-battle copy;
- animate the replacement;
- reject switching when Wrapped, escape-prevented or Rooted;
- open/coordinate the party screen;
- consume switch selections;
- apply Spikes and switch-in ability/item effects.

The implementation repeatedly assumes a six-slot party and at most four active battlers. Multi Battle additionally partitions party access into three-slot halves.

## Spikes and switch-in effects

`atk52_switchineffects` applies original Ruby Spikes damage as:

`maxHP / ((5 - spikesAmount) * 2)`

with a minimum of 1 HP, while Flying types and Levitate are immune. It then runs switch-in ability effects and held-item effects before clearing the switch action.

This is a key future hazard/entry-trigger modernization point because later generations add many more entry hazards and switch-in trigger classes.

## Move learning

Opcodes 0x59..0x5B implement the original four-move learning flow:

- `MonTryLearningNewMove` returns a candidate move;
- if all four slots are occupied, the battle opens the move-summary screen;
- the player selects one of four slots or cancels;
- HM moves are protected from forgetting;
- PP bonuses are removed from the forgotten slot;
- the party mon and any matching active battle copy are updated.

The UI and replacement logic are explicitly four-slot. A future engine can keep four selectable moves for compatibility while separating the storage namespace from this UI constraint.

## Trainer reward

`atk5D_getmoneyreward` uses the level of the trainer's final party entry and trainer-class base money. Normal reward calculation is:

`4 * level * moneyMultiplier * (doubleBattle ? 2 : 1) * trainerClassBaseMoney`

Secret Base battles use a separate `20 * firstPartyLevel * moneyMultiplier` path.

## Controller widths

- sound/fanfare IDs are 16-bit;
- species/move IDs copied into text/battle structures remain 16-bit;
- party indexes and battler IDs remain byte-sized;
- move/PP refresh in opcode 0x5E loops over exactly four move slots.

## Next opcode

Opcode 0x60 `atk60_incrementgamestat` begins at Retail **0x0802446C** / Debug **0x08027A10**, still at delta **+0x35A4**.
