# German coord_event_weather module

The complete `coord_event_weather` text module has been bounded directly in the supplied German Retail Rev 0, Retail Rev 1 and Debug ROMs.

## Module boundary

| Profile | Start | End exclusive | Size | SHA-256 |
| --- | --- | --- | ---: | --- |
| Retail Rev 0 / Rev 1 | 0x080696AC | 0x0806977C | **208 bytes (0xD0)** | `1feb1b8af8896d001a06e5ee56afc0c1241e27be57db500b24719aacb1a097ac` |
| Debug | 0x0806DD88 | 0x0806DE58 | **208 bytes (0xD0)** | `67d18d6dff683b8e4a2720e65b6a8157ade01b3deaaed66013778f292b26ac3b` |

Retail Rev 0 and Rev 1 are byte-identical across the complete module. Debug adds no module text, so the accumulated Retail-to-Debug displacement remains **+0x46DC**.

## Weather wrapper anchor

The module opens with 13 compact wrappers, each loading an internal weather ID and calling `SetWeather`.

Each wrapper is 12 bytes:

`00 B5 <weather-id> 20 ...BL SetWeather... 01 BC 00 47`

Binary order of the IDs is:

`1, 2, 3, 4, 5, 6, 9, 7, 8, 11, 12, 20, 21`

Source-correlated meanings:

1. Clouds
2. Sunny
3. Light Rain
4. Snow
5. medium rain / thunderstorm
6. Fog 1
9. Fog 2 / diagonal fog
7. Ash
8. Sandstorm
11. Shade / Dark
12. Drought
20. Route 119 cycle
21. Route 123 cycle

The command/event weather IDs used by map coordinate events are mapped to these internal weather IDs by the dispatch table; the two ID domains are intentionally not treated as identical.

## Dispatcher

The final function is source-correlated as `DoCoordEventWeather`. It scans a 13-entry table of coordinate-event weather selectors and function pointers. If a selector matches, it calls the corresponding weather wrapper and returns.

No Debug-only source section exists in this module, consistent with the identical code size.

## Next-module anchor

`field_tasks` begins immediately afterward:

- Retail Rev 0 / Rev 1: **0x0806977C**
- Debug: **0x0806DE58**
- accumulated delta: **+0x46DC**

The first function is source-correlated as `Task_RunPerStepCallback`. Its first 28 bytes, before the profile-specific branch displacement, are identical:

`00 B5 00 06 00 0E 07 4A 81 00 09 18 C9 00 89 18 08 22 89 5E 04 4A 89 00 89 18 09 68`

It reads the per-step callback index from the task and dispatches through the callback table. This independently anchors the weather-module end.
