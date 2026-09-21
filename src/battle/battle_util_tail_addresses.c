#include <stdint.h>

struct GermanBattleUtilTailSymbol
{
    const char *name;
    uint32_t retailAddress;
    uint32_t debugAddress;
    uint16_t retailSize;
    uint16_t debugSize;
};

const struct GermanBattleUtilTailSymbol gGermanBattleUtilTailSymbols[] =
{
    { "ItemBattleEffects", 0x0801A200u, 0x0801D754u, 5088, 5088 },
    { "unref_sub_801B40C", 0x0801B5E0u, 0x0801EB34u, 392, 392 },
    { "sub_801B594", 0x0801B768u, 0x0801ECBCu, 44, 44 },
    { "GetMoveTarget", 0x0801B794u, 0x0801ECE8u, 872, 872 },
    { "IsMonDisobedient", 0x0801BAFCu, 0x0801F050u, 1760, 1796 },
};

const unsigned int gGermanBattleUtilTailSymbolCount =
    sizeof(gGermanBattleUtilTailSymbols) / sizeof(gGermanBattleUtilTailSymbols[0]);
