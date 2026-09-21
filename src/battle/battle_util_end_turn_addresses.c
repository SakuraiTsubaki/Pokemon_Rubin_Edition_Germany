#include <stdint.h>

struct GermanBattleUtilEndTurnSymbol
{
    const char *name;
    uint32_t retailAddress;
    uint32_t debugAddress;
    uint16_t codeSpan;
};

const struct GermanBattleUtilEndTurnSymbol gGermanBattleUtilEndTurnSymbols[] =
{
    { "DoFieldEndTurnEffects", 0x08015FD0u, 0x08019058u, 1884 },
    { "TurnBasedEffects", 0x0801672Cu, 0x080197B4u, 2948 },
    { "HandleWishPerishSongOnTurnEnd", 0x080172B0u, 0x0801A338u, 712 },
    { "HandleFaintedMonActions", 0x08017578u, 0x0801A600u, 804 },
    { "TryClearRageStatuses", 0x0801789Cu, 0x0801A924u, 80 },
    { "AtkCanceller_UnableToUseMove", 0x080178ECu, 0x0801A974u, 2304 },
    { "sub_8018018", 0x080181ECu, 0x0801B274u, 416 },
    { "CastformDataTypeChange", 0x0801838Cu, 0x0801B414u, 364 },
};

const unsigned int gGermanBattleUtilEndTurnSymbolCount =
    sizeof(gGermanBattleUtilEndTurnSymbols) / sizeof(gGermanBattleUtilEndTurnSymbols[0]);
