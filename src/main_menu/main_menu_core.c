#include "german_ruby/main_menu.h"

/*
 * Initial high-level reconstruction of the German main-menu module.
 *
 * This file intentionally promotes only routines whose behavior and German
 * layout constants have already been tied back to the supplied binaries.
 * The full menu task state machine is mapped in manifests/main-menu-symbols.json
 * and will be promoted incrementally.
 */

#define EOS 0xFF

#if defined(GERMAN_RUBY_DEBUG)
#define SAVE_BLOCK2_BASE ((uintptr_t)0x02025148u)
#else
#define SAVE_BLOCK2_BASE ((uintptr_t)0x02024EA4u)
#endif

#define SAVE_PLAYER_NAME       ((uint8_t *)(SAVE_BLOCK2_BASE + 0x00u))
#define SAVE_PLAYER_GENDER     (*(volatile uint8_t *)(SAVE_BLOCK2_BASE + 0x08u))
#define SAVE_PLAY_TIME_HOURS   (*(volatile uint16_t *)(SAVE_BLOCK2_BASE + 0x0Eu))
#define SAVE_PLAY_TIME_MINUTES (*(volatile uint8_t *)(SAVE_BLOCK2_BASE + 0x10u))

extern void RunTasks(void);
extern void AnimateSprites(void);
extern void BuildOamBuffer(void);
extern void UpdatePaletteFade(void);
extern void LoadOam(void);
extern void ProcessSpriteCopyRequests(void);
extern void TransferPlttBuffer(void);

extern uint32_t InitMainMenu(uint8_t fromOptions);

extern void Menu_PrintText(const uint8_t *text, uint8_t left, uint8_t top);
extern void Menu_PrintTextPixelCoords(const uint8_t *text, uint16_t x, uint16_t y, uint8_t copyToVram);
extern void FormatPlayTime(uint8_t *dest, uint16_t hours, uint8_t minutes, uint8_t mode);
extern void AlignStringInMenuWindow(uint8_t *dest, const uint8_t *src, uint8_t width, uint8_t mode);
extern void AlignInt1InMenuWindow(uint8_t *dest, uint16_t value, uint8_t width, uint8_t mode);
extern uint16_t GetPokedexSeenCount(void);
extern uint8_t GetBadgeCount(void);
extern uint8_t *ConvertIntToDecimalString(uint8_t *dest, int32_t value);

extern const uint8_t gMainMenuString_Player[];
extern const uint8_t gMainMenuString_Time[];
extern const uint8_t gMainMenuString_Pokedex[];
extern const uint8_t gMainMenuString_Badges[];

/* German retail 0x08009890; German Debug 0x08009A70. */
void CB2_MainMenu(void)
{
    RunTasks();
    AnimateSprites();
    BuildOamBuffer();
    UpdatePaletteFade();
}

/* German retail 0x080098A8; German Debug 0x08009A88. */
void VBlankCB_MainMenu(void)
{
    LoadOam();
    ProcessSpriteCopyRequests();
    TransferPlttBuffer();
}

/* German retail 0x080098BC; German Debug 0x08009A9C. */
void CB2_InitMainMenu(void)
{
    InitMainMenu(0);
}

/* German retail 0x080098C8; German Debug 0x08009AA8. */
static void CB2_InitMainMenuFromOptions(void)
{
    InitMainMenu(1);
}

/* German retail 0x0800A2EC; German Debug 0x0800A4CC. */
static void PrintPlayerName(void)
{
    Menu_PrintText(gMainMenuString_Player, 2, 3);
    Menu_PrintText(SAVE_PLAYER_NAME, 9, 3);
}

/*
 * German retail 0x0800A310; German Debug 0x0800A4F0.
 *
 * German-specific layout recovered directly from the binaries:
 *   TIME label: pixel x=124, y=24
 *   formatted play-time alignment width: 40 px
 *   aligned value: tile column 23, row 3
 */
static void PrintPlayTime(void)
{
    uint8_t playTime[16];
    uint8_t alignedPlayTime[32];

    Menu_PrintTextPixelCoords(gMainMenuString_Time, 124, 24, 1);
    FormatPlayTime(playTime, SAVE_PLAY_TIME_HOURS, SAVE_PLAY_TIME_MINUTES, 1);
    AlignStringInMenuWindow(alignedPlayTime, playTime, 40, 1);
    Menu_PrintText(alignedPlayTime, 23, 3);
}

/* German retail 0x0800A358; German Debug 0x0800A538. */
static void PrintPokedexCount(void)
{
    uint8_t buffer[16];

    Menu_PrintText(gMainMenuString_Pokedex, 2, 5);
    AlignInt1InMenuWindow(buffer, GetPokedexSeenCount(), 18, 0);
    Menu_PrintText(buffer, 9, 5);
}

/*
 * German retail 0x0800A390; German Debug 0x0800A570.
 *
 * German-specific layout:
 *   BADGES label: pixel x=124, y=40
 *   numeric count: pixel x=205, y=40
 */
static void PrintBadgeCount(void)
{
    uint8_t buffer[16];

    Menu_PrintTextPixelCoords(gMainMenuString_Badges, 124, 40, 1);
    ConvertIntToDecimalString(buffer, GetBadgeCount());
    Menu_PrintTextPixelCoords(buffer, 205, 40, 1);
}

/* German retail 0x0800A2D4; German Debug 0x0800A4B4. */
static void PrintSaveFileInfo(void)
{
    PrintPlayerName();
    PrintPokedexCount();
    PrintPlayTime();
    PrintBadgeCount();
}
