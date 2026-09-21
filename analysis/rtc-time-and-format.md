# German retail RTC formatting and local-time block

The contiguous retail block after RtcReset has now been mapped through the end of the RTC utility subsystem.

| ROM address | Reconstructed function |
| --- | --- |
| 0x08009608 | FormatDecimalTime |
| 0x08009640 | FormatHexTime |
| 0x08009678 | FormatHexRtcTime |
| 0x08009690 | FormatDecimalDate |
| 0x080096C8 | FormatHexDate |
| 0x08009700 | RtcCalcTimeDifference |
| 0x08009784 | RtcCalcLocalTime |
| 0x080097AC | RtcInitLocalTimeOffset |
| 0x080097C0 | RtcCalcLocalTimeOffset |
| 0x080097F0 | CalcTimeDifference |
| 0x08009858 | RtcGetMinuteCount |

## Formatting evidence

- 0x08006D24 is called by the decimal time/date routines.
- 0x08006E88 is called by the hexadecimal time/date routines.
- Character 0xF0 is inserted between time fields.
- Character 0xAE is inserted between date fields.
- 0xFF terminates the generated text.
- Time fields use width 2; year formatting uses width 4.

## Time structure

The arithmetic routines establish this layout:

- +0x00: signed 16-bit days
- +0x02: signed 8-bit hours
- +0x03: signed 8-bit minutes
- +0x04: signed 8-bit seconds

Negative seconds borrow 60 from minutes; negative minutes borrow 60 from hours; negative hours borrow 24 from days.

## Recovered locations

- 0x03004048: local-time structure.
- 0x02023C4F: save-resident local-time offset field.
- 0x03000460: cached RTC record, reused by formatting and minute-count routines.

## Revision comparison

ROM offsets 0x00009608 through 0x00009889 are byte-identical between German retail Rev 0 and Rev 1.

The next function begins at 0x08009890 and is outside this RTC utility block, so 0x08009888 is the verified end of the retail RTC utility subsystem currently reconstructed.
