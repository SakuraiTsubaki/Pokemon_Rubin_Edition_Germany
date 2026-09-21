# German battle-controller emitter protocol

The complete command-emitter tail of the German battle-controller module is now mapped.

## Exact slice

| Profile | Start | End exclusive | Size | SHA-256 |
| --- | --- | --- | ---: | --- |
| Retail Rev 0 / Rev 1 | 0x0800C7EC | 0x0800D40C | 3,104 bytes | 5debedeab09cd8a8b401345cfd75d15eb97915582661a85624a204ac9eb38935 |
| Debug | 0x0800CA08 | 0x0800D628 | 3,104 bytes | 7d19ce0e6c41d743eaf46cef52af0a66ed0fd98d273c9aeaeafcd4d98b74ff9f |

Retail Rev 0 and Rev 1 are byte-identical throughout the complete emitter block.

All 56 emitter entry points in the Debug image remain exactly +0x21C from Retail. No additional Debug-only insertion occurs inside this block.

## Command map

| ID | Function | Retail | Debug | Code bytes | Packet bytes |
| ---: | --- | --- | --- | ---: | --- |
| 0 | BtlController_EmitGetMonData | 0x0800C7EC | 0x0800CA08 | 36 | 4 |
| 1 | BtlController_EmitGetRawMonData | 0x0800C810 | 0x0800CA2C | 40 | 4 |
| 2 | BtlController_EmitSetMonData | 0x0800C838 | 0x0800CA54 | 64 | 3+bytes |
| 3 | BtlController_EmitSetRawMonData | 0x0800C878 | 0x0800CA94 | 64 | 3+bytes |
| 4 | BtlController_EmitLoadMonSprite | 0x0800C8B8 | 0x0800CAD4 | 32 | 4 |
| 5 | BtlController_EmitSwitchInAnim | 0x0800C8D8 | 0x0800CAF4 | 36 | 4 |
| 6 | BtlController_EmitReturnMonToBall | 0x0800C8FC | 0x0800CB18 | 32 | 2 |
| 7 | BtlController_EmitDrawTrainerPic | 0x0800C91C | 0x0800CB38 | 32 | 4 |
| 8 | BtlController_EmitTrainerSlide | 0x0800C93C | 0x0800CB58 | 32 | 4 |
| 9 | BtlController_EmitTrainerSlideBack | 0x0800C95C | 0x0800CB78 | 32 | 4 |
| 10 | BtlController_EmitFaintAnimation | 0x0800C97C | 0x0800CB98 | 32 | 4 |
| 11 | BtlController_EmitPaletteFade | 0x0800C99C | 0x0800CBB8 | 32 | 4 |
| 12 | BtlController_EmitSuccessBallThrowAnim | 0x0800C9BC | 0x0800CBD8 | 32 | 4 |
| 13 | BtlController_EmitBallThrowAnim | 0x0800C9DC | 0x0800CBF8 | 32 | 2 |
| 14 | BtlController_EmitPause | 0x0800C9FC | 0x0800CC18 | 72 | 2+3*count |
| 15 | BtlController_EmitMoveAnimation | 0x0800CA44 | 0x0800CC60 | 216 | 44 |
| 16 | BtlController_EmitPrintString | 0x0800CB1C | 0x0800CD38 | 288 | 68 |
| 17 | BtlController_EmitPrintSelectionString | 0x0800CC3C | 0x0800CE58 | 240 | 68 |
| 18 | BtlController_EmitChooseAction | 0x0800CD2C | 0x0800CF48 | 44 | 4 |
| 19 | BtlController_EmitUnknownYesNoBox | 0x0800CD58 | 0x0800CF74 | 32 | 2 |
| 20 | BtlController_EmitChooseMove | 0x0800CD78 | 0x0800CF94 | 60 | 24 |
| 21 | BtlController_EmitChooseItem | 0x0800CDB4 | 0x0800CFD0 | 52 | 4 |
| 22 | BtlController_EmitChoosePokemon | 0x0800CDE8 | 0x0800D004 | 60 | 8 (7 initialized) |
| 23 | BtlController_EmitCmd23 | 0x0800CE24 | 0x0800D040 | 32 | 4 |
| 24 | BtlController_EmitHealthBarUpdate | 0x0800CE44 | 0x0800D060 | 56 | 4 |
| 25 | BtlController_EmitExpUpdate | 0x0800CE7C | 0x0800D098 | 52 | 4 |
| 26 | BtlController_EmitStatusIconUpdate | 0x0800CEB0 | 0x0800D0CC | 84 | 9 |
| 27 | BtlController_EmitStatusAnimation | 0x0800CF04 | 0x0800D120 | 60 | 6 |
| 28 | BtlController_EmitStatusXor | 0x0800CF40 | 0x0800D15C | 32 | 2 |
| 29 | BtlController_EmitDataTransfer | 0x0800CF60 | 0x0800D17C | 72 | 4+len |
| 30 | BtlController_EmitDMA3Transfer | 0x0800CFA8 | 0x0800D1C4 | 104 | 7+len |
| 31 | BtlController_EmitPlayBGM | 0x0800D010 | 0x0800D22C | 72 | 3+len |
| 32 | BtlController_EmitCmd32 | 0x0800D058 | 0x0800D274 | 72 | 3+len |
| 33 | BtlController_EmitTwoReturnValues | 0x0800D0A0 | 0x0800D2BC | 44 | 4 |
| 34 | BtlController_EmitChosenMonReturnValue | 0x0800D0CC | 0x0800D2E8 | 56 | 5 |
| 35 | BtlController_EmitOneReturnValue | 0x0800D104 | 0x0800D320 | 44 | 4 |
| 36 | BtlController_EmitOneReturnValue_Duplicate | 0x0800D130 | 0x0800D34C | 44 | 4 |
| 37 | BtlController_EmitCmd37 | 0x0800D15C | 0x0800D378 | 32 | 4 |
| 38 | BtlController_EmitCmd38 | 0x0800D17C | 0x0800D398 | 32 | 2 |
| 39 | BtlController_EmitCmd39 | 0x0800D19C | 0x0800D3B8 | 32 | 4 |
| 40 | BtlController_EmitCmd40 | 0x0800D1BC | 0x0800D3D8 | 32 | 4 |
| 41 | BtlController_EmitHitAnimation | 0x0800D1DC | 0x0800D3F8 | 32 | 4 |
| 42 | BtlController_EmitCmd42 | 0x0800D1FC | 0x0800D418 | 32 | 4 |
| 43 | BtlController_EmitPlaySE | 0x0800D21C | 0x0800D438 | 44 | 4 |
| 44 | BtlController_EmitPlayFanfareOrBGM | 0x0800D248 | 0x0800D464 | 44 | 4 |
| 45 | BtlController_EmitFaintingCry | 0x0800D274 | 0x0800D490 | 32 | 4 |
| 46 | BtlController_EmitIntroSlide | 0x0800D294 | 0x0800D4B0 | 32 | 2 |
| 47 | BtlController_EmitIntroTrainerBallThrow | 0x0800D2B4 | 0x0800D4D0 | 32 | 4 |
| 48 | BtlController_EmitDrawPartyStatusSummary | 0x0800D2D4 | 0x0800D4F0 | 72 | 52 |
| 49 | BtlController_EmitHidePartyStatusSummary | 0x0800D31C | 0x0800D538 | 32 | 4 |
| 50 | BtlController_EmitEndBounceEffect | 0x0800D33C | 0x0800D558 | 32 | 4 |
| 51 | BtlController_EmitSpriteInvisibility | 0x0800D35C | 0x0800D578 | 36 | 4 |
| 52 | BtlController_EmitBattleAnimation | 0x0800D380 | 0x0800D59C | 44 | 4 |
| 53 | BtlController_EmitLinkStandbyMsg | 0x0800D3AC | 0x0800D5C8 | 32 | 2 |
| 54 | BtlController_EmitResetActionMoveSelection | 0x0800D3CC | 0x0800D5E8 | 32 | 2 |
| 55 | BtlController_EmitCmd55 | 0x0800D3EC | 0x0800D608 | 32 | 2 |

## Protocol properties recovered from the German binary

- Command ID is byte 0 of gBattleBuffersTransferData.
- The shared transfer staging buffer is addressed through 0x03004050 in Retail and 0x030040D0 in Debug.
- Fixed command IDs span 0 through 55 with no gaps.
- Commands 2, 3, 14, 29, 30, 31 and 32 have variable packet length.
- Command 15 (move animation) sends 44 bytes: 16-byte header plus a 28-byte disable-state structure.
- Commands 16 and 17 send 68 bytes: 4-byte command header plus a 64-byte battle-string context.
- Command 20 sends 24 bytes.
- Command 22 sends 8 bytes even though only seven bytes are explicitly initialized before transfer.
- Command 48 sends 52 bytes: 4-byte header plus 48 bytes of six padded HP/status records.

## Expansion pressure points

This protocol is one of the places that must be audited before modern-content expansion:

- move IDs in move-animation packets are 16-bit;
- string IDs are 16-bit;
- item/move/battle fields embedded in the 64-byte string context inherit Generation III field widths;
- controller command IDs are 8-bit;
- command 20 carries a fixed 20-byte move-selection payload;
- command 48 assumes six party status records in a fixed 48-byte payload;
- link transfer framing uses 16-bit payload sizes but the surrounding link ring is bounded to 0x1000 bytes in the earlier transport layer.

These are evidence-backed original constraints, not yet expansion changes.

## Module boundary

The emitter block ends at 0x0800D40C (Retail) / 0x0800D628 (Debug), which is also the end of battle_controllers.

The next linked source module begins there and is identified as the decompression module.
