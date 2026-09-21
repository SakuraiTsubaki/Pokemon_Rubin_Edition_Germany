# RTC day-count reconstruction

## Verified German retail address map

| Address | Identification | Evidence |
| --- | --- | --- |
| 0x08009314 | leap-year predicate | modulo-by-4/100/400 control flow |
| 0x0800934C | date-to-day-count routine | year loop, literal 365, month loop, leap-day adjustment, day addition |
| 0x080093D0 | literal 365 | loaded by the year loop |
| 0x080093D4 | pointer 0x081F4598 | points to the month-length table |
| 0x081F4598 | month-length table | 31,28,31,30,31,30,31,31,30,31,30,31 |

The mapping above is derived from the supplied German retail ROMs. Public source trees are not required to establish the identification.

## Rev 0 versus Rev 1

At 0x08009366:

- Rev 0 instruction condition: BLE
- Rev 1 instruction condition: BLT

At 0x0800938A:

- Rev 0 instruction condition: BGT
- Rev 1 instruction condition: BGE

The affected loop initializes i = year - 1 and repeatedly adds 365 plus one extra day when i is a leap year.

Therefore the loop condition is reconstructed as:

- Rev 0: i > 0
- Rev 1: i >= 0

This is the first promoted ROM-address-to-C reconstruction in this repository.

## Function boundary

The reconstructed date-count routine begins at 0x0800934C and returns at 0x080093CE. Literal pool data begins at 0x080093D0.

## Status

The semantics are verified from German ROM control flow and data. Compiler/build byte matching is the next step; src/rtc/date_count.c is a high-level reconstruction and is not yet claimed byte-identical when compiled.
