#include <stdint.h>

struct GermanBattleMainInitSymbol
{
    const char *name;
    uint32_t retailAddress;
    uint32_t debugAddress;
    uint16_t retailSize;
    uint16_t debugSize;
};

const struct GermanBattleMainInitSymbol gGermanBattleMainInitSymbols[] =
{
    { "CB2_InitBattle", 0x0800E998u, 0x0800EC0Cu, 52, 52 },
    { "CB2_InitBattleInternal", 0x0800E9CCu, 0x0800EC40u, 500, 532 },
    { "BufferPartyVsScreenHealth_AtStart", 0x0800EBC0u, 0x0800EE54u, 192, 192 },
    { "SetPlayerBerryDataInBattleStruct", 0x0800EC80u, 0x0800EF14u, 92, 92 },
    { "SetAllPlayersBerryData", 0x0800ECDCu, 0x0800EF70u, 316, 316 },
    { "TryCorrectShedinjaLanguage", 0x0800EE18u, 0x0800F0ACu, 88, 88 },
    { "CB2_HandleStartBattle", 0x0800EE70u, 0x0800F104u, 912, 956 },
};

const unsigned int gGermanBattleMainInitSymbolCount =
    sizeof(gGermanBattleMainInitSymbols) / sizeof(gGermanBattleMainInitSymbols[0]);
