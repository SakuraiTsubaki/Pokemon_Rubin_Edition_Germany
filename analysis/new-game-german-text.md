# German new-game intro text evidence

The nine dialogue resources referenced by the mapped Birch intro state machine have now been located directly in the supplied German ROMs.

## Block identity

| Profile | Start | End exclusive | Size | SHA-256 |
| --- | --- | --- | ---: | --- |
| Retail Rev 0 / Rev 1 | 0x081D3C9F | 0x081D40CC | 1,069 bytes | 0870c7b96b0b35756558df922f8135f8b9ce0498601f8da9eb2fb9fe1205bc0d |
| Debug | 0x081EC9F3 | 0x081ECE20 | 1,069 bytes | 0870c7b96b0b35756558df922f8135f8b9ce0498601f8da9eb2fb9fe1205bc0d |

The complete text block is byte-identical between Retail and Debug. The Debug copy is located exactly +0x18D54 bytes after the retail copy.

## Per-string evidence

| State | Retail | Debug | Bytes | SHA-256 | Short preview |
| ---: | --- | --- | ---: | --- | --- |
| 3 | 0x081D3C9F | 0x081EC9F3 | 134 | 805d3360b9fc99182402fba64c98e653c2bea093026b89379ca05765713e3732 | Sorry, dass du warten musstest. |
| 4 | 0x081D3D25 | 0x081ECA79 | 30 | d046998cb15c3187068869ef8be123541d4614dc4c5250a3026be13566051673 | Das nennen wir ein “POKéMON”. |
| 8 | 0x081D3D43 | 0x081ECA97 | 472 | 8507a17c7a10d993439c3edb635eb948ebb2324bbfffb469d6594fc38a667454 | Auf dieser Welt leben Wesen, … |
| 9 | 0x081D3F1B | 0x081ECC6F | 17 | de572bc601eab5bf2d6df9d059fcb9cf4fdad7031d461726cd343cc66d10b4bb | Und wer bist du? |
| 14 | 0x081D3F2C | 0x081ECC80 | 45 | 808c1b2684bcee3ec6638c126a218d97d930699281a336f2a030d5cce54a74b6 | Bist du ein Junge? … |
| 19 | 0x081D3F59 | 0x081ECCAD | 24 | b2892f13f043a5977a555dc71d203c170053f6c8d9fe5e16f0a1b5493eeec471 | Fein! … |
| 23 | 0x081D3F71 | 0x081ECCC5 | 23 | 6f0b0f8e6d52e4e8c85225ba2ce54d01a870516632cd7f358ceec93716299ffc | Ah, du bist also {PLAYER}? |
| 27 | 0x081D3F88 | 0x081ECCDC | 103 | a6ca7d95c122b2ffb7b168b01b9a244c6ced4b6d5dbf4eb4e61cbf9ede06d352 | Ah, okay! … |
| 29 | 0x081D3FEF | 0x081ECD43 | 221 | 4d1eb62afbf05383e52fdeb2d09c0c30fc52cb81e60d83ec94b296e7a4fd4a18 | Gut, bist du bereit? … |

The long dialogue contents are intentionally not duplicated into this public repository. tools/extract_new_game_text.py reproduces the decoded strings from a locally supplied verified ROM.

## Encoding observations

The German text uses the Western Generation III character set, including:

- 0xF1 / 0xF2 / 0xF3 = Ä / Ö / Ü
- 0xF4 / 0xF5 / 0xF6 = ä / ö / ü
- 0x15 = ß
- 0x1B = é
- 0xFE = line break
- 0xFB = paragraph/control break in this text block
- 0xFA = pause marker
- 0xFD xx = variable placeholder
- 0xFF = end of string

State 23 and state 27 contain variable placeholders for the chosen player name.

## Independence rule

The addresses, lengths, hashes, byte equality and decoded German strings are recovered from the supplied German ROM images. Character-map labels are merely decoding notation; the binary bytes remain the authoritative evidence.
