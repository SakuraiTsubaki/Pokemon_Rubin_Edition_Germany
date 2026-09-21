# German retail RTC core

This record promotes the contiguous German retail RTC block from byte-level evidence into named C routines.

## Verified function map

| ROM address | Reconstructed function |
| --- | --- |
| 0x080092C0 | RtcDisableInterrupts |
| 0x080092D8 | RtcRestoreInterrupts |
| 0x080092EC | ConvertBcdToBinary |
| 0x08009314 | IsLeapYear |
| 0x0800934C | ConvertDateToDayCount |
| 0x080093D8 | RtcGetDayCount |
| 0x08009414 | RtcInit |
| 0x08009474 | RtcGetErrorStatus |
| 0x08009480 | RtcGetInfo |
| 0x080094B0 | RtcGetDateTime |
| 0x080094C8 | RtcGetStatus |
| 0x080094E0 | RtcGetRawInfo |
| 0x080094F4 | RtcCheckInfo |
| 0x080095F4 | RtcReset |

## Recovered RAM locations

| Address | Role |
| --- | --- |
| 0x03000458 | RTC error status |
| 0x03000460 | cached RTC info |
| 0x0300046C | probe result |
| 0x0300046E | saved IME value |

The interrupt wrappers directly reference REG_IME at 0x04000208.

## Recovered ROM data

- 0x081F458C: dummy RTC record beginning with year=0, month=1, day=1.
- 0x081F4598: month-length table 31,28,31,30,31,30,31,31,30,31,30,31.

## External RTC library calls

The retail block calls the following fixed targets:

- 0x081ECE84: RTC unprotect operation.
- 0x081ECEB4: RTC probe operation.
- 0x081ECF8C: RTC reset operation.
- 0x081ED010: RTC status read.
- 0x081ED184: RTC date/time read.

Names in source describe behavior established from call context and are not treated as proof of source provenance.

## Revision comparison

Within ROM offsets 0x000092B0 through 0x00009610, Rev 0 and Rev 1 differ at only:

- 0x00009367
- 0x0000938B

Those are the two conditional-branch bytes in ConvertDateToDayCount. Every later function in the promoted RTC core is byte-identical between the two German retail revisions.

## Source status

src/rtc/rtc.c is a high-level reconstruction. It has been syntax-checked for both GERMAN_RUBY_REV0 and GERMAN_RUBY_REV1 profiles. Exact compiler/toolchain byte matching remains a later milestone.
