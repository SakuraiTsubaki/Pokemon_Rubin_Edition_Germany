# German pokedex module

The complete `pokedex` text module has been bounded directly in the supplied German Retail Rev 0, Retail Rev 1 and Debug ROMs.

## Boundary

- Retail Rev 0 / Rev 1: **0x0808C430..0x08093260**, size **0x6E30 = 28,208 bytes**, SHA-256 `6e9cb760626238d323e52e2e7e273e108d3231c4a7aa03a1d93da7721bbf94f9`
- Debug: **0x08099864..0x080A0694**, size **0x6E30 = 28,208 bytes**, SHA-256 `adfc0aa3861ad4c0f5269d0ed3193cdaae58a7cf026c704bc381d826683fec62`
- Retail Rev 0 and Rev 1 are byte-identical.
- Debug adds no Pokédex text; accumulated displacement remains **+0xD434**.

## Entry: ResetPokedex

Common first 36 bytes:

`70 B5 16 48 00 21 01 80 15 4A 40 20 10 70 15 48 01 70 15 4C 00 20 61 76 21 76 A1 76 E1 76 E0 61 20 62 60 62`

The reset loop terminates with:

`48 1C 00 04 01 0C 33 29 F2 D9`

The `cmp #0x33` loop bound verifies **52 bytes** of Pokédex owned/seen flags, matching `POKEMON_SLOTS_NUMBER = 412` and `DEX_FLAGS_NO = 52`.

## Runtime scope

The source-correlated module contains **131 explicit functions** and no Debug-only code.

It implements the complete Pokédex runtime:

- Pokédex reset and scroll-position reset;
- Hoenn/National list generation and sorting;
- seen/owned counting;
- list scrolling and Pokémon sprite movement;
- entry information pages;
- area, cry and size screens;
- search-menu loading and interaction;
- name/color/type/mode/order search parameters;
- search result generation and ordering;
- BG highlight and search-parameter boxes;
- animated search scroll arrows.

German ROM boundaries and hashes are binary evidence; source names are semantic correlation only.

## Tail

The final function is source-correlated as `CreateSearchParameterScrollArrows`.

- Retail: **0x080931DC..0x08093260**
- Debug: **0x080A0610..0x080A0694**
- size **0x84**
- Retail SHA-256: `f92c2f9f66b399e72a99f1ebe646d4348cbde9d87b0cd6881750c479f14f1dc3`
- Debug SHA-256: `ac30dd4644022b708eaef9615e3057a11637b3941c5ff66f84535b0c44795e0a`

Common first 24 bytes:

`70 B5 4E 46 45 46 60 B4 05 1C 2D 06 2D 0E 1A 4E 30 1C B8 21 04 22 00 23`

It creates the up/down search-parameter arrow sprites, stores the controlling task ID and direction and flips the lower arrow vertically.

## Next: trainer_card

`trainer_card` begins immediately afterward:

- Retail: **0x08093260**
- Debug: **0x080A0694**
- entry delta: **+0xD434**

Retail starts directly with source-correlated `TrainerCard_ShowPlayerCard`:

`00 B5 00 F0 CB F8 04 48 6D F7 4A F9 03 48 9C 30 05 21 01 70 01 BC 00 47`

The final store writes German language ID **5** to the trainer-card runtime structure.

Debug starts the same function with an additional Debug-state clear before the ordinary initialization:

`00 B5 07 4A 00 21 11 70 00 F0 20 F9`

This confirms the Pokédex end while also showing that `trainer_card` itself will grow in Debug.
