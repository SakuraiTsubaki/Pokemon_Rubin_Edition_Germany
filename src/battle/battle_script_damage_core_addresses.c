#include <stdint.h>

struct GermanBattleDamageCoreSymbol
{
    const char *name;
    uint32_t retailAddress;
    uint32_t debugAddress;
    uint16_t codeSize;
};

const struct GermanBattleDamageCoreSymbol gGermanBattleDamageCoreSymbols[] =
{
    { "atk01_accuracycheck", 0x0801C490u, 0x0801FA08u, 908 },
    { "atk02_attackstring", 0x0801C81Cu, 0x0801FD94u, 84 },
    { "atk03_ppreduce", 0x0801C870u, 0x0801FDE8u, 476 },
    { "atk04_critcalc", 0x0801CA4Cu, 0x0801FFC4u, 372 },
    { "atk05_damagecalc", 0x0801CBC0u, 0x08020138u, 268 },
    { "AI_CalcDmg", 0x0801CCCCu, 0x08020244u, 244 },
    { "ModulateDmgByType", 0x0801CDC0u, 0x08020338u, 216 },
    { "atk06_typecalc", 0x0801CE98u, 0x08020410u, 632 },
    { "CheckWonderGuardAndLevitate", 0x0801D110u, 0x08020688u, 652 },
    { "ModulateDmgByType2", 0x0801D39Cu, 0x08020914u, 184 },
    { "TypeCalc", 0x0801D454u, 0x080209CCu, 476 },
    { "AI_TypeCalc", 0x0801D630u, 0x08020BA8u, 280 },
    { "Unused_ApplyRandomDmgMultiplier", 0x0801D748u, 0x08020CC0u, 60 },
    { "atk07_adjustnormaldamage", 0x0801D784u, 0x08020CFCu, 432 },
    { "atk08_adjustnormaldamage2", 0x0801D934u, 0x08020EACu, 396 },
};

const unsigned int gGermanBattleDamageCoreSymbolCount =
    sizeof(gGermanBattleDamageCoreSymbols) / sizeof(gGermanBattleDamageCoreSymbols[0]);
