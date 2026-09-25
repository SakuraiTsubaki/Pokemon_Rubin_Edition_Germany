# German kagaya_debug_menu module

`kagaya_debug_menu` is a Debug-only source module. It is absent from Retail Rev 0 / Rev 1 and has been bounded directly in the German Debug ROM.

## Boundary

- Debug: **0x080B05C4..0x080B082C**
- size: **0x268 = 616 bytes**
- SHA-256: `4c12dd142520ba4092d845b622771c5b5ab31988d606746c06b8af8fb9a34526`

The connected source contains 13 explicit functions and is globally `#if DEBUG`.

## Entry

The first function is `InitKagayaDebugMenu_A`:

`00 B5 00 F0 03 F8 00 20 02 BC 08 47`

It initializes the Kagaya Debug menu and returns FALSE.

The module exposes Debug actions for trainer-card viewing, exchange-card viewing, slot machine startup, fishing/surf-related field effects, Fly map entry and Dive warp testing.

## Tail

The final function is `debug_sub_80B0800`:

- **0x080B0800..0x080B082C**
- size **0x2C**
- SHA-256 `60a1c0b773316494820caa986f65f8ee90c0b6c609bde4275e496e8aa32dcc28`

It closes the menu, checks for a Dive warp, fills field-effect arguments and launches field effect 0x2C when valid.

## Rejoin at mail_data

Retail reaches `mail_data` directly after `fldeff_cut`:

- Retail `mail_data`: **0x080A2C68**

Debug reaches `mail_data` after this Debug-only module:

- Debug `mail_data`: **0x080B082C**

Therefore the accumulated Retail-to-Debug displacement at `mail_data` entry is **+0xDBC4**.

Both profiles begin `ClearMailData` with the same prefix:

`30 B5 00 24 07 4D E0 00 00 19 80 00 40 19 00 F0 0B F8`
