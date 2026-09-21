# German battle script status, utility and field-effect core

This slice maps opcodes 0x60 through 0x7F. Recorded byte counts are physical spans to the next opcode entry and can include nearby private helpers.

## Exact slice

| Profile | Start | End exclusive | Size | SHA-256 |
| --- | --- | --- | ---: | --- |
| Retail Rev 0 / Rev 1 | 0x0802446C | 0x08025A70 | 5,636 bytes | 387c50cd9ce66f37d2317559fbeb3b67a874d229b51fcdeb292431c9d01723e0 |
| Debug | 0x08027A10 | 0x08029014 | 5,636 bytes | 86932d3b4f5a519048f6c4eaead2593027189a246bf598f2aa709bd12203eb8a |

Retail Rev 0 and Rev 1 are byte-identical. No new Debug-only insertion occurs; every opcode remains at **+0x35A4**.

## Opcode map

| Opcode | Function | Retail | Debug | Span | Role |
| ---: | --- | --- | --- | ---: | --- |
| 0x60 | atk60_incrementgamestat | 0x0802446C | 0x08027A10 | 48 | increment game stat for player-side attacker |
| 0x61 | atk61_drawpartystatussummary | 0x0802449C | 0x08027A40 | 200 | build six HpAndStatus entries and draw party summary |
| 0x62 | atk62_hidepartystatussummary | 0x08024564 | 0x08027B08 | 48 | hide party status summary |
| 0x63 | atk63_jumptorandomattack | 0x08024594 | 0x08027B38 | 100 | jump to script for gRandomMove move effect |
| 0x64 | atk64_statusanimation | 0x080245F8 | 0x08027B9C | 144 | play primary-status animation when visible |
| 0x65 | atk65_status2animation | 0x08024688 | 0x08027C2C | 168 | play masked status2 animation |
| 0x66 | atk66_chosenstatusanimation | 0x08024730 | 0x08027CD4 | 148 | play explicitly encoded status animation |
| 0x67 | atk67_yesnobox | 0x080247C4 | 0x08027D68 | 176 | generic battle yes/no UI |
| 0x68 | atk68_cancelallactions | 0x08024874 | 0x08027E18 | 56 | mark every active battler action finished |
| 0x69 | atk69_adjustsetdamage | 0x080248AC | 0x08027E50 | 380 | fixed-damage survival adjustment for Endure/Focus Band/False Swipe |
| 0x6A | atk6A_removeitem | 0x08024A28 | 0x08027FCC | 108 | move held item to usedHeldItems and clear battler item |
| 0x6B | atk6B_atknameinbuff1 | 0x08024A94 | 0x08028038 | 60 | buffer attacker nickname reference |
| 0x6C | atk6C_drawlvlupbox | 0x08024AD0 | 0x08028074 | 848 | four-state level-up stat box UI |
| 0x6D | atk6D_resetsentmonsvalue | 0x08024E20 | 0x080283C4 | 24 | rebuild sent-party tracking |
| 0x6E | atk6E_setatktoplayer0 | 0x08024E38 | 0x080283DC | 32 | set attacker to player-left battler |
| 0x6F | atk6F_makevisible | 0x08024E58 | 0x080283FC | 52 | clear sprite invisibility |
| 0x70 | atk70_recordlastability | 0x08024E8C | 0x08028430 | 92 | record last-used ability; original cursor increment is +1 despite one-byte argument |
| 0x71 | atk71_buffermovetolearn | 0x08024EE8 | 0x0802848C | 24 | buffer 16-bit move-to-learn ID |
| 0x72 | atk72_jumpifplayerran | 0x08024F00 | 0x080284A4 | 68 | attempt run and jump on success |
| 0x73 | atk73_hpthresholds | 0x08024F44 | 0x080284E8 | 188 | categorize opposing HP percentage into four scale bands |
| 0x74 | atk74_hpthresholds2 | 0x08025000 | 0x080285A4 | 188 | categorize HP loss since switch-in into four bands |
| 0x75 | atk75_useitemonopponent | 0x080250BC | 0x08028660 | 88 | apply opponent trainer item to enemy party mon |
| 0x76 | atk76_various | 0x08025114 | 0x080286B8 | 496 | seven-subcommand battle helper multiplexer |
| 0x77 | atk77_setprotectlike | 0x08025304 | 0x080288A8 | 316 | Protect/Detect/Endure success and consecutive-use counter |
| 0x78 | atk78_faintifabilitynotdamp | 0x08025440 | 0x080289E4 | 284 | Explosion/Selfdestruct faint path unless Damp exists |
| 0x79 | atk79_setatkhptozero | 0x0802555C | 0x08028B00 | 96 | set attacker HP to zero and synchronize |
| 0x7A | atk7A_jumpifnexttargetvalid | 0x080255BC | 0x08028B60 | 164 | iterate valid double-battle target for Intimidate-style loops |
| 0x7B | atk7B_tryhealhalfhealth | 0x08025660 | 0x08028C04 | 124 | prepare negative half-max-HP healing value |
| 0x7C | atk7C_trymirrormove | 0x080256DC | 0x08028C80 | 456 | select last taken move and redirect into its effect script |
| 0x7D | atk7D_setrain | 0x080258A4 | 0x08028E48 | 84 | start five-turn rain or fail if already raining |
| 0x7E | atk7E_setreflect | 0x080258F8 | 0x08028E9C | 184 | start five-turn Reflect and choose single/double message |
| 0x7F | atk7F_setseeded | 0x080259B0 | 0x08028F54 | 192 | apply Leech Seed unless immune/already seeded/no-effect |

## Fixed party/status presentation

Opcode 0x61 allocates exactly six `HpAndStatus` records and transmits them through the party-summary controller command. This independently confirms the six-party UI/protocol assumption already found in earlier battle layers.

Status animations in 0x64..0x66 are suppressed for semi-invulnerable battlers, substitutes and global no-animation state.

## Level-up UI

`atk6C_drawlvlupbox` displays six level-up stats:

- HP
- Special Attack
- Attack
- Special Defense
- Defense
- Speed

It first shows stat deltas, then absolute values, and closes on input. This is presentation logic rather than the EXP calculation itself.

## Original cursor quirk — opcode 0x70

`atk70_recordlastability` consumes a battler argument but advances the battle-script cursor by **1 byte**, not 2. The comparison source itself marks this as buggy. The German original behavior is preserved as compatibility evidence; an extended script format must not accidentally depend on this misalignment.

## atk76 multiplexer

`atk76_various` exposes seven subcommands:

0. cancel multi-turn moves;
1. swap attacker/target context and honor Follow Me;
2. evaluate whether running is possible;
3. recompute move target;
4. report whether the selected battler is already faint-marked;
5. clear Intimidate/Trace per-battler flags;
6. clear a Choice-locked move if it no longer exists in the battler's four move slots.

This is another example of several unrelated behaviors sharing one opcode/subcommand byte.

## Protect / Endure

`atk77_setprotectlike` uses the original consecutive-use success thresholds:

- 0xFFFF
- 0x7FFF
- 0x3FFF
- 0x1FFF

corresponding approximately to 100%, 50%, 25% and 12.5% against a 16-bit RNG comparison. It also refuses success when the user is the final action of the turn.

## HP scale helpers

Opcode 0x73 categorizes current opposing HP:

- >=70% or zero HP -> scale 0;
- 40..69% -> 1;
- 10..39% -> 2;
- below 10% -> 3.

Opcode 0x74 instead categorizes percent HP lost since switch-in into four bands.

## Field/status effects

- 0x7D starts temporary Rain for five turns;
- 0x7E starts Reflect for five turns;
- 0x7F applies Leech Seed and rejects Grass types, existing seed or no-effect state.

These commands directly mutate the original weather/side/status bitfields. Later-generation terrain, screens and hazards should use generalized field-effect records while preserving these Ruby opcodes.

## Next opcode

Opcode 0x80 `atk80_manipulatedamage` begins at Retail **0x08025A70** / Debug **0x08029014**, still at delta **+0x35A4**.
