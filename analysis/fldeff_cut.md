# German fldeff_cut module

The complete `fldeff_cut` text module has been bounded directly in the German Retail Rev 0, Retail Rev 1 and Debug ROMs.

## Boundary

- Retail Rev 0 / Rev 1: **0x080A2654..0x080A2C68**, size **0x614 = 1,556 bytes**, SHA-256 `6be9fdd17acaf4a027dfaa86910ed014dc98c1652e88518454fe51e0a004c548`
- Debug: **0x080AFEE4..0x080B05C4**, size **0x6E0 = 1,760 bytes**, SHA-256 `337c6fba9a54af29502dc2e62fcfa5e99ed0a24655c343e93ede974a0a94746d`
- Retail Rev 0 and Rev 1 are byte-identical.
- Debug growth: **0xCC bytes**
- accumulated delta: **+0xD890 → +0xD95C**

## Runtime scope

The source-correlated module implements the Cut field move on cuttable trees and 3x3 grass regions, including map metatile replacement, Cut grass sprites, field-effect setup and object/script unlock on completion.

## Debug growth

The sole Debug-only executable function is `Debug_SetUpFieldMove_Cut`.

- Debug: **0x080AFEE4..0x080AFFB0**
- size **0xCC**
- SHA-256 `daa2efebe8574e6b559ae418eb20884950d8d3a7519ae8c88617636fac1a906d`

It checks a cuttable tree or nearby grass directly, launches the corresponding Cut callback without the normal party-menu setup, and unlocks field controls if Cut is not valid.

The ordinary `SetUpFieldMove_Cut` follows immediately in Debug and is the Retail entry function.

## Tail

The final function is `StartCutTreeFieldEffect`.

- Retail: **0x080A2C50..0x080A2C68**, size 0x18, SHA-256 `7efe7b605c208fa906fb0fab38e7dcfdbbbc761e07271e0ee6fc3c0ebd8f92e2`
- Debug: **0x080B05AC..0x080B05C4**, size 0x18, SHA-256 `357678a73b9bbe53f16963c07c5047f266afe9da96d3e5ef85033ee6f342beb7`

It plays the Cut sound, removes the Cut-on-tree field effect from the active list and re-enables script execution.

## Next modules

The next executable source differs by profile.

Retail skips the globally DEBUG-guarded Kagaya menu and begins `mail_data`:

- Retail start **0x080A2C68**
- first function `ClearMailData`
- prefix `30 B5 00 24 07 4D E0 00 00 19 80 00 40 19 00 F0 0B F8`

Debug begins `kagaya_debug_menu`:

- Debug start **0x080B05C4**
- first function `InitKagayaDebugMenu_A`
- bytes `00 B5 00 F0 03 F8 00 20 02 BC 08 47`

The different post-module targets are expected and are recorded separately.
