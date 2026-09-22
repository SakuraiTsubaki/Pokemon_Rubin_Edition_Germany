#include <stdint.h>

struct GermanPokemon1Symbol
{
    const char *name;
    uint32_t retailAddress;
    uint32_t debugAddress;
    uint16_t codeSize;
};

const struct GermanPokemon1Symbol gGermanPokemon1Symbols[] =
{
    { "ZeroBoxMonData", 0x0803A894u, 0x0803E768u, 24 },
    { "ZeroMonData", 0x0803A8ACu, 0x0803E780u, 128 },
    { "ZeroPlayerPartyMons", 0x0803A92Cu, 0x0803E800u, 32 },
    { "ZeroEnemyPartyMons", 0x0803A94Cu, 0x0803E820u, 32 },
    { "CreateMon", 0x0803A96Cu, 0x0803E840u, 112 },
    { "CreateBoxMon", 0x0803A9DCu, 0x0803E8B0u, 724 },
    { "CreateMonWithNature", 0x0803ACB0u, 0x0803EB84u, 104 },
    { "CreateMonWithGenderNatureLetter", 0x0803AD18u, 0x0803EBECu, 256 },
    { "CreateMaleMon", 0x0803AE18u, 0x0803ECECu, 104 },
    { "CreateMonWithIVsPersonality", 0x0803AE80u, 0x0803ED54u, 64 },
    { "CreateMonWithIVsOTID", 0x0803AEC0u, 0x0803ED94u, 116 },
    { "CreateMonWithEVSpread", 0x0803AF34u, 0x0803EE08u, 136 },
    { "sub_803ADE8", 0x0803AFBCu, 0x0803EE90u, 400 },
    { "sub_803AF78", 0x0803B14Cu, 0x0803F020u, 428 },
    { "CalculateBoxMonChecksum", 0x0803B2F8u, 0x0803F1CCu, 148 },
    { "CalculateMonStats", 0x0803B38Cu, 0x0803F260u, 764 },
    { "ExpandBoxMon", 0x0803B688u, 0x0803F804u, 80 },
    { "GetLevelFromMonExp", 0x0803B6D8u, 0x0803F854u, 108 },
    { "GetLevelFromBoxMonExp", 0x0803B744u, 0x0803F8C0u, 108 },
    { "GiveMoveToMon", 0x0803B7B0u, 0x0803F92Cu, 20 },
    { "GiveMoveToBoxMon", 0x0803B7C4u, 0x0803F940u, 112 },
    { "GiveMoveToBattleMon", 0x0803B834u, 0x0803F9B0u, 68 },
    { "SetMonMoveSlot", 0x0803B878u, 0x0803F9F4u, 64 },
    { "SetBattleMonMoveSlot", 0x0803B8B8u, 0x0803FA34u, 48 },
    { "GiveMonInitialMoveset", 0x0803B8E8u, 0x0803FA64u, 12 },
    { "GiveBoxMonInitialMoveset", 0x0803B8F4u, 0x0803FA70u, 168 },
    { "MonTryLearningNewMove", 0x0803B99Cu, 0x0803FB18u, 268 },
    { "DeleteFirstMoveAndGiveMoveToMon", 0x0803BAA8u, 0x0803FC24u, 172 },
    { "DeleteFirstMoveAndGiveMoveToBoxMon", 0x0803BB54u, 0x0803FCD0u, 172 },
};

const unsigned int gGermanPokemon1SymbolCount =
    sizeof(gGermanPokemon1Symbols) / sizeof(gGermanPokemon1Symbols[0]);

const uint32_t gGermanPokemon1DebugGenderTestRecalcStats = 0x0803F55Cu;
