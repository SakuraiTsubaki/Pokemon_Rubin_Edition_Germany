# German trainer-class localization helper module

This module is German-specific and begins exactly at the address encoded in its historical source-file name: `de_rom_8040FE0`.

## Module boundary

| Profile | Start | End exclusive | Size | SHA-256 |
| --- | --- | --- | ---: | --- |
| Retail Rev 0 / Rev 1 | 0x08040FE0 | 0x08041110 | 304 bytes (0x130) | 0d60aa9e91ffd588e2d962a26e20f137a0e4b34fc6fc4eddde613c11890bca22 |
| Debug | 0x0804515C | 0x0804528C | 304 bytes (0x130) | d1c9e7698dc63c6b0e4a22b887172ed5aff2e9d91c5be92e4e2a64bd15d3d2bb |

Retail Rev 0 and Rev 1 are byte-identical. There is no Debug-only growth; every function keeps the inherited **+0x417C** displacement.

## Function map

| Function | Retail | Debug | Span |
| --- | --- | --- | ---: |
| de_sub_8040FE0 | 0x08040FE0 | 0x0804515C | 20 |
| de_sub_8040FF4 | 0x08040FF4 | 0x08045170 | 24 |
| de_sub_804100C | 0x0804100C | 0x08045188 | 24 |
| de_sub_8041024 | 0x08041024 | 0x080451A0 | 232 |
| de_sub_804110C | 0x0804110C | 0x08045288 | 4 |

## Fixed localized trainer-class helpers

The first three helpers accept a byte argument but the compiled German binaries do not use it in the returned index. Their literal arithmetic resolves to fixed entries of the 13-byte-wide `gTrainerClassNames` table:

- `de_sub_8040FE0` -> trainer-class index **26** = `TRAINER_CLASS_SCHOOL_KID`;
- `de_sub_8040FF4` -> index **46** = `TRAINER_CLASS_POKEMON_TRAINER_3`;
- `de_sub_804100C` -> index **25** = `TRAINER_CLASS_LEADER`.

This is verified from German machine code: each helper loads the class-name table base and adds the constant index × 13. The apparent gender argument does not alter the returned pointer in the shipped German binaries.

## de_sub_8041024 dispatcher

The 232-byte dispatcher normalizes trainer-class name selection across ordinary trainer records and special trainer contexts.

It compares its first selector against **0x100, 0x400 and 0x800**. Source correlation identifies those branches with facility/Battle Tower, Secret Base and e-Reader-style trainer sources. The ordinary path reads the trainer's class byte from the 40-byte Trainer record and applies German-specific normalization before returning a pointer into `gTrainerClassNames`.

Directly verified ordinary-record cases include:

- class 26 -> fixed School Kid class-name entry;
- class 46 with the correlated female/class condition -> fixed Pokémon Trainer 3 entry;
- class 25 -> fixed Leader entry;
- otherwise -> `gTrainerClassNames[trainerClass]`.

The special-context paths perform the same kind of normalization after obtaining their class/name indices from their respective subsystems.

This code matters to the German project because localized trainer-class rendering is **not purely a data-table lookup**. Context-sensitive code participates in choosing the class-name string.

## de_sub_804110C

The final four-byte helper simply returns its second argument unchanged:

`return arg1;`

## Next module

`trig` begins immediately at:

- Retail **0x08041110**
- Debug **0x0804528C**
- delta **+0x417C**

The first function is `Sin`.
