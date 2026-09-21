#include <stdint.h>

struct GermanBattleMainLinkSymbol
{
    const char *name;
    uint32_t retailAddress;
    uint32_t debugAddress;
    uint16_t retailSize;
    uint16_t debugSize;
};

const struct GermanBattleMainLinkSymbol gGermanBattleMainLinkSymbols[] =
{
    { "PrepareOwnMultiPartnerBuffer", 0x0800F200u, 0x0800F4C0u, 216, 216 },
    { "sub_800F104", 0x0800F2D8u, 0x0800F598u, 404, 452 },
    { "CB2_HandleStartMultiBattle", 0x0800F46Cu, 0x0800F75Cu, 1392, 1436 },
    { "BattleMainCB2", 0x0800F9DCu, 0x0800FCF8u, 48, 248 },
    { "sub_800F828", 0x0800FA0Cu, 0x0800FDF0u, 16, 16 },
    { "sub_800F838", 0x0800FA1Cu, 0x0800FE00u, 160, 160 },
    { "CreateNPCTrainerParty", 0x0800FABCu, 0x0800FEA0u, 1004, 1004 },
    { "sub_800FCD4", 0x0800FEA8u, 0x0801028Cu, 40, 40 },
    { "sub_800FCFC", 0x0800FED0u, 0x080102B4u, 176, 176 },
    { "nullsub_36", 0x0800FF80u, 0x08010364u, 4, 4 },
    { "sub_800FDB0", 0x0800FF84u, 0x08010368u, 112, 112 },
    { "sub_800FE20", 0x0800FFF4u, 0x080103D8u, 32, 32 },
    { "sub_800FE40", 0x08010014u, 0x080103F8u, 468, 468 },
    { "c2_8011A1C", 0x080101E8u, 0x080105CCu, 420, 420 },
    { "sub_80101B8", 0x0801038Cu, 0x08010770u, 28, 28 },
    { "c2_081284E0", 0x080103A8u, 0x0801078Cu, 116, 116 },
};

const unsigned int gGermanBattleMainLinkSymbolCount =
    sizeof(gGermanBattleMainLinkSymbols) / sizeof(gGermanBattleMainLinkSymbols[0]);
