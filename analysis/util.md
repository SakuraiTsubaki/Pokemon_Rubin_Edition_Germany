# German util module

The complete `util` text module is mapped from the supplied German ROMs.

## Boundary

| Profile | Start | End exclusive | Size | SHA-256 |
| --- | --- | --- | ---: | --- |
| Retail Rev 0 / Rev 1 | 0x080411D8 | 0x08041534 | 860 bytes (0x35C) | 23eb87e96a7473038854c0f9edc982689d01efc389454663a1cd2d5a32419b96 |
| Debug | 0x08045354 | 0x080456B0 | 860 bytes (0x35C) | 7d86e6c9bd856b123c5b322d05da50efaeefd70d8b657bb36da5bbbe435ab35e |

Retail Rev 0 and Rev 1 are byte-identical. There is no Debug-only growth; all function starts remain at **+0x417C**.

## Function map

| Function | Retail | Debug | Span | Role |
| --- | --- | --- | ---: | --- |
| CreateInvisibleSpriteWithCallback | 0x080411D8 | 0x08045354 | 56 | create hidden sprite at (248,168), subpriority 14 and install callback |
| StoreWordInTwoHalfwords | 0x08041210 | 0x0804538C | 12 | store low/high halves of 32-bit word |
| LoadWordFromTwoHalfwords | 0x0804121C | 0x08045398 | 16 | reassemble 32-bit word from two halfwords |
| SetBgAffineStruct | 0x0804122C | 0x080453A8 | 44 | populate GBA affine-background source structure |
| DoBgAffineSet | 0x08041258 | 0x080453D4 | 76 | stack-create affine source data then call BIOS BgAffineSet |
| CopySpriteTiles | 0x080412A4 | 0x08045420 | 460 | copy 4bpp sprite tiles with X/Y flip handling |
| CountTrailingZeroBits | 0x08041470 | 0x080455EC | 40 | count trailing zero bits; zero input returns 0 |
| CalcCRC16 | 0x08041498 | 0x08045614 | 88 | bitwise CRC16 |
| CalcCRC16WithTable | 0x080414F0 | 0x0804566C | 68 | table-driven equivalent CRC16 |

## Invisible helper sprite

`CreateInvisibleSpriteWithCallback` creates a sprite from the common dummy template at coordinates **(248, 168)** with subpriority **14**, sets the invisible flag and replaces the callback.

This is a utility task/sprite anchor rather than a visible battle object.

## 32-bit packing helpers

`StoreWordInTwoHalfwords` stores a 32-bit word as low then high 16-bit halves.

`LoadWordFromTwoHalfwords` rebuilds the word using the original signed-high-half expression. At the bit level the stored 32-bit payload is preserved exactly.

## Background affine helpers

`SetBgAffineStruct` writes texX, texY, screen X/Y, scale X/Y and angle into the BIOS-compatible affine source structure.

`DoBgAffineSet` builds that structure on the stack and invokes the GBA BIOS `BgAffineSet` routine for one destination entry.

## Sprite tile copier

`CopySpriteTiles` uses a fixed sprite-dimension table for three OAM shapes × four sizes. Each 4bpp tile is **32 bytes**.

The source tilemap entry uses:

- low 10 bits: tile number;
- 0x400: X flip;
- 0x800: Y flip.

The routine handles unflipped, Y-flipped, X-flipped and combined X+Y-flipped copies. X flip reverses four bytes per tile row while swapping the high/low nibbles in each byte, which is the correct 4bpp pixel reversal.

## CountTrailingZeroBits quirk

The routine tests at most 32 bits and returns the first set-bit index. For input **0**, it falls through and returns **0**, not 32.

That zero-input behavior is a compatibility quirk worth preserving where callers may depend on it.

## CRC16

Both CRC functions use the same non-default initialization/finalization:

- initial CRC: **0x1121**;
- reflected polynomial: **0x8408**;
- result: bitwise complement of the accumulated CRC.

The table-driven implementation uses a 256-entry 16-bit table:

- Retail table: **0x082157AC**
- Debug table: **0x0822E944**
- size: 512 bytes
- SHA-256: `638dbc5f735cced09b3d0d767a72a8800baeb1b3bb399a514af61b3ea7be8a01`

The table payload is byte-identical between Retail and Debug.

## Next module

`blend_palette` begins at:

- Retail **0x08041534**
- Debug **0x080456B0**
- delta **+0x417C**
