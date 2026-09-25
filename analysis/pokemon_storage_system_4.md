# German pokemon_storage_system_4 module

The complete fourth Pokémon storage-system text module has been bounded directly in the German Retail Rev 0, Retail Rev 1 and Debug ROMs.

## Boundary

- Retail Rev 0 / Rev 1: **0x08099D4C..0x0809D3C0**, size **0x3674 = 13,940 bytes**, SHA-256 `fa563c2968cda273f355dbe20f353a7456a6248c35153e669e141f850c023440`
- Debug: **0x080A7554..0x080AAC04**, size **0x36B0 = 14,000 bytes**, SHA-256 `2aa8bc2a89eb92b52cab450eb6c9760b5ffe20c3b78f598960c72a1ba446aebd`
- Retail Rev 0 and Rev 1 are byte-identical.
- Debug growth: **0x3C bytes**
- accumulated delta: **+0xD808 → +0xD844**

## Runtime scope

This module contains the largest storage-system UI/data layer: box wallpaper loading and scrolling, box cursor movement, held/placed/shifted Pokémon state, marking/release/action menus, menu text construction, storage copy/fill helpers and queued tile-copy operations.

## Debug growth

The direct Debug-only function is `debug_sub_80AA40C`:

- **0x080AA40C..0x080AA434**
- size **0x28**
- SHA-256 `5d048de796db4afffef269f327ceb12176906d75266abf00fdbce48077d202b0`

The remaining **0x14 bytes** are the source-guarded Debug branch in `sub_809CAB0`, which diverts to the Debug action-menu builder when the Debug storage flag is active.

Together: **0x28 + 0x14 = 0x3C**.

## Tail

The final function is source-correlated as `sub_809D1C4`.

- Retail: **0x0809D318..0x0809D3C0**
- Debug: **0x080AAB5C..0x080AAC04**
- size **0xA8**
- byte-identical across profiles
- SHA-256 `d24bb1809f5e43ee4ef1bedad792a0dd54f8f37e21d2d4452564550db20ae012`

It performs the queued large 16-bit DMA fill across the configured rectangular tile region.

## Next module

`pokemon_icon` begins immediately afterward:

- Retail: **0x0809D3C0**
- Debug: **0x080AAC04**
- delta: **+0xD844**

The first function is source-correlated as `unref_sub_809D26C`.

Common prefix:

`70 B5 46 46 40 B4 86 B0 1E 1C 0B 9B 00 04 00 0C 1B 06 1B 0E E8 46 17 4C`

It builds a Pokémon icon sprite template from the species icon table and palette index, creates the icon sprite and advances its animation frame.
