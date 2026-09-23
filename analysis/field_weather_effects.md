# German field_weather_effects module

The complete `field_weather_effects` text module has been bounded directly in the supplied German Retail Rev 0, Retail Rev 1 and Debug ROMs.

## Module boundary

| Profile | Start | End exclusive | Size | SHA-256 |
| --- | --- | --- | ---: | --- |
| Retail Rev 0 / Rev 1 | 0x0807E2AC | 0x08080CA8 | **10,748 bytes (0x29FC)** | `98060a9865c5cb3ff0063d8a0690b12597ccf7f14faafefaff17c9aa954920e1` |
| Debug | 0x08085660 | 0x0808805C | **10,748 bytes (0x29FC)** | `f6f8ba11e0c8e6d356c26ef7a053d68785e2699933f06176d6fdc76f8ee68780` |

Retail Rev 0 and Rev 1 are byte-identical across the complete module. The connected source has no Debug-only text in this module, matching the binary result: accumulated Retail-to-Debug displacement remains **+0x73B4** at entry and exit.

## Entry anchor

The first function is source-correlated as `Clouds_InitVars`.

Common first 48 bytes:

`00 B5 0D 48 00 68 0D 4A 81 18 00 22 0A 70 0C 49 43 18 14 21 19 70 0B 4B C1 18 0A 70 06 3B C1 18 0A 80 09 49 40 18 00 78 00 28 03 D1 00 20 10 21`

It resets cloud-weather gamma/init state and, if cloud sprites are not already active, initializes the cloud blend coefficients.

## Runtime scope

The connected source contains **101 explicit functions** and no `#if DEBUG` code.

The module implements the visual/runtime side of the field-weather system, including:

- cloud sprite creation, movement, blending and cleanup;
- drought palette loading and drought visual progression;
- light/medium/heavy rain sprites, splash timing and rain transitions;
- snowflake creation/motion;
- fog 1/fog 2 sprite creation, affine/blend behavior and cleanup;
- volcanic ash;
- sandstorm sprite layers and motion;
- shade;
- underwater/bubble weather;
- save-block weather storage and translation;
- Route 119 and Route 123 four-stage weather cycles;
- per-day weather-cycle advancement;
- rain-exposure game-stat updates.

Historical numeric function labels are semantic identifiers only; all addresses in this file are German-ROM evidence values.

## Tail

The final three source-correlated operations are:

1. `TranslateWeatherNum`
2. `UpdateWeatherPerDay`
3. `UpdateRainCounter`

`UpdateWeatherPerDay` advances the save-block weather-cycle stage modulo 4.

`UpdateRainCounter` is the final function:

- Retail Rev 0 / Rev 1: **0x08080C88..0x08080CA8**
- Debug: **0x0808803C..0x0808805C**
- size: **0x20 bytes**

SHA-256:

- Retail: `12e8879d7e0e70c121609d1eb1833fc782eea64c2f4eb6e7c4a1a0b45367780f`
- Debug: `d247f4096e91cced24bf183ffc36cd1f94794531c676df80e46ad7eab01b9ac4`

The source semantics increment the rain-exposure game statistic only when the weather actually changes into light or medium rain.

## Next-module anchor

`field_fadetransition` begins immediately afterward:

- Retail Rev 0 / Rev 1: **0x08080CA8**
- Debug: **0x0808805C**
- accumulated delta: **+0x73B4**

The first function is source-correlated as `palette_bg_fill_white`.

It occupies:

- Retail: **0x08080CA8..0x08080CCC**
- Debug: **0x0808805C..0x08088080**
- size: **0x24 bytes**

It prepares the duplicated white value `0x7FFF7FFF`, targets the profile-specific faded palette buffer, and fills `0x400` bytes.

The immediately following `palette_bg_fill_black` begins at Retail **0x08080CCC** / Debug **0x08088080** and uses the same palette-buffer/size literals with a zero fill value. This white/black pair strongly anchors the module transition.
