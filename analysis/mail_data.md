# German mail_data module

The complete `mail_data` text module has been bounded directly in the German Retail Rev 0, Retail Rev 1 and Debug ROMs.

## Boundary

- Retail Rev 0 / Rev 1: **0x080A2C68..0x080A3094**, size **0x42C = 1,068 bytes**, SHA-256 `d1f7c56133c3f2cfaf49ca8e2563296e1d0d23c109e832aa5a8ed6fa520e25f7`
- Debug: **0x080B082C..0x080B0C58**, size **0x42C**, SHA-256 `4cae863753115f6685058df5d06f329b1c58d1d70dc3a047500794c19b066855`
- Retail Rev 0 and Rev 1 are byte-identical.
- no Debug-only text; delta remains **+0xDBC4**.

## Runtime scope

The source-correlated module contains **12 explicit functions** and no Debug-only code.

It implements the save-mail layer:
- clearing all 16 mail slots;
- clearing an individual mail struct;
- checking whether a Pokémon owns mail;
- giving/removing/copying mail;
- mapping Unown personality forms into the mail-species encoding;
- identifying the 12 mail items.

Mail slots 0..5 are used for party Pokémon; 6..15 are available for transferring mail away from a Pokémon.

## Entry

The first function is `ClearMailData`.

Common prefix:

`30 B5 00 24 07 4D E0 00 00 19 80 00 40 19 00 F0 0B F8`

It iterates all 16 save mail records and clears each via `ClearMailStruct`.

## Tail

The final function is `ItemIsMail`.

- Retail: **0x080A307C..0x080A3094**
- Debug: **0x080B0C40..0x080B0C58**
- size **0x18**
- byte-identical across profiles
- SHA-256 `c95417e6a9324955274a945c1465d4e64bc47b5fa59d79522d36d3f260fffa1f`

It recognizes the contiguous Ruby mail-item ID range.

## Next module

`map_name_popup` begins immediately afterward:

- Retail: **0x080A3094**
- Debug: **0x080B0C58**
- delta: **+0xDBC4**

The first function is source-correlated as `unref_sub_80A2F44`.

Retail bytes:

`00 B5 CE F7 51 FF 00 F0 03 F8 01 20 02 BC 08 47`

Debug has the same function shape with a relocated call. It closes the menu, shows the map-name popup and returns TRUE.
