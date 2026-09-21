# German battle script command table

The battle-script VM dispatch table has been located directly in the supplied German ROMs.

## Exact table

- opcode range: **0x00..0xF7**
- command count: **248**
- entry width: **4-byte Thumb pointer**
- Retail table: **0x0820770C**
- Debug table: **0x082208A4**
- Retail SHA-256: `ebba8be19326d32b19c90c944ff3085dc0d8f190c100479e6290e6d7835c0d56`
- Debug SHA-256: `18d9c5501e2f2d84cf9f8c2f1274248ad2a9e264816c8fad97c817a268e37258`

Opcode order is defined by the table, not by physical function order. For example, opcode 0x40 is physically emitted near the beginning of the source module.

## Correct module entry

Opcode 0x00 points to atk00_attackcanceler:

- Retail pointer 0x0801BE25 -> code entry **0x0801BE24**
- Debug pointer 0x0801F39D -> code entry **0x0801F39C**

This corrects the previous false boundary at 0x0801C1DC / 0x0801F754; those addresses are an internal helper pair.

## Debug divergence

### opcode 0x15 — atk15_seteffectwithchance

The Debug build adds a bit-0x04 path that can force a secondary move effect when it is otherwise eligible. This adds **44 bytes (0x2C)**, moving subsequent normally ordered commands from +0x3578 to +0x35A4.

Opcode 0x40 retains +0x3578 because its code is physically emitted before this growth.

### opcode 0x9E — atk9E_metronome

The Debug build adds a Metronome move-test path, growing the command by **192 bytes (0xC0)**. From opcode 0x9F onward the normal command delta becomes **+0x3664**.

## First interpreter slice

- Retail 0x0801BE24..0x0801F8EB: 15,048 bytes, SHA-256 `98198ef573895e423f4c6f5a6f85df5bf4145225292980093ef9833bfc18c190`
- Debug 0x0801F39C..0x08022E8F: 15,092 bytes, SHA-256 `a9bf3e2e2cee14e7d9f016fb6cce568c52fa265f21136ff3eeed153157c86df7`

This covers atk00 through atk16, excluding atk17. The 44-byte difference is exactly the Debug branch in atk15.

## Expansion significance

The original VM consumes one-byte opcodes and already occupies 248 of 256 possible values. Only eight raw opcode values remain if the legacy encoding is kept unchanged. A Gen-10-ready design should therefore avoid casually assigning new one-byte opcodes; an escape/extended opcode or versioned extended script format is safer while preserving legacy scripts.

All 248 opcode IDs and source-comparison names are recorded in `manifests/battle-script-command-table.json`. Runtime addresses remain authoritative from the verified German ROM pointer tables.
