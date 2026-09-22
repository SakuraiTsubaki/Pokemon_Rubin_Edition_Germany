# German script module

The complete `script` text module has been bounded directly in the supplied German Retail Rev 0, Retail Rev 1 and Debug ROMs.

## Module boundary

| Profile | Start | End exclusive | Size | SHA-256 |
| --- | --- | --- | ---: | --- |
| Retail Rev 0 / Rev 1 | 0x080656D4 | 0x08065BAC | **1,240 bytes (0x4D8)** | `4b56a2c1b4a0c91db332dffcf8e65e87224c4537ee058c459c13aab7467a7b1f` |
| Debug | 0x08069CD4 | 0x0806A1AC | **1,240 bytes (0x4D8)** | `95e62a9bfde97ee285c346060870dde56d3c0b285e5df1060db1aa133dde25e6` |

Retail Rev 0 and Rev 1 are byte-identical across the complete module. Debug adds no `script` text, so the accumulated Retail-to-Debug displacement remains **+0x4600** at both entry and exit.

## Entry anchor

The first function is source-correlated as `InitScriptContext`. The first 48 bytes are identical in all three German profiles:

`00 B5 03 1C 00 20 58 70 98 60 18 70 58 60 D9 65 1A 66 00 22 03 21 18 1C 70 30 02 60 04 38 01 39 00 29 FA DA 19 1C 0C 31 00 22 18 1C 58 30 02 60`

The function clears interpreter state, stores command-table bounds, clears the four data words and clears the 20-entry return stack.

## ScriptContext ABI

The source-correlated `ScriptContext` contains:

- stack depth
- mode
- comparison result
- native callback
- script pointer
- 20-entry script return stack
- command-table start/end pointers
- four 32-bit local data slots

The interpreter supports stopped, bytecode and native execution modes.

## Interpreter flow

The module contains **34 source-correlated functions**:

- context initialization/setup/stop;
- bytecode/native command dispatch;
- script call stack push/pop/jump/call/return;
- 16-bit and 32-bit bytecode readers;
- field-control lock/unlock;
- global and immediate script contexts;
- map-script dispatch;
- on-load/transition/resume/dive-warp/frame/warp-in map scripts;
- RAM-script checksum, clear, initialization and lookup.

The bytecode dispatcher validates command-table bounds before invoking a command handler. The source-correlated null-script path intentionally halts indefinitely with SWI/SVC behavior.

## Map script layer

Map script table entries are selected by tag. Immediate map scripts use a separate interpreter context, while frame-table scripts can hand execution to the global script context.

The layer supports the map-script categories used by the overworld transition/runtime code already mapped earlier in this project.

## RAM script layer

The source-correlated RAM script magic is **51 (0x33)**. The German binary tail independently contains the `cmp #0x33` logic inside `GetRamScript`.

Profile-specific EWRAM references visible in the final function include:

| Global | Retail | Debug |
| --- | --- | --- |
| `gRamScriptRetAddr` | 0x02028DC8 | 0x0202906C |
| `gSaveBlock1` base used by RAM-script access | 0x0202E8AC | 0x0202EB50 |

`GetRamScript` validates magic, map group, map number, local ID and checksum before returning the stored RAM script. Failed checksum validation clears the RAM script.

## Next-module anchor

`scrcmd` starts immediately afterward:

- Retail Rev 0 / Rev 1: **0x08065BAC**
- Debug: **0x0806A1AC**
- accumulated delta: **+0x4600**

The first commands are source-correlated as `ScrCmd_nop`, `ScrCmd_nop1`, then `ScrCmd_end`.

The German bytes begin:

`00 20 70 47 00 20 70 47 00 B5 FF F7 B5 FD 00 20 02 BC 08 47`

The first two four-byte functions are independent `return FALSE` leaves. The third calls `StopScript` and returns false. This provides a strong multi-function anchor for the `script` → `scrcmd` boundary without borrowing an address from another ROM.
