# German Birch new-game speech state machine

The 33-state new-game intro immediately follows the save-info rendering block.

## Exact module slice

| Profile | Start | End exclusive | Size | SHA-256 |
| --- | --- | --- | ---: | --- |
| Retail Rev 0 / Rev 1 | 0x0800A3C8 | 0x0800B234 | 3,692 bytes | 8c81b39a88fe3b5d1a12eaee333692fee3d5ca87e1d52f2f62426572ba02e73e |
| Debug | 0x0800A5A8 | 0x0800B414 | 3,692 bytes | f7c78291c4f9031b5585252d2e9a7099c7598c4a3dac258568ebf47f4aaf5938 |

Retail Rev 0 and Rev 1 are byte-identical throughout the complete 33-state intro.

Every verified Debug state starts exactly +0x1E0 bytes after its retail counterpart. The function immediately after state 33 is also +0x1E0: retail 0x0800B234 versus Debug 0x0800B414.

## State map

| State | Retail | Debug | Primary role |
| ---: | --- | --- | --- |
| 1 | 0x0800A3C8 | 0x0800A5A8 | initialize Birch intro graphics, sprites, window state and fade |
| 2 | 0x0800A4B4 | 0x0800A694 | fade in Birch/Azurill/background |
| 3 | 0x0800A52C | 0x0800A70C | display welcome text |
| 4 | 0x0800A59C | 0x0800A77C | advance to the 'this is Pokemon' text |
| 5 | 0x0800A5E8 | 0x0800A7C8 | wait for text completion |
| 6 | 0x0800A618 | 0x0800A7F8 | create Pokeball presentation sprite |
| 7 | 0x0800A68C | 0x0800A86C | handle Pokeball/Pokemon reveal and cry |
| 8 | 0x0800A6FC | 0x0800A8DC | display world-inhabited-by-Pokemon text |
| 9 | 0x0800A738 | 0x0800A918 | display transition toward player introduction |
| 10 | 0x0800A780 | 0x0800A960 | fade out professor/background for player selection |
| 11 | 0x0800A7F8 | 0x0800A9D8 | wait for fade completion |
| 12 | 0x0800A83C | 0x0800AA1C | bring player trainer presentation on screen |
| 13 | 0x0800A8EC | 0x0800AACC | wait for player presentation transition |
| 14 | 0x0800A930 | 0x0800AB10 | display boy-or-girl prompt |
| 15 | 0x0800A970 | 0x0800AB50 | create gender selection menu |
| 16 | 0x0800A9A8 | 0x0800AB88 | process gender selection or sprite switch |
| 17 | 0x0800AA48 | 0x0800AC28 | slide old trainer sprite out |
| 18 | 0x0800AAF0 | 0x0800ACD0 | slide selected trainer sprite in |
| 19 | 0x0800AB48 | 0x0800AD28 | display name prompt |
| 20 | 0x0800AB88 | 0x0800AD68 | create preset-name menu |
| 21 | 0x0800ABC0 | 0x0800ADA0 | process preset/custom/back name selection |
| 22 | 0x0800AC80 | 0x0800AE60 | enter naming screen for custom name |
| 23 | 0x0800ACC0 | 0x0800AEA0 | display confirmation text with player name |
| 24 | 0x0800AD0C | 0x0800AEEC | display yes/no confirmation menu |
| 25 | 0x0800AD44 | 0x0800AF24 | process confirmation or return to gender choice |
| 26 | 0x0800ADF4 | 0x0800AFD4 | complete trainer/background fade-out transition |
| 27 | 0x0800AE2C | 0x0800B00C | restore Birch/Azurill and display contextual player text |
| 28 | 0x0800AF1C | 0x0800B0FC | fade Birch/Azurill back out after text |
| 29 | 0x0800AFC8 | 0x0800B1A8 | restore selected trainer and display ready text |
| 30 | 0x0800B0A8 | 0x0800B288 | start trainer shrink/fade/BGM transition |
| 31 | 0x0800B158 | 0x0800B338 | wait for affine shrink animation |
| 32 | 0x0800B194 | 0x0800B374 | finish palette transition and prepare final state |
| 33 | 0x0800B208 | 0x0800B3E8 | enter new game callback and destroy intro task |

## High-level flow

The sequence divides cleanly into five phases:

1. **Professor/Pokemon presentation — states 1-9**
   - initializes the intro scene;
   - fades in Birch and Azurill;
   - displays the welcome/Pokemon-world dialogue;
   - performs the Pokeball/Pokemon reveal and cry.
2. **Trainer gender selection — states 10-18**
   - fades from Birch to the trainer presentation;
   - displays the boy/girl prompt;
   - swaps Brendan/May sprites while the selection changes.
3. **Player naming — states 19-25**
   - displays the name prompt;
   - offers preset names or the naming screen;
   - expands the chosen player name into confirmation text;
   - returns to gender selection on rejection/back.
4. **Final speech/presentation — states 26-30**
   - restores Birch/Azurill;
   - displays the contextual player line and ready line;
   - transitions back to the selected trainer;
   - begins trainer shrink and BGM/palette fade.
5. **Commit to new game — states 31-33**
   - waits for the affine animation;
   - finalizes the display transition;
   - switches the main callback to the new-game entry point and destroys the intro task.

## Dialogue references mapped in this slice

- gBirchSpeech_Welcome — state 3
- gBirchSpeech_ThisIsPokemon — state 4
- gBirchSpeech_WorldInhabitedByPokemon — state 8
- gBirchSpeech_AndYouAre — state 9
- gBirchSpeech_AreYouBoyOrGirl — state 14
- gBirchSpeech_WhatsYourName — state 19
- gBirchSpeech_SoItsPlayer — state 23
- gBirchSpeech_AhOkayYouArePlayer — state 27
- gBirchSpeech_AreYouReady — state 29

The next localization pass must resolve these references to the actual German encoded strings and preserve their byte ranges separately from semantic labels.

## Important branch loops

- State 16 can proceed to state 19 after a committed gender choice or to state 17 when switching the displayed trainer.
- State 18 returns to state 16.
- State 21 can return to state 14, enter state 22 for a custom name, or proceed to state 23 for a preset name.
- State 25 can return to state 14 after rejecting the confirmation or proceed to state 26.

## Reconstruction status

All 33 entry addresses and the complete slice boundaries are verified from the German binaries. The current repository records the full control-flow topology and stage semantics. Full statement-level C promotion remains incremental so that each state can be tied to German-localized data and exact call targets rather than copied from another Ruby source tree.
