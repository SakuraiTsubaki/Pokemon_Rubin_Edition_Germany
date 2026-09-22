# German battle graphics / SFX utility module

The complete `battle_gfx_sfx_util` module boundary has been mapped in the supplied German Retail, Rev 1 and Debug ROMs.

## Module boundary

| Profile | Start | End exclusive | Size | SHA-256 |
| --- | --- | --- | ---: | --- |
| Retail Rev 0 / Rev 1 | 0x080314C4 | 0x08032CB0 | 6,124 bytes (0x17EC) | 232a9dc36ee0e1f7879e1f12c3d57c526001a486532b3f505b57fa0f5c3f5676 |
| Debug | 0x0803527C | 0x08036A68 | 6,124 bytes (0x17EC) | b2f91dfeb5ce20260b34fb83911b76a16e92385034e7ec18446c88086b0d4e74 |

Retail Rev 0 and Rev 1 are byte-identical over the entire module.

There is **no additional Debug growth** in this module. Every mapped boundary keeps the inherited displacement **+0x3DB8** from the player-controller module.

## Verified entry functions

- SpriteCB_WaitForBattlerBallReleaseAnim: Retail 0x080314C4 / Debug 0x0803527C
- unref_sub_8031364: Retail 0x08031538 / Debug 0x080352F0
- SpriteCB_TrainerSlideIn: Retail 0x08031574 / Debug 0x0803532C
- move_anim_start_t2_for_situation: Retail 0x080315A4 / Debug 0x0803535C

These starts are taken from the German binaries. Historical source names that contain addresses are not treated as German addresses.

## Functional scope

This module is the shared graphics/sound bridge used by battle controllers. Its function inventory covers:

- Poké Ball release and trainer-slide sprite callbacks;
- mapping status/status2 conditions to status animations;
- generic battle-animation table launching;
- special animation setup and completion checks;
- no-animation checks;
- opponent/player Pokémon sprite loading;
- trainer-back decompression;
- battle-bar graphics;
- visibility synchronization across battle sprites;
- Substitute sprite loading and restoration;
- behind-Substitute state handling;
- low-HP music start/stop;
- battler affine-mode transitions.

Because the player and opponent controllers share these helpers, modern battle-presentation work should extend this common layer instead of duplicating graphics logic in each controller.

## Function inventory

- 1. SpriteCB_WaitForBattlerBallReleaseAnim
- 2. unref_sub_8031364
- 3. SpriteCB_TrainerSlideIn
- 4. move_anim_start_t2_for_situation
- 5. TryHandleLaunchBattleTableAnimation
- 6. sub_80315E8
- 7. sub_803163C
- 8. InitAndLaunchSpecialAnimation
- 9. sub_80316CC
- 10. IsMoveWithoutAnimation
- 11. mplay_80342A4
- 12. BattleLoadOpponentMonSprite
- 13. BattleLoadPlayerMonSprite
- 14. unref_sub_8031A64
- 15. nullsub_9
- 16. sub_8031A6C
- 17. DecompressTrainerBackPic
- 18. nullsub_10
- 19. sub_8031B74
- 20. unref_sub_8031BA0
- 21. sub_8031C30
- 22. LoadBattleBarGfx
- 23. battle_load_something
- 24. sub_8031EE8
- 25. sub_8031F0C
- 26. CopyAllBattleSpritesInvisibilities
- 27. sub_8031F88
- 28. sub_8031FC4
- 29. BattleLoadSubstituteSprite
- 30. refresh_graphics_maybe
- 31. TrySetBehindSubstituteSpriteBit
- 32. sub_80324E0
- 33. HandleLowHpMusicChange
- 34. BattleStopLowHpSound
- 35. unref_sub_8032604
- 36. sub_8032638
- 37. SetBattlerSpriteAffineMode
- 38. sub_80327CC
- 39. sub_80328A4
- 40. sub_8032978
- 41. sub_8032984
- 42. sub_8032A08
- 43. sub_8032A38
- 44. sub_8032AA8

## Architecture observations

The module keeps battle presentation separate from battle-script state mutation. Controllers request visual/sound operations, while this layer coordinates sprite callbacks, animation tables, affine state, Substitute visibility and low-HP audio.

This separation is useful for later-generation modernization: the legacy Ruby presentation can remain as a compatibility renderer while higher-level battle logic adopts newer mechanics.

## Next module

The next linked source module is `battle_controller_opponent`.

Its first function `nullsub_45` begins at:

- Retail **0x08032CB0**
- Debug **0x08036A68**
- delta **+0x3DB8**

The following `SetBankFuncToOpponentBufferRunCommand` starts immediately after the empty function, confirming the module transition.
