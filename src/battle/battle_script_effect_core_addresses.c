#include <stdint.h>

struct GermanBattleEffectCoreSymbol
{
    const char *name;
    uint32_t retailAddress;
    uint32_t debugAddress;
    uint16_t retailSize;
    uint16_t debugSize;
};

const struct GermanBattleEffectCoreSymbol gGermanBattleEffectCoreSymbols[] =
{
    { "atk09_attackanimation", 0x0801DAC0u, 0x08021038u, 372, 372 },
    { "atk0A_waitanimation", 0x0801DC34u, 0x080211ACu, 32, 32 },
    { "atk0B_healthbarupdate", 0x0801DC54u, 0x080211CCu, 204, 204 },
    { "atk0C_datahpupdate", 0x0801DD20u, 0x08021298u, 1020, 1020 },
    { "atk0D_critmessage", 0x0801E11Cu, 0x08021694u, 84, 84 },
    { "atk0E_effectivenesssound", 0x0801E170u, 0x080216E8u, 208, 208 },
    { "atk0F_resultmessage", 0x0801E240u, 0x080217B8u, 432, 432 },
    { "atk10_printstring", 0x0801E3F0u, 0x08021968u, 64, 64 },
    { "atk11_printselectionstring", 0x0801E430u, 0x080219A8u, 68, 68 },
    { "atk12_waitmessage", 0x0801E474u, 0x080219ECu, 92, 92 },
    { "atk13_printfromtable", 0x0801E4D0u, 0x08021A48u, 84, 84 },
    { "atk14_printselectionstringfromtable", 0x0801E524u, 0x08021A9Cu, 100, 100 },
    { "GetBattlerTurnOrderNum", 0x0801E588u, 0x08021B00u, 56, 56 },
    { "SetMoveEffect", 0x0801E5C0u, 0x08021B38u, 4648, 4648 },
    { "atk15_seteffectwithchance", 0x0801F7E8u, 0x08022D60u, 244, 288 },
    { "atk16_seteffectprimary", 0x0801F8DCu, 0x08022E80u, 16, 16 },
};

const unsigned int gGermanBattleEffectCoreSymbolCount =
    sizeof(gGermanBattleEffectCoreSymbols) / sizeof(gGermanBattleEffectCoreSymbols[0]);
