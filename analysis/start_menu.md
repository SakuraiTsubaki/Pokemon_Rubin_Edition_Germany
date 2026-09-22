# German start_menu module

The complete `start_menu` text module has been bounded directly in the supplied German Retail Rev 0, Retail Rev 1 and Debug ROMs.

## Module boundary

| Profile | Start | End exclusive | Size | SHA-256 |
| --- | --- | --- | ---: | --- |
| Retail Rev 0 / Rev 1 | 0x080712D0 | 0x08071F3C | **3,180 bytes (0xC6C)** | `0bd17feffa3874c6540ebb08928be1b9110dcf2c6960f6e4eccc6caf0a710a58` |
| Debug | 0x08075C30 | 0x08076AC8 | **3,740 bytes (0xE98)** | `7e26e68bee12d4aa582c831bf90b6b87b4e2df21119b308409607e7dc31e4d0f` |

Retail Rev 0 and Rev 1 are byte-identical across the complete module.

Debug is **560 bytes (0x22C)** larger. The accumulated Retail-to-Debug displacement changes from **+0x4960** at module entry to **+0x4B8C** at module exit.

## Profile-specific entry

Retail compilation starts directly with the common `BuildStartMenuActions` function:

`00 B5 05 48 00 21 01 70 E3 F7 9E F9`

Debug compilation begins with a Debug-only prefix before the common start-menu implementation:

`00 B5 03 F0 B9 FA 00 F0 B1 F8 01 20 02 BC 08 47`

The common `BuildStartMenuActions` body begins in Debug at **0x08075E5C**.

## Debug-only prefix

The Debug prefix is exactly **0x22C bytes**:

- start: **0x08075C30**
- end exclusive: **0x08075E5C**
- SHA-256: `69afdd1b92fc99c5287650915d4d422f107e77365c356bd1e9c934fb9e499bf6`

It consists of five functions:

| Function | Range | Size | SHA-256 |
| --- | --- | ---: | --- |
| `debug_sub_8075C30` | 0x08075C30..0x08075C40 | 0x10 | `fdc3517658f7a66b128155de08291e05ed35ca02c03c11abcee98c3e26e3a42f` |
| `debug_sub_8075C40` | 0x08075C40..0x08075D9C | 0x15C | `dfe24c9787a1d35cd9812b41d88f4c42e456f8600cce8421c3c1315fea1733e9` |
| `debug_sub_8075D9C` | 0x08075D9C..0x08075DB4 | 0x18 | `dcba1dd32bcd7ebd2f18b781ab6f1c52be503d4345e6ae3626f4932e47b183d2` |
| `debug_sub_8075DB4` | 0x08075DB4..0x08075E38 | 0x84 | `8ca7fd6db939a01b67f8f967df3ac6482d074f5e1aebf2dad7fc3ac73f9b9a31` |
| `unref_sub_8070F90` | 0x08075E38..0x08075E5C | 0x24 | `4007784d0fb970efb51a70324a3cd40b7035ebaf9a632dd7ddee31ae409320fc` |

The same `unref_sub_8070F90` behavior appeared as a Retail-only tail in `party_menu`; in Debug it is compiled here inside the start-menu Debug block. This source-layout quirk is preserved rather than normalized.

## Common body

The common body is exactly **0xC6C bytes** in both Retail and Debug.

It owns:

- construction of Normal/Safari/Link start-menu action lists;
- Safari Ball counter display;
- multistep start-menu initialization;
- menu task/input processing;
- Pokédex/Pokémon/Bag/PokéNav/player/save/options/exit/retire callbacks;
- save-dialog state machine;
- save overwrite/different-file handling;
- save success/error timeout and sound flow;
- the fade/secret-base save transition helper.

The source file contains **58 explicit function definitions** total:

- 53 common
- 5 Debug-only prefix functions

## Save-dialog policy

The save path distinguishes normal save, overwrite of a different save file and error states. It uses a callback-driven state machine and preserves the original timing/sound behavior.

The late `sub_80719FC` multistep initializer resets display/sprite/task/palette state, initializes the menu window and restores VBlank operation before the save-specific task takes over.

## Next-module split

The linker path differs by build profile immediately after `start_menu`.

### Retail

The separate `debug/start_menu_debug` object contributes no text when DEBUG is disabled. Therefore Retail goes directly to `menu`:

- `menu` Retail start: **0x08071F3C**
- first function: `CloseMenu`

Retail `CloseMenu` begins:

`00 B5 05 20 03 F0 88 FC`

and then calls the erase/unfreeze/unlock/cursor-destroy path.

### Debug

Debug proceeds to the separate `debug/start_menu_debug` module:

- Debug module start: **0x08076AC8**
- first function: `debug_sub_8076AC8`

Its first 16 bytes:

`10 B5 82 B0 00 06 00 0E 1B 4A 81 00 09 18 49 00`

Thus the `start_menu` end is independently anchored in both profiles even though the following module differs.
