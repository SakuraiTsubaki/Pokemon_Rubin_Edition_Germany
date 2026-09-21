# German main-menu core

The module immediately following the RTC utilities is the main-menu module.

## Module transition

Retail:

- RTC utility end: 0x08009888
- main-menu first function: 0x08009890

Debug:

- Debug RTC helper end: 0x08009A6C
- main-menu first function: 0x08009A70

The first main-menu core functions in Debug are shifted by exactly +0x1E0 from the retail addresses.

## Verified callback map

| Function | Retail | Debug |
| --- | --- | --- |
| CB2_MainMenu | 0x08009890 | 0x08009A70 |
| VBlankCB_MainMenu | 0x080098A8 | 0x08009A88 |
| CB2_InitMainMenu | 0x080098BC | 0x08009A9C |
| CB2_InitMainMenuFromOptions | 0x080098C8 | 0x08009AA8 |
| InitMainMenu | 0x080098D4 | 0x08009AB4 |

CB2_MainMenu calls four subsystems in sequence: task processing, sprite animation, OAM-buffer construction, and palette-fade update. VBlankCB_MainMenu performs OAM load, sprite-copy processing, and palette transfer.

## Mapped main-menu task state machine

| Function | Retail | Debug |
| --- | --- | --- |
| Task_MainMenuCheckSave | 0x08009A44 | 0x08009C24 |
| Task_MainMenuWaitForSaveErrorAck | 0x08009BE8 | 0x08009DC8 |
| Task_MainMenuCheckRtc | 0x08009C30 | 0x08009E10 |
| Task_MainMenuWaitForRtcErrorAck | 0x08009CF8 | 0x08009ED8 |
| Task_MainMenuDraw | 0x08009D40 | 0x08009F20 |
| Task_MainMenuHighlight | 0x08009F0C | 0x0800A0EC |
| MainMenuProcessKeyInput | 0x08009F38 | 0x0800A118 |
| Task_MainMenuProcessKeyInput | 0x0800A04C | 0x0800A22C |
| Task_MainMenuPressedA | 0x0800A07C | 0x0800A25C |
| Task_MainMenuPressedB | 0x0800A17C | 0x0800A35C |
| HighlightCurrentMenuItem | 0x0800A1A8 | 0x0800A388 |
| PrintMainMenuItem | 0x0800A288 | 0x0800A468 |

These routines are address-mapped now; their C promotion is intentionally staged separately from the already promoted callback/rendering helpers.

## Save-information rendering map

| Function | Retail | Debug |
| --- | --- | --- |
| PrintSaveFileInfo | 0x0800A2D4 | 0x0800A4B4 |
| PrintPlayerName | 0x0800A2EC | 0x0800A4CC |
| PrintPlayTime | 0x0800A310 | 0x0800A4F0 |
| PrintPokedexCount | 0x0800A358 | 0x0800A538 |
| PrintBadgeCount | 0x0800A390 | 0x0800A570 |
| first new-game speech task | 0x0800A3C8 | 0x0800A5A8 |

The boundary at 0x0800A3C8 / 0x0800A5A8 is used as the end of the current main-menu-core reconstruction slice.

## German SaveBlock2 evidence

Literal pools identify the active SaveBlock2 base used by these functions:

- Retail: 0x02024EA4
- Debug: 0x02025148

The accessed fields in this slice establish:

- +0x00 player name
- +0x08 player gender
- +0x0E play-time hours (16-bit)
- +0x10 play-time minutes (8-bit)

The retail RTC local-time offset address corrected in the preceding verification pass is 0x02024F3C, which is exactly retail SaveBlock2 + 0x98.

## German-specific menu layout

PrintPlayTime contains explicit German layout constants:

- TIME label at pixel x=124, y=24
- formatted time aligned in a 40-pixel field
- final aligned value printed at tile column 23, row 3

PrintBadgeCount contains:

- BADGES label at pixel x=124, y=40
- numeric badge count at pixel x=205, y=40

These constants occur in both the German retail and German Debug binaries.

## Revision equality

The complete retail slice 0x00009890..0x0000A3C7 is byte-identical between Rev 0 and Rev 1. The only Rev 0/Rev 1 executable differences remain the previously recorded RTC branch bytes.
