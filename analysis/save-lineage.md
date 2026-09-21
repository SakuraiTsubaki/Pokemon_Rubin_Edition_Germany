# Supplied save lineage

The three supplied 128 KiB save files are valid Gen III-style rotating sector saves, but they are not independent histories.

Each main save snapshot consists of all section IDs 0 through 13 with signature 0x08012025. All 28 main-save sectors in each supplied file pass their section checksum using the Ruby/Sapphire section data lengths.

| Supplied save | Complete main-save indices |
| --- | --- |
| Debug Version | 3, 4 |
| Rev 1 | 4, 5 |
| Retail Rev 0 | 5, 6 |

## Byte-identical inherited snapshots

- Debug index 4 == Rev 1 index 4
  - reconstructed 14-sector snapshot SHA-256: b9e6b8fddf9553ab0add36e9e9ec8ecf73e719f6f7a974f72bafcfcc165cfed0
- Rev 1 index 5 == Retail Rev 0 index 5
  - reconstructed 14-sector snapshot SHA-256: 193ec09deef46f60f98570618da526ebd1adc5286506112f9a005a5581120082

Observed history therefore forms:

Debug (index 4) -> Rev 1 (index 5) -> Retail Rev 0 (index 6)

This describes the supplied files only. It does not imply that a German Ruby ROM revision intrinsically requires or creates that lineage.

## Project consequence

ROM identities remain separate from save histories. Future compatibility tests must create clean per-profile saves as well as preserve these supplied lineage samples for migration/regression analysis.
