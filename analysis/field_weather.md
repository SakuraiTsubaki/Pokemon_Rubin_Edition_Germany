# German field_weather module

The complete `field_weather` text module has been bounded directly in the supplied German Retail Rev 0, Retail Rev 1 and Debug ROMs.

## Module boundary

| Profile | Start | End exclusive | Size | SHA-256 |
| --- | --- | --- | ---: | --- |
| Retail Rev 0 / Rev 1 | 0x0807CC5C | 0x0807E2AC | **5,712 bytes (0x1650)** | `65ba9a03483a5b4582d2484bb26c8993ed8ce9d2f1eae56cb9b37ebc4b173cf8` |
| Debug | 0x08083F14 | 0x08085660 | **5,964 bytes (0x174C)** | `e45bd520d56f26c9f5eac43dabde70ad7146e9182b06ff8929ea3dcae846e9c7` |

Retail Rev 0 and Rev 1 are byte-identical across the complete module.

Debug adds exactly **0xFC bytes**. The accumulated Retail-to-Debug text displacement changes from **+0x72B8** at module entry to **+0x73B4** at module exit.

## Entry anchor

The first function is source-correlated as `StartWeather`.

All profiles begin:

`70 B5 30 48`

After the profile-specific branch instruction, all profiles share:

`00 06 06 0E 00 2E 55 D1 90 20 40 01`

The function checks whether the weather main task is already active, allocates the weather sprite palettes, copies the weather palette, builds gamma-shift tables, resets weather sprite/runtime counters, initializes blend coefficients and creates the weather-init task.

## Runtime weather model

The source-correlated module owns the central weather state machine and palette processing.

It includes:

- current/next weather switching;
- weather-init and weather-main tasks;
- 15 weather callback slots;
- four weather-palette states;
- gamma-shift table generation and application;
- fade-in/fade-out integration;
- fog palette lightening;
- drought palette decompression/loading;
- weather blend coefficient control;
- rain sound-strength tracking;
- current weather queries;
- palette preservation/reset.

The source contains **48 explicit function definitions including the two Debug-only functions**.

## Weather callback table

The 15 source-correlated weather callback slots are:

0. none
1. clouds
2. sunny/weather2
3. light rain
4. snow
5. medium rain
6. fog 1
7. ash
8. sandstorm
9. fog 2
10. fog 3 / fog 1 callbacks
11. shade
12. drought
13. heavy rain
14. bubbles

The palette-state dispatch has four states: changing weather, screen fading in, screen fading out and idle.

## Debug-only weather menu

The Retail build ends after `ResetPreservedPalettesInWeather`.

The Debug build then appends exactly two functions:

### debug_sub_8085564

- Debug: **0x08085564..0x0808560C**
- size **0xA8**
- SHA-256 `ea49cdc926960635156453ff66e6fac79ac6f1b5dbc41994efd220211925950b`

Source correlation: R/L cycle the selected debug weather across 15 entries, menu text is refreshed on changes, and A applies the selected weather and closes the menu.

### debug_sub_808560C

- Debug: **0x0808560C..0x08085660**
- size **0x54**
- SHA-256 `75abe94de07942eec0e6b6998eb34861c6e62b9a609ff0b2a2d1620f20bd63a8`

Source correlation: initializes the selection from the current weather, clears/prepares the debug menu window, displays the selected weather text and installs the first function as the menu callback.

The sizes account for all Debug growth:

**0xA8 + 0x54 = 0xFC**

## Last common Retail function

The last non-Debug function is source-correlated as `ResetPreservedPalettesInWeather`.

| Profile | Start | End exclusive | Size | SHA-256 |
| --- | --- | --- | ---: | --- |
| Retail Rev 0 / Rev 1 | 0x0807E29C | 0x0807E2AC | 0x10 | `e9e2e88b835b73156afabff9d07d55285bc3a039572b43a6825791769ad2c33a` |
| Debug common copy | 0x08085554 | 0x08085564 | 0x10 | `d0b6eb4feccd7aaa7170c0bb881baeaf364dd397f1640b40f516c2fd8e80e141` |

The code restores the palette-gamma-type pointer to the base palette-gamma table. Its literal pool is included in the function range.

## Next-module anchor

`field_weather_effects` begins immediately afterward:

- Retail Rev 0 / Rev 1: **0x0807E2AC**
- Debug: **0x08085660**
- accumulated delta: **+0x73B4**

The first function is source-correlated as `Clouds_InitVars`.

Common prefix:

`00 B5 0D 48 00 68 0D 4A 81 18 00 22 0A 70 0C 49 43 18 14 21 19 70 0B 4B C1 18 0A 70 06 3B C1 18 0A 80 09 49 40 18 00 78 00 28 03 D1 00 20 10 21`

It resets cloud-weather gamma/init state and, when cloud sprites are not already present, initializes blend coefficients. This independently anchors the `field_weather` end.
