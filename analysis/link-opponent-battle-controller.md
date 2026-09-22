# German link-opponent battle controller

The complete `battle_controller_link_opponent` module is mapped from the supplied German ROMs.

## Module boundary

| Profile | Start | End exclusive | Size | SHA-256 |
| --- | --- | --- | ---: | --- |
| Retail Rev 0 / Rev 1 | 0x080376E0 | 0x0803A894 | 12,724 bytes | be0ae41d9a3ac32369d15f31fc5c4f72491b238c6b48bdca06e8dd117d73357d |
| Debug | 0x0803B5B4 | 0x0803E768 | 12,724 bytes | 7b481172fd4c9d3ae43e56c0151c323a02fa9dc70244d103e8b49d6f1d5bc09b |

Retail Rev 0 and Rev 1 are byte-identical across the module. There is **no Debug-only growth**; the complete module and all 57 handler entries remain at delta **+0x3ED4**.

## Dispatch table

- command range: 0x00..0x38
- command count: 57
- Retail table: **0x08208018**
- Debug table: **0x082211B0**
- Retail table SHA-256: `ab46af9102042f243e39cda3b3586461130ce252ddcb16fc1ef80c65ee85d959`
- Debug table SHA-256: `e86c03defee73f1b93445225d3f8071ae611ffdf52a61f922267afcef2b9b6d3`

## Architecture

The link-opponent controller uses the same 57-command wire protocol as the local player and local opponent controllers. It implements the remote-opponent presentation/data endpoint while link synchronization determines when each command completes.

Unlike `battle_controller_opponent`, this module has no Debug AI-selection or trainer-picture overrides. That makes it a useful clean reference for the controller ABI itself.

Common protocol operations include attribute get/set, sprite load/send-out/return, trainer animations, move animation, battle text, HP/status updates, sound, hit animation, battle animation, link standby and battle completion.

## Stable ABI implication

The same 0x00..0x38 command namespace appearing across player, opponent and link-opponent controllers strongly suggests preserving this command layer as a legacy controller ABI. Modern UI, AI and networking can be implemented behind adapters while legacy battle scripts continue producing the original controller messages.

## Next module

The next linked module is `pokemon_1`.

`ZeroBoxMonData` begins at:

- Retail **0x0803A894**
- Debug **0x0803E768**
- delta **+0x3ED4**.

The preceding link-opponent command 0x38 is the empty `LinkOpponentHandlecmd56`, ending at the module boundary.
