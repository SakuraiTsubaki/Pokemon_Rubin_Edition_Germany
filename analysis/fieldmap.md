# German fieldmap module

The complete `fieldmap` text module has been bounded directly in the supplied German Retail Rev 0, Retail Rev 1 and Debug ROMs.

## Module boundary

| Profile | Start | End exclusive | Size | SHA-256 |
| --- | --- | --- | ---: | --- |
| Retail Rev 0 / Rev 1 | 0x080562D0 | 0x080570DC | **3,596 bytes (0xE0C)** | 437e6883063d29a9c67acba6402374456c7e3da2067129e483fbee6ed4b0b7f5 |
| Debug | 0x0805A7B8 | 0x0805B5C4 | **3,596 bytes (0xE0C)** | 710a595e8e0b1594e27d27812fbc91fd480ecf538041ff855fbb2d5f9139b000 |

Retail Rev 0 and Rev 1 are byte-identical across the complete module. Debug contains no additional `fieldmap` code: the module length is identical and the accumulated Retail-to-Debug displacement remains **+0x44E8** from entry through the next module boundary.

The different full-module hashes are caused by relocated references / branch displacements in the Debug image, not by extra fieldmap functions.

## Boundary fingerprints

`fieldmap` begins with `GetMapHeaderFromConnection`.

The first eight bytes are identical in Retail and Debug:

`00 B5 02 7A 41 7A 10 1C`

This reads the connection map group / map number fields before the profile-specific branch displacement to the map-header lookup.

The following module begins immediately at the end-exclusive address in both profiles:

`01 20 70 47`

which is the complete Thumb body of `MetatileBehavior_IsATile` (`return TRUE`). This independently anchors the `fieldmap` end and the `metatile_behavior` start.

## Map grid word

Each backup/current map cell is a 16-bit word:

- bits 0..9: metatile ID (`0x03FF`)
- bits 10..11: collision (`0x0C00`)
- bits 12..15: elevation (`0xF000`)

The fieldmap layer therefore preserves tile identity, collision class and elevation in one `u16` cell. These masks are exposed in `include/german_ruby/fieldmap.h` for later map conversion and compatibility work.

## Metatile attributes

The fieldmap routines resolve a map cell to metatile attributes through the active primary / secondary tilesets.

The confirmed attribute fields are:

- bits 0..7: metatile behavior
- bits 12..15: layer type

Primary metatile IDs occupy the first 512 entries; secondary metatile IDs are resolved against the secondary tileset after the primary range. The map model therefore exposes **512 primary + 512 secondary** metatile slots.

## MapLayout ABI

The confirmed layout order is:

1. width
2. height
3. border
4. map
5. primaryTileset
6. secondaryTileset

The corresponding GBA offsets are `0x00`, `0x04`, `0x08`, `0x0C`, `0x10`, `0x14`, with a `0x18`-byte layout record.

This is the runtime bridge from high-level `MapHeader` ownership in `overworld` to concrete map cells and tilesets in `fieldmap`.

## Backup map geometry

The runtime copies the current layout into a padded backup map used for camera movement and connection stitching.

Confirmed constants:

- `MAP_OFFSET = 7`
- extra backup width = 15 cells
- extra backup height = 14 cells
- `MAX_MAP_DATA_SIZE = 0x2800` `u16` cells

The asymmetry between extra width 15 and extra height 14 follows the original runtime buffer geometry; it is not normalized in this project.

## Connections

The backup layout is extended with adjacent maps through the four cardinal connection directions:

- South
- North
- West
- East

Connection loading copies map strips into the padded backup layout so movement and rendering can cross a map boundary without replacing the entire runtime grid first.

`InitBackupMapLayoutConnections` retains the original null-dereference undefined-behavior path present in the German binary. The evidence layer documents that behavior rather than silently repairing it. A later development layer may wrap it safely, but compatibility mode must remain able to reproduce the Retail behavior.

## Tilesets and palettes

Confirmed runtime capacities:

- primary metatiles: 512
- secondary metatiles: 512
- primary palettes: 6
- total map palettes: 12

The fieldmap code copies / resolves primary and secondary tileset graphics and metatile data while keeping the original split between the two tileset domains.

## Role in the project

This module is the core compatibility layer for moving legacy maps into the GBA map model:

`MapHeader -> MapLayout -> Tileset -> metatile -> behavior -> connection`

For later Kanto / Johto work, terrain and events should be translated into this structure rather than represented as an unrelated custom map format. The German ROM remains the binary truth for the compatibility profile; higher-level development code may expose safer or more expressive APIs above it.

## Next module

`metatile_behavior` starts at:

- Retail: **0x080570DC**
- Debug: **0x0805B5C4**
- accumulated delta: **+0x44E8**

Its first function is `MetatileBehavior_IsATile`, whose complete body is `01 20 70 47` (`return TRUE`).
