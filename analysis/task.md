# German task module

The complete `task` text module has been bounded directly in the supplied German Retail Rev 0, Retail Rev 1 and Debug ROMs.

## Module boundary

| Profile | Start | End exclusive | Size | SHA-256 |
| --- | --- | --- | ---: | --- |
| Retail Rev 0 / Rev 1 | 0x0807ADE8 | 0x0807B114 | **812 bytes (0x32C)** | `68d30c1dfd7fa6d080cabae3fbfdf8e37dd0a8f08b53ade8b916dd1620772920` |
| Debug | 0x08082054 | 0x08082388 | **820 bytes (0x334)** | `ceabbb2065c235e4d0dac09d37c5835886c406f1dfb86f1e498d970ecb482cc3` |

Retail Rev 0 and Rev 1 are byte-identical across the complete module.

Debug is exactly **8 bytes larger**. The accumulated Retail-to-Debug text displacement changes from **+0x726C** at module entry to **+0x7274** at module exit.

## Entry anchor: ResetTasks

The first function is source-correlated as `ResetTasks`.

The first 0x30 bytes are identical across all profiles before the relocated `memset` call:

`F0 B5 00 24 13 4E 37 1C 08 37 A0 00 00 19 C0 00 82 19 00 21 11 71 10 49 11 60 54 71 01 34 94 71 01 21 49 42 0D 1C FF 21 D1 71 C0 19 00 21 20 22`

The binary loop establishes:

- **16 Task records**
- **Task size 0x28 bytes**
- **Task data size 0x20 bytes**
- head sentinel **0xFE**
- tail sentinel **0xFF**

Profile-specific task array addresses:

- Retail Rev 0 / Rev 1 `gTasks`: **0x03004B30**
- Debug `gTasks`: **0x03004C10**

The `TaskDummy` Thumb pointers loaded by `ResetTasks` are:

- Retail: **0x0807B011**
- Debug: **0x08082285**

## Debug growth: CreateTask

The connected source contains one `#if DEBUG` text region:

`Crash(gError_NoTasksLeft);`

It is inside `CreateTask` after all 16 task slots have been tested.

German function ranges:

| Profile | CreateTask range | Size | SHA-256 |
| --- | --- | ---: | --- |
| Retail Rev 0 / Rev 1 | 0x0807AE48..0x0807AE9C | 0x54 | `f2013a49d64d7d8e490d9bbdbb6b8fd2355153b80dfc74005afe452084ac1154` |
| Debug | 0x080820B4..0x08082110 | 0x5C | `4b6b4aa00f2492030c4f6ffb0a686dede295fad9d55ca354fc0484da7eef00a7` |

The exact **0x8-byte increase** accounts for the entire module growth.

The Debug function's final literal is the Debug task-overflow message address:

**0x083B8B18**

No guessed redistribution of bytes to other functions is needed.

## Task queue model

The source-correlated module contains **12 explicit functions**:

1. `ResetTasks`
2. `CreateTask`
3. `InsertTask`
4. `DestroyTask`
5. `RunTasks`
6. `FindFirstActiveTask`
7. `TaskDummy`
8. `SetTaskFuncWithFollowupFunc`
9. `SwitchTaskToFollowupFunc`
10. `FuncIsActiveTask`
11. `FindTaskIdByFunc`
12. `GetTaskCount`

The queue is priority ordered and linked through each Task record's `prev` and `next` bytes. The 16-record task array is reset to an inactive linked sequence, then active tasks are inserted into the priority chain.

The follow-up-function helpers store a 32-bit function pointer in the final two task-data halfwords and later reconstruct it.

## Tail and next-module anchor

`GetTaskCount` is the final task function. Its literal pool contains the profile-specific `gTasks` base and is included through the module end.

`reshow_battle_screen` begins immediately afterward:

- Retail Rev 0 / Rev 1: **0x0807B114**
- Debug: **0x08082388**
- accumulated delta: **+0x7274**

The first function is `ReshowBattleScreenDummy`, which compiles to:

`70 47 00 00`

The next function, `ReshowBattleScreenAfterMenu`, begins immediately afterward with the common prefix:

`00 B5 0D 4A 10 7A 80 21 08 43 10 72 00 20`

This two-function sequence independently anchors the task-module end.
