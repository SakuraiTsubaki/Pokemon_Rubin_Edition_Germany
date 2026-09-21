#include <stdint.h>

struct GermanBattleScriptSwitchSymbol
{
    const char *name;
    uint8_t opcode;
    uint32_t retailAddress;
    uint32_t debugAddress;
    uint16_t spanToNextOpcode;
};

const struct GermanBattleScriptSwitchSymbol gGermanBattleScriptSwitchSymbols[] =
{
    { "atk4A_typecalc2", 74, 0x080224B0u, 0x08025A54u, 592 },
    { "atk4B_returnatktoball", 75, 0x08022700u, 0x08025CA4u, 80 },
    { "atk4C_getswitchedmondata", 76, 0x08022750u, 0x08025CF4u, 116 },
    { "atk4D_switchindataupdate", 77, 0x080227C4u, 0x08025D68u, 404 },
    { "atk4E_switchinanim", 78, 0x08022958u, 0x08025EFCu, 172 },
    { "atk4F_jumpifcantswitch", 79, 0x08022A04u, 0x08025FA8u, 616 },
    { "atk50_openpartyscreen", 80, 0x08022C6Cu, 0x08026210u, 2180 },
    { "atk51_switchhandleorder", 81, 0x080234F0u, 0x08026A94u, 520 },
    { "atk52_switchineffects", 82, 0x080236F8u, 0x08026C9Cu, 680 },
    { "atk53_trainerslidein", 83, 0x080239A0u, 0x08026F44u, 64 },
    { "atk54_playse", 84, 0x080239E0u, 0x08026F84u, 60 },
    { "atk55_fanfare", 85, 0x08023A1Cu, 0x08026FC0u, 60 },
    { "atk56_playfaintcry", 86, 0x08023A58u, 0x08026FFCu, 48 },
    { "atk57", 87, 0x08023A88u, 0x0802702Cu, 56 },
    { "atk58_returntoball", 88, 0x08023AC0u, 0x08027064u, 52 },
    { "atk59_handlelearnnewmove", 89, 0x08023AF4u, 0x08027098u, 472 },
    { "atk5A_yesnoboxlearnmove", 90, 0x08023CCCu, 0x08027270u, 892 },
    { "atk5B_yesnoboxstoplearningmove", 91, 0x08024048u, 0x080275ECu, 272 },
    { "atk5C_hitanimation", 92, 0x08024158u, 0x080276FCu, 144 },
    { "atk5D_getmoneyreward", 93, 0x080241E8u, 0x0802778Cu, 384 },
    { "atk5E", 94, 0x08024368u, 0x0802790Cu, 180 },
    { "atk5F_swapattackerwithtarget", 95, 0x0802441Cu, 0x080279C0u, 80 },
};

const unsigned int gGermanBattleScriptSwitchSymbolCount =
    sizeof(gGermanBattleScriptSwitchSymbols) / sizeof(gGermanBattleScriptSwitchSymbols[0]);
