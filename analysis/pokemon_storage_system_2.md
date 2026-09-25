# German pokemon_storage_system_2 module

The complete second Pokémon storage-system text module has been bounded directly in the German Retail Rev 0, Retail Rev 1 and Debug ROMs.

## Boundary

| Profile | Start | End exclusive | Size | SHA-256 |
| --- | --- | --- | ---: | --- |
| Retail Rev 0 / Rev 1 | 0x08096908 | 0x08098C90 | **9,096 bytes (0x2388)** | `eeef7c2b7e2abc0fcae65e71e5ba650b1894a6bf6043df93d5c6ae1cf557dd58` |
| Debug | 0x080A3FB4 | 0x080A6498 | **9,444 bytes (0x24E4)** | `2c576e8a2aba3aa8a7b2d6972656ac485cfa2e5e730bc4036d80e555bb7a6f0b` |

Retail Rev 0 and Rev 1 are byte-identical. Debug adds **0x15C bytes**, changing the accumulated Retail-to-Debug displacement from **+0xD6AC** to **+0xD808**.

## Entry

The first function is `task_intro_29`.

Common prefix:

`00 B5 00 06 00 0E 04 49 08 70 04 49 48 71 04 48`

It records the selected storage mode and installs the storage-system initialization callback.

The following `sub_80967DC` clears all BG horizontal/vertical offsets and independently confirms the module start.

## Runtime scope

The source-correlated module contains **65 explicit functions including three Debug-only functions**.

It implements the main storage-system screen/runtime:

- storage-screen boot and return paths;
- VBlank/main callbacks;
- box/party cursor movement;
- Pokémon selection, pickup, drop, swap and release;
- summary-screen transitions;
- box scrolling and wallpaper changes;
- party/box sprite rendering;
- action text;
- yes/no menus;
- storage action command dispatch.

German-specific storage text formatting is preserved, including the German release-message path.

## Debug growth

Direct Debug-only functions:

- `debug_sub_80A4300`: **0x080A4300..0x080A433C**, size 0x3C, SHA-256 `0984327cafb08159a22d50312193b0bf4f3c346d670889585e9298c468268eb2`
- `debug_sub_80A433C`: **0x080A433C..0x080A435C**, size 0x20, SHA-256 `b2a54853b5c67a97b7d32f80134f952bc3b7b9c8f9ad261e8c1857f022f8beb9`
- `debug_sub_80A435C`: **0x080A435C..0x080A43B4**, size 0x58, SHA-256 `6b58e42c5765e0913697b2d9487df7d0f117bce422012527ac29f537d55a4264`

Direct Debug functions total **0xB4 bytes**.

The remaining **0xA8 bytes** of module growth are in ordinary functions under source `#if DEBUG` guards: Debug storage state reset, Debug break paths and the extra Debug action case. No per-site byte split is invented beyond this aggregate binary-proven remainder.

## Tail

The final function is `sub_8098AA8`.

- Retail: **0x08098BFC..0x08098C90**, size 0x94, SHA-256 `bed1d08334439e11ea3b8287b38dfba8c658a35ffc88c995512eb5e43189c211`
- Debug: **0x080A6404..0x080A6498**, size 0x94, SHA-256 `2c92985e8adb8fe066085b9e0c1593dacc4065cc89e00d42d82bad0232c33cdf`

It selects one of four groups of storage action strings and refreshes the action text layer.

## Next module

`pokemon_storage_system_3` starts immediately afterward:

- Retail: **0x08098C90**
- Debug: **0x080A6498**
- delta: **+0xD808**

The first function is `get_preferred_box`:

`01 48 00 78 70 47 00 00`

The following literal is the profile-specific `gPokemonStorage.currentBox` address.
