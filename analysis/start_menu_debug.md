# German debug/start_menu_debug module

This module is present only in the German Debug profile. Retail Rev 0 and Rev 1 contribute no text from `src/debug/start_menu_debug.c`.

## Module boundary

| Profile | Start | End exclusive | Size | SHA-256 |
| --- | --- | --- | ---: | --- |
| Retail Rev 0 / Rev 1 | — | — | **0 bytes** | — |
| Debug | 0x08076AC8 | 0x080791A8 | **9,952 bytes (0x26E0)** | `8e40baceb26a68d08faf009bdf0b4c64bd2aa7e8424d05304c684eb8293ec627` |

The accumulated Retail-to-Debug text displacement therefore changes from **+0x4B8C** at the Debug module entry point to **+0x726C** when both profiles rejoin at `menu`.

## Entry anchor

The first function is source-correlated as `debug_sub_8076AC8`.

First 32 bytes:

`10 B5 82 B0 00 06 00 0E 1B 4A 81 00 09 18 49 00 1A 48 09 18 11 60 00 24 08 78 FF 28 04 D0 01 34`

This is a genuine Debug-only implementation layer, not a Retail function relocated into Debug.

## Runtime scope

The connected source contains **172 explicit Debug functions**. The module includes the main developer/debug menu system and tools for:

- developer-specific submenus;
- teleport and field-start/continue controls;
- encounter controls;
- Pokémon creation/editing/graphics views;
- trainer, battle, Safari, Hall of Fame and Battle Tower diagnostics;
- RTC/time records and time editing;
- Pokédex/National Dex helpers;
- berry, Pokéblock, weather and cell information;
- flash/save/debug hardware diagnostics;
- random-number and backup tests;
- German/Japanese/European debug text/font inspection paths.

This module is intentionally kept separate from ordinary `start_menu` because it exists only in the Debug ROM.

## Tail anchor

The final function is source-correlated as `DebugMenu_OpenKiwa` for this non-English Debug profile.

German Debug range:

- **0x0807918C..0x080791A8**
- size: **0x1C**
- SHA-256: `ec317a686616260b61ce4133187dc72d6bcbcb0d35cf554d98fef4cddc07caf5`

## Rejoin with Retail: menu

After this Debug-only module, both profiles reach the ordinary `menu` module.

- Retail `menu` start: **0x08071F3C**
- Debug `menu` start: **0x080791A8**
- accumulated delta: **+0x726C**

The first function is `CloseMenu`.

Retail begins:

`00 B5 05 20 03 F0 88 FC`

Debug begins:

`00 B5 05 20 03 F0 88 FC`

The first eight bytes are identical. The function then erases the menu, unfreezes object events, unlocks player field controls and destroys the menu cursor.
