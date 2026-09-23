# German title_screen module

The complete German `title_screen` text module has been bounded directly in the supplied Retail Rev 0, Retail Rev 1 and Debug ROMs.

## Module boundary

| Profile | Start | End exclusive | Size | SHA-256 |
| --- | --- | --- | ---: | --- |
| Retail Rev 0 / Rev 1 | 0x0807C1C0 | 0x0807CC5C | **2,716 bytes (0xA9C)** | `04b39c6221fdf7b12a2d274b0ced8c35d99e4c82490808b8a38b0d2c9368b2b4` |
| Debug | 0x08083434 | 0x08083F14 | **2,784 bytes (0xAE0)** | `e301c3aec31b83cd9038880e95e02f1e8908c5dfe8606b5920a8fc928e5f3a9f` |

Retail Rev 0 and Rev 1 are byte-identical across the complete module.

The Debug build adds **0x44 bytes**. Therefore the accumulated Retail-to-Debug text displacement changes from **+0x7274** at module entry to **+0x72B8** at module exit.

## Entry anchor

The first function is source-correlated as `SpriteCallback_VersionBannerLeft`.

The first 48 bytes are identical across all three profiles:

`10 B5 02 1C 30 20 11 5E 88 00 40 18 C0 00 09 49 44 18 0A 21 60 5E 00 28 0E D0 51 78 0D 20 40 42 08 40 50 70 54 20 50 84 3E 32 11 78 59 38 08 40 10 70`

The callback follows the task state attached to the version-banner sprite, slides the left banner toward its target Y position and drives the title-screen alpha blend.

## German title-screen layout

The connected German source configuration matches the German binary behavior and provides the semantic constants:

- version-banner OAM shape: **square**
- right banner tile offset: **128**
- version-banner graphics allocation: **0x2000 bytes**
- left banner X: **108**
- right banner X: **172**
- Ruby version-banner target Y: **84**
- initial version-banner Y: **44**
- German start-banner center X: **118**

German `CreatePressStartBanner` creates the normal three banner sprites and additionally creates the two German-only pieces using animation indices **8** and **9**.

These are source-correlated semantics; German code boundaries and address evidence come from the supplied German ROMs.

## Runtime flow

The source-correlated title-screen module covers:

- version-banner callbacks;
- Press Start / copyright banner creation;
- Pokémon-logo shine sprite and palette effects;
- title VBlank callback;
- title-screen initialization and VRAM/palette reset;
- Groudon graphics/tilemap loading for Ruby;
- title phase 1/2/3 task state machine;
- main-menu, clear-save, reset-RTC and copyright transitions;
- animated Groudon marking color.

The connected source contains **19 function definitions when Debug-only code is included**.

## Debug growth

There are two executable Debug additions.

### 1. Task_TitleScreenPhase3 SELECT path

Retail:

- **0x0807CA78..0x0807CBA8**
- size **0x130**
- SHA-256 `05e0926eaa6ed0d93e2aaab3eacfd9f5cb9b0858db308c7ed519a544281bc92c`

Debug:

- **0x08083CEC..0x08083E44**
- size **0x158**
- SHA-256 `0629023932f881ccc4abd12caf3993305dc3cd3616f6ad2cc35258ad2bf6eb62`

The Debug phase-3 function is **0x28 bytes larger**. Source correlation identifies the added branch as the held-SELECT path that fades to black and selects `CB2_GoToTestMenu`.

### 2. CB2_GoToTestMenu

The Debug-only callback occupies:

- **0x08083E60..0x08083E7C**
- size **0x1C**
- SHA-256 `6b016e7833466b735eddf30f9b9caeef4b22049bc75beea7a5b77ebd35d49927`

It waits for the palette fade to complete and then installs the test-menu initializer.

The two additions sum exactly:

**0x28 + 0x1C = 0x44 bytes**

which fully explains the title-screen Debug growth.

## Tail anchor

The final function is source-correlated as `UpdateLegendaryMarkingColor`.

| Profile | Start | End exclusive | Size | SHA-256 |
| --- | --- | --- | ---: | --- |
| Retail Rev 0 / Rev 1 | 0x0807CC18 | 0x0807CC5C | 0x44 | `3b955f0ccfcac7c4dedc1be663e9b68d00c430d4a23fa37125866b658e5a8fff` |
| Debug | 0x08083ED0 | 0x08083F14 | 0x44 | `cbffa9a9f56a5d8887f77cbc55b40371fee05178f919d4615845cd30fd3831d9` |

For Ruby the marking color is driven through the blue component. The function updates only every fourth frame and loads one color into palette index 0xEF.

## Next-module anchor

`field_weather` begins immediately afterward:

- Retail Rev 0 / Rev 1: **0x0807CC5C**
- Debug: **0x08083F14**
- accumulated delta: **+0x72B8**

The first function is source-correlated as `StartWeather`.

Both profiles begin:

`70 B5 30 48`

and, after the profile-specific branch instruction, share:

`00 06 06 0E 00 2E 55 D1 90 20 40 01`

This function first tests whether the weather main task is already active, then initializes the weather palette/task state, independently anchoring the title-screen end.
