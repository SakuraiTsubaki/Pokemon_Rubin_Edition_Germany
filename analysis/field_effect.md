# German field_effect module

The complete `field_effect` text module has been bounded directly in the supplied German Retail Rev 0, Retail Rev 1 and Debug ROMs.

## Module boundary

| Profile | Start | End exclusive | Size | SHA-256 |
| --- | --- | --- | ---: | --- |
| Retail Rev 0 / Rev 1 | 0x08085ABC | 0x080899CC | **16,144 bytes (0x3F10)** | `e418e172cdc0829670b913fdf38594527b10e679132790a06b6851fbc43281aa` |
| Debug | 0x08092E88 | 0x08096D98 | **16,144 bytes (0x3F10)** | `b7072798d60d961371bc0c636b19ae2afe6f00e950625f966666c4400eeb5bb3` |

Retail Rev 0 and Rev 1 are byte-identical across the complete module. Connected source contains no Debug-only text, matching the binary result: accumulated Retail-to-Debug displacement remains **+0xD3CC** at entry and exit.

## Entry anchor

The first function is source-correlated as `FieldEffectStart`.

Common prefix:

`30 B5 82 B0 04 1C 24 06 24 0E 20 1C`

The routine adds the effect ID to the active list, fetches its field-effect script and runs the script through the field-effect command table until the native/script sequence completes.

## Runtime scope

The connected source contains **210 explicit functions** and no Debug-only text.

The module is the main field-effect implementation layer and includes:

- field-effect script command interpreter;
- sprite-sheet/palette loading commands;
- active-effect list management;
- Poké Ball/Birch/monitor visual effects;
- healing-center and Hall-of-Fame monitor effects;
- field-move streaks;
- Surf/Waterfall/Dive-related effects;
- Strength and field-move preparation;
- ash/grass/footprint/ripple effects;
- shadow/reflection-related field visuals;
- Poké Ball glow/particle effects;
- Fly-out/Fly-in transition sprites/tasks;
- player-avatar state handoff and camera synchronization.

Historical numeric labels are semantic correlation only; German addresses come from the supplied German binaries.

## Tail anchor

The final function is source-correlated as `fishE`.

- Retail Rev 0 / Rev 1: **0x08089950..0x080899CC**
- Debug: **0x08096D1C..0x08096D98**
- size: **0x7C**

SHA-256:

- Retail: `863bbc7bc016752fa840645f1d4b41a06486dfd5f76f47fbe67235906cf662de`
- Debug: `f9f711a6e6face161e28afdddf007e5a1893985043b835c35597988b5039e942`

It completes the Fly-in task: restores the player graphics/state, removes the Fly-in active-field-effect bit and destroys the controlling task.

## Next-module anchor

`scanline_effect` begins immediately afterward:

- Retail Rev 0 / Rev 1: **0x080899CC**
- Debug: **0x08096D98**
- accumulated delta: **+0xD3CC**

The first function is source-correlated as `ScanlineEffect_Stop`.

Common first 34 bytes:

`10 B5 0B 4C 00 20 60 75 0A 49 4A 89 0A 48 10 40 48 81 4A 89 09 48 10 40 48 81 48 89 20 7E FF 28 03 D0`

It clears the scanline-effect state, stops DMA channel 0 and destroys the wave task if one is active.
