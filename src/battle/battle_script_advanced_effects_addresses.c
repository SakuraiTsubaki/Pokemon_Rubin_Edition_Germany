#include <stdint.h>

struct GermanBattleScriptAdvancedSymbol
{
    const char *name;
    uint8_t opcode;
    uint32_t retailAddress;
    uint32_t debugAddress;
    uint16_t spanToNextOpcode;
};

const struct GermanBattleScriptAdvancedSymbol gGermanBattleScriptAdvancedSymbols[] =
{
    { "atk80_manipulatedamage", 128, 0x08025A70u, 0x08029014u, 128 },
    { "atk81_trysetrest", 129, 0x08025AF0u, 0x08029094u, 208 },
    { "atk82_jumpifnotfirstturn", 130, 0x08025BC0u, 0x08029164u, 72 },
    { "atk83_nop", 131, 0x08025C08u, 0x080291ACu, 172 },
    { "atk84_jumpifcantmakeasleep", 132, 0x08025CB4u, 0x08029258u, 124 },
    { "atk85_stockpile", 133, 0x08025D30u, 0x080292D4u, 124 },
    { "atk86_stockpiletobasedamage", 134, 0x08025DACu, 0x08029350u, 296 },
    { "atk87_stockpiletohpheal", 135, 0x08025ED4u, 0x08029478u, 236 },
    { "atk88_negativedamage", 136, 0x08025FC0u, 0x08029564u, 1240 },
    { "atk89_statbuffchange", 137, 0x08026498u, 0x08029A3Cu, 84 },
    { "atk8A_normalisebuffs", 138, 0x080264ECu, 0x08029A90u, 84 },
    { "atk8B_setbide", 139, 0x08026540u, 0x08029AE4u, 112 },
    { "atk8C_confuseifrepeatingattackends", 140, 0x080265B0u, 0x08029B54u, 64 },
    { "atk8D_setmultihitcounter", 141, 0x080265F0u, 0x08029B94u, 76 },
    { "atk8E_initmultihitstring", 142, 0x0802663Cu, 0x08029BE0u, 296 },
    { "atk8F_forcerandomswitch", 143, 0x08026764u, 0x08029D08u, 764 },
    { "atk90_tryconversiontypechange", 144, 0x08026A60u, 0x0802A004u, 420 },
    { "atk91_givepaydaymoney", 145, 0x08026C04u, 0x0802A1A8u, 144 },
    { "atk92_setlightscreen", 146, 0x08026C94u, 0x0802A238u, 184 },
    { "atk93_tryKO", 147, 0x08026D4Cu, 0x0802A2F0u, 736 },
    { "atk94_damagetohalftargethp", 148, 0x0802702Cu, 0x0802A5D0u, 60 },
    { "atk95_setsandstorm", 149, 0x08027068u, 0x0802A60Cu, 88 },
    { "atk96_weatherdamage", 150, 0x080270C0u, 0x0802A664u, 376 },
    { "atk97_tryinfatuating", 151, 0x08027238u, 0x0802A7DCu, 468 },
    { "atk98_updatestatusicon", 152, 0x0802740Cu, 0x0802A9B0u, 272 },
    { "atk99_setmist", 153, 0x0802751Cu, 0x0802AAC0u, 148 },
    { "atk9A_setfocusenergy", 154, 0x080275B0u, 0x0802AB54u, 92 },
    { "atk9B_transformdataexecution", 155, 0x0802760Cu, 0x0802ABB0u, 416 },
    { "atk9C_setsubstitute", 156, 0x080277ACu, 0x0802AD50u, 260 },
    { "atk9D_mimicattackcopy", 157, 0x080278B0u, 0x0802AE54u, 476 },
    { "atk9E_metronome", 158, 0x08027A8Cu, 0x0802B030u, 168 },
    { "atk9F_dmgtolevel", 159, 0x08027B34u, 0x0802B198u, 48 },
};

const unsigned int gGermanBattleScriptAdvancedSymbolCount =
    sizeof(gGermanBattleScriptAdvancedSymbols) / sizeof(gGermanBattleScriptAdvancedSymbols[0]);
