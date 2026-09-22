# German opponent battle controller

The complete `battle_controller_opponent` module and its 57-command dispatch table are mapped from the supplied German ROMs.

## Module boundary

| Profile | Start | End exclusive | Size | SHA-256 |
| --- | --- | --- | ---: | --- |
| Retail Rev 0 / Rev 1 | 0x08032CB0 | 0x080361C0 | 13,584 bytes | 5aead473c0aa0e87861721324c5e59275a32c4b94272ce9c177675a0a1ad6bc8 |
| Debug | 0x08036A68 | 0x0803A084 | 13,852 bytes | 2087279f73310a779b9615932200a34c5bd722e3475055ec516bf1d810fb48fc |

Retail Rev 0 and Rev 1 are byte-identical throughout the module.

Debug is **268 bytes (0x10C)** larger. The growth is fully localized by command-pointer delta transitions.

## Dispatch table

- commands: **0x00..0x38** (57)
- Retail table: **0x08207F2C**
- Debug table: **0x082210C4**
- Retail table SHA-256: `94f93ad58b25d4be6b9354903bae1be753b4fa5dba2f8d7aa86f85d6e0d8b80f`
- Debug table SHA-256: `19e1a40f578aa5973776361b3e4fa749e6552b469e47628d71a645431a6dad40`

The command protocol is the same 57-command namespace used by the player controller. The opponent side changes handler implementation, not command IDs.

## Debug growth

Command pointer deltas prove two Debug-only insertions:

1. Commands 0x00..0x07: **+0x3DB8**.
   `OpponentHandleTrainerThrow` contains a Debug override for trainer-front-picture selection. It adds **0x24 bytes (36)**.

2. Commands 0x08..0x14: **+0x3DDC**.
   `OpponentHandlecmd20` contains Debug AI move-cycling and target-test logic. It adds **0xE8 bytes (232)**.

3. Commands 0x15..0x38 and module end: **+0x3EC4**.

Total Debug growth: `0x24 + 0xE8 = 0x10C`.

## Important opponent-side differences

`OpponentHandlecmd20` is the key automatic action-selection path. In normal trainer/first-battle/Safari/roamer contexts it calls the battle AI, converts the chosen result to an action/move/target return value and completes the controller request. In simpler non-trainer contexts it can fall back to random selection from the battler's four non-empty move slots.

The Debug version can instead cycle through the four move slots deterministically and choose target patterns, making it useful as a battle-AI/controller test harness.

`OpponentHandleTrainerThrow` also has a Debug-only path that replaces the normal Secret Base / Battle Tower / e-Reader / trainer-table picture selection with a configured trainer picture.

## Shared protocol constraints

The opponent controller confirms the same original limits already seen on the player side:

- command ID: one byte;
- command count used here: 57;
- battle buffer per battler: 0x200 bytes;
- move-selection structure: four moves;
- active battle topology: maximum four battlers.

## Player vs opponent controller

Both sides consume the same command-buffer protocol for sprite loading, send-out/return, trainer animation, move animation, text, HP/status updates, sound, battle animations, link standby and end-of-battle handling.

The main architectural difference is input ownership: the player controller contains UI/input handlers, while the opponent controller resolves action choice through AI or automatic logic. This makes the shared controller protocol a strong candidate for a stable compatibility ABI while modern AI/input implementations evolve independently.

## Next module

`battle_ai_switch_items` starts immediately after the empty opponent command-56 handler:

- Retail: **0x080361C0**
- Debug: **0x0803A084**
- delta: **+0x3EC4**

The next function is `ShouldSwitchIfPerishSong`.
