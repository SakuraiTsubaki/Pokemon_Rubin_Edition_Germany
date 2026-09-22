# German smokescreen module

The complete smoke-effect module is mapped directly from the German binaries.

## Boundary

| Profile | Start | End exclusive | Size | SHA-256 |
| --- | --- | --- | ---: | --- |
| Retail Rev 0 / Rev 1 | 0x08046558 | 0x08046724 | 460 bytes (0x1CC) | 9d3da42856cd6652a3631b80949bc24d715b76379255c937072272f904847534 |
| Debug | 0x0804A724 | 0x0804A8F0 | 460 bytes (0x1CC) | a68ab77999306175e97fbfccb0b864511952e7a087099004f40a31d02e4879ab |

There is no Debug-only growth; delta is **+0x41CC** throughout.

## Function map

| Semantic/source function | Retail | Debug | Bytes |
| --- | --- | --- | ---: |
| sub_8046234 | 0x08046558 | 0x0804A724 | 340 |
| sub_8046388 | 0x080466AC | 0x0804A878 | 68 |
| sub_80463CC | 0x080466F0 | 0x0804A8BC | 52 |

The historical source-name numbers are not German addresses; the table above records the German ROM locations.

## Effect construction

The first function loads the smoke tile/palette only when the tile tag is not already present, creates one invisible controller sprite and four visible smoke sprites arranged as a 2×2 group around the requested X/Y coordinate.

Each smoke child:

- points back to the controller sprite through data[0];
- increments the controller's live-child counter;
- selects one of four animation indexes.

## Lifetime / cleanup

Each child decrements the controller count when its animation ends and then destroys itself.

When the controller count reaches zero it frees the smoke tile and palette resources. Depending on the caller flag, the controller either destroys itself or becomes a dummy callback.

This is a compact reference-counted presentation effect.

## Next module

`pokeball` begins at:

- Retail **0x08046724**
- Debug **0x0804A8F0**
- delta **+0x41CC**

The first function is `DoPokeballSendOutAnimation`.
