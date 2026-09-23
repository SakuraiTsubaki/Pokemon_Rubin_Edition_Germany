# German trainer_see module

The complete `trainer_see` text module has been bounded directly in the supplied German Retail Rev 0, Retail Rev 1 and Debug ROMs.

## Module boundary

| Profile | Start | End exclusive | Size | SHA-256 |
| --- | --- | --- | ---: | --- |
| Retail Rev 0 / Rev 1 | 0x08084410 | 0x08084DCC | **2,492 bytes (0x9BC)** | `47081b39ac7750874dc7441a768a4053b922dc7445d5b605e578062863d79b18` |
| Debug | 0x0809177C | 0x08092138 | **2,492 bytes (0x9BC)** | `ce5879427fd13bf636c31ee85ccbc4f8f06c5dac625e81177c0a4bf532a7c748` |

Retail Rev 0 and Rev 1 are byte-identical across the complete module. Debug adds no `trainer_see` text, so the accumulated Retail-to-Debug displacement remains **+0xD36C** from entry through exit.

## Entry anchor

The first function is source-correlated as `CheckTrainers`.

Common first 32 bytes:

`30 B5 00 24 0A 4D E0 00 00 19 80 00 41 19 08 78 C0 07 00 28 0E D0 C8 79 01 28 01 D0 03 28 09 D1`

It scans up to **16 object-event slots**, checks active trainer objects, filters by trainer type and calls the per-trainer sight test.

## Trainer sight and approach model

The source-correlated module contains **30 explicit functions** and no Debug-only text.

It provides:

- four directional approach-distance helpers: south, north, west and east;
- sight-range and collision-path validation;
- trainer battle desire/approach task creation;
- a **12-entry** main trainer-approach state-function table;
- a **4-entry** reveal/pop-out follow-up table;
- player/trainer facing and held-movement transitions;
- buried-trainer reveal handling;
- trainer approach task teardown;
- exclamation-mark, question-mark and heart field-effect sprites.

Historical numeric labels are semantic correlation only; the German addresses below come from the supplied German binaries.

## Field-effect icon tail

The final two functions are source-correlated as `sub_8084894` and `objc_exclamation_mark_probably`.

`sub_8084894`:

- Retail: **0x08084CE8..0x08084D34**
- Debug: **0x08092054..0x080920A0**
- size: **0x4C**

`objc_exclamation_mark_probably`:

- Retail: **0x08084D34..0x08084DCC**
- Debug: **0x080920A0..0x08092138**
- size: **0x98**
- Retail SHA-256: `cfb42c98e9a778414924ecd58ee3107c724f6a2b64d3b56e5a3293bc93678792`
- Debug SHA-256: `b17fc9ff4c4876e0024eee1759cd0adefbb711d949738d19ba7b316fb53f8553`

The callback tracks the owning object-event sprite, stops the field effect if the object disappears or animation ends, otherwise follows the object sprite and applies the short vertical bounce.

## Next-module anchor

`wild_encounter` begins immediately afterward:

- Retail Rev 0 / Rev 1: **0x08084DCC**
- Debug: **0x08092138**
- accumulated delta: **+0xD36C**

The first function is source-correlated as `DisableWildEncounters`:

`01 49 08 70 70 47 00 00`

The following literal is the profile-specific `gWildEncountersDisabled` byte:

- Retail: **0x0202FF7C**
- Debug: **0x02030228**

That literal provides an independent boundary anchor for the transition into `wild_encounter`.
