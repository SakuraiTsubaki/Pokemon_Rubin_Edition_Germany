# German clock module

The complete `clock` text module has been bounded directly in the supplied German Retail Rev 0, Retail Rev 1 and Debug ROMs.

## Module boundary

| Profile | Start | End exclusive | Size | SHA-256 |
| --- | --- | --- | ---: | --- |
| Retail Rev 0 / Rev 1 | 0x0806A668 | 0x0806A7C0 | **344 bytes (0x158)** | `f6a44a7060cc399cfa1c4b8ba180697d7f4a5e0ed52081c21dde417d006ee112` |
| Debug | 0x0806ED44 | 0x0806EE9C | **344 bytes (0x158)** | `366852d55b6dc05ee1b5e64bdcaa07cf5529929790be452720451d038b1c775b` |

Retail Rev 0 and Rev 1 are byte-identical across the complete module. Debug adds no `clock` text, so the accumulated Retail-to-Debug displacement remains **+0x46DC** at entry and exit.

## Function layout

The source-correlated module contains six functions. German Retail starts are:

1. `InitTimeBasedEvents` — 0x0806A668
2. `DoTimeBasedEvents` — 0x0806A6A0
3. `UpdatePerDay` — 0x0806A6D0
4. `UpdatePerMinute` — 0x0806A734
5. `ReturnFromStartWallClock` — 0x0806A78C
6. `StartWallClock` — 0x0806A7A0

Debug preserves the same relative layout at +0x46DC.

## InitTimeBasedEvents anchor

The first function begins:

`00 B5 09 48`

and contains two stable immediate literals:

- `FLAG_SYS_CLOCK_SET = 0x0835`
- `VAR_DAYS = 0x4040`

It sets the clock flag, recalculates local RTC time, copies `gLocalTime` into the save block's last-berry-tree update timestamp, and stores the current day count.

## Daily update path

`DoTimeBasedEvents` only runs the daily/minute update path when the system clock flag is set.

`UpdatePerDay` advances daily state when saved `VAR_DAYS` is behind the current local day. Its source-correlated update chain includes:

- daily-flag clearing;
- Dewford trend;
- TV shows;
- weather;
- Pokérus;
- Mirage Island RNG/state;
- Birch state;
- Shoal Cave item state;
- lottery number.

The stored day variable is then advanced to the current local day.

## Minute update path

`UpdatePerMinute` computes a signed minute delta between the current local time and the last berry-tree update timestamp:

`24 * 60 * days + 60 * hours + minutes`

Only positive elapsed time advances berry trees. The saved last-update timestamp is replaced with the current local time after a successful update.

## Wall-clock transition

`StartWallClock` installs the wall-clock main callback and records `ReturnFromStartWallClock` as the saved callback. Returning from the wall clock reinitializes time-based events and resumes field/script execution with map music.

The profile-specific `gMain` addresses visible in the final function are:

- Retail: **0x03001770**
- Debug: **0x030017F0**

## Next-module anchor

`reset_rtc_screen` begins immediately afterward:

- Retail Rev 0 / Rev 1: **0x0806A7C0**
- Debug: **0x0806EE9C**
- accumulated delta: **+0x46DC**

Its first function is source-correlated as `SpriteCB_ResetRtcCusor0`. The first 16 bytes are identical across all three German profiles:

`00 B5 03 1C 0A 4A 2E 20 19 5E 88 00 40 18 C0 00`

The function reads the reset-RTC task selection through the cursor sprite's task ID and updates cursor visibility/animation/position. This independently anchors the `clock` end.
