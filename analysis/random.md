# German random module

The complete `random` module consists of the game's main 32-bit linear congruential RNG update and 16-bit seeding function.

## Boundary

| Profile | Start | End exclusive | Size | SHA-256 |
| --- | --- | --- | ---: | --- |
| Retail Rev 0 / Rev 1 | 0x080411A8 | 0x080411D8 | 48 bytes (0x30) | 0124eac0db619a26f2570eac3dc66b5963878fb31e450a0b0aa8f6f223cd55a4 |
| Debug | 0x08045324 | 0x08045354 | 48 bytes (0x30) | 519530735ef7cefd06e9c01b6abd00cc661c01fea7d2aa829be89b51cb4e65cf |

No Debug code is added; the text displacement remains **+0x417C**.

## RNG algorithm

`Random` updates the global 32-bit state as:

`state = 1103515245 * state + 24691`

and returns the upper 16 bits.

Constants:

- multiplier: decimal 1103515245 = **0x41C64E6D**;
- increment: decimal 24691 = **0x6073**.

`SeedRng` takes a 16-bit seed and writes it to the 32-bit state.

## Global state

- Retail `gRngValue`: **0x03004828**
- Debug `gRngValue`: **0x030048F8**

Unlike the text code, this EWRAM global shifts by **+0xD0** between Retail and Debug due to the different runtime data layout.

## Function map

- `Random`: Retail 0x080411A8 / Debug 0x08045324, 32-byte physical span;
- `SeedRng`: Retail 0x080411C8 / Debug 0x08045344, 16-byte physical span.

## Next module

`util` begins at Retail **0x080411D8** / Debug **0x08045354**.
