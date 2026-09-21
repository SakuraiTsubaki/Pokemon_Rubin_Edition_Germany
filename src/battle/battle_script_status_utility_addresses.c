#include <stdint.h>

struct GermanBattleScriptUtilitySymbol
{
    const char *name;
    uint8_t opcode;
    uint32_t retailAddress;
    uint32_t debugAddress;
    uint16_t spanToNextOpcode;
};

const struct GermanBattleScriptUtilitySymbol gGermanBattleScriptUtilitySymbols[] =
{
    { "atk60_incrementgamestat", 96, 0x0802446Cu, 0x08027A10u, 48 },
    { "atk61_drawpartystatussummary", 97, 0x0802449Cu, 0x08027A40u, 200 },
    { "atk62_hidepartystatussummary", 98, 0x08024564u, 0x08027B08u, 48 },
    { "atk63_jumptorandomattack", 99, 0x08024594u, 0x08027B38u, 100 },
    { "atk64_statusanimation", 100, 0x080245F8u, 0x08027B9Cu, 144 },
    { "atk65_status2animation", 101, 0x08024688u, 0x08027C2Cu, 168 },
    { "atk66_chosenstatusanimation", 102, 0x08024730u, 0x08027CD4u, 148 },
    { "atk67_yesnobox", 103, 0x080247C4u, 0x08027D68u, 176 },
    { "atk68_cancelallactions", 104, 0x08024874u, 0x08027E18u, 56 },
    { "atk69_adjustsetdamage", 105, 0x080248ACu, 0x08027E50u, 380 },
    { "atk6A_removeitem", 106, 0x08024A28u, 0x08027FCCu, 108 },
    { "atk6B_atknameinbuff1", 107, 0x08024A94u, 0x08028038u, 60 },
    { "atk6C_drawlvlupbox", 108, 0x08024AD0u, 0x08028074u, 848 },
    { "atk6D_resetsentmonsvalue", 109, 0x08024E20u, 0x080283C4u, 24 },
    { "atk6E_setatktoplayer0", 110, 0x08024E38u, 0x080283DCu, 32 },
    { "atk6F_makevisible", 111, 0x08024E58u, 0x080283FCu, 52 },
    { "atk70_recordlastability", 112, 0x08024E8Cu, 0x08028430u, 92 },
    { "atk71_buffermovetolearn", 113, 0x08024EE8u, 0x0802848Cu, 24 },
    { "atk72_jumpifplayerran", 114, 0x08024F00u, 0x080284A4u, 68 },
    { "atk73_hpthresholds", 115, 0x08024F44u, 0x080284E8u, 188 },
    { "atk74_hpthresholds2", 116, 0x08025000u, 0x080285A4u, 188 },
    { "atk75_useitemonopponent", 117, 0x080250BCu, 0x08028660u, 88 },
    { "atk76_various", 118, 0x08025114u, 0x080286B8u, 496 },
    { "atk77_setprotectlike", 119, 0x08025304u, 0x080288A8u, 316 },
    { "atk78_faintifabilitynotdamp", 120, 0x08025440u, 0x080289E4u, 284 },
    { "atk79_setatkhptozero", 121, 0x0802555Cu, 0x08028B00u, 96 },
    { "atk7A_jumpifnexttargetvalid", 122, 0x080255BCu, 0x08028B60u, 164 },
    { "atk7B_tryhealhalfhealth", 123, 0x08025660u, 0x08028C04u, 124 },
    { "atk7C_trymirrormove", 124, 0x080256DCu, 0x08028C80u, 456 },
    { "atk7D_setrain", 125, 0x080258A4u, 0x08028E48u, 84 },
    { "atk7E_setreflect", 126, 0x080258F8u, 0x08028E9Cu, 184 },
    { "atk7F_setseeded", 127, 0x080259B0u, 0x08028F54u, 192 },
};

const unsigned int gGermanBattleScriptUtilitySymbolCount =
    sizeof(gGermanBattleScriptUtilitySymbols) / sizeof(gGermanBattleScriptUtilitySymbols[0]);
