# German main-menu helper tail and module boundary

The remainder of the German main-menu module has now been mapped from the post-naming callback through the preset-name copier.

## Helper map

| Function | Retail | Debug | Size | Role |
| --- | --- | --- | ---: | --- |
| CB_ContinueNewGameSpeechPart2 | 0x0800B234 | 0x0800B414 | 476 | reinitialize graphics after naming screen and resume at confirmation |
| nullsub_34 | 0x0800B410 | 0x0800B5F0 | 4 | empty sprite callback |
| ShrinkPlayerSprite | 0x0800B414 | 0x0800B5F4 | 28 | move/shrink player sprite during final intro transition |
| CreateAzurillSprite | 0x0800B430 | 0x0800B610 | 112 | decompress/load Azurill graphics and create intro sprite |
| AddBirchSpeechObjects | 0x0800B4A0 | 0x0800B680 | 288 | create Birch, Azurill, Brendan and May intro sprites |
| Task_SpriteFadeOut | 0x0800B5C0 | 0x0800B7A0 | 108 | sprite alpha fade-out task |
| StartSpriteFadeOut | 0x0800B62C | 0x0800B80C | 112 | launch sprite fade-out helper task |
| Task_SpriteFadeIn | 0x0800B69C | 0x0800B87C | 108 | sprite alpha fade-in task |
| StartSpriteFadeIn | 0x0800B708 | 0x0800B8E8 | 116 | launch sprite fade-in helper task |
| HandleFloorShadowFadeOut | 0x0800B77C | 0x0800B95C | 108 | background/floor-shadow fade-out task |
| StartBackgroundFadeOut | 0x0800B7E8 | 0x0800B9C8 | 64 | launch background fade-out helper task |
| HandleFloorShadowFadeIn | 0x0800B828 | 0x0800BA08 | 108 | background/floor-shadow fade-in task |
| StartBackgroundFadeIn | 0x0800B894 | 0x0800BA74 | 64 | launch background fade-in helper task |
| CreateGenderMenu | 0x0800B8D4 | 0x0800BAB4 | 96 | draw and initialize the boy/girl selection menu |
| GenderMenuProcessInput | 0x0800B934 | 0x0800BB14 | 16 | read non-wrapping gender menu input |
| CreateNameMenu | 0x0800B944 | 0x0800BB24 | 136 | draw and initialize preset-name selection menu |
| NameMenuProcessInput | 0x0800B9CC | 0x0800BBAC | 16 | read preset-name menu input |
| SetPresetPlayerName | 0x0800B9DC | 0x0800BBBC | 80 | copy selected preset name into German SaveBlock2 player name |

## Exact tail slice

| Profile | Start | End exclusive | Size | SHA-256 |
| --- | --- | --- | ---: | --- |
| Retail Rev 0 / Rev 1 | 0x0800B234 | 0x0800BA2C | 2,040 | 844fad2a520d6b7b769786399de8d3c5a5e351cb0f97a7465f67df53e430d031 |
| Debug | 0x0800B414 | 0x0800BC0C | 2,040 | 74260300a0830783b57573d9defeafaa4084e65025418d2631ba9508bd5a3757 |

Retail Rev 0 and Rev 1 are byte-identical throughout this complete tail.

All helper entry points retain the +0x1E0 Debug address delta. The two tiny menu-input wrappers have different initial BL encodings because their callees are relocated, but their function boundaries and high-level behavior remain aligned.

## Complete main-menu module

With this tail mapped, the complete German main-menu module is now bounded as:

| Profile | Start | End exclusive | Size | SHA-256 |
| --- | --- | --- | ---: | --- |
| Retail Rev 0 / Rev 1 | 0x08009890 | 0x0800BA2C | 8,604 | 6aab6354e6342ade67758f5a293db2e45a9c27a0adbe983487eb28f752f0ea06 |
| Debug | 0x08009A70 | 0x0800BC0C | 8,604 | 86c703c4790622849580374f46b5bb0a2974757e0d6b0afbf66925c98e2307c7 |

The Retail and Debug modules have the same size but differ in 899 byte positions, largely because of relocated code/data references and Debug-specific surrounding layout.

## Next module boundary

The instruction stream beginning at:

- Retail: 0x0800BA2C
- Debug: 0x0800BC0C

is no longer main-menu code. Control-flow and module-order comparison identify this as the start of the battle-controller module.

This gives the German project its first fully bounded non-RTC source module.
