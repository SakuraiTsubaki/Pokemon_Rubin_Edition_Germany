# Project

## Scope

Pokemon_Rubin_Edition_Germany is a self-contained German Pokemon Ruby reconstruction and expansion project.

First-class input profiles:

- Germany retail Rev 0
- Germany retail Rev 1
- Germany Debug Version
- the supplied save corresponding to each of those inputs

## Independence

- No source repository is a required upstream dependency.
- No code or data is assumed identical merely because another Ruby project implements it.
- Cross-project comparisons must be labeled as references and independently verified against the German binaries before promotion.
- German ROM/SAV evidence wins when a comparison disagrees.

## Reconstruction layers

### 1. Binary evidence / disassembly

Track ROM addresses, ARM/Thumb instructions, data boundaries, pointers, revision deltas, debug-only regions, text encodings, graphics, and save structures.

### 2. Decompiled source

Promote evidence into readable C/assembly/data only when the mapping is reproducible. The source tree becomes the main development surface; assembly remains available for exactness and unresolved regions.

### 3. Exact target profiles

- Rev 1: primary retail reconstruction target.
- Rev 0: separately reproducible retail revision.
- Debug: separately reconstructed research/debug profile; never silently merged into retail behavior.

### 4. German localization reconstruction

Recover German strings, terminology, font/character encoding, line wrapping, UI layout, map/event text, trainer data, Pokedex text, and localized graphics from the German targets.

### 5. Save reconstruction

Document the 128 KiB flash layout, rotating 14-section main saves, checksums, version compatibility, and observed save lineage. Keep ROM-profile identity separate from save-file history.

### 6. Expansion

Only after the original German targets have reproducible build/evidence coverage: expand identifiers, tables, save metadata, content capacity, and ROM layout inside this repository. Expansion work must preserve regression profiles for the original German releases.

## Current execution order

1. Lock ROM/SAV identities and hashes.
2. Build address maps and Rev 0 <-> Rev 1 binary delta records.
3. Map Debug-only code/data and development facilities.
4. Establish symbols and disassembly coverage.
5. Decompile Rev 1 and prove mappings against the binary.
6. Express Rev 0 and Debug differences as explicit target profiles.
7. Reconstruct German assets/localization and save behavior.
8. Add automated comparison/build verification.
9. Begin independent capacity expansion.

## Evidence rule

A semantic claim is not considered reconstructed merely because it matches a public decompilation. It must be tied back to German target bytes, symbols, data, behavior, or reproducible tests.
