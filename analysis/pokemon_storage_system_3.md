# German pokemon_storage_system_3 module

The complete third Pokémon storage-system text module has been bounded directly in the German Retail Rev 0, Retail Rev 1 and Debug ROMs.

## Boundary

- Retail Rev 0 / Rev 1: **0x08098C90..0x08099D4C**, size **0x10BC = 4,284 bytes**, SHA-256 `2b83265be47e0550f0cb19b77f1d254e64bdc4cf294c319058bbab1f54b4ef24`
- Debug: **0x080A6498..0x080A7554**, size **0x10BC**, SHA-256 `581caea6528b19ab4c8e36957f663fad9abeacc98ff3bd3fecc654cdd086d2a5`
- Retail Rev 0 and Rev 1 are byte-identical.
- no Debug-only text; accumulated delta remains **+0xD808**.

## Runtime scope

The source-correlated module contains **34 explicit functions** and no Debug-only code.

It owns Pokémon storage icon/runtime behavior:
- current/preferred box lookup;
- storage icon sprite reset;
- party and box icon spawning;
- box-column scrolling;
- held-mon icon handling;
- icon swaps and affine transitions;
- species icon graphics caching/reference counting;
- Unown personality icon conversion;
- mon-icon sprite teardown.

## Entry

The first function is `get_preferred_box`:

`01 48 00 78 70 47 00 00`

It returns the profile-specific `gPokemonStorage.currentBox` byte.

## Tail

The final function is `PSS_DestroyMonIconSprite`.

- Retail: **0x08099D34..0x08099D4C**, size 0x18, SHA-256 `8cb8b62d810194c7f33dc8c329a86cdfa8baedbf47e2ab46153e165ef036d0e5`
- Debug: **0x080A753C..0x080A7554**, size 0x18, SHA-256 `232695a9ce7115bd592a0169c77bd524eb5244d427c986325c1fa85d26e4ac24`

It decrements the cached species-icon graphics reference and destroys the sprite.

## Next module

`pokemon_storage_system_4` begins immediately afterward:

- Retail: **0x08099D4C**
- Debug: **0x080A7554**
- delta: **+0xD808**

The first function is source-correlated as `sub_8099BF8`.

Common prefix:

`10 B5 81 B0 04 1C 24 06 24 0E 13 48 00 68 13 49 42 18 00 21 11 70`

It resets box-wallpaper transition state, clears the BG2 screen buffer and initializes the selected box's wallpaper, icons and BG2 control.
