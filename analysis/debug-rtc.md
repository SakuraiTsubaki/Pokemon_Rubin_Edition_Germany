# German Debug RTC profile

The German Debug build has its own RTC address map. It is not address-compatible with either retail ROM, but its high-level RTC logic closely tracks the retail implementation.

## Major layout difference

Before the RTC utilities begin, the Debug build contains additional development code. As a result:

- Retail RtcDisableInterrupts: 0x080092C0
- Debug RtcDisableInterrupts: 0x0800943C

The initial RTC block is therefore shifted by 0x17C bytes in the Debug image.

## Date-loop behavior

The Debug ConvertDateToDayCount routine starts at 0x080094C8.

Its year loop uses the same branch conditions as retail Rev 0:

- loop-entry test corresponds to i > 0
- loop-back branch corresponds to continuing while i > 0

Therefore the Debug build belongs to the pre-Rev-1 RTC behavior for this routine. Rev 1 remains the only supplied German ROM with the i >= 0 fix.

## Debug-only RTC helpers

After FormatHexDate, four Debug-only helpers are present:

| Address | Reconstructed role |
| --- | --- |
| 0x0800987C | format cached RTC date as hexadecimal text |
| 0x08009894 | format RTC day count as right-aligned decimal text |
| 0x080098B8 | format RTC status byte as hexadecimal text |
| 0x08009A60 | refresh the cached RTC structure from hardware |

The first three insert 0x54 bytes before RtcCalcTimeDifference, moving the later common functions from a +0x17C shift to +0x1D0 relative to retail. The final refresh helper is inserted after RtcGetMinuteCount.

## Debug-specific data locations

- sRtcDummy: 0x0820D2E0
- month-length table: 0x0820D2EC
- gLocalTime: 0x030040C8
- save local-time offset field: 0x020251E0

The cached RTC/error globals remain at the same 0x03000458-0x0300046E range as retail.

## Source policy

src/rtc/rtc.c now supports GERMAN_RUBY_DEBUG in addition to the two retail profiles. Debug-only helper functions compile only for the Debug profile. This preserves one semantic reconstruction while keeping each binary profile explicit.
