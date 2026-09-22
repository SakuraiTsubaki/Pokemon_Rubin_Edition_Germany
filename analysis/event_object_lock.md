# German event_object_lock module

The complete `event_object_lock` text module has been bounded directly in the supplied German Retail Rev 0, Retail Rev 1 and Debug ROMs.

## Module boundary

| Profile | Start | End exclusive | Size | SHA-256 |
| --- | --- | --- | ---: | --- |
| Retail Rev 0 / Rev 1 | 0x08065000 | 0x08065234 | **564 bytes (0x234)** | `b82387f905398a3c212afd964dab927367abaaacf016cafc8d5b0a8d5fe00a2d` |
| Debug | 0x08069600 | 0x08069834 | **564 bytes (0x234)** | `f43b11ba73cfa31e0990719d4f824bd5220881e86bb9dbec3c4c1cb55f96dfc0` |

Retail Rev 0 and Rev 1 are byte-identical across the entire module. Debug adds no `event_object_lock` text, so the accumulated Retail-to-Debug displacement remains **+0x4600** from entry through exit.

## Entry anchor

The first function is source-correlated as `walkrun_is_standing_still`. It returns false only while the player avatar is in the tile-transition state.

Stable prefix:

`00 B5 03 48 C0 78 01 28 04 D0 01 20 03 E0`

The embedded `gPlayerAvatar` address is profile-specific:

- Retail Rev 0 / Rev 1: **0x0202E858**
- Debug: **0x0202EAFC**

Stable suffix:

`00 20 02 BC 08 47`

## Runtime globals

The German binaries establish the profile-specific RAM addresses consumed by the lock layer:

| Global | Retail | Debug | Literal refs in module |
| --- | --- | --- | ---: |
| `gPlayerAvatar` | 0x0202E858 | 0x0202EAFC | 1 |
| `gObjectEvents` | 0x030048B0 | 0x03004980 | 6 |
| `gSelectedObjectEvent` | 0x03004AF0 | 0x03004BC4 | 5 |
| `gSpecialVar_Facing` | 0x0202E8E0 | 0x0202EB84 | 1 |

These are evidence addresses for the German profiles; they are not copied from historical source labels.

## Locking model

The module contains **11 explicit source-correlated functions**:

1. `walkrun_is_standing_still`
2. `sub_8064CDC`
3. `sub_8064CFC`
4. `ScriptFreezeObjectEvents`
5. `sub_8064D38`
6. `sub_8064DB4`
7. `LockSelectedObjectEvent`
8. `ScriptUnfreezeObjectEvents`
9. `unref_sub_8064E5C`
10. `sub_8064EAC`
11. `sub_8064ED4`

There are no `#if DEBUG` text sections in the connected source for this module, consistent with the identical Retail/Debug code size.

The runtime layer coordinates player standing state with generic object-event freezing:

- freeze all ordinary object events while scripts run;
- optionally exclude the selected object until its movement completes;
- wait for player tile movement to settle;
- freeze the selected object once its single movement ends;
- unfreeze and clear held movement on completion;
- face the selected object opposite the requested direction when needed.

The lock task uses two task-data flags to track independent completion of the player-standing condition and selected-object movement condition.

## Relationship to surrounding modules

`field_player_avatar` provides the player tile-transition state and facing/movement helpers. `event_object_movement` provides freezing, held-movement and object lookup primitives. `event_object_lock` combines those primitives into script-safe locking policy.

## Next-module anchor

`text_window` begins immediately afterward:

- Retail Rev 0 / Rev 1: **0x08065234**
- Debug: **0x08069834**
- accumulated delta: **+0x4600**

Its first function is source-correlated as `TextWindow_SetBaseTileNum`. The first 16 bytes are identical across all three German profiles:

`00 04 00 0C 02 49 08 80 09 30 00 04 00 0C 70 47`

The following literal is the shared IWRAM storage address for `sTextWindowBaseTileNum`:

**0x030005AC**

The function stores the input 16-bit base tile number and returns `baseTileNum + 9`. This independently anchors the end of `event_object_lock`.
