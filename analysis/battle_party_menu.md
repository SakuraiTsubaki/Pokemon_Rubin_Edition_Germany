# German battle_party_menu module

The complete `battle_party_menu` text module has been bounded directly in the German Retail Rev 0, Retail Rev 1 and Debug ROMs.

## Boundary

- Retail Rev 0 / Rev 1: **0x08094A78..0x08095A54**, size **0xFDC = 4,060 bytes**, SHA-256 `02680c6402ce257154810b6eaef7d672e22e8f55a1df1edc23052fce4287a776`
- Debug: **0x080A1FC8..0x080A2FA4**, size **0xFDC**, SHA-256 `1c48bbe28aa8b11afb25bed72bd5df2648ed6ad6bc1fb4765a0f330002c428a7`
- Retail Rev 0 and Rev 1 are byte-identical.
- no Debug-only text; delta remains **+0xD550**.

## Runtime scope

The source-correlated module contains **31 explicit functions** and no Debug-only code.

It handles:
- battle-party ordering;
- link/double-battle party slot mapping;
- party-menu opening from battle;
- switch/summary/cancel popup actions;
- unable-to-switch / fainted / egg / already-selected messages;
- party order swapping;
- summary-screen return and battle-screen restoration.

## Entry

The first function is source-correlated as `unref_sub_8094928`.

Common prefix:

`00 B5 03 49 03 4A`

It copies the global Pokémon storage structure into the supplied destination. The following function copies it back.

## Tail

The final function is `Task_BattlePartyMenuCancel`.

- Retail: **0x08095A14..0x08095A54**, size 0x40, SHA-256 `d2e230758f9d51fd25a3a448409cd19025d2e854b0cb8337ff60be58f3c3326d`
- Debug: **0x080A2F64..0x080A2FA4**, size 0x40, SHA-256 `dab4185229433a7fc779b1077bf0a065875f376db753ecc19ebcae13f7c39959`

It destroys the cursor, closes the party popup, restores task state, redraws the prompt and switches to the follow-up task function.

## Next

`unk_text_8095904` begins immediately afterward:

- Retail: **0x08095A54**
- Debug: **0x080A2FA4**
- delta: **+0xD550**

The first function is source-correlated as `sub_8095904`.

Common first 32 bytes:

`F0 B5 57 46 4E 46 45 46 E0 B4 87 B0 00 90 0F 1C 14 1C 0F 98 24 06 24 0E 1B 04 1B 0C 01 93 00 06`
