# German trig module

The complete `trig` text module is mapped from the German ROMs.

## Text boundary

| Profile | Start | End exclusive | Size | SHA-256 |
| --- | --- | --- | ---: | --- |
| Retail Rev 0 / Rev 1 | 0x08041110 | 0x080411A8 | 152 bytes (0x98) | 4ca4702ed06a970f5502bb52b7354e995528a32dae91ade3d9ddbf48f1e276aa |
| Debug | 0x0804528C | 0x08045324 | 152 bytes (0x98) | 0542d9f677d3195b88fbe91590a9167b8fb741f5635c6aa39420e576d050bc6e |

No Debug-only code is inserted; the text displacement remains **+0x417C**.

## Functions

| Function | Retail | Debug | Span |
| --- | --- | --- | ---: |
| Sin | 0x08041110 | 0x0804528C | 28 |
| Cos | 0x0804112C | 0x080452A8 | 32 |
| Sin2 | 0x0804114C | 0x080452C8 | 68 |
| Cos2 | 0x08041190 | 0x0804530C | 24 |

`Sin` and `Cos` use a signed **Q8.8** lookup table and compute amplitude-scaled values. `Cos` reuses the same table with a +64 index phase shift.

`Sin2` accepts degrees, reduces modulo 180, obtains the sign from the 180-degree half-cycle and reads a signed **Q4.12** degree table. `Cos2(angle)` delegates to `Sin2(angle + 90)`.

## Lookup tables

The code points to ROM-resident tables outside this text module:

- `gSineTable`: 320 signed 16-bit entries, Retail **0x08215314**, Debug **0x0822E4AC**, 640 bytes, SHA-256 `dbdf49974fb8a6f319acc84a54ad90b3167aa588b2a3eafc62a6289c4d926205`;
- `gSineDegreeTable`: 180 signed 16-bit entries, Retail **0x08215594**, Debug **0x0822E72C**, 360 bytes, SHA-256 `353f23c8d42a29b25f44f9ef952af11f4745681ab8c479887b23f984631c72a0`.

The table payloads are byte-identical between Retail and Debug even though their ROM addresses differ by the later data-layout displacement.

## Next module

`random` begins at Retail **0x080411A8** / Debug **0x08045324**.
