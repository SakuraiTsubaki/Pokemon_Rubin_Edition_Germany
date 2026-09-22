# German egg-hatch module

The complete `egg_hatch` module has been bounded directly in the supplied German ROMs.

## Module boundary

| Profile | Start | End exclusive | Size | SHA-256 |
| --- | --- | --- | ---: | --- |
| Retail Rev 0 / Rev 1 | 0x08042BC8 | 0x08043A60 | 3,736 bytes (0xE98) | f588c592f49c79df973673fae1a61b27e72ade82e4e4f83c2c8b7c5f46112749 |
| Debug | 0x08046D44 | 0x08047BDC | 3,736 bytes (0xE98) | 2c9dea76d3666146f7d70064330d2ca25a3996912f475fea3cf9663602f0986b |

Retail Rev 0 and Rev 1 are byte-identical. No Debug-only code is inserted; the full module remains at **+0x417C**.

## Function inventory

- 1. CreatedHatchedMon
- 2. AddHatchedMonToParty
- 3. ScriptHatchMon
- 4. DaycareMonReceivedMail_
- 5. DaycareMonReceivedMail
- 6. EggHatchCreateMonSprite
- 7. VBlankCB_EggHatch
- 8. EggHatch
- 9. Task_EggHatch
- 10. CB2_EggHatch_0
- 11. EggHatchSetMonNickname
- 12. Task_EggHatchPlayBGM
- 13. CB2_EggHatch_1
- 14. SpriteCB_Egg_0
- 15. SpriteCB_Egg_1
- 16. SpriteCB_Egg_2
- 17. SpriteCB_Egg_3
- 18. SpriteCB_Egg_4
- 19. SpriteCB_Egg_5
- 20. SpriteCB_EggShard
- 21. CreateRandomEggShardSprite
- 22. CreateEggShardSprite
- 23. EggHatchPrintMessage1
- 24. EggHatchPrintMessage2
- 25. EggHatchUpdateWindowText

## Egg → hatched Pokémon conversion

`CreatedHatchedMon` reconstructs a normal Pokémon from the Egg while preserving selected Egg provenance.

Preserved from the Egg:

- species;
- exactly **four moves**;
- personality/PID;
- all **six IVs**;
- met-game value;
- markings;
- Pokérus byte.

The routine calls `CreateMon` at the fixed **EGG_HATCH_LEVEL = 5** using the original personality, then writes those preserved values back.

The newly hatched Pokémon receives:

- `GAME_LANGUAGE` — German in the German build;
- friendship **120**.

A source comment explicitly notes that Ruby/Sapphire do **not** copy the later FRLG `eventLegal` field during hatching. That distinction matters for cross-generation provenance compatibility.

## Party finalization

`AddHatchedMonToParty` then:

- clears the Egg flag;
- replaces the Egg nickname with the species name;
- sets both Pokédex seen/caught flags;
- forces Poké Ball as the recorded ball;
- stores met level 0;
- stores the **current map** as met location;
- restores move PP;
- recalculates stats.

Thus the Egg's creation metadata and the hatched Pokémon's final “met” presentation are intentionally transformed during hatching.

## Hatch presentation state machines

`CB2_EggHatch_0` is a **9-state (0..8)** graphics/setup state machine. It resets task/sprite state, initializes the text window, loads textbox and Egg graphics, converts the Egg to the hatched Pokémon, creates the Pokémon sprite and switches into the active hatch callback.

`CB2_EggHatch_1` is a **12-state (0..11)** interaction/presentation state machine. It handles:

- palette fade-in;
- Egg animation start;
- hatch completion wait;
- hatched-species message;
- fanfare wait;
- nickname prompt;
- yes/no menu;
- naming-screen transition;
- final fade back to field.

The nickname path opens naming screen type **3** with the hatched species, gender and personality.

## Egg animation

The Egg sprite sequence has six callbacks (`SpriteCB_Egg_0` through `SpriteCB_Egg_5`) plus a shard callback.

The rocking animation directly calls the previously mapped `Sin` utility, tying this module to the Q8.8 trigonometric lookup layer.

The shard system uses a fixed table of **19 Q8.8 velocity pairs**. Each requested shard consumes the next velocity pair and selects one of four sprite animations using the main RNG.

The animation ends by fading to white, hiding the Egg, revealing/affine-scaling the hatched Pokémon sprite, then fading back.

## Audio

The hatch flow uses dedicated sound/fanfare sequencing and a task-driven BGM transition. Presentation timing is therefore part of the original state machine rather than a single blocking animation call.

## Compatibility constraints

This module reinforces several legacy assumptions that should remain behind a Ruby compatibility renderer/data adapter:

- hatch level fixed at 5;
- four copied moves;
- six copied IVs;
- friendship reset to 120;
- current-map met location assignment;
- 19-entry fixed shard-velocity animation script;
- hard-wired field/naming-screen transition sequence;
- Ruby omission of FRLG's later event-legal provenance copy.

## Next module

`battle_interface` begins at:

- Retail **0x08043A60**
- Debug **0x08047BDC**
- delta **+0x417C**

The first function is `do_nothing`, and its complete machine code is the distinctive four-byte sequence:

`09 20 70 47` — `movs r0, #9; bx lr`.

The next function immediately follows at 0x08043A64.
