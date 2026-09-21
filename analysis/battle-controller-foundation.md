# German battle-controller foundation

The module beginning immediately after the completed main-menu module is the battle-controller module.

## Module entry

- Retail Rev 0 / Rev 1: 0x0800BA2C
- German Debug: 0x0800BC0C

The first entry therefore inherits the +0x1E0 Debug displacement established by the Debug-only RTC additions.

## Early function map

| Function | Retail | Debug | Delta | Retail size | Role |
| --- | --- | --- | ---: | ---: | --- |
| HandleLinkBattleSetup | 0x0800BA2C | 0x0800BC0C | +0x1E0 | 44 | link-battle setup entry |
| SetUpBattleVarsAndBirchPoochyena | 0x0800BA58 | 0x0800BC38 | +0x1E0 | 204 | battle globals/controllers initialization; first-battle Poochyena setup |
| sub_800B950 | 0x0800BB24 | 0x0800BD40 | +0x21C | 88 | select single/link controllers, assign party slots, initialize battlers |
| InitSinglePlayerBtlControllers | 0x0800BB7C | 0x0800BD98 | +0x21C | 208 | single-player controller topology |
| InitLinkBtlControllers | 0x0800BC4C | 0x0800BE68 | +0x21C | 732 | link/multi battle controller topology |
| SetBattlePartyIds | 0x0800BF28 | 0x0800C144 | +0x21C | 328 | select valid party member indexes for battlers |
| PrepareBufferDataTransfer | 0x0800C070 | 0x0800C28C | +0x21C | 140 | route controller payload to link or local battle buffers |
| CreateTasksForSendRecvLinkBuffers | 0x0800C0FC | 0x0800C318 | +0x21C | 200 | initialize link send/receive tasks and buffers |
| PrepareBufferDataTransferLink | 0x0800C1C4 | 0x0800C3E0 | +0x21C | 440 | pack controller payload into link-send ring buffer |
| Task_HandleSendLinkBuffersData | 0x0800C37C | 0x0800C598 | +0x21C | 436 | link-send task state machine |
| sub_800C35C | 0x0800C530 | 0x0800C74C | +0x21C | 288 | copy received link blocks into battle receive buffer |
| Task_HandleCopyReceivedLinkBuffersData | 0x0800C650 | 0x0800C86C | +0x21C | 412 | dispatch received link controller blocks |
| BtlController_EmitGetMonData | 0x0800C7EC | 0x0800CA08 | +0x21C | next slice | first controller command emitter; next slice |

## First Debug-specific battle divergence

The first function, HandleLinkBattleSetup, has the same 44-byte size in Retail and Debug.

SetUpBattleVarsAndBirchPoochyena is different:

- Retail: 0x0800BA58..0x0800BB23 = 204 bytes
- Debug: 0x0800BC38..0x0800BD3F = 264 bytes
- Debug-only growth: **60 bytes (0x3C)**

Consequently, all following mapped functions in this slice move from the previous +0x1E0 Debug displacement to **+0x21C**.

The Debug-only tail contains literals for:

- 0x02023A0C
- shared-memory base 0x02000000
- offsets 0x160FD and 0x160FF
- 0x030041D0

This establishes that the Debug build performs extra battle-initialization work touching a debug/control location, three bytes in shared battle memory around 0x160FD..0x160FF, and a battle transfer-buffer/global location. These operations do not exist in either German retail revision.

## Retail revision equality

Retail Rev 0 and Rev 1 are byte-identical over the entire mapped early battle-controller slice:

- 0x0800BA2C..0x0800C7EB
- 3,520 bytes
- SHA-256: ed1195f99f35a971e23d8018c26ccdd043155efacb7ec9b3fca5aba8fab1dd6c

The corresponding Debug slice is:

- 0x0800BC0C..0x0800CA07
- 3,580 bytes
- SHA-256: 39f0347ff1bd8a793d2f09bffe6d846fd71a399c279ad2a997924682406c304d

The exact 60-byte size difference is fully accounted for by the expanded Debug SetUpBattleVarsAndBirchPoochyena routine.

## Structural findings

This slice already exposes several engine systems that will matter later for expansion:

- controller-function arrays for up to four battlers;
- player/opponent/link-partner topology;
- party-index assignment;
- local A/B battle command buffers;
- link send/receive tasks;
- 0x1000-byte ring/wrap behavior for link battle communication;
- controller command packet framing.

The next function at 0x0800C7EC / 0x0800CA08 begins the long series of BtlController_Emit* command constructors.
