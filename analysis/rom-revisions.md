# Germany Rev 0 / Rev 1 binary delta

Verified directly from the supplied 16 MiB ROM images.

Exactly four byte offsets differ:

| ROM offset | Rev 0 | Rev 1 | Classification |
| ---: | ---: | ---: | --- |
| 0x000000BC | 0x00 | 0x01 | GBA software version |
| 0x000000BD | 0x42 | 0x41 | GBA header checksum |
| 0x00009367 | 0xDD | 0xDB | executable code byte |
| 0x0000938B | 0xDC | 0xDA | executable code byte |

The two code-byte changes alter Thumb conditional branches. Their final high-level function/semantic names are intentionally not promoted here until this repository has an independently reproducible address-to-symbol mapping.

## Debug comparison

Germany Debug versus Germany retail Rev 0:

- differing bytes: 6,751,723
- first differing offset: 0x00000128
- last differing offset: 0x006DF84F
- contiguous differing runs: 263,540

This is therefore treated as a distinct development build profile, not as a small retail revision patch.

## Next proof step

Disassemble the region around 0x08009366 and 0x0800938A, recover its callers/data flow, assign a verified symbol, then promote the routine into decompiled source with Rev 0 / Rev 1 target conditionals only if byte matching proves the mapping.
