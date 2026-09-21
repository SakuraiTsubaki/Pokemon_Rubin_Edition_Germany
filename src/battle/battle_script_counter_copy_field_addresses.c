#include <stdint.h>

struct GermanBattleScriptFieldRuleSymbol
{
    const char *name;
    uint8_t opcode;
    uint32_t retailAddress;
    uint32_t debugAddress;
    uint16_t spanToNextOpcode;
};

const struct GermanBattleScriptFieldRuleSymbol gGermanBattleScriptFieldRuleSymbols[] =
{
    { "atkA0_psywavedamageeffect", 160, 0x08027B64u, 0x0802B1C8u, 84 },
    { "atkA1_counterdamagecalculator", 161, 0x08027BB8u, 0x0802B21Cu, 248 },
    { "atkA2_mirrorcoatdamagecalculator", 162, 0x08027CB0u, 0x0802B314u, 248 },
    { "atkA3_disablelastusedattack", 163, 0x08027DA8u, 0x0802B40Cu, 324 },
    { "atkA4_trysetencore", 164, 0x08027EECu, 0x0802B550u, 308 },
    { "atkA5_painsplitdmgcalc", 165, 0x08028020u, 0x0802B684u, 248 },
    { "atkA6_settypetorandomresistance", 166, 0x08028118u, 0x0802B77Cu, 504 },
    { "atkA7_setalwayshitflag", 167, 0x08028310u, 0x0802B974u, 88 },
    { "atkA8_copymovepermanently", 168, 0x08028368u, 0x0802B9CCu, 652 },
    { "atkA9_trychoosesleeptalkmove", 169, 0x080285F4u, 0x0802BC58u, 312 },
    { "atkAA_setdestinybond", 170, 0x0802872Cu, 0x0802BD90u, 144 },
    { "atkAB_trysetdestinybondtohappen", 171, 0x080287BCu, 0x0802BE20u, 24 },
    { "atkAC_remaininghptopower", 172, 0x080287D4u, 0x0802BE38u, 104 },
    { "atkAD_tryspiteppreduce", 173, 0x0802883Cu, 0x0802BEA0u, 496 },
    { "atkAE_healpartystatus", 174, 0x08028A2Cu, 0x0802C090u, 636 },
    { "atkAF_cursetarget", 175, 0x08028CA8u, 0x0802C30Cu, 156 },
    { "atkB0_trysetspikes", 176, 0x08028D44u, 0x0802C3A8u, 140 },
    { "atkB1_setforesight", 177, 0x08028DD0u, 0x0802C434u, 48 },
    { "atkB2_trysetperishsong", 178, 0x08028E00u, 0x0802C464u, 184 },
    { "atkB3_rolloutdamagecalculation", 179, 0x08028EB8u, 0x0802C51Cu, 380 },
    { "atkB4_jumpifconfusedandstatmaxed", 180, 0x08029034u, 0x0802C698u, 104 },
    { "atkB5_furycuttercalc", 181, 0x0802909Cu, 0x0802C700u, 180 },
    { "atkB6_happinesstodamagecalculation", 182, 0x08029150u, 0x0802C7B4u, 132 },
    { "atkB7_presentdamagecalculation", 183, 0x080291D4u, 0x0802C838u, 188 },
    { "atkB8_setsafeguard", 184, 0x08029290u, 0x0802C8F4u, 144 },
    { "atkB9_magnitudedamagecalculation", 185, 0x08029320u, 0x0802C984u, 292 },
    { "atkBA_jumpifnopursuitswitchdmg", 186, 0x08029444u, 0x0802CAA8u, 376 },
    { "atkBB_setsunny", 187, 0x080295BCu, 0x0802CC20u, 88 },
    { "atkBC_maxattackhalvehp", 188, 0x08029614u, 0x0802CC78u, 128 },
    { "atkBD_copyfoestats", 189, 0x08029694u, 0x0802CCF8u, 72 },
    { "atkBE_rapidspinfree", 190, 0x080296DCu, 0x0802CD40u, 324 },
    { "atkBF_setdefensecurlbit", 191, 0x08029820u, 0x0802CE84u, 48 },
};

const unsigned int gGermanBattleScriptFieldRuleSymbolCount =
    sizeof(gGermanBattleScriptFieldRuleSymbols) / sizeof(gGermanBattleScriptFieldRuleSymbols[0]);
