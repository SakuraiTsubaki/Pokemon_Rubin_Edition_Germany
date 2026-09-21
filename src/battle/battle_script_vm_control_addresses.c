#include <stdint.h>

struct GermanBattleScriptControlSymbol
{
    const char *name;
    uint8_t opcode;
    uint32_t retailAddress;
    uint32_t debugAddress;
    uint16_t codeSpan;
};

const struct GermanBattleScriptControlSymbol gGermanBattleScriptControlSymbols[] =
{
    { "atk30_subbyte", 48, 0x08021164u, 0x08024708u, 44 },
    { "atk31_copyarray", 49, 0x08021190u, 0x08024734u, 84 },
    { "atk32_copyarraywithindex", 50, 0x080211E4u, 0x08024788u, 108 },
    { "atk33_orbyte", 51, 0x08021250u, 0x080247F4u, 44 },
    { "atk34_orhalfword", 52, 0x0802127Cu, 0x08024820u, 56 },
    { "atk35_orword", 53, 0x080212B4u, 0x08024858u, 68 },
    { "atk36_bicbyte", 54, 0x080212F8u, 0x0802489Cu, 44 },
    { "atk37_bichalfword", 55, 0x08021324u, 0x080248C8u, 56 },
    { "atk38_bicword", 56, 0x0802135Cu, 0x08024900u, 68 },
    { "atk39_pause", 57, 0x080213A0u, 0x08024944u, 64 },
    { "atk3A_waitstate", 58, 0x080213E0u, 0x08024984u, 32 },
    { "atk3B_healthbar_update", 59, 0x08021400u, 0x080249A4u, 88 },
    { "atk3C_return", 60, 0x08021458u, 0x080249FCu, 12 },
    { "atk3D_end", 61, 0x08021464u, 0x08024A08u, 32 },
    { "atk3E_end2", 62, 0x08021484u, 0x08024A28u, 24 },
    { "atk3F_end3", 63, 0x0802149Cu, 0x08024A40u, 48 },
    { "atk41_call", 65, 0x080214CCu, 0x08024A70u, 48 },
    { "atk42_jumpiftype2", 66, 0x080214FCu, 0x08024AA0u, 92 },
    { "atk43_jumpifabilitypresent", 67, 0x08021558u, 0x08024AFCu, 76 },
    { "atk44_endselectionscript", 68, 0x080215A4u, 0x08024B48u, 32 },
    { "atk45_playanimation", 69, 0x080215C4u, 0x08024B68u, 196 },
    { "atk46_playanimation2", 70, 0x08021688u, 0x08024C2Cu, 204 },
    { "atk47_setgraphicalstatchangevalues", 71, 0x08021754u, 0x08024CF8u, 124 },
    { "atk48_playstatchangeanimation", 72, 0x080217D0u, 0x08024D74u, 508 },
    { "atk49_moveend", 73, 0x080219CCu, 0x08024F70u, 2788 },
};

const unsigned int gGermanBattleScriptControlSymbolCount =
    sizeof(gGermanBattleScriptControlSymbols) / sizeof(gGermanBattleScriptControlSymbols[0]);
