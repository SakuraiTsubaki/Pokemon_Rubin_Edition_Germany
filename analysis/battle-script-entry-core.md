# German battle script entry core

The first battle-script command and its physically adjacent helpers have been separated using German ROM control flow rather than source-file ordering assumptions.

## Exact physical order

| Function | Retail | Debug | Bytes | Kind |
| --- | --- | --- | ---: | --- |
| atk00_attackcanceler | 0x0801BE24 | 0x0801F39C | 952 | opcode 0x00 |
| JumpIfMoveFailed | 0x0801C1DC | 0x0801F754 | 144 | helper |
| atk40_jumpifaffectedbyprotect | 0x0801C26C | 0x0801F7E4 | 112 | opcode 0x40 |
| JumpIfMoveAffectedByProtect | 0x0801C2DC | 0x0801F854 | 108 | helper |
| AccuracyCalcHelper | 0x0801C348 | 0x0801F8C0 | 328 | helper |
| atk01_accuracycheck | 0x0801C490 | 0x0801FA08 | next slice | opcode 0x01 |

All entries in this physical block retain the initial Debug displacement **+0x3578**.

## Why opcode 0x40 appears here

`atk40_jumpifaffectedbyprotect` is opcode 0x40 in the dispatch table, but the linker/compiler places its implementation next to the Protect helpers used by the early accuracy/cancellation path. This is why physical code address ordering must never be used as opcode numbering.

## atk00 role

`atk00_attackcanceler` is the VM's pre-move gate. The recovered flow includes:

- stop immediately when a battle outcome already exists;
- handle a fainted attacker;
- run `AtkCanceller_UnableToUseMove`;
- run move-blocking ability effects;
- reject zero-PP use except special/multi-turn cases;
- run obedience handling;
- process Magic Coat / Snatch-style interception;
- process Lightning Rod redirection state;
- then advance the battle-script cursor when no blocking branch takes over.

This directly ties the previously reconstructed battle_util cancellation/obedience logic to opcode 0x00.

## Helper boundaries

The earlier false module boundary at 0x0801C1DC is now positively identified as `JumpIfMoveFailed`, a 144-byte internal helper. The matching Debug address is 0x0801F754.

Physical spans in Retail:

- atk00: 0x0801BE24..0x0801C1DB — 952 bytes
- JumpIfMoveFailed: 0x0801C1DC..0x0801C26B — 144 bytes
- atk40: 0x0801C26C..0x0801C2DB — 112 bytes
- JumpIfMoveAffectedByProtect: 0x0801C2DC..0x0801C347 — 108 bytes
- AccuracyCalcHelper: 0x0801C348..0x0801C48F — 328 bytes
- atk01 begins at 0x0801C490.

## Expansion significance

This entry core shows that battle-script opcodes are thin orchestration commands sitting on top of reusable battle helpers. Later-generation mechanics should preferentially extend/generalize helpers and trigger systems rather than duplicating logic into new opcodes wherever possible.
