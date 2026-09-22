# German play-time counter module

The complete `play_time` module has been mapped from the German binaries.

## Boundary

| Profile | Start | End exclusive | Size | SHA-256 |
| --- | --- | --- | ---: | --- |
| Retail Rev 0 / Rev 1 | 0x08052F68 | 0x08053040 | **216 bytes (0xD8)** | cbe0ba61dc55c205fab73d819b5c367d5f6660e0e60a7506f29a3af9d1e23ee7 |
| Debug | 0x08057158 | 0x08057230 | **216 bytes (0xD8)** | 942d56b27ff8b4f95fdd33623153482f69d052ce76ffcf0808e1706368da4281 |

Retail Rev 0 and Rev 1 are byte-identical. There is no Debug-only growth; the module stays at **+0x41F0**.

## German function map

| Function | Retail | Debug |
| --- | --- | --- |
| PlayTimeCounter_Reset | 0x08052F68 | 0x08057158 |
| PlayTimeCounter_Start | 0x08052F88 | 0x08057178 |
| PlayTimeCounter_Stop | 0x08052FB0 | 0x080571A0 |
| PlayTimeCounter_Update | 0x08052FBC | 0x080571AC |
| PlayTimeCounter_SetToMax | 0x0805301C | 0x0805720C |

## State machine

The counter has three internal states:

- STOPPED = 0;
- RUNNING = 1;
- MAXED_OUT = 2.

Reset clears SaveBlock2 play time and leaves the counter stopped.

Start sets RUNNING and immediately clamps if stored hours are already above 999.

Stop returns to STOPPED.

## Time fields

The already mapped SaveBlock2 fields are used directly:

- +0x0E: 16-bit hours;
- +0x10: minutes;
- +0x11: seconds;
- +0x12: VBlank counter.

While RUNNING, every update increments the VBlank byte. Each field rolls after **59**:

- 60 VBlanks -> +1 second;
- 60 seconds -> +1 minute;
- 60 minutes -> +1 hour.

## Maximum display/storage value

When hours exceed 999, the module switches to MAXED_OUT and stores:

**999:59:59 + 59 VBlanks**

This is the exact legacy saturation value used by the German Ruby build.

A modern play-time accumulator can be wider internally, but the legacy SaveBlock2 adapter must clamp to this representation.

## Next module

`new_game` begins at:

- Retail **0x08053040**
- Debug **0x08057230**
- delta **+0x41F0**

The first routine is `write_word_to_mem`; its first 16 bytes are byte-identical in Retail and Debug.
