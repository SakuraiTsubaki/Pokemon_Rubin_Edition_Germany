# German save_menu_util module

The complete `save_menu_util` text module has been bounded directly in the supplied German Retail Rev 0, Retail Rev 1 and Debug ROMs.

## Boundary

- Retail Rev 0 / Rev 1: **0x08094710..0x08094A78**, size **0x368 = 872 bytes**, SHA-256 `0a9d4d825cd91a353ea71b0efb13671f13106a4b9af8da1cdef58207bc38f13f`
- Debug: **0x080A1C60..0x080A1FC8**, size **0x368 = 872 bytes**, SHA-256 `bad9adc07eade99b078687abc0d749a8215e9dffccac1bb899d10f906ee943c8`
- Retail Rev 0 and Rev 1 are byte-identical.
- Debug adds no text; accumulated displacement remains **+0xD550**.

## Runtime scope

The source-correlated module contains **10 explicit functions** and no Debug-only code.

It provides:
- save-window drawing/closing;
- player/map/badge/Pokédex/play-time display;
- badge counting;
- Pokédex seen counting;
- play-time string formatting.

The save window selects width 12 or 13 and includes the Pokédex row only when the system Pokédex flag is set.

## Tail: FormatPlayTime

- Retail: **0x08094A34..0x08094A78**
- Debug: **0x080A1F84..0x080A1FC8**
- size **0x44**
- Retail SHA-256: `d612081b2b477c5d3de1379d5e13ccbbd79b6684352d04f422e6664c0c7e1bfc`
- Debug SHA-256: `c2f9f543aa71125de78cc00f46c0351d375482b6afb0f380c0f1dd81e1202e8f`

It converts hours, writes either the colon character **0xF0** or zero between hours/minutes, then writes two-digit minutes.

## Next: battle_party_menu

`battle_party_menu` begins immediately afterward:

- Retail: **0x08094A78**
- Debug: **0x080A1FC8**
- delta: **+0xD550**

The first function is source-correlated as `unref_sub_8094928`.

Common structural entry:

`00 B5 03 49 03 4A`

It copies the global Pokémon storage structure into the caller-provided destination.
