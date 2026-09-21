#include <stdint.h>

struct GermanBattleEndTurnSymbol
{
    const char *name;
    uint32_t retailAddress;
    uint32_t debugAddress;
    uint16_t codeSize;
};

const struct GermanBattleEndTurnSymbol gGermanBattleEndTurnSymbols[] =
{
    { "RunTurnActionsFunctions", 0x08013AC4u, 0x08016B4Cu, 168 },
    { "HandleEndTurn_BattleWon", 0x08013B6Cu, 0x08016BF4u, 460 },
    { "HandleEndTurn_BattleLost", 0x08013D38u, 0x08016DC0u, 120 },
    { "HandleEndTurn_RanFromBattle", 0x08013DB0u, 0x08016E38u, 108 },
    { "HandleEndTurn_MonFled", 0x08013E1Cu, 0x08016EA4u, 84 },
    { "HandleEndTurn_FinishBattle", 0x08013E70u, 0x08016EF8u, 268 },
    { "FreeResetData_ReturnToOvOrDoEvolutions", 0x08013F7Cu, 0x08017004u, 80 },
    { "TryEvolvePokemon", 0x08013FCCu, 0x08017054u, 144 },
    { "WaitForEvoSceneToFinish", 0x0801405Cu, 0x080170E4u, 40 },
    { "ReturnFromBattleToOverworld", 0x08014084u, 0x0801710Cu, 164 },
    { "RunBattleScriptCommands_PopCallbacksStack", 0x08014128u, 0x080171B0u, 104 },
    { "RunBattleScriptCommands", 0x08014190u, 0x08017218u, 44 },
};

const unsigned int gGermanBattleEndTurnSymbolCount =
    sizeof(gGermanBattleEndTurnSymbols) / sizeof(gGermanBattleEndTurnSymbols[0]);
