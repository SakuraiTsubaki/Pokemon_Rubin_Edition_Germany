# German field_player_avatar module

The complete `field_player_avatar` text module has been bounded directly in the supplied German Retail Rev 0, Retail Rev 1 and Debug ROMs. The German ROM binaries are the address and boundary authority; connected source is used only to attach semantic names and behavior to binary-proven regions.

## Module boundary

| Profile | Start | End exclusive | Size | SHA-256 |
| --- | --- | --- | ---: | --- |
| Retail Rev 0 / Rev 1 | 0x08058AF4 | 0x0805AD90 | **8,860 bytes (0x229C)** | `222f2eee68b4ca41ba6c9329b2691f18980b045715ba5926f149466f44c4dcfd` |
| Debug | 0x0805CFDC | 0x0805F348 | **9,068 bytes (0x236C)** | `bb5acc900b4dc33878bceef76755552d5bde8752ac9b8d35e8b65476551858ad` |

Retail Rev 0 and Rev 1 are byte-identical across the complete module.

Unlike the preceding `fieldmap`, `metatile_behavior`, `field_camera` and `field_door` modules, Debug **does add player-avatar code**. The module is **208 bytes (0xD0)** larger in Debug.

The accumulated Retail-to-Debug text displacement changes from **+0x44E8** at module entry to **+0x45B8** at module exit / the next module.

## Debug growth

The Debug image splits cleanly at the start of its two Debug-only tail functions:

- Debug common-body end / Debug-only tail start: **0x0805F2B0**
- Debug module end: **0x0805F348**

Compared with the complete Retail body, the Debug common body is **0x38 bytes larger**. Connected source correlates that growth with two conditional Debug paths inside common functions:

1. `TryDoMetatileBehaviorForcedMovement` can bypass forced movement when the Debug working flag is active and R is held.
2. `MovePlayerNotOnBike` can route movement through the Debug movement handler when the Debug working flag is active.

The final **0x98 bytes** are two Debug-only functions:

| Semantic source name | German Debug range | Size | SHA-256 |
| --- | --- | ---: | --- |
| `debug_sub_805F2B0` | 0x0805F2B0..0x0805F2DC | 0x2C | `f617e6afde734d0fe7db07543484fc9d95d658a6bb3da8505410ec3bfd4888bf` |
| `debug_sub_805F2DC` | 0x0805F2DC..0x0805F348 | 0x6C | `4e34a8b6306b1e55f192bf62a9c0be141b1c11b6c4a3afe352bb6b927e8d04e2` |

Combined Debug-only tail SHA-256:

`6cafd04d4c299ff17733bd4fa9083da2c28aaafecc7056a400f840d5e15193fd`

This gives a binary-proven growth decomposition of **0x38 internal conditional growth + 0x98 Debug-only tail = 0xD0**. No guessed per-conditional split is recorded.

The first tail function checks R and dispatches to the second handler. The second handler preserves the source-correlated Debug behavior: no direction faces the current movement direction; blocked tracked-camera movement collides; otherwise it uses the speed-4 movement path.

## Entry anchor

The module starts with the macro-generated `MovementType_Player` wrapper. Retail and Debug share the same stable entry prefix before the profile-specific branch displacement:

`00 B5 01 1C 2E 20 0A 5E D0 00 80 18 80 00 03 4A 80 18 03 4A`

At offset **+0x24** from module start, both profiles contain the generated callback leaf:

`00 20 70 47`

which returns zero.

The wrapper attaches the player movement-type callback to the live player `ObjectEvent`. Historical numeric labels embedded in source names are semantic source labels only and are never treated as German addresses.

## Player avatar runtime state

The source-correlated `PlayerAvatar` record is **0x24 bytes** and carries the field-control state used throughout this module, including avatar mode flags, running/tile-transition state, sprite and ObjectEvent IDs, `preventStep`, gender, and Acro Bike input histories.

The module is therefore the policy layer between keypad movement intent and the lower-level object-event movement engine that follows it in ROM.

## Forced movement

The source-correlated forced-movement classifier contains **18 metatile behavior tests**. Their result selects from **19 movement handlers**, including the default/no-forced-movement state.

Covered behaviors include slippery/ice movement, forced directional walking, water currents, directional slides, waterfall movement, Secret Base jump/spin mats and muddy slopes.

This consumes the one-byte metatile behavior produced by `fieldmap` and classified by `metatile_behavior`; it does not own map geometry itself.

## Ordinary movement and collision

Non-bike movement is divided into three input states: not moving, turn in place, and moving.

The module performs player-specific collision decisions on top of the object-event collision engine, including live-object collisions, directional metatile collision, ledge jumping, bike-specific collision paths, surfable/fishable-water checks, and camera-tracked movement restrictions.

Movement helpers expose walking/running speeds, water-current movement, speed-4 Debug movement, facing, turning, ledge jumps and Acro Bike wheelie/hop transitions.

## Avatar transitions

The player transition layer covers normal/on-foot, Mach Bike, Acro Bike, Surfing, Underwater and return-to-field restoration. It selects the appropriate graphics/state representation and keeps the live player ObjectEvent synchronized with the avatar state.

## Surf, field effects and Strength

The module includes policy and transition helpers for party Surf availability, north-facing Surf state, surfable/fishable water in front of the player, Surf state transitions, Strength/boulder bump tasks, Secret Base jump/spin-mat tasks, and the field-effect transition that clears Surfing state and restores on-foot state.

## Fishing state machine

Fishing is implemented as a **16-state task state machine** (`Fishing1` through `Fishing16`). It covers field-control lock, fishing animation, timed dot rounds, bite/no-bite decisions, reaction timing, hook success/failure messages, graphics/Surf-offset restoration, wild-encounter start and cleanup.

`AlignFishingAnimationFrames` is the final common Retail function. In Debug it is followed by the two Debug-only movement functions described above.

## Source-correlated function inventory

The connected source contains **147 explicit function definitions**, of which the final two are Debug-only. The `movement_type_empty_callback(MovementType_Player)` macro additionally emits **two common functions** (`MovementType_Player` and its zero-return callback).

Profile totals are therefore:

- Retail: **147** source-correlated functions (145 common explicit + 2 macro-generated)
- Debug: **149** source-correlated functions (147 explicit + 2 macro-generated)

Historical `sub_805xxxx`-style names are semantic correlation labels only.

## Next-module anchor

`event_object_movement` begins immediately afterward:

- Retail Rev 0 / Rev 1: **0x0805AD90**
- Debug: **0x0805F348**
- accumulated delta: **+0x45B8**

Its first function is source-correlated as `ClearObjectEvent`. The first 32-byte German function body independently anchors the boundary by:

1. preserving the object pointer;
2. calling `memset(object, 0, 0x24)` — exactly the ObjectEvent size;
3. storing player/undefined sentinels in `localId`, `mapNum`, `mapGroup`;
4. storing `0xFF` in `movementActionId`;
5. returning.

Stable prefix before the profile-specific `memset` branch:

`10 B5 04 1C 00 21 24 22`

Invariant suffix:

`FF 20 20 72 01 20 40 42 60 72 A0 72 20 77 10 BC 01 BC 00 47`

This closes `field_player_avatar` and establishes `event_object_movement` without copying an address from another decompilation.
