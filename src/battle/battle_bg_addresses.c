#include <stdint.h>

struct GermanBattleBgSymbol
{
    const char *name;
    uint32_t retailAddress;
    uint32_t debugAddress;
    uint16_t retailSize;
    uint16_t debugSize;
};

const struct GermanBattleBgSymbol gGermanBattleBgSymbols[] =
{
    { "debug_sub_800D684", 0x0800D858u, 0x0800DA74u, 64, 64 },
    { "sub_800D6C4", 0x0800D898u, 0x0800DAB4u, 16, 16 },
    { "sub_800D6D4", 0x0800D8A8u, 0x0800DAC4u, 120, 120 },
    { "ApplyPlayerChosenFrameToBattleMenu", 0x0800D920u, 0x0800DB3Cu, 108, 108 },
    { "DrawMainBattleBackground", 0x0800D98Cu, 0x0800DBA8u, 768, 768 },
    { "LoadBattleTextboxAndBackground", 0x0800DC8Cu, 0x0800DEA8u, 64, 152 },
    { "sub_800DAF8", 0x0800DCCCu, 0x0800DF40u, 300, 300 },
    { "PrintLinkBattleWinLossTie", 0x0800DDF8u, 0x0800E06Cu, 524, 524 },
    { "InitLinkBattleVsScreen", 0x0800E004u, 0x0800E278u, 1036, 1036 },
    { "DrawBattleEntryBackground", 0x0800E410u, 0x0800E684u, 472, 472 },
    { "LoadChosenBattleElement", 0x0800E5E8u, 0x0800E85Cu, 944, 944 },
};

struct GermanBattleEnvironmentResourceSet
{
    uint32_t tileset;
    uint32_t tilemap;
    uint32_t entryTileset;
    uint32_t entryTilemap;
    uint32_t palette;
};

const struct GermanBattleEnvironmentResourceSet gGermanBattleEnvironmentResources[10] =
{
    { 0x08E5DED4u, 0x08E5E4BCu, 0x08E63A7Cu, 0x08E64004u, 0x08E5E484u }, /* GRASS */
    { 0x08E5E76Cu, 0x08E5EE24u, 0x08E641C0u, 0x08E648D0u, 0x08E5EDE4u }, /* LONG_GRASS */
    { 0x08E5F0D4u, 0x08E5F714u, 0x08E64B08u, 0x08E6504Cu, 0x08E5F6CCu }, /* SAND */
    { 0x08E5F9C4u, 0x08E5FFC4u, 0x08E651F4u, 0x08E656C0u, 0x08E5FF7Cu }, /* UNDERWATER */
    { 0x08E60274u, 0x08E6088Cu, 0x08E65850u, 0x08E65E5Cu, 0x08E60848u }, /* WATER */
    { 0x08E60B3Cu, 0x08E61124u, 0x08E66000u, 0x08E6654Cu, 0x08E610E4u }, /* POND */
    { 0x08E613D4u, 0x08E619D0u, 0x08E66698u, 0x08E66C78u, 0x08E61994u }, /* MOUNTAIN */
    { 0x08E61C80u, 0x08E622C0u, 0x08E66E0Cu, 0x08E67628u, 0x08E62278u }, /* CAVE */
    { 0x08E625ACu, 0x08E62B94u, 0x08E678D0u, 0x08E67CE0u, 0x08E636FCu }, /* BUILDING */
    { 0x08E625ACu, 0x08E62B94u, 0x08E678D0u, 0x08E67CE0u, 0x08E62570u }, /* PLAIN */
};
