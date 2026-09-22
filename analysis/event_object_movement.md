# German event_object_movement module

The complete `event_object_movement` text module has been bounded directly in the supplied German Retail Rev 0, Retail Rev 1 and Debug ROMs.

## Module boundary

| Profile | Start | End exclusive | Size | SHA-256 |
| --- | --- | --- | ---: | --- |
| Retail Rev 0 / Rev 1 | 0x0805AD90 | 0x08064DB4 | **40,996 bytes (0xA024)** | `5828818871f2779b9f5a9500c2c1c4b5ffc02a06e928e9c8e1de3aa1c0b2e6f5` |
| Debug | 0x0805F348 | 0x080693B4 | **41,068 bytes (0xA06C)** | `c7e94d987507ecc1dfee7ecfd442963054b5931d732be1fd2ef41f09e29a7609` |

Retail Rev 0 and Rev 1 are byte-identical across the complete module.

Debug is **72 bytes (0x48)** larger. The accumulated Retail-to-Debug displacement changes from **+0x45B8** at module entry to **+0x4600** at the following `field_message_box` module.

## Entry anchor: ClearObjectEvent

The first function is source-correlated as `ClearObjectEvent`. The first 32 bytes form an independent ABI anchor:

- preserve the ObjectEvent pointer;
- call `memset(object, 0, 0x24)`;
- write sentinel values to `localId`, `mapNum`, `mapGroup` and `movementActionId`;
- return.

The invariant prefix is:

`10 B5 04 1C 00 21 24 22`

The invariant suffix is:

`FF 20 20 72 01 20 40 42 60 72 A0 72 20 77 10 BC 01 BC 00 47`

The profile-specific BL to `memset` is deliberately not copied across profiles.

## Debug profile

Connected source has one Debug-only BSS counter, `gUnknown_Debug_03004BC0`, plus six Debug-only counter-update sites inside otherwise common functions:

1. reset after `ClearAllObjectEvents`;
2. increment after object-state initialization from a template;
3. decrement when removing an object event;
4. decrement when sprite creation fails;
5. reset before the bulk object-event reposition pass;
6. increment for each active object processed by that pass.

The BSS byte does not contribute to the text-module size. The six conditional code sites correlate with the binary-proven **0x48** Debug text growth. No guessed per-site byte split is recorded.

## ObjectEvent runtime model

The module operates on the **16 live ObjectEvent slots** already established elsewhere in the German project. Each ObjectEvent record is **0x24 bytes**.

It owns the low-level runtime lifecycle beneath `field_player_avatar`:

- clearing/resetting live object state;
- looking up object IDs by local ID/map/coordinates;
- initializing from map ObjectEventTemplate data;
- spawning/removing object-event sprites;
- dynamic graphics and palette selection;
- player object binding;
- camera-tracked object updates.

The higher-level player module chooses player movement policy; this module performs the generic live-object execution.

## Movement engine

The module contains the object-event movement dispatcher and the movement-action execution layer. Connected source contains **660 explicit function definitions**; additional movement callbacks/actions are emitted through macros and included data tables, so 660 is not treated as a total machine-function count.

The movement system includes:

- fixed-facing and look-around behaviors;
- wandering and ranged movement;
- back-and-forth paths;
- long movement sequences;
- copy-player movement families;
- disguise/hidden states;
- walk/jog/run-in-place behaviors;
- single/held movement actions;
- movement delay and animation state;
- coordinate stepping and mini-step helpers.

Historical numeric labels such as `sub_805xxxx` are semantic source names only and are never interpreted as German addresses.

## Collision and coordinates

Object-event collision checks combine:

- object-to-object occupancy;
- Z/elevation compatibility;
- map-grid metatile collision;
- directional impassability;
- movement ranges;
- current/previous/initial coordinates.

The coordinate helpers update movement direction and camera-relative positions while preserving the fieldmap collision/elevation model established by the preceding modules.

## Sprite, camera and visibility layer

The module owns the generic object-event sprite bridge:

- sprite template construction from ObjectEvent graphics info;
- dynamic graphics IDs and palette tags;
- object-event sprite creation/removal;
- camera object callbacks;
- subpriority by elevation;
- off-screen and visibility checks;
- reflection sprite support.

The source-correlated camera-object dispatch contains **3 camera object callbacks**.

## Ground effects and reflections

Ground effects are evaluated from the current/previous metatile behaviors and movement transitions. The source-correlated ground-effect dispatch contains **20 handlers**, covering:

- tall/long grass;
- water and ice reflections;
- flowing water;
- sand/deep-sand tracks;
- ripples and puddles;
- sand piles;
- jump splashes and landing dust;
- short grass;
- hot springs;
- seaweed/bubbles.

Covering effects can be filtered when disabled, and puddle effects are filtered for jump landings.

## Freeze / unfreeze policy

The module implements freezing and restoration of individual or all live object events. Frozen objects preserve and restore sprite animation/affine-animation pause state. The player ObjectEvent is excluded from the ordinary bulk-freeze pass where required.

## Mini-step primitives

The generic sprite mini-step layer has five source-correlated step profiles with lengths:

`16, 8, 6, 4, 2`

and corresponding 1/2/3/4/8-pixel step primitives. Jump helpers add Y-offset arcs above the base movement.

## Tail anchor

The final source-correlated function is `DoRippleFieldEffect`. Near the end of both German profiles it stores the ripple field-effect arguments, including constants **151**, **3**, and field-effect ID **5**. The verifier anchors the invariant byte sequence:

`97 20 90 60 03 20 D0 60 05 20`

inside the final 0x80 bytes of the module.

## Next module

`field_message_box` starts immediately afterward:

- Retail Rev 0 / Rev 1: **0x08064DB4**
- Debug: **0x080693B4**
- accumulated delta: **+0x4600**

The first function is `InitFieldMessageBox`. Its first 16 bytes are identical across all three German profiles:

`00 B5 06 49 00 20 08 70 05 48 00 88 00 F0 A2 FB`

This initializes the hidden message-box mode and begins text-window setup, independently anchoring the end of `event_object_movement`.
