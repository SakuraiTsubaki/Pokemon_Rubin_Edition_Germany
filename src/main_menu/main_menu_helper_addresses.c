#include <stdint.h>

/*
 * Address scaffold for the post-intro helper tail of the German main-menu
 * module. Statement-level C promotion is kept separate from the address map.
 */

struct GermanMainMenuHelperAddress
{
    const char *name;
    uint32_t retailAddress;
    uint32_t debugAddress;
};

const struct GermanMainMenuHelperAddress gGermanMainMenuHelpers[] =
{
    { "CB_ContinueNewGameSpeechPart2", 0x0800B234u, 0x0800B414u },
    { "nullsub_34", 0x0800B410u, 0x0800B5F0u },
    { "ShrinkPlayerSprite", 0x0800B414u, 0x0800B5F4u },
    { "CreateAzurillSprite", 0x0800B430u, 0x0800B610u },
    { "AddBirchSpeechObjects", 0x0800B4A0u, 0x0800B680u },
    { "Task_SpriteFadeOut", 0x0800B5C0u, 0x0800B7A0u },
    { "StartSpriteFadeOut", 0x0800B62Cu, 0x0800B80Cu },
    { "Task_SpriteFadeIn", 0x0800B69Cu, 0x0800B87Cu },
    { "StartSpriteFadeIn", 0x0800B708u, 0x0800B8E8u },
    { "HandleFloorShadowFadeOut", 0x0800B77Cu, 0x0800B95Cu },
    { "StartBackgroundFadeOut", 0x0800B7E8u, 0x0800B9C8u },
    { "HandleFloorShadowFadeIn", 0x0800B828u, 0x0800BA08u },
    { "StartBackgroundFadeIn", 0x0800B894u, 0x0800BA74u },
    { "CreateGenderMenu", 0x0800B8D4u, 0x0800BAB4u },
    { "GenderMenuProcessInput", 0x0800B934u, 0x0800BB14u },
    { "CreateNameMenu", 0x0800B944u, 0x0800BB24u },
    { "NameMenuProcessInput", 0x0800B9CCu, 0x0800BBACu },
    { "SetPresetPlayerName", 0x0800B9DCu, 0x0800BBBCu },
};

const unsigned int gGermanMainMenuHelperCount =
    sizeof(gGermanMainMenuHelpers) / sizeof(gGermanMainMenuHelpers[0]);
