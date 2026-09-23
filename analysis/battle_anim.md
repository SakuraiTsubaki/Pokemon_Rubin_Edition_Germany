# German battle_anim module

The complete `battle_anim` text module has been bounded directly in the supplied German Retail Rev 0, Retail Rev 1 and Debug ROMs.

## Module boundary

| Profile | Start | End exclusive | Size | SHA-256 |
| --- | --- | --- | ---: | --- |
| Retail Rev 0 / Rev 1 | 0x080759E4 | 0x08077E7C | **9,368 bytes (0x2498)** | `c5eda52f36c5b7ff1bb83de262b3ceab7dbc7a6308933eeffa3aab014aa9c013` |
| Debug | 0x0807CC50 | 0x0807F0E8 | **9,368 bytes (0x2498)** | `819df18b3733a0edb4ac128c409fdbd68cd179a0b0a2fdaa00be9471dd1a3c3f` |

Retail Rev 0 and Rev 1 are byte-identical across the complete module. Connected source contains no Debug-only text in this module, matching the binary result: the accumulated Retail-to-Debug displacement remains **+0x726C** from entry through exit.

## Entry anchor

The first function is source-correlated as `ClearBattleAnimationVars`.

Common first 32 bytes:

`F0 B5 4F 46 46 46 C0 B4 22 48 00 21 01 70 22 48 01 70 22 48 01 70 22 48 01 70 22 48 00 21 01 60`

The function clears the core battle-animation interpreter counters/state, resets animation arguments and sprite-index tracking, and clears attacker/target and move-animation state.

## Runtime interpreter

The source-correlated module contains **75 explicit functions** and a **48-entry animation script command table**.

The command set covers compressed animation sprite graphics load/unload, sprite and visual-task creation, delays and waits, call/return/jump, animation arguments, battler background routing, blending, animation-background fade/load/restore, panned/repeated sound effects, sound tasks, contest/double-battle branches, battler visibility, BG priority and sound-stop cleanup.

## Tail anchor

The final function is source-correlated as `ScriptCmd_stopsound`.

- Retail Rev 0 / Rev 1: **0x08077E54..0x08077E7C**
- Debug: **0x0807F0C0..0x0807F0E8**
- size: **0x28 bytes**

It stops both SE players and increments the battle-animation script pointer. The final literal pool contains:

| Literal | Retail | Debug |
| --- | --- | --- |
| SE1 | 0x030073D0 | 0x030074E0 |
| SE2 | 0x03007410 | 0x03007520 |
| `sBattleAnimScriptPtr` | 0x0202F7A4 | 0x0202FA48 |

## Next-module anchor

`rom_8077ABC` begins immediately afterward:

- Retail Rev 0 / Rev 1: **0x08077E7C**
- Debug: **0x0807F0E8**
- accumulated delta: **+0x726C**

Its first function is source-correlated as `GetBattlerSpriteCoord`.

Common first 32 bytes:

`30 B5 00 06 05 0E 09 06 0C 0E FF F7 8B F8 00 06 00 28 04 D0 03 2C 02 D1 03 2D 00 D1 01 24 04 2C`

Historical `8077ABC` naming is retained only as a semantic/source identifier; it is not treated as the German ROM address.
