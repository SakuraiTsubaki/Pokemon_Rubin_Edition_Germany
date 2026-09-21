# German battle script faint, EXP and generic VM core

This slice maps battle-script opcodes 0x17 through 0x2F and the internal MoveValuesCleanUp helper.

## Exact slice

| Profile | Start | End exclusive | Size | SHA-256 |
| --- | --- | --- | ---: | --- |
| Retail Rev 0 / Rev 1 | 0x0801F8EC | 0x08021164 | 6,264 bytes | f5f2a488df39c10cbba61705aec1c94623d31a6a5d16b9cb65e4fc8cb8bbff73 |
| Debug | 0x08022E90 | 0x08024708 | 6,264 bytes | bddba2d8ebb93f3266d79c3eaeab0a4d3a75c7852e1cb46d171d52c39f48c1ad |

Retail Rev 0 and Rev 1 are byte-identical throughout this slice. No Debug-only insertion occurs here; all opcode entries remain at **+0x35A4**.

## Opcode map

| Opcode | Function | Retail | Debug | Span bytes | Role |
| ---: | --- | --- | --- | ---: | --- |
| 0x17 | atk17_seteffectsecondary | 0x0801F8EC | 0x08022E90 | 16 | apply move effect as secondary/non-primary |
| 0x18 | atk18_clearstatusfromeffect | 0x0801F8FC | 0x08022EA0 | 132 | clear status1/status2 flag selected by move-effect byte |
| 0x19 | atk19_tryfaintmon | 0x0801F980 | 0x08022F24 | 904 | faint detection, counters, friendship, Destiny Bond and Grudge handling |
| 0x1A | atk1A_dofaintanimation | 0x0801FD08 | 0x080232AC | 60 | emit faint animation |
| 0x1B | atk1B_cleareffectsonfaint | 0x0801FD44 | 0x080232E8 | 100 | clear status and undo attraction/trapping/switch-dependent effects |
| 0x1C | atk1C_jumpifstatus | 0x0801FDA8 | 0x0802334C | 120 | conditional jump on 32-bit primary-status mask |
| 0x1D | atk1D_jumpifstatus2 | 0x0801FE20 | 0x080233C4 | 120 | conditional jump on 32-bit volatile-status mask |
| 0x1E | atk1E_jumpifability | 0x0801FE98 | 0x0802343C | 240 | conditional jump on battler/side ability query |
| 0x1F | atk1F_jumpifsideaffecting | 0x0801FF88 | 0x0802352C | 120 | conditional jump on 16-bit side-status mask |
| 0x20 | atk20_jumpifstat | 0x08020000 | 0x080235A4 | 248 | compare one stat stage and branch |
| 0x21 | atk21_jumpifstatus3condition | 0x080200F8 | 0x0802369C | 132 | conditional/inverted jump on status3 flags |
| 0x22 | atk22_jumpiftype | 0x0802017C | 0x08023720 | 92 | conditional jump if battler has requested type |
| 0x23 | atk23_getexp | 0x080201D8 | 0x0802377C | 2480 | experience/EV distribution and level-up state machine |
| 0x24 | atk24 | 0x08020B88 | 0x0802412C | 488 | party defeat/win and link-fainted-state outcome check; span includes MoveValuesCleanUp helper |
| 0x25 | atk25_movevaluescleanup | 0x08020D70 | 0x08024314 | 24 | reset move result/damage/critical/effect transient values |
| 0x26 | atk26_setmultihit | 0x08020D88 | 0x0802432C | 24 | initialize multi-hit counter |
| 0x27 | atk27_decrementmultihit | 0x08020DA0 | 0x08024344 | 72 | decrement multi-hit counter and branch/continue |
| 0x28 | atk28_goto | 0x08020DE8 | 0x0802438C | 32 | unconditional script pointer jump |
| 0x29 | atk29_jumpifbyte | 0x08020E08 | 0x080243AC | 160 | generic byte comparison and jump |
| 0x2A | atk2A_jumpifhalfword | 0x08020EA8 | 0x0802444C | 168 | generic 16-bit comparison and jump |
| 0x2B | atk2B_jumpifword | 0x08020F50 | 0x080244F4 | 180 | generic 32-bit comparison and jump |
| 0x2C | atk2C_jumpifarrayequal | 0x08021004 | 0x080245A8 | 136 | byte-array equality test and jump |
| 0x2D | atk2D_jumpifarraynotequal | 0x0802108C | 0x08024630 | 132 | byte-array inequality test and jump |
| 0x2E | atk2E_setbyte | 0x08021110 | 0x080246B4 | 40 | write immediate byte through script pointer |
| 0x2F | atk2F_addbyte | 0x08021138 | 0x080246DC | 44 | add immediate byte through script pointer |

Internal helper:

- MoveValuesCleanUp: Retail 0x08020D24, Debug 0x080242C8, 76 bytes.

## Faint pipeline

Opcode 0x19 is the main faint transition gate. It:

- checks HP/absence state;
- records player/opponent faint counters;
- updates friendship penalties based on level difference;
- clears last-taken-move metadata;
- handles Destiny Bond;
- handles Grudge by zeroing the chosen move's PP and synchronizing it through the controller;
- pushes the correct faint battle script.

Opcode 0x1B then clears status and delegates persistent cross-battler cleanup to `UndoEffectsAfterFainting`.

## Conditional script commands

Opcodes 0x1C..0x22 provide direct branching over:

- primary status (32-bit);
- status2 (32-bit);
- abilities, including whole-side/opposing-side queries;
- side conditions (16-bit);
- stat-stage comparisons;
- status3 flags;
- battler types.

This is the point where battle-script bytecode directly exposes battle-state bitfields and stat-stage layout.

## EXP state machine — opcode 0x23

`atk23_getexp` is **2,480 bytes** and implements the complete original Ruby battle EXP flow.

Core formula:

`calculatedExp = defeatedSpecies.expYield * defeatedLevel / 7`

Distribution behavior:

- six-player-party scan;
- count living participating party members;
- count Exp. Share holders;
- with Exp. Share, split half among participating Pokemon and half among Exp. Share holders;
- without Exp. Share, divide the whole value among participants;
- minimum distributed share is 1;
- Lucky Egg multiplier: ×1.5;
- trainer battle multiplier: ×1.5;
- traded Pokemon multiplier: ×1.5;
- level 100 receives no further EXP;
- EVs are awarded through `MonGainEVs`;
- controller EXP update performs the actual level change;
- level-up records pre-level stats, triggers level-up script/friendship, refreshes active battle stats and marks the party slot for post-battle evolution.

This is a major later-generation modernization boundary: EXP Share behavior, modern EXP formulas, affection/traded/language bonuses, level scaling, party-wide EXP and EV rules should be introduced as a new ruleset while retaining this exact legacy path.

## Outcome check — opcode 0x24

`atk24` sums HP across exactly six player-party and six enemy-party slots to establish win/loss, then handles link/multi faint-state conditions over active battlers.

The same physical span also contains the internal `MoveValuesCleanUp` helper immediately before opcode 0x25.

## Generic VM operations — opcodes 0x26..0x2F

This portion shows that the battle VM already provides general-purpose bytecode primitives:

- multi-hit loop counter;
- unconditional goto;
- byte / 16-bit / 32-bit comparisons;
- common-bit / no-common-bit comparisons;
- array equality / inequality;
- arbitrary byte write and add through embedded pointers.

These generic commands are useful for preserving legacy scripts. A future extended VM should avoid breaking their operand widths and pointer encoding.

## Next opcode

Opcode 0x30 `atk30_subbyte` starts at Retail **0x08021164** / Debug **0x08024708**, still at delta **+0x35A4**.
