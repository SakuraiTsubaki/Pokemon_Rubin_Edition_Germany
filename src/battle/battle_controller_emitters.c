#include <stdint.h>

struct GermanBattleControllerEmitter
{
    const char *name;
    uint8_t commandId;
    uint32_t retailAddress;
    uint32_t debugAddress;
    uint16_t codeSize;
};

const struct GermanBattleControllerEmitter gGermanBattleControllerEmitters[56] =
{
    { "BtlController_EmitGetMonData", 0, 0x0800C7ECu, 0x0800CA08u, 36 },
    { "BtlController_EmitGetRawMonData", 1, 0x0800C810u, 0x0800CA2Cu, 40 },
    { "BtlController_EmitSetMonData", 2, 0x0800C838u, 0x0800CA54u, 64 },
    { "BtlController_EmitSetRawMonData", 3, 0x0800C878u, 0x0800CA94u, 64 },
    { "BtlController_EmitLoadMonSprite", 4, 0x0800C8B8u, 0x0800CAD4u, 32 },
    { "BtlController_EmitSwitchInAnim", 5, 0x0800C8D8u, 0x0800CAF4u, 36 },
    { "BtlController_EmitReturnMonToBall", 6, 0x0800C8FCu, 0x0800CB18u, 32 },
    { "BtlController_EmitDrawTrainerPic", 7, 0x0800C91Cu, 0x0800CB38u, 32 },
    { "BtlController_EmitTrainerSlide", 8, 0x0800C93Cu, 0x0800CB58u, 32 },
    { "BtlController_EmitTrainerSlideBack", 9, 0x0800C95Cu, 0x0800CB78u, 32 },
    { "BtlController_EmitFaintAnimation", 10, 0x0800C97Cu, 0x0800CB98u, 32 },
    { "BtlController_EmitPaletteFade", 11, 0x0800C99Cu, 0x0800CBB8u, 32 },
    { "BtlController_EmitSuccessBallThrowAnim", 12, 0x0800C9BCu, 0x0800CBD8u, 32 },
    { "BtlController_EmitBallThrowAnim", 13, 0x0800C9DCu, 0x0800CBF8u, 32 },
    { "BtlController_EmitPause", 14, 0x0800C9FCu, 0x0800CC18u, 72 },
    { "BtlController_EmitMoveAnimation", 15, 0x0800CA44u, 0x0800CC60u, 216 },
    { "BtlController_EmitPrintString", 16, 0x0800CB1Cu, 0x0800CD38u, 288 },
    { "BtlController_EmitPrintSelectionString", 17, 0x0800CC3Cu, 0x0800CE58u, 240 },
    { "BtlController_EmitChooseAction", 18, 0x0800CD2Cu, 0x0800CF48u, 44 },
    { "BtlController_EmitUnknownYesNoBox", 19, 0x0800CD58u, 0x0800CF74u, 32 },
    { "BtlController_EmitChooseMove", 20, 0x0800CD78u, 0x0800CF94u, 60 },
    { "BtlController_EmitChooseItem", 21, 0x0800CDB4u, 0x0800CFD0u, 52 },
    { "BtlController_EmitChoosePokemon", 22, 0x0800CDE8u, 0x0800D004u, 60 },
    { "BtlController_EmitCmd23", 23, 0x0800CE24u, 0x0800D040u, 32 },
    { "BtlController_EmitHealthBarUpdate", 24, 0x0800CE44u, 0x0800D060u, 56 },
    { "BtlController_EmitExpUpdate", 25, 0x0800CE7Cu, 0x0800D098u, 52 },
    { "BtlController_EmitStatusIconUpdate", 26, 0x0800CEB0u, 0x0800D0CCu, 84 },
    { "BtlController_EmitStatusAnimation", 27, 0x0800CF04u, 0x0800D120u, 60 },
    { "BtlController_EmitStatusXor", 28, 0x0800CF40u, 0x0800D15Cu, 32 },
    { "BtlController_EmitDataTransfer", 29, 0x0800CF60u, 0x0800D17Cu, 72 },
    { "BtlController_EmitDMA3Transfer", 30, 0x0800CFA8u, 0x0800D1C4u, 104 },
    { "BtlController_EmitPlayBGM", 31, 0x0800D010u, 0x0800D22Cu, 72 },
    { "BtlController_EmitCmd32", 32, 0x0800D058u, 0x0800D274u, 72 },
    { "BtlController_EmitTwoReturnValues", 33, 0x0800D0A0u, 0x0800D2BCu, 44 },
    { "BtlController_EmitChosenMonReturnValue", 34, 0x0800D0CCu, 0x0800D2E8u, 56 },
    { "BtlController_EmitOneReturnValue", 35, 0x0800D104u, 0x0800D320u, 44 },
    { "BtlController_EmitOneReturnValue_Duplicate", 36, 0x0800D130u, 0x0800D34Cu, 44 },
    { "BtlController_EmitCmd37", 37, 0x0800D15Cu, 0x0800D378u, 32 },
    { "BtlController_EmitCmd38", 38, 0x0800D17Cu, 0x0800D398u, 32 },
    { "BtlController_EmitCmd39", 39, 0x0800D19Cu, 0x0800D3B8u, 32 },
    { "BtlController_EmitCmd40", 40, 0x0800D1BCu, 0x0800D3D8u, 32 },
    { "BtlController_EmitHitAnimation", 41, 0x0800D1DCu, 0x0800D3F8u, 32 },
    { "BtlController_EmitCmd42", 42, 0x0800D1FCu, 0x0800D418u, 32 },
    { "BtlController_EmitPlaySE", 43, 0x0800D21Cu, 0x0800D438u, 44 },
    { "BtlController_EmitPlayFanfareOrBGM", 44, 0x0800D248u, 0x0800D464u, 44 },
    { "BtlController_EmitFaintingCry", 45, 0x0800D274u, 0x0800D490u, 32 },
    { "BtlController_EmitIntroSlide", 46, 0x0800D294u, 0x0800D4B0u, 32 },
    { "BtlController_EmitIntroTrainerBallThrow", 47, 0x0800D2B4u, 0x0800D4D0u, 32 },
    { "BtlController_EmitDrawPartyStatusSummary", 48, 0x0800D2D4u, 0x0800D4F0u, 72 },
    { "BtlController_EmitHidePartyStatusSummary", 49, 0x0800D31Cu, 0x0800D538u, 32 },
    { "BtlController_EmitEndBounceEffect", 50, 0x0800D33Cu, 0x0800D558u, 32 },
    { "BtlController_EmitSpriteInvisibility", 51, 0x0800D35Cu, 0x0800D578u, 36 },
    { "BtlController_EmitBattleAnimation", 52, 0x0800D380u, 0x0800D59Cu, 44 },
    { "BtlController_EmitLinkStandbyMsg", 53, 0x0800D3ACu, 0x0800D5C8u, 32 },
    { "BtlController_EmitResetActionMoveSelection", 54, 0x0800D3CCu, 0x0800D5E8u, 32 },
    { "BtlController_EmitCmd55", 55, 0x0800D3ECu, 0x0800D608u, 32 },
};

const unsigned int gGermanBattleControllerEmitterCount = 56;
