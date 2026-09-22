# German field_tasks module

The complete `field_tasks` text module has been bounded directly in the supplied German Retail Rev 0, Retail Rev 1 and Debug ROMs.

## Module boundary

| Profile | Start | End exclusive | Size | SHA-256 |
| --- | --- | --- | ---: | --- |
| Retail Rev 0 / Rev 1 | 0x0806977C | 0x0806A668 | **3,820 bytes (0xEEC)** | `71549fd25ff83140a1e90464aff4a3db7d3ca0092fc533c4feafa7b3a8f370ca` |
| Debug | 0x0806DE58 | 0x0806ED44 | **3,820 bytes (0xEEC)** | `be1aee30a11d8ceba061f45a3c54d4da36cf5ad198a97f146f1864774ec75e46` |

Retail Rev 0 and Rev 1 are byte-identical across the entire module. Debug adds no `field_tasks` text, so the accumulated Retail-to-Debug displacement remains **+0x46DC** at entry and exit.

## Entry anchor

The first function is source-correlated as `Task_RunPerStepCallback`.

Stable first 28 bytes:

`00 B5 00 06 00 0E 07 4A 81 00 09 18 C9 00 89 18 08 22 89 5E 04 4A 89 00 89 18 09 68`

The function reads the active per-step callback index from the task data and dispatches through the callback table.

## Per-step callback table

The callback table has eight entries:

- Retail Rev 0 / Rev 1: **0x08381B4C**
- Debug: **0x0839ACF4**

Retail entries:

1. 0x0806991D — DummyPerStepCallback
2. 0x0806A2A5 — ash-grass callback
3. 0x08069DE1 — Sootopolis cracked-ice callback
4. 0x08069BA5 — Fortree bridge callback
5. 0x0806A115 — cracked-floor callback
6. 0x080C78FD — EndTruckSequence
7. 0x080BD0B1 — external field-special callback
8. 0x0806A3BD — final per-step callback

Debug relocates the six callbacks owned by this module by exactly **+0x46DC**. External callbacks follow their own later-module relocation profiles and are therefore not forced into the field_tasks delta.

## Runtime responsibilities

The module provides the overworld per-step task layer for:

- periodic time-based event checks and ambient cries;
- per-step callback selection/reset;
- Pacifidlog floating/submerged log animation;
- Fortree bridge depression/restoration;
- Sootopolis Gym cracked-ice persistence and break animation;
- ash-grass clearing and soot collection;
- cracked-floor timing;
- muddy-slope animation;
- map/camera compensation for active mudslide effects.

The source-correlated implementation contains **27 explicit functions** and no `#if DEBUG` text.

## Map integration

The Pacifidlog, Fortree, Sootopolis and muddy-slope handlers operate directly on the map grid and call the field-camera redraw path already mapped earlier in the project.

Sootopolis cracked-ice persistence converts between map-grid coordinates and map-local coordinates using the established **MAP_OFFSET = 7**.

The muddy-slope task supports up to four simultaneous three-word animation records in task data, each with a 32-frame lifetime.

## Tail anchor

The final function is source-correlated as `Task_MuddySlope`. Its final epilogue is identical in all three profiles:

`01 B0 08 BC 98 46 F0 BC 01 BC 00 47`

The final four bytes `01 BC 00 47` are included in the module boundary.

## Next-module anchor

`clock` begins immediately afterward:

- Retail Rev 0 / Rev 1: **0x0806A668**
- Debug: **0x0806ED44**
- accumulated delta: **+0x46DC**

Its first function is source-correlated as `InitTimeBasedEvents`.

The function begins with `00 B5 09 48`, sets `FLAG_SYS_CLOCK_SET = 0x0835`, calculates local RTC time, copies the local time into the save block's last-berry-update field, stores `VAR_DAYS = 0x4040`, and returns.

The `0x0835` and `0x4040` literals in the first clock function provide independent semantic anchors for the transition.
