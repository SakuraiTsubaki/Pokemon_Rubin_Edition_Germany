#include <stdint.h>

struct GermanBattleUtilSymbol
{
    const char *name;
    uint32_t retailAddress;
    uint32_t debugAddress;
    uint16_t codeSpan;
};

const struct GermanBattleUtilSymbol gGermanBattleUtilFoundation[] =
{
    { "GetBattlerForBattleScript", 0x08015324u, 0x080183ACu, 132 },
    { "PressurePPLose", 0x080153A8u, 0x08018430u, 200 },
    { "PressurePPLoseOnUsingImprision", 0x08015470u, 0x080184F8u, 308 },
    { "PressurePPLoseOnUsingPerishSong", 0x080155A4u, 0x0801862Cu, 276 },
    { "MarkAllBattlersForControllerExec", 0x080156B8u, 0x08018740u, 112 },
    { "MarkBattlerForControllerExec", 0x08015728u, 0x080187B0u, 80 },
    { "sub_80155A4", 0x08015778u, 0x08018800u, 80 },
    { "CancelMultiTurnMoves", 0x080157C8u, 0x08018850u, 108 },
    { "WasUnableToUseMove", 0x08015834u, 0x080188BCu, 88 },
    { "PrepareStringBattle", 0x0801588Cu, 0x08018914u, 36 },
    { "ResetSentPokesToOpponentValue", 0x080158B0u, 0x08018938u, 100 },
    { "sub_8015740", 0x08015914u, 0x0801899Cu, 132 },
    { "sub_80157C4", 0x08015998u, 0x08018A20u, 104 },
    { "BattleScriptPush", 0x08015A00u, 0x08018A88u, 32 },
    { "BattleScriptPushCursor", 0x08015A20u, 0x08018AA8u, 36 },
    { "BattleScriptPop", 0x08015A44u, 0x08018ACCu, 36 },
    { "TrySetCantSelectMoveBattleScript", 0x08015A68u, 0x08018AF0u, 516 },
    { "CheckMoveLimitations", 0x08015C6Cu, 0x08018CF4u, 504 },
    { "AreAllMovesUnusable", 0x08015E64u, 0x08018EECu, 204 },
    { "IsImprisoned", 0x08015F30u, 0x08018FB8u, 160 },
};

const unsigned int gGermanBattleUtilFoundationCount =
    sizeof(gGermanBattleUtilFoundation) / sizeof(gGermanBattleUtilFoundation[0]);
