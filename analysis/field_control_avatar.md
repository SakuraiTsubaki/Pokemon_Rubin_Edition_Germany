# German field_control_avatar module

The complete `field_control_avatar` text module has been bounded directly in the supplied German Retail Rev 0, Retail Rev 1 and Debug ROMs.

## Module boundary

| Profile | Start | End exclusive | Size | SHA-256 |
| --- | --- | --- | ---: | --- |
| Retail Rev 0 / Rev 1 | 0x0806822C | 0x08069370 | **4,420 bytes (0x1144)** | `24d30b6e9f0e240d2f9836789b64db8ff68502ad5130e61b0858e4ae5ec26d5b` |
| Debug | 0x0806C82C | 0x0806DA4C | **4,640 bytes (0x1220)** | `e7cfd157fdd22d2de76d97f1c66c5721fdef4eccee7d05548f8f611c74cbe27f` |

Retail Rev 0 and Rev 1 are byte-identical across the complete module.

Debug is **220 bytes (0xDC)** larger. The accumulated Retail-to-Debug text displacement changes from **+0x4600** at module entry to **+0x46DC** at the following `event_data` module.

## Entry anchor

The first function is source-correlated as `ClearPlayerFieldInput`. Its complete German body is identical in all three profiles:

`30 B5 02 21 49 42 03 23 5B 42 05 24 64 42 09 25 6D 42 00 22 02 70 42 78 11 40 19 40 21 40 29 40 41 70 00 21 81 70 30 BC 01 BC 00 47`

It clears the defined field-input flags and direction state while preserving unspecified bits in the packed input bytes.

## Debug growth

Connected source contains five `#if DEBUG` regions, all inside the input collection and input processing path rather than separate Debug-only functions.

Source-correlated Debug behavior includes:

- R + Start conversion into a Debug input flag;
- Debug-working-mode R handling that suppresses ordinary step/wild-encounter processing and exposes a Select shortcut;
- an L-button Debug input flag;
- direct dive-warp processing;
- bypass of trainer/frame-script checks in the Debug movement mode;
- Debug menu actions from the extra input flags.

The German binary proves only the aggregate module growth of **0xDC**; this project does not invent a byte split for individual source conditionals.

## FieldInput policy

The source-correlated `FieldInput` record is four bytes of packed buttons/state plus direction/padding. This module translates raw new/held keys and player movement state into field actions:

- A/B/Start/Select input;
- D-pad direction;
- tile-step completion;
- standard wild-encounter eligibility;
- forced-movement suppression;
- interaction, warp and registered-key-item dispatch.

The input layer consumes player movement state from `field_player_avatar` and metatile behavior from `fieldmap` / `metatile_behavior`.

## Field action order

`ProcessPlayerFieldInput` source correlation shows the gameplay-priority chain:

1. Debug-only dive shortcut when enabled;
2. trainer detection;
3. frame map scripts;
4. B-button dive emerge;
5. step-based processing;
6. standard wild encounter;
7. arrow/conditional warp logic;
8. front-facing interaction;
9. door/inside warp consideration;
10. A-button dive down;
11. Start menu;
12. registered key item;
13. Debug-only field/debug menus.

This order matters because successful earlier actions prevent later actions from running during the same field-input pass.

## Interaction and map events

The module resolves front-facing interaction through object events, background events, metatile scripts and water interaction scripts. It also handles counter interactions, hidden/background events, Secret Base surfaces, PCs, shelves and other behavior-driven interactions.

Map-position lookups subtract the established **MAP_OFFSET = 7** before matching warp, coordinate and background-event records stored in map-local coordinates.

## Step-based field systems

The step path integrates:

- game step statistics;
- coordinate event scripts;
- warp events;
- cracked-floor holes;
- happiness steps;
- poison steps;
- egg hatching;
- Safari Zone step handling;
- S.S. Tidal step handling;
- Repel decrement/update;
- standard wild encounters with a short post-battle immunity window.

The wild-encounter immunity counter counts up from zero to four steps before normal encounter testing resumes.

## Warp layer

The module resolves warp events by map position/elevation and distinguishes ordinary warp doors, ladders, escalators and special Hoenn warp behaviors. Dive emerge/down logic uses map type and metatile behavior together.

The same `MAP_OFFSET = 7` coordinate conversion used by the field grid is preserved here.

## Tail anchor

The final source-correlated function is `SetCableClubWarp`. The final literal pool contains the profile-specific `gMapHeader` address:

- Retail Rev 0 / Rev 1: **0x0202E828**
- Debug: **0x0202EACC**

These four bytes belong to `field_control_avatar` and are included in the module boundary.

A preliminary Debug end candidate at `0x0806DA48` was rejected before commit because the four bytes there are this final `gMapHeader` literal. The binary-verified Debug end is **0x0806DA4C**.

## Next-module anchor

`event_data` begins immediately afterward:

- Retail Rev 0 / Rev 1: **0x08069370**
- Debug: **0x0806DA4C**
- accumulated delta: **+0x46DC**

Its first function is source-correlated as `InitEventData`. The common first 12 bytes are:

`10 B5 0C 4C 90 22 52 00 20 1C 00 21`

The function performs three clears, the last of which is the 16-byte temporary special-event flag buffer. The corresponding final literal is:

- Retail: **0x0202E8E2**
- Debug: **0x0202EB86**

This independently anchors the `field_control_avatar` → `event_data` transition.
