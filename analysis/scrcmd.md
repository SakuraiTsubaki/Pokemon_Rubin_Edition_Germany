# German scrcmd module

The complete `scrcmd` text module has been bounded directly in the supplied German Retail Rev 0, Retail Rev 1 and Debug ROMs.

## Module boundary

| Profile | Start | End exclusive | Size | SHA-256 |
| --- | --- | --- | ---: | --- |
| Retail Rev 0 / Rev 1 | 0x08065BAC | 0x0806822C | **9,856 bytes (0x2680)** | `d9abe33055babd8e6e68fbb4838afb265c5475bfeb71b0a8a4fc3126ae34d372` |
| Debug | 0x0806A1AC | 0x0806C82C | **9,856 bytes (0x2680)** | `de537d1d54882ba4d7ee7d9af4f581141a23ad320e6ba938a5312140eb207b5f` |

Retail Rev 0 and Rev 1 are byte-identical across the complete module. The connected source contains no `#if DEBUG` text in this module, matching the binary result: Debug adds no `scrcmd` code and the accumulated Retail-to-Debug displacement remains **+0x4600** at entry and exit.

## Entry anchor

The module starts with three consecutive command handlers:

1. `ScrCmd_nop`
2. `ScrCmd_nop1`
3. `ScrCmd_end`

German entry bytes:

`00 20 70 47 00 20 70 47 00 B5 FF F7 B5 FD 00 20 02 BC 08 47`

The first two are independent four-byte `return FALSE` leaves. The third calls `StopScript` and returns false. This is a strong multi-function boundary anchor.

## Command layer

The connected source contains **207 explicit function definitions** in `scrcmd.c`. Historical numeric function names are semantic source labels only; addresses in this project are always re-established from the German binaries.

The command layer covers the full field-script command surface, including:

- control flow: goto/call/return/native/std/conditional variants;
- local data, bytes, words, variables, comparisons and arithmetic;
- flags and special variables;
- items, PC items, money and coins;
- text/message buffering and placeholder expansion;
- movement and object-event commands;
- warps, fades, weather and map transitions;
- party/Pokémon operations;
- trainer and scripted wild battles;
- shops, decorations and slot machine;
- contests;
- field effects;
- metatile edits;
- door open/close animation;
- respawn and player-gender queries.

The module is the concrete bytecode-command implementation layer driven by the `script` interpreter mapped immediately before it.

## Shared script state

The source-correlated virtual-address commands use an EWRAM relocation accumulator, while many commands communicate through special variables and the global script result.

The final literal pool of the German module is the profile-specific `gSpecialVar_Result` address:

- Retail Rev 0 / Rev 1: **0x0202E8DC**
- Debug: **0x0202EB80**

That literal is included in the module boundary; the following byte starts the next module.

## Map integration

The command handlers directly consume the map/runtime layers already mapped in this repository:

- `MapGridSetMetatileIdAt` and the map-grid collision mask;
- `FieldAnimateDoorOpen` / `FieldAnimateDoorClose`;
- `FieldSetDoorOpened` / `FieldSetDoorClosed`;
- field effects and map warps;
- object movement and player control locks.

For the door/metatile commands, script coordinates are shifted by the established map offset of **7** before operating on the backup/current field grid.

## Next-module anchor

`field_control_avatar` starts immediately afterward:

- Retail Rev 0 / Rev 1: **0x0806822C**
- Debug: **0x0806C82C**
- accumulated delta: **+0x4600**

Its first function is source-correlated as `ClearPlayerFieldInput`. The first German function body is identical in all profiles:

`30 B5 02 21 49 42 03 23 5B 42 05 24 64 42 09 25 6D 42 00 22 02 70 42 78 11 40 19 40 21 40 29 40 41 70 00 21 81 70 30 BC 01 BC 00 47`

The compiler preserves unspecified bits while clearing the source-defined input flags and direction fields. This sequence independently anchors the `scrcmd` end.

## Boundary correction note

A preliminary candidate at `0x08068220` was rejected before commit because it still lay inside the final command handler's literal pool. The binary-verified end is **0x0806822C**, including the final `gSpecialVar_Result` literal. The verifier enforces this exact boundary.
