# German player battle controller

The complete `battle_controller_player` module boundary and its 57-command dispatch table have been located directly in the supplied German ROMs.

## Module boundary

| Profile | Start | End exclusive | Size | SHA-256 |
| --- | --- | --- | ---: | --- |
| Retail Rev 0 / Rev 1 | 0x0802C144 | 0x080314C4 | 21,376 bytes (0x5380) | 7b2e93299fcb177e344049e3b6443099374d57a624ba2c86f80ef3bd2c1093fb |
| Debug | 0x0802F7A8 | 0x0803527C | 23,252 bytes (0x5AD4) | bc563162bc54b9e206540d86fcb8509c040cc12bf77f9eedb317c7e86ad18f68 |

Retail Rev 0 and Rev 1 are byte-identical throughout the module.

Debug is **1,876 bytes (0x754)** larger. The module begins at the inherited battle-script delta +0x3664, but every command handler and the module end are shifted by **+0x3DB8**. The increase therefore occurs in the controller's pre-handler/input code.

Source comparison identifies the extra Debug path as move-selection and move-animation inspection tooling: START/SELECT/L/R/D-pad controls, move-ID walking, animation-turn control, sprite/task/OAM-matrix counters, and two Debug-only callbacks. Exact byte attribution among those DEBUG blocks remains a statement-level follow-up; the binary size increase itself is proven.

## Dispatch table

- command range: **0x00..0x38**
- command count: **57**
- entry width: **4-byte Thumb pointer**
- Retail table: **0x08207D68**
- Debug table: **0x08220F00**
- Retail table SHA-256: `96b74032006663bbeb41941c1331912b07f7cb5e31dc4cea4bb18c92c48e8d4f`
- Debug table SHA-256: `4380e6eff2e2beabccb6ced1f9817bd951f8e406d02786585edb3fdabb2ba99e`

`PlayerBufferRunCommand` reads byte 0 from the active battler's 0x200-byte battle buffer. Values below 0x39 dispatch through this table; values outside the 57-command range complete the controller request instead.

## Controller entry core

- BattleControllerDummy: Retail 0x0802C144 / Debug 0x0802F7A8
- SetBankFuncToPlayerBufferRunCommand: 0x0802C148 / 0x0802F7AC
- PlayerBufferExecCompleted: 0x0802C170 / 0x0802F7D4
- PlayerBufferRunCommand: 0x0802C1E8 / 0x0802F84C
- first handler PlayerHandleGetAttributes: 0x0802E6A4 / 0x0803245C

Before the Debug-only growth, these controller-core entries keep delta +0x3664. All 57 dispatch handlers use +0x3DB8.

## Completion protocol

In local/non-link battles `PlayerBufferExecCompleted` clears the active battler bit from `gBattleControllerExecFlags`. In link battles it transfers the multiplayer player ID and rewrites command byte 0 to 0x38 for link completion synchronization.

## German-specific UI evidence

The move/action UI contains an explicit regional compile-time difference:

- English tile-data text offset: 440
- **German tile-data text offset: 444**

The German value is used when drawing `BattleText_OtherMenu`. This is direct evidence that localization affects controller/UI geometry, not only strings.

## Fixed-capacity evidence

The player controller repeatedly exposes the original architecture:

- per-battler command buffer: 0x200 bytes;
- four move IDs and four PP values in move-selection structures;
- six party-status entries;
- at most four active battlers;
- command ID itself is one byte.

## Next module

The next linked module is `battle_gfx_sfx_util`. Its first function `SpriteCB_WaitForBattlerBallReleaseAnim` starts at Retail **0x080314C4** / Debug **0x0803527C**, after the empty command-56 handler.
