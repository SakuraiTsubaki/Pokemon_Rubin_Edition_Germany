#include <stdint.h>

struct GermanBattleCoreSymbol
{
    const char *name;
    uint32_t retailAddress;
    uint32_t debugAddress;
    uint16_t retailSize;
    uint16_t debugSize;
};

const struct GermanBattleCoreSymbol gGermanBattleCoreTurnOrderSymbols[] =
{
    { "BattleMainCB1", 0x080109F8u, 0x080139E4u, 80, 212 },
    { "BattleStartClearSetData", 0x08010A48u, 0x08013AB8u, 788, 812 },
    { "SwitchInClearSetData", 0x08010D5Cu, 0x08013DE4u, 960, 960 },
    { "UndoEffectsAfterFainting", 0x0801111Cu, 0x080141A4u, 888, 888 },
    { "bc_8012FAC", 0x08011494u, 0x0801451Cu, 116, 116 },
    { "BattlePrepIntroSlide", 0x08011508u, 0x08014590u, 80, 80 },
    { "sub_8011384", 0x08011558u, 0x080145E0u, 636, 636 },
    { "bc_801333C", 0x080117D4u, 0x0801485Cu, 416, 416 },
    { "bc_battle_begin_message", 0x08011974u, 0x080149FCu, 56, 56 },
    { "bc_8013568", 0x080119ACu, 0x08014A34u, 40, 40 },
    { "sub_8011800", 0x080119D4u, 0x08014A5Cu, 52, 52 },
    { "sub_8011834", 0x08011A08u, 0x08014A90u, 144, 144 },
    { "bc_801362C", 0x08011A98u, 0x08014B20u, 140, 140 },
    { "unref_sub_8011950", 0x08011B24u, 0x08014BACu, 32, 32 },
    { "sub_8011970", 0x08011B44u, 0x08014BCCu, 68, 68 },
    { "sub_80119B4", 0x08011B88u, 0x08014C10u, 180, 180 },
    { "unref_sub_8011A68", 0x08011C3Cu, 0x08014CC4u, 152, 152 },
    { "BattleBeginFirstTurn", 0x08011CD4u, 0x08014D5Cu, 712, 712 },
    { "bc_8013B1C", 0x08011F9Cu, 0x08015024u, 196, 196 },
    { "BattleTurnPassed", 0x08012060u, 0x080150E8u, 412, 412 },
    { "CanRunFromBattle", 0x080121FCu, 0x08015284u, 560, 560 },
    { "sub_8012258", 0x0801242Cu, 0x080154B4u, 204, 204 },
    { "sub_8012324", 0x080124F8u, 0x08015580u, 3224, 3224 },
    { "SwapTurnOrder", 0x08013190u, 0x08016218u, 52, 52 },
    { "GetWhoStrikesFirst", 0x080131C4u, 0x0801624Cu, 984, 984 },
    { "SetActionsAndBanksTurnOrder", 0x0801359Cu, 0x08016624u, 660, 660 },
    { "TurnValuesCleanUp", 0x08013830u, 0x080168B8u, 288, 288 },
    { "SpecialStatusesClear", 0x08013950u, 0x080169D8u, 80, 80 },
    { "CheckFocusPunch_ClearVarsBeforeTurnStarts", 0x080139A0u, 0x08016A28u, 292, 292 },
};

const unsigned int gGermanBattleCoreTurnOrderSymbolCount =
    sizeof(gGermanBattleCoreTurnOrderSymbols) /
    sizeof(gGermanBattleCoreTurnOrderSymbols[0]);
