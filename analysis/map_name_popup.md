# German map_name_popup module

The complete `map_name_popup` text module has been bounded directly in the German Retail Rev 0, Retail Rev 1 and Debug ROMs.

## Boundary

| Profile | Start | End exclusive | Size | SHA-256 |
| --- | --- | --- | ---: | --- |
| Retail Rev 0 / Rev 1 | 0x080A3094 | 0x080A3268 | **468 bytes (0x1D4)** | `b217476853bbcbe13fc7cd03a6e2fa7d3e11a8da30591a3307bb4f16d010f3f0` |
| Debug | 0x080B0C58 | 0x080B0E2C | **468 bytes (0x1D4)** | `db6295fd772da9c7c31d1be82d8b6aa1c2ff72010af3b050169327a963554de6` |

Retail Rev 0 and Rev 1 are byte-identical. Debug adds no module text, so the accumulated Retail-to-Debug displacement remains **+0xDBC4**.

## Runtime scope

The source-correlated module contains **5 functions** and no Debug-only code:

1. `unref_sub_80A2F44`
2. `ShowMapNamePopup`
3. `Task_MapNamePopup`
4. `HideMapNamePopup`
5. `DrawMapNamePopup`

It manages the small field map-name banner: task creation, slide-in, 120-frame hold, slide-out, redraw requests, BG0 vertical offset, and map-section-name rendering.

## Entry

Retail entry bytes:

`00 B5 CE F7 51 FF 00 F0 03 F8 01 20 02 BC 08 47`

Debug has the same call/return shape with relocated BL instructions. The function closes the menu, shows the map-name popup and returns TRUE.

## Tail

The final function is `DrawMapNamePopup`.

- Retail: **0x080A3230..0x080A3268**
- Debug: **0x080B0DF4..0x080B0E2C**
- size: **0x38 bytes**

The final literal is the profile-specific `gMapHeader` address:

- Retail: **0x0202E828**
- Debug: **0x0202EACC**

The function loads the standard frame graphics, obtains the current region-map-section name, draws the 13x3 window and centers the map name.

## Next module

`item_menu` begins immediately afterward:

- Retail: **0x080A3268**
- Debug: **0x080B0E2C**
- delta: **+0xDBC4**

The first function is source-correlated as `sub_80A3118`. It calls, in order, sprite animation, OAM building, task execution, the bag-specific per-frame helper and palette-fade update, then returns.

Retail first-function bytes:

`00 B5 5D F7 2D FB 5D F7 51 FB D7 F7 97 FE 04 F0 71 F9 D0 F7 3F FE 01 BC 00 47 00 00`

Debug has the identical function shape with relocated branch encodings.
