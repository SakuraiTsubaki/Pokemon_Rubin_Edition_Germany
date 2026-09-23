# German trainer_card module

The complete `trainer_card` text module has been bounded directly in the supplied German Retail Rev 0, Retail Rev 1 and Debug ROMs.

## Boundary

- Retail Rev 0 / Rev 1: **0x08093260..0x08094710**, size **0x14B0 = 5,296 bytes**, SHA-256 `914172d616e63504c6322025b7e281bf630fe89fdfe5d6d170c44394b95ff1d1`
- Debug: **0x080A0694..0x080A1C60**, size **0x15CC = 5,580 bytes**, SHA-256 `c52635154eecab15c54d75afeda752b5469de06a2bdcae02c347ee52483ac4cf`
- Retail Rev 0 and Rev 1 are byte-identical.
- Debug grows by **0x11C bytes**.
- accumulated displacement changes **+0xD434 -> +0xD550**.

## Entry

The first function is source-correlated as `TrainerCard_ShowPlayerCard`.

Retail function:
- **0x08093260..0x08093280**
- size 0x20
- SHA-256 `5bc1d1cf3feb483055aa791271efcab80062d6dd88a75701f05884b72d98bd93`

Debug function:
- **0x080A0694..0x080A06BC**
- size 0x28
- SHA-256 `7c0a82805f04003cf13014acbe6aeacfcaca14c9e1b4fd019c9a10962d826577`

The Debug build adds a clear of the trainer-card Debug flag before ordinary setup. German language ID **5** is written to the card runtime structure.

## Link-card entry

`TrainerCard_ShowLinkCard` also contains Debug instrumentation:

- Retail: **0x08093280..0x080932C4**, size 0x44, SHA-256 `ff902a462973abb6f5960b120ab287f2cc2f9a4be3ea23d0e34e7d37992f44b8`
- Debug: **0x080A06BC..0x080A0710**, size 0x54, SHA-256 `d1c78797ef4063380c330215a2ca1376cb4e2eabeef98529b93d1bd4fdd7ce6d`

Growth: **0x10 bytes**.

## Debug-only trainer-card test functions

Three dedicated Debug functions follow:

- `debug_sub_80A0710`: **0x080A0710..0x080A073C**, 0x2C, SHA-256 `8f528e340a14ea981588f8f5c9432f011e6d2a21e0dd5faa9b5688746b883696`
- `debug_sub_80A073C`: **0x080A073C..0x080A0780**, 0x44, SHA-256 `ef2a3c703f49824838ca426f494cdd001903b8f0b1be9e949010450acf92e158`
- `debug_sub_80A0780`: **0x080A0780..0x080A07A8**, 0x28, SHA-256 `ac51fa79059dfd66ceb364c9408e65e5181b65b5f1ad8384276db535549dfc5f`

These total **0x98 bytes**.

Together with the ShowPlayerCard **+0x08** and ShowLinkCard **+0x10** instrumentation, the early Debug growth is **0xB0 bytes**.

The remaining **0x6C bytes** of Debug growth occur in three source-guarded common-code paths:
- forcing all trainer-card record/flag sections visible in Debug;
- R-button star-count cycling and palette/star refresh;
- bypassing ordinary Pokédex-label suppression while Debug trainer-card mode is active.

## Runtime scope

The source-correlated file contains **84 explicit functions including the three Debug-only test functions**.

It implements:
- player and link trainer-card setup;
- card data gathering and star calculation;
- badge ownership and card-section visibility;
- front/back card state machine;
- card flip animation and HBlank scaling;
- trainer graphics/tilemap/palette setup;
- money, Pokédex, play time, Hall of Fame and link records;
- easy-chat phrase rendering;
- German trainer-card name formatting.

## Tail

The final function is source-correlated as `unref_sub_8094588`.

- Retail: **0x080946D8..0x08094710**, size 0x38, SHA-256 `3b6bd699d5cb5173691d9705a313c7717e50e4fe45650a5386b85c3b4742f8d9`
- Debug: **0x080A1C28..0x080A1C60**, size 0x38, SHA-256 `f931a40fb2767b7e2213f725b98520c9a744140b5909f67b54579d9c13b0de1c`

It selects the BOY/GIRL text from the saved player gender and prints it at the requested coordinates.

## Next: save_menu_util

`save_menu_util` starts immediately afterward:

- Retail: **0x08094710**
- Debug: **0x080A1C60**
- delta: **+0xD550**

The first function is source-correlated as `HandleDrawSaveWindowInfo`.

Common first 24 bytes:

`70 B5 00 04 05 0C 09 04 0C 0C 0C 26 00 F0 B6 F8 00 06 00 28 00 D0 0D 26`

It selects save-window width 12/13, tests whether the Pokédex flag is present, and draws the appropriate save-information layout.
