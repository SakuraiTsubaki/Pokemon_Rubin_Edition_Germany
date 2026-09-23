# German option_menu module

The complete `option_menu` text module has been bounded directly in the supplied German Retail Rev 0, Retail Rev 1 and Debug ROMs.

## Module boundary

- Retail Rev 0 / Rev 1: **0x0808BA64..0x0808C430**, size **0x9CC = 2508 bytes**, SHA-256 `1efa501a7455ed6c5fe575bb962f9ac8ecb94717bd872f704d5027819d3a8614`
- Debug: **0x08098E98..0x08099864**, size **0x9CC = 2508 bytes**, SHA-256 `673d41e14bbbe9d80e8f473de6b7209a1cdec157cac0b4b64e2152ce12ea7b5c`
- Retail Rev 0 and Rev 1 are byte-identical.
- Debug adds no text; accumulated Retail-to-Debug displacement remains **+0xD434**.

## Entry

The first function is source-correlated as `MainCB`. It runs tasks, animates sprites, builds OAM and updates the palette fade once per frame.

Retail bytes:

`00 B5 EF F7 9D FA 74 F7 2D FF 74 F7 51 FF E8 F7 43 FA 01 BC 00 47`

Debug bytes differ only in relocated branch targets.

## Runtime scope

The source-correlated module contains **21 explicit functions** and no Debug-only code. It implements:

- option-menu initialization and callbacks;
- text-speed selection;
- battle-scene selection;
- battle-style selection;
- mono/stereo sound selection;
- frame-type selection;
- button-mode selection;
- save-back to SaveBlock2 and fade-out return.

German-specific source layout values include:

- text-speed choice X positions: **120 / 161 / 202**
- battle-style SET X position: **178**
- German frame-type string construction into a 16-byte local text buffer.

These are semantic/source correlations; module addresses come from German ROM evidence.

## Tail

The final function is source-correlated as `ButtonMode_DrawChoices`.

- Retail: **0x0808C3DC..0x0808C430**
- Debug: **0x08099810..0x08099864**
- size: **0x54**
- Retail SHA-256: `4cfcde4898d967ad8f61dc3d80b0a112988c24064b2576923640ad2d50604667`
- Debug SHA-256: `dba036b2229f5ddc91e2f854f3b67d6a96d7070a8d7c90813d352d9ec764ac0e`

It draws NORMAL, LR and LA at X positions 120, 166 and 188.

## Next-module anchor

`pokedex` begins immediately afterward:

- Retail: **0x0808C430**
- Debug: **0x08099864**
- delta: **+0xD434**

The first function is source-correlated as `ResetPokedex`.

Common first 36 bytes:

`70 B5 16 48 00 21 01 80 15 4A 40 20 10 70 15 48 01 70 15 4C 00 20 61 76 21 76 A1 76 E1 76 E0 61 20 62 60 62`

The reset loop ends with:

`48 1C 00 04 01 0C 33 29 F2 D9`

The immediate **0x33** confirms 52 Pokédex flag bytes (`DEX_FLAGS_NO = 52`) in the German Ruby build.
