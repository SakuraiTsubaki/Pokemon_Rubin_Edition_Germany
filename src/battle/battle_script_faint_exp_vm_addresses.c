#include <stdint.h>

struct GermanBattleScriptVmSymbol
{
    const char *name;
    uint8_t opcode;
    uint32_t retailAddress;
    uint32_t debugAddress;
    uint16_t codeSpan;
};

const struct GermanBattleScriptVmSymbol gGermanBattleScriptFaintExpVmSymbols[] =
{
    { "atk17_seteffectsecondary", 23, 0x0801F8ECu, 0x08022E90u, 16 },
    { "atk18_clearstatusfromeffect", 24, 0x0801F8FCu, 0x08022EA0u, 132 },
    { "atk19_tryfaintmon", 25, 0x0801F980u, 0x08022F24u, 904 },
    { "atk1A_dofaintanimation", 26, 0x0801FD08u, 0x080232ACu, 60 },
    { "atk1B_cleareffectsonfaint", 27, 0x0801FD44u, 0x080232E8u, 100 },
    { "atk1C_jumpifstatus", 28, 0x0801FDA8u, 0x0802334Cu, 120 },
    { "atk1D_jumpifstatus2", 29, 0x0801FE20u, 0x080233C4u, 120 },
    { "atk1E_jumpifability", 30, 0x0801FE98u, 0x0802343Cu, 240 },
    { "atk1F_jumpifsideaffecting", 31, 0x0801FF88u, 0x0802352Cu, 120 },
    { "atk20_jumpifstat", 32, 0x08020000u, 0x080235A4u, 248 },
    { "atk21_jumpifstatus3condition", 33, 0x080200F8u, 0x0802369Cu, 132 },
    { "atk22_jumpiftype", 34, 0x0802017Cu, 0x08023720u, 92 },
    { "atk23_getexp", 35, 0x080201D8u, 0x0802377Cu, 2480 },
    { "atk24", 36, 0x08020B88u, 0x0802412Cu, 488 },
    { "atk25_movevaluescleanup", 37, 0x08020D70u, 0x08024314u, 24 },
    { "atk26_setmultihit", 38, 0x08020D88u, 0x0802432Cu, 24 },
    { "atk27_decrementmultihit", 39, 0x08020DA0u, 0x08024344u, 72 },
    { "atk28_goto", 40, 0x08020DE8u, 0x0802438Cu, 32 },
    { "atk29_jumpifbyte", 41, 0x08020E08u, 0x080243ACu, 160 },
    { "atk2A_jumpifhalfword", 42, 0x08020EA8u, 0x0802444Cu, 168 },
    { "atk2B_jumpifword", 43, 0x08020F50u, 0x080244F4u, 180 },
    { "atk2C_jumpifarrayequal", 44, 0x08021004u, 0x080245A8u, 136 },
    { "atk2D_jumpifarraynotequal", 45, 0x0802108Cu, 0x08024630u, 132 },
    { "atk2E_setbyte", 46, 0x08021110u, 0x080246B4u, 40 },
    { "atk2F_addbyte", 47, 0x08021138u, 0x080246DCu, 44 },
};

const unsigned int gGermanBattleScriptFaintExpVmSymbolCount =
    sizeof(gGermanBattleScriptFaintExpVmSymbols) / sizeof(gGermanBattleScriptFaintExpVmSymbols[0]);
