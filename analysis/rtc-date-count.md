# RTC date-count reconstruction

## Verified German retail address map

| Address | Identification | Evidence |
| --- | --- | --- |
| 0x08009314 | IsLeapYear | modulo-by-4/100/400 control flow |
| 0x0800934C | ConvertDateToDayCount | year loop, literal 365, month loop, leap-day adjustment, day addition |
| 0x080093D0 | literal 365 | loaded by the year loop |
| 0x080093D4 | pointer 0x081F4598 | month-length table |
| 0x081F4598 | month-length table | 31,28,31,30,31,30,31,31,30,31,30,31 |

## Rev 0 versus Rev 1

At 0x08009366:

- Rev 0 halfword: 0xDD11 (BLE)
- Rev 1 halfword: 0xDB11 (BLT)

At 0x0800938A:

- Rev 0 halfword: 0xDCED (BGT)
- Rev 1 halfword: 0xDAED (BGE)

The loop initializes i = year - 1 and repeatedly adds 365 plus a leap-day adjustment.

Therefore:

- Rev 0 reconstructs as i > 0.
- Rev 1 reconstructs as i >= 0.

The function starts at 0x0800934C and returns at 0x080093CE. Literal pool data follows at 0x080093D0.

The promoted implementation now lives in src/rtc/rtc.c together with the surrounding RTC core.
