#ifndef GERMAN_RUBY_BATTLE_CONTROLLER_PROTOCOL_H
#define GERMAN_RUBY_BATTLE_CONTROLLER_PROTOCOL_H

#include <stdint.h>

enum GermanBattleControllerCommand
{
    GERMAN_BTL_CMD_0 = 0, /* BtlController_EmitGetMonData */
    GERMAN_BTL_CMD_1 = 1, /* BtlController_EmitGetRawMonData */
    GERMAN_BTL_CMD_2 = 2, /* BtlController_EmitSetMonData */
    GERMAN_BTL_CMD_3 = 3, /* BtlController_EmitSetRawMonData */
    GERMAN_BTL_CMD_4 = 4, /* BtlController_EmitLoadMonSprite */
    GERMAN_BTL_CMD_5 = 5, /* BtlController_EmitSwitchInAnim */
    GERMAN_BTL_CMD_6 = 6, /* BtlController_EmitReturnMonToBall */
    GERMAN_BTL_CMD_7 = 7, /* BtlController_EmitDrawTrainerPic */
    GERMAN_BTL_CMD_8 = 8, /* BtlController_EmitTrainerSlide */
    GERMAN_BTL_CMD_9 = 9, /* BtlController_EmitTrainerSlideBack */
    GERMAN_BTL_CMD_10 = 10, /* BtlController_EmitFaintAnimation */
    GERMAN_BTL_CMD_11 = 11, /* BtlController_EmitPaletteFade */
    GERMAN_BTL_CMD_12 = 12, /* BtlController_EmitSuccessBallThrowAnim */
    GERMAN_BTL_CMD_13 = 13, /* BtlController_EmitBallThrowAnim */
    GERMAN_BTL_CMD_14 = 14, /* BtlController_EmitPause */
    GERMAN_BTL_CMD_15 = 15, /* BtlController_EmitMoveAnimation */
    GERMAN_BTL_CMD_16 = 16, /* BtlController_EmitPrintString */
    GERMAN_BTL_CMD_17 = 17, /* BtlController_EmitPrintSelectionString */
    GERMAN_BTL_CMD_18 = 18, /* BtlController_EmitChooseAction */
    GERMAN_BTL_CMD_19 = 19, /* BtlController_EmitUnknownYesNoBox */
    GERMAN_BTL_CMD_20 = 20, /* BtlController_EmitChooseMove */
    GERMAN_BTL_CMD_21 = 21, /* BtlController_EmitChooseItem */
    GERMAN_BTL_CMD_22 = 22, /* BtlController_EmitChoosePokemon */
    GERMAN_BTL_CMD_23 = 23, /* BtlController_EmitCmd23 */
    GERMAN_BTL_CMD_24 = 24, /* BtlController_EmitHealthBarUpdate */
    GERMAN_BTL_CMD_25 = 25, /* BtlController_EmitExpUpdate */
    GERMAN_BTL_CMD_26 = 26, /* BtlController_EmitStatusIconUpdate */
    GERMAN_BTL_CMD_27 = 27, /* BtlController_EmitStatusAnimation */
    GERMAN_BTL_CMD_28 = 28, /* BtlController_EmitStatusXor */
    GERMAN_BTL_CMD_29 = 29, /* BtlController_EmitDataTransfer */
    GERMAN_BTL_CMD_30 = 30, /* BtlController_EmitDMA3Transfer */
    GERMAN_BTL_CMD_31 = 31, /* BtlController_EmitPlayBGM */
    GERMAN_BTL_CMD_32 = 32, /* BtlController_EmitCmd32 */
    GERMAN_BTL_CMD_33 = 33, /* BtlController_EmitTwoReturnValues */
    GERMAN_BTL_CMD_34 = 34, /* BtlController_EmitChosenMonReturnValue */
    GERMAN_BTL_CMD_35 = 35, /* BtlController_EmitOneReturnValue */
    GERMAN_BTL_CMD_36 = 36, /* BtlController_EmitOneReturnValue_Duplicate */
    GERMAN_BTL_CMD_37 = 37, /* BtlController_EmitCmd37 */
    GERMAN_BTL_CMD_38 = 38, /* BtlController_EmitCmd38 */
    GERMAN_BTL_CMD_39 = 39, /* BtlController_EmitCmd39 */
    GERMAN_BTL_CMD_40 = 40, /* BtlController_EmitCmd40 */
    GERMAN_BTL_CMD_41 = 41, /* BtlController_EmitHitAnimation */
    GERMAN_BTL_CMD_42 = 42, /* BtlController_EmitCmd42 */
    GERMAN_BTL_CMD_43 = 43, /* BtlController_EmitPlaySE */
    GERMAN_BTL_CMD_44 = 44, /* BtlController_EmitPlayFanfareOrBGM */
    GERMAN_BTL_CMD_45 = 45, /* BtlController_EmitFaintingCry */
    GERMAN_BTL_CMD_46 = 46, /* BtlController_EmitIntroSlide */
    GERMAN_BTL_CMD_47 = 47, /* BtlController_EmitIntroTrainerBallThrow */
    GERMAN_BTL_CMD_48 = 48, /* BtlController_EmitDrawPartyStatusSummary */
    GERMAN_BTL_CMD_49 = 49, /* BtlController_EmitHidePartyStatusSummary */
    GERMAN_BTL_CMD_50 = 50, /* BtlController_EmitEndBounceEffect */
    GERMAN_BTL_CMD_51 = 51, /* BtlController_EmitSpriteInvisibility */
    GERMAN_BTL_CMD_52 = 52, /* BtlController_EmitBattleAnimation */
    GERMAN_BTL_CMD_53 = 53, /* BtlController_EmitLinkStandbyMsg */
    GERMAN_BTL_CMD_54 = 54, /* BtlController_EmitResetActionMoveSelection */
    GERMAN_BTL_CMD_55 = 55, /* BtlController_EmitCmd55 */
    GERMAN_BTL_CMD_COUNT = 56
};

#define GERMAN_BTL_MOVE_ANIMATION_PACKET_SIZE 44u
#define GERMAN_BTL_STRING_PACKET_SIZE 68u
#define GERMAN_BTL_CHOOSE_MOVE_PACKET_SIZE 24u
#define GERMAN_BTL_PARTY_STATUS_PACKET_SIZE 52u

#if defined(GERMAN_RUBY_DEBUG)
#define GERMAN_BATTLE_TRANSFER_BUFFER_ADDRESS 0x030040D0u
#else
#define GERMAN_BATTLE_TRANSFER_BUFFER_ADDRESS 0x03004050u
#endif

#endif
