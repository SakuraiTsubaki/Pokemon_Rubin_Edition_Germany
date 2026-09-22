# German metatile_behavior module

The complete `metatile_behavior` text module has been bounded directly in the supplied German Retail Rev 0, Retail Rev 1 and Debug ROMs.

## Module boundary

| Profile | Start | End exclusive | Size | SHA-256 |
| --- | --- | --- | ---: | --- |
| Retail Rev 0 / Rev 1 | 0x080570DC | 0x08057CFC | **3,104 bytes (0xC20)** | 59c48f4631b4be59d63f8e5c72ace080955549f44bf7bda668cf08bd5ea8846f |
| Debug | 0x0805B5C4 | 0x0805C1E4 | **3,104 bytes (0xC20)** | d51e8243f9f4f8711253eeca9927b2d6be617a54d449865804470aba03f526bd |

Retail Rev 0 and Rev 1 are byte-identical across the entire module. Debug contains no additional `metatile_behavior` code. The accumulated Retail-to-Debug displacement is **+0x44E8** at both entry and exit.

The different Retail / Debug module hashes are explained by relocated literal references, not by added predicates.

## Entry anchor

The first function is `MetatileBehavior_IsATile` and its complete Thumb body is:

`01 20 70 47`

That is the four-byte leaf `return TRUE` already used to close the preceding `fieldmap` module.

The next function, `MetatileBehavior_IsEncounterTile`, indexes the behavior-attribute byte table and tests bit 0.

## Behavior attribute table

`MetatileBehavior_IsEncounterTile` contains a ROM literal pointing to the profile-specific copy of the same 240-byte (`0xF0`) attribute table:

| Profile | Table address | Size | SHA-256 |
| --- | --- | ---: | --- |
| Retail Rev 0 / Rev 1 | 0x08314614 | 240 bytes | cf25f69a32000022fe10be1c2fc9efec780d830e8eb0d6fe205cb4feb0d1badb |
| Debug | 0x0832D7BC | 240 bytes | cf25f69a32000022fe10be1c2fc9efec780d830e8eb0d6fe205cb4feb0d1badb |

The table entries use only the low three bits:

- bit 0 (`0x01`): wild-encounter capable
- bit 1 (`0x02`): surfable
- bit 2 (`0x04`): traversable/unused legacy attribute retained by the original table

The table covers metatile behavior IDs `0x00..0xEF`.

## Predicate layer

This module is a policy/query layer over the one-byte behavior value extracted by `fieldmap`. It does not own map geometry. It classifies behavior values into movement, interaction, encounter and special-map categories.

The connected source is used only to correlate semantic function names. The German ROM defines the addresses, lengths and fingerprints.

The source-correlated function inventory contains **131 functions**. Representative groups include:

- encounter / terrain: grass, sand, ice, water, puddles, ash grass, footprints;
- warps / doors: animated/non-animated doors, ladders, arrow warps, escalators;
- forced movement: currents, slides, directional walk tiles, jump tiles;
- collision policy: north/south/east/west blocked prdicates;
- bridge / log / rail classifications;
- Secret Base surfaces and decorations;
- special Hoenn interactions such as PC, TV, region map, roulette and Pokeblock feeder;
- shelf / vase / trash can / blueprint interaction tiles.

Historical function names from reference source are semantic labels only. Their embedded `sub_805xxxx`-style numbers, when present elsewhere in the source tree, are never treated as German addresses.

## Tail anchor

The final seven source-correlated predicates are single-value checks for behavior IDs `0xE0..0xE6`:

- `MetatileBehavior_IsPictureBookShelf` (`0xE0`)
- `MetatileBehavior_IsBookShelf` (`0xE1`)
- `MetatileBehavior_IsPokeCenterBookShelf` (`0xE2`)
- `MetatileBehavior_IsVase` (`0xE3`)
- `MetatileBehavior_IsTrashCan` (`0xE4`)
- `MetatileBehavior_IsShopShelf` (`0xE5`)
- `MetatileBehavior_IsBlueprint` (`0xE6`)

In the German binaries these seven 20-byte predicate bodies occur consecutively. The `0xE6` predicate ends exactly at the module end-exclusive address.

## Next module

`field_camera` begins immediately after `metatile_behavior`:

- Retail: **0x08057CFC**
 Debug: **0x0805C1E4**
- accumulated delta: **+0x44E8**

Its first 16 bytes are identical in Retail and Debug:

`00 21 81 70 C1 70 01 70 41 70 01 21 01 71 70 47`

This is the first camera-offset initialization helper: it zeros the four tile/pixel offset bytes, sets the copy-to-VRAM flag, and returns. It is an indepent binary anchor for the `metatile_behavior` end boundary.
