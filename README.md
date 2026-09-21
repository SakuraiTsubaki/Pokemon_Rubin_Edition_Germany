# Pokemon_Rubin_Edition_Germany

Independent reconstruction, disassembly, decompilation, save-format research, and expansion workspace for Pokemon - Rubin-Edition (Germany).

## Project rule

This repository stands on the German releases themselves. It does not depend on RUBY, PocketMonsters-Ruby-Decompilation, or another Ruby repository as its build/source base. Other projects may be consulted only as non-authoritative comparison material.

## Verified local baselines

| Profile | Size | Game code | Header revision | SHA-1 |
| --- | ---: | --- | ---: | --- |
| Germany retail | 16 MiB | AXVD | 0 | 1c2a53332382e14dab8815e3a6dd81ad89534050 |
| Germany Rev 1 | 16 MiB | AXVD | 1 | 424740be1fc67a5ddb954794443646e6aeee2c1b |
| Germany Debug Version | 16 MiB | AXVD | 0 | ca5e3d415c4b47353a73a616878ba833f3648b7a |

The corresponding supplied saves are 128 KiB. Their complete main-save sector sets and hashes are recorded in manifests/baselines.json.

## Reconstruction strategy

1. Preserve byte-level evidence with disassembly and binary comparison.
2. Promote understood routines and data into reviewed decompiled source.
3. Reproduce Germany Rev 1 as the primary retail reconstruction target.
4. Preserve Germany retail Rev 0 as a separately reproducible revision profile.
5. Recover and document Debug-only code/data as a first-class research profile.
6. Reconstruct German text, fonts, UI, graphics, events, maps, and save behavior from German evidence.
7. Expand this repository independently after the original German targets are reproducible.

Disassembly is the evidence layer. Decompilation is the main development layer.

## Storage policy

Do not commit ROM images. Commit lawful non-ROM research outputs, source, tools, manifests, logs, comparisons, patches, validation material, extracted metadata, and other reproducible work products.

See PROJECT.md for the execution order.
