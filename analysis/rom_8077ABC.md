# German rom_8077ABC module

The historical source filename `rom_8077ABC` is retained only as a semantic identifier. **0x08077ABC is not treated as a German ROM address.** The complete German module has been re-bounded directly from the supplied Retail Rev 0, Retail Rev 1 and Debug binaries.

## Module boundary

| Profile | Start | End exclusive | Size | SHA-256 |
| --- | --- | --- | ---: | --- |
| Retail Rev 0 / Rev 1 | 0x08077E7C | 0x0807ADE8 | **12,140 bytes (0x2F6C)** | `45ac9b3545cb3dfc58e3e2b02c2cd0b193e72cb998e2f0c85dc21d3ad8d337fa` |
| Debug | 0x0807F0E8 | 0x08082054 | **12,140 bytes (0x2F6C)** | `b077bfd1b8f84650c1fe96a10724f3d215b876d880c62c0319234564d87867b7` |

Retail Rev 0 and Rev 1 are byte-identical across the complete module. Connected source contains no Debug-only text, matching the binary result: the accumulated Retail-to-Debug displacement remains **+0x726C** at both entry and exit.

## Entry anchor

The first function is source-correlated as `GetBattlerSpriteCoord`.

Common first 32 bytes:

`30 B5 00 06 05 0E 09 06 0C 0E FF F7 8B F8 00 06 00 28 04 D0 03 2C 02 D1 03 2D 00 D1 01 24 04 2C`

It normalizes the battler slot/coordinate selector, handles Contest coordinate behavior, and then dispatches among fixed battler positions and species/form-derived sprite coordinates.

## Runtime scope

The connected source contains **118 explicit functions** and no `#if DEBUG` text.

This module provides a broad set of battle sprite and animation geometry helpers, including:

- battler X/Y coordinate selection;
- front/back sprite Y offsets;
- Unown personality-form coordinate resolution;
- Castform form coordinates/elevations;
- attacker/target/partner sprite-ID lookup;
- stored sprite callbacks and wait callbacks;
- sprite translation helpers;
- animation sprite positioning relative to attacker/target;
- battler sprite priority/subpriority and BG priority;
- duplicate/transparency sprite helpers;
- palette/resource cleanup;
- coordinate-attribute queries and average battler positions;
- several low-level animation sprite/task implementations historically grouped under this source filename.

Historical numeric names such as `sub_807A9BC` are semantic labels only. They are never used as German address evidence.

## Tail anchor

The final source-correlated function is `sub_807A9BC`.

- Retail Rev 0 / Rev 1: **0x0807AD7C..0x0807ADE8**
- Debug: **0x08081FE8..0x08082054**
- size: **0x6C bytes**

SHA-256:

- Retail: `bf5c11aa0f0330b73deb89f6afb0c3eee4f0240f6168c48418cbc5dbaa2c1bfd`
- Debug: `035e1847ab0e415478379d66fecd1ea36f25379df79968e279de1371150ac722`

Its final literal pool is included through the module end. The following byte starts `task`.

## Next-module anchor: task / ResetTasks

`task` begins immediately afterward:

- Retail Rev 0 / Rev 1: **0x0807ADE8**
- Debug: **0x08082054**
- accumulated delta: **+0x726C**

The first function is source-correlated as `ResetTasks`. Its first **0x30 bytes** are identical across profiles before the relocated `memset` branch:

`F0 B5 00 24 13 4E 37 1C 08 37 A0 00 00 19 C0 00 82 19 00 21 11 71 10 49 11 60 54 71 01 34 94 71 01 21 49 42 0D 1C FF 21 D1 71 C0 19 00 21 20 22`

The German binary independently confirms the task ABI:

- **16 task slots**
- **Task size 0x28 bytes**
- **task data area 0x20 bytes**
- head sentinel **0xFE**
- tail sentinel **0xFF**

Profile-specific literals in `ResetTasks`:

| Symbol | Retail | Debug |
| --- | --- | --- |
| `gTasks` | 0x03004B30 | 0x03004C10 |
| `TaskDummy` Thumb pointer | 0x0807B011 | 0x08082285 |

The final literal `0x0000025E` is the byte offset used to reach the last task's `next` byte from the start of `gTasks` (15 × 0x28 + 6).

This loop/sentinel structure independently fixes the `rom_8077ABC` → `task` boundary.
