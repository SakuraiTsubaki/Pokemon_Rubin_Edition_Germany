# German battle script VM control and move-end core

This slice maps the physical command block from opcode 0x30 through opcode 0x49, excluding opcode 0x40 because its implementation is physically located in the earlier Protect helper block.

## Exact physical slice

| Profile | Start | End exclusive | Size | SHA-256 |
| --- | --- | --- | ---: | --- |
| Retail Rev 0 / Rev 1 | 0x08021164 | 0x080224B0 | 4,940 bytes | eafda36717d95918b2233c1b582886630954e30ed4a235c4102ceb0eee044ecf |
| Debug | 0x08024708 | 0x08025A54 | 4,940 bytes | 0a4a16537389dd12cf1f96241506ef8906b6ab8663297fa126972bd03157a7b6 |

Retail Rev 0 and Rev 1 are byte-identical. All commands in this physical slice remain at **+0x35A4** in Debug.

Opcode 0x40 is not physically inside this range. It was previously mapped at Retail 0x0801C26C / Debug 0x0801F7E4 with delta +0x3578.

## Command map

| Opcode | Function | Retail | Debug | Bytes | Role |
| ---: | --- | --- | --- | ---: | --- |
| 0x30 | atk30_subbyte | 0x08021164 | 0x08024708 | 44 | subtract immediate byte through script pointer |
| 0x31 | atk31_copyarray | 0x08021190 | 0x08024734 | 84 | copy byte array from source pointer |
| 0x32 | atk32_copyarraywithindex | 0x080211E4 | 0x08024788 | 108 | copy byte array with pointer-provided source index |
| 0x33 | atk33_orbyte | 0x08021250 | 0x080247F4 | 44 | OR immediate byte into pointed memory |
| 0x34 | atk34_orhalfword | 0x0802127C | 0x08024820 | 56 | OR immediate 16-bit value |
| 0x35 | atk35_orword | 0x080212B4 | 0x08024858 | 68 | OR immediate 32-bit value |
| 0x36 | atk36_bicbyte | 0x080212F8 | 0x0802489C | 44 | clear immediate byte bits |
| 0x37 | atk37_bichalfword | 0x08021324 | 0x080248C8 | 56 | clear 16-bit bits |
| 0x38 | atk38_bicword | 0x0802135C | 0x08024900 | 68 | clear 32-bit bits |
| 0x39 | atk39_pause | 0x080213A0 | 0x08024944 | 64 | wait a script-provided frame count |
| 0x3A | atk3A_waitstate | 0x080213E0 | 0x08024984 | 32 | wait until controller flags are idle |
| 0x3B | atk3B_healthbar_update | 0x08021400 | 0x080249A4 | 88 | emit HP-bar update for attacker or target |
| 0x3C | atk3C_return | 0x08021458 | 0x080249FC | 12 | pop battle-script cursor |
| 0x3D | atk3D_end | 0x08021464 | 0x08024A08 | 32 | end script action and clear move result |
| 0x3E | atk3E_end2 | 0x08021484 | 0x08024A28 | 24 | end script action without clearing move result |
| 0x3F | atk3F_end3 | 0x0802149C | 0x08024A40 | 48 | pop battle script and battle-main function stack |
| 0x41 | atk41_call | 0x080214CC | 0x08024A70 | 48 | call battle-script pointer while pushing return cursor |
| 0x42 | atk42_jumpiftype2 | 0x080214FC | 0x08024AA0 | 92 | conditional type jump variant |
| 0x43 | atk43_jumpifabilitypresent | 0x08021558 | 0x08024AFC | 76 | branch if ability exists anywhere on field |
| 0x44 | atk44_endselectionscript | 0x080215A4 | 0x08024B48 | 32 | mark attacker selection script finished |
| 0x45 | atk45_playanimation | 0x080215C4 | 0x08024B68 | 196 | emit explicit battle animation |
| 0x46 | atk46_playanimation2 | 0x08021688 | 0x08024C2C | 204 | animation ID and argument loaded indirectly |
| 0x47 | atk47_setgraphicalstatchangevalues | 0x08021754 | 0x08024CF8 | 124 | translate stat-change descriptor to animation args |
| 0x48 | atk48_playstatchangeanimation | 0x080217D0 | 0x08024D74 | 508 | validate stat changes and emit appropriate stat animation |
| 0x49 | atk49_moveend | 0x080219CC | 0x08024F70 | 2788 | 17-stage end-of-move cleanup/effect state machine |

## VM memory/control primitives

Opcodes 0x30..0x38 extend the generic VM memory operations with subtraction, indexed copy, OR and bit-clear operations over 8/16/32-bit values.

Opcodes 0x39..0x3F provide pause/wait, health-bar dispatch, script return and three end modes. `atk3F_end3` additionally pops the battle-main function stack, so battle scripting and the C-level battle callback stack are explicitly coupled.

`atk41_call` provides a normal script subroutine call by pushing the return cursor.

## Animation commands

Opcodes 0x45 and 0x46 emit battle animations while respecting no-animation and semi-invulnerable states. Opcode 0x48 determines whether requested stat changes are actually legal before choosing single/multiple plus/minus animation IDs.

Stat animation prevention already depends on:

- Mist;
- Clear Body;
- White Smoke;
- Keen Eye for Accuracy;
- Hyper Cutter for Attack;
- min/max stat-stage bounds.

## atk49_moveend

`atk49_moveend` spans **2,788 bytes** and is a 17-stage post-move state machine:

- 0: RAGE
- 1: DEFROST
- 2: SYNCHRONIZE_TARGET
- 3: MOVE_END_ABILITIES
- 4: STATUS_IMMUNITY_ABILITIES
- 5: SYNCHRONIZE_ATTACKER
- 6: CHOICE_MOVE
- 7: CHANGED_ITEMS
- 8: ATTACKER_INVISIBLE
- 9: ATTACKER_VISIBLE
- 10: TARGET_VISIBLE
- 11: ITEM_EFFECTS_ALL
- 12: KINGSROCK_SHELLBELL
- 13: SUBSTITUTE
- 14: UPDATE_LAST_MOVES
- 15: MIRROR_MOVE
- 16: NEXT_TARGET

It is the central cleanup bridge after a move resolves. Among other things it handles Rage buildup, thawing from Fire moves, Synchronize, end-of-move ability hooks, status-immunity abilities, Choice-move locking, changed items, attacker/target visibility restoration, item effects, King's Rock/Shell Bell, Substitute cleanup, last-move history, Mirror Move state and multi-target progression.

This is another major modernization hook: later-generation end-of-move triggers should be modeled as ordered trigger phases while preserving this 17-stage Ruby ordering for legacy rules.

## Next opcode

Opcode 0x4A `atk4A_typecalc2` begins at Retail **0x080224B0** / Debug **0x08025A54**, still at delta **+0x35A4**.
