# German pokemon_icon module

The complete `pokemon_icon` text module has been bounded directly in the German Retail Rev 0, Retail Rev 1 and Debug ROMs.

## Boundary

- Retail Rev 0 / Rev 1: **0x0809D3C0..0x0809D998**, size **0x5D8 = 1,496 bytes**, SHA-256 `2fd41d5d628f62c828a537eea74fce8d51a105d30752d920aca70ca01571de63`
- Debug: **0x080AAC04..0x080AB1DC**, size **0x5D8**, SHA-256 `c347fc84c44cde896ad7c0238c9f46c959596747c70b0990f83667962632ae9f`
- Retail Rev 0 and Rev 1 are byte-identical.
- no Debug-only text; delta remains **+0xD844**.

## Runtime scope

The source-correlated module contains **18 explicit functions** and no Debug-only code.

It implements:
- Pokémon icon sprite creation;
- Unown letter selection by personality;
- icon/species conversion;
- mon icon palette loading/freeing;
- icon frame animation;
- generic icon sprite create/destroy;
- party HP-bar sprite setup.

## Entry

The first function is source-correlated as `unref_sub_809D26C`.

Common prefix:

`70 B5 46 46 40 B4 86 B0 1E 1C 0B 9B 00 04 00 0C 1B 06 1B 0E E8 46 17 4C`

It builds a Pokémon icon sprite template from species icon/palette data, creates the sprite and advances the initial frame.

## Next module

`pokemon_summary_screen` begins immediately afterward:

- Retail: **0x0809D998**
- Debug: **0x080AB1DC**
- delta: **+0xD844**

The first function is `sub_809D844`.

Retail begins with the four ordinary per-frame calls:

`00 B5 DD F7 03 FB 62 F7 93 FF 62 F7 B7 FF D6 F7 A9 FA 01 BC 00 47`

Debug begins with an enlarged stack frame and the same runtime calls, followed by the source-correlated link-receive Debug display path. Therefore the next module is expected to change the accumulated Retail/Debug delta.
