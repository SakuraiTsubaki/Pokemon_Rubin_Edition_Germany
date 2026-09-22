# German tileset_anim module

The complete `tileset_anim` text module has been bounded directly in the supplied German Retail Rev 0, Retail Rev 1 and Debug ROMs.

## Module boundary

| Profile | Start | End exclusive | Size | SHA-256 |
| --- | --- | --- | ---: | --- |
| Retail Rev 0 / Rev 1 | 0x080731B8 | 0x08073DD4 | **3,100 bytes (0xC1C)** | `7011b493762e4c0d139d5131f086d25f350b721c508af6e1c703821d68a54ae3` |
| Debug | 0x0807A424 | 0x0807B040 | **3,100 bytes (0xC1C)** | `f784aeb3924ed7c71106fdc69fc74202927ba96547673242fd4c76981f8393b9` |

Retail Rev 0 and Rev 1 are byte-identical across the complete module. Debug adds no `tileset_anim` text, so the accumulated Retail-to-Debug displacement remains **+0x726C**.

## DMA queue entry

The first function is `ClearTilesetAnimDmas`.

Stable code prefix:

`00 B5 81 B0 06 49 00 20 08 70 00 20 00 90 05 49 05 4A 68 46`

It clears the queue count and zero-fills the 20-entry tileset-animation DMA array.

Profile-specific runtime addresses:

- queue count: Retail **0x030006C0**, Debug **0x030006E0**
- DMA request array: Retail **0x0202E9D8**, Debug **0x0202EC7C**
- queue capacity: **20**

Each source-correlated DMA entry stores source pointer, destination pointer and transfer size.

## Animation runtime

The module owns primary and secondary tileset animation state:

- frame counters and animation lengths;
- primary/secondary callback pointers;
- queued DMA transfer requests;
- callback reset/start/update paths;
- General/Building primary tileset animation callbacks;
- secondary-map animation callbacks for Hoenn locations and interiors.

The connected source contains **63 explicit function definitions** and no Debug-only text.

## Map/graphics integration

Animation callbacks do not replace map metatile logic. They periodically copy animated 4bpp tile frames into the BG character/tile graphics destinations used by the active primary or secondary tileset.

This directly complements the already mapped chain:

`MapLayout -> Tileset -> metatile -> field_camera`

by supplying frame updates for animated tile graphics while preserving the same map/metatile identities.

## Tail anchor

The final function is source-correlated as `sub_80739EC`. Its final literal pool includes:

- source frame pointer
- BG tile destination **0x06007E00**

Those literals belong to `tileset_anim` and are included through end-exclusive **0x08073DD4 / 0x0807B040**.

## Next-module anchor

`palette` begins immediately afterward:

- Retail Rev 0 / Rev 1: **0x08073DD4**
- Debug: **0x0807B040**
- accumulated delta: **+0x726C**

The first function is `LoadCompressedPalette`. Its stable setup begins:

`70 B5 0C 1C 15 1C 24 04 24 0C 2D 04 0A 4E 31 1C`

It decompresses the palette to a work buffer, then copies the requested range into both unfaded and faded palette buffers. This independently anchors the module transition.
