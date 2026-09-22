# German event_data module

The complete `event_data` text module has been bounded directly in the supplied German Retail Rev 0, Retail Rev 1 and Debug ROMs.

## Module boundary

| Profile | Start | End exclusive | Size | SHA-256 |
| --- | --- | --- | ---: | --- |
| Retail Rev 0 / Rev 1 | 0x08069370 | 0x080696A8 | **824 bytes (0x338)** | `c067fcbf7336ebb8130910c86cddbca42abb2afef909b13e32aedc453cebf315` |
| Debug | 0x0806DA4C | 0x0806DD84 | **824 bytes (0x338)** | `b9ca3102a2d1327456e53b525bf06ce062131f2a8331391cca7e478898effc8a` |

Retail Rev 0 and Rev 1 are byte-identical across the complete module. The connected source contains no Debug-only text, matching the binary result: the accumulated Retail-to-Debug displacement remains **+0x46DC** at entry and exit.

## Entry anchor

The first function is source-correlated as `InitEventData`. Its common first 12 bytes are:

`10 B5 0C 4C 90 22 52 00 20 1C 00 21`

The function clears three regions: the persistent flag array, the persistent variable array, and a 16-byte temporary event-flag buffer.

The final literal of this 0x3C-byte function is the profile-specific temporary buffer:

- Retail Rev 0 / Rev 1: **0x0202E8E2**
- Debug: **0x0202EB86**

## Runtime data model

The source-correlated event-data layer defines:

- 12 special variables `0x8000..0x800B`;
- `gSpecialVar_Result`;
- `gSpecialVar_LastTalked`;
- `gSpecialVar_Facing`;
- a 16-byte temporary special-event flag buffer.

Profile addresses for the final special-variable group are contiguous:

| Symbol | Retail | Debug |
| --- | --- | --- |
| `gSpecialVar_Result` | 0x0202E8DC | 0x0202EB80 |
| `gSpecialVar_LastTalked` | 0x0202E8DE | 0x0202EB82 |
| `gSpecialVar_Facing` | 0x0202E8E0 | 0x0202EB84 |
| temporary event buffer | 0x0202E8E2 | 0x0202EB86 |

These addresses are German-profile evidence values, not imported addresses from another ROM.

## Clear/reset constants

The source-correlated clear sizes are:

- temporary flags: **4 bytes**
- daily flags: **8 bytes**
- temporary vars: **0x20 bytes**
- temporary special-event buffer: **0x10 bytes**

The layer also owns enabling/disabling and verification for National Pokédex, Mystery Event and Reset RTC state.

## Variable API

The variable path distinguishes ordinary save variables from special variables. `GetVarPointer` returns NULL for IDs below the ordinary variable range, a save-block pointer for ordinary variables, and a special-variable pointer for the special range.

`VarGet` returns the ID itself when no variable pointer exists; `VarSet` reports failure in that case.

## Flag API

The flag path uses ordinary persistent save flags below the special threshold and the temporary 16-byte event buffer for high special flag IDs.

The module exposes set, clear and get operations, plus the temporary/daily clear routines used by map/session transitions.

## Source-correlated function inventory

The connected source contains **20 explicit functions** and no `#if DEBUG` text:

1. `InitEventData`
2. `ClearTempFieldEventData`
3. `ClearDailyFlags`
4. `DisableNationalPokedex`
5. `EnableNationalPokedex`
6. `IsNationalPokedexEnabled`
7. `DisableMysteryEvent`
8. `EnableMysteryEvent`
9. `IsMysteryEventEnabled`
10. `DisableResetRTC`
11. `EnableResetRTC`
12. `CanResetRTC`
13. `GetVarPointer`
14. `VarGet`
15. `VarSet`
16. `VarGetObjectEventGraphicsId`
17. `GetFlagPointer`
18. `FlagSet`
19. `FlagClear`
20. `FlagGet`

## Next-module anchor

`coord_event_weather` begins immediately afterward:

- Retail Rev 0 / Rev 1: **0x080696A8**
- Debug: **0x0806DD84**
- accumulated delta: **+0x46DC**

The next module begins with 13 compact weather-dispatch wrappers. Each wrapper has the form:

`00 B5 <weather-id> 20 ...BL SetWeather... 01 BC 00 47`

The first 13 source-correlated internal weather IDs, in binary order, are:

`1, 2, 3, 4, 5, 6, 9, 7, 8, 11, 12, 20, 21`

This sequence corresponds to Clouds, Sunny, Light Rain, Snow, medium rain/thunderstorm, Fog 1, Fog 2, Ash, Sandstorm, Shade/Dark, Drought, Route 119 cycle and Route 123 cycle. It provides a strong repeated boundary anchor for the end of `event_data`.
