#include <stdint.h>

struct GermanBattleScriptLateGen3Symbol
{
    const char *name;
    uint8_t opcode;
    uint32_t retailAddress;
    uint32_t debugAddress;
    uint16_t spanToNextOpcode;
};

const struct GermanBattleScriptLateGen3Symbol gGermanBattleScriptLateGen3Symbols[] =
{
    { "atkC0_recoverbasedonsunlight", 192, 0x08029850u, 0x0802CEB4u, 264 },
    { "atkC1_hiddenpowercalc", 193, 0x08029958u, 0x0802CFBCu, 296 },
    { "atkC2_selectfirstvalidtarget", 194, 0x08029A80u, 0x0802D0E4u, 116 },
    { "atkC3_trysetfutureattack", 195, 0x08029AF4u, 0x0802D158u, 296 },
    { "atkC4_trydobeatup", 196, 0x08029C1Cu, 0x0802D280u, 528 },
    { "atkC5_setsemiinvulnerablebit", 197, 0x08029E2Cu, 0x0802D490u, 132 },
    { "atkC6_clearsemiinvulnerablebit", 198, 0x08029EB0u, 0x0802D514u, 144 },
    { "atkC7_setminimize", 199, 0x08029F40u, 0x0802D5A4u, 64 },
    { "atkC8_sethail", 200, 0x08029F80u, 0x0802D5E4u, 88 },
    { "atkC9_jumpifattackandspecialattackcannotfall", 201, 0x08029FD8u, 0x0802D63Cu, 156 },
    { "atkCA_setforcedtarget", 202, 0x0802A074u, 0x0802D6D8u, 76 },
    { "atkCB_setcharge", 203, 0x0802A0C0u, 0x0802D724u, 100 },
    { "atkCC_callenvironmentattack", 204, 0x0802A124u, 0x0802D788u, 116 },
    { "atkCD_cureifburnedparalysedorpoisoned", 205, 0x0802A198u, 0x0802D7FCu, 132 },
    { "atkCE_settorment", 206, 0x0802A21Cu, 0x0802D880u, 88 },
    { "atkCF_jumpifnodamage", 207, 0x0802A274u, 0x0802D8D8u, 92 },
    { "atkD0_settaunt", 208, 0x0802A2D0u, 0x0802D934u, 116 },
    { "atkD1_trysethelpinghand", 209, 0x0802A344u, 0x0802D9A8u, 168 },
    { "atkD2_tryswapitems", 210, 0x0802A3ECu, 0x0802DA50u, 664 },
    { "atkD3_trycopyability", 211, 0x0802A684u, 0x0802DCE8u, 120 },
    { "atkD4_trywish", 212, 0x0802A6FCu, 0x0802DD60u, 212 },
    { "atkD5_trysetroots", 213, 0x0802A7D0u, 0x0802DE34u, 88 },
    { "atkD6_doubledamagedealtifdamaged", 214, 0x0802A828u, 0x0802DE8Cu, 104 },
    { "atkD7_setyawn", 215, 0x0802A890u, 0x0802DEF4u, 112 },
    { "atkD8_setdamagetohealthdifference", 216, 0x0802A900u, 0x0802DF64u, 108 },
    { "atkD9_scaledamagebyhealthratio", 217, 0x0802A96Cu, 0x0802DFD0u, 100 },
    { "atkDA_tryswapabilities", 218, 0x0802A9D0u, 0x0802E034u, 152 },
    { "atkDB_tryimprison", 219, 0x0802AA68u, 0x0802E0CCu, 256 },
    { "atkDC_trysetgrudge", 220, 0x0802AB68u, 0x0802E1CCu, 88 },
    { "atkDD_weightdamagecalculation", 221, 0x0802ABC0u, 0x0802E224u, 152 },
    { "atkDE_assistattackselect", 222, 0x0802AC58u, 0x0802E2BCu, 376 },
    { "atkDF_trysetmagiccoat", 223, 0x0802ADD0u, 0x0802E434u, 132 },
};

const unsigned int gGermanBattleScriptLateGen3SymbolCount =
    sizeof(gGermanBattleScriptLateGen3Symbols) / sizeof(gGermanBattleScriptLateGen3Symbols[0]);
