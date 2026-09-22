# German Poké Ball presentation module

This module is the battle-presentation layer for Poké Ball send-out, recall, capture/ball motion, ball resource loading and associated healthbox slide effects. Capture probability itself lives in the previously mapped battle-script opcode 0xEF, not here.

## Boundary

| Profile | Start | End exclusive | Size | SHA-256 |
| --- | --- | --- | ---: | --- |
| Retail Rev 0 / Rev 1 | 0x08046724 | 0x08047CF0 | 5,580 bytes (0x15CC) | 118403c067324952cec68297957f769cc66c87579a83561c4213ea250dcb6b66 |
| Debug | 0x0804A8F0 | 0x0804BEBC | 5,580 bytes (0x15CC) | 01145d9d2698d8fc33e6b6145a8fa77794ee41c2ddafb9c4fd99c742bf5bd11b |

Retail Rev 0 and Rev 1 are byte-identical. The source contains no Debug-only conditional code, and the complete module remains at **+0x41CC**.

## Function inventory

- 1. DoPokeballSendOutAnimation
- 2. SendOutMonAnimation
- 3. objc_0804ABD4
- 4. sub_80466E8
- 5. sub_80466F4
- 6. sub_8046760
- 7. sub_80467F8
- 8. sub_804684C
- 9. sub_8046944
- 10. sub_8046984
- 11. sub_8046AD0
- 12. sub_8046C78
- 13. sub_8046E7C
- 14. sub_8046E9C
- 15. sub_8046FBC
- 16. SendOutPlayerMonAnimation_Step0
- 17. SendOutPlayerMonAnimation_Step1
- 18. SendOutMonAnimation_Delay
- 19. SendOutOpponentMonAnimation_Step0
- 20. sub_80472B0
- 21. sub_80472D8
- 22. CreatePokeballSprite
- 23. sub_80473D0
- 24. sub_804748C
- 25. sub_8047580
- 26. sub_8047638
- 27. sub_80476E0
- 28. sub_8047754
- 29. obj_delete_and_free_associated_resources_
- 30. StartHealthboxSlideIn
- 31. sub_804780C
- 32. sub_8047830
- 33. DoHitAnimHealthboxEffect
- 34. oamc_804BEB4
- 35. LoadBallGraphics
- 36. FreeBallGraphics
- 37. GetBattlerBall

## Ball graphics registry

The module has exactly **12 Poké Ball presentation entries**:

1. Poké Ball
2. Great Ball
3. Safari Ball
4. Ultra Ball
5. Master Ball
6. Net Ball
7. Dive Ball
8. Nest Ball
9. Repeat Ball
10. Timer Ball
11. Luxury Ball
12. Premier Ball

Their object tags are consecutive **55000..55011**. Each compressed ball sprite sheet declares **384 bytes** of decompressed OBJ tile data and has a corresponding palette entry.

This is a fixed presentation registry and is a direct expansion point for later-generation Ball types.

## Stored ball provenance

`GetBattlerBall` reads `MON_DATA_POKEBALL` from the active party Pokémon, choosing player or enemy party by battler side.

`SendOutMonAnimation` converts that stored ball number to a processing index and selects the matching graphics/template. The caught Pokémon's ball is therefore visible provenance in ordinary send-out animation.

## Send-out animation

`DoPokeballSendOutAnimation`:

- marks battle animation active;
- marks the active battler's ball animation active;
- creates the send-out task at priority 5;
- records side/battler parameters in task data.

The player and opponent paths use separate sprite callbacks and positions. A third nonstandard selector path is retained as an internal/debug-like animation path even in retail source; it is not a DEBUG-ROM-only compile block.

Ball movement uses the shared trigonometric helpers and affine sprite animation. Bounce stages play four distinct ball-bounce sound effects.

## Generic ball sprite helpers

The module also exposes generic open/close helpers used outside the ordinary battle send-out path:

- create a ball sprite at caller coordinates;
- emit ball-open particles;
- scale/show the attached Pokémon sprite;
- reverse the flow to return/hide it;
- destroy the ball and associated resources.

These helpers store 32-bit caller data across two 16-bit sprite data fields, another recurring GBA presentation pattern.

## Healthbox coupling

`StartHealthboxSlideIn` and the hit-healthbox effect live in this module even though the healthbox renderer itself is in `battle_interface`.

The slide direction is inverted for the opponent side, and one double-battle battler position receives a fixed 20-frame delay.

This is presentation coupling that should be disentangled in a modern renderer while preserved for legacy playback.

## Ball resource loading

`LoadBallGraphics` lazily loads a ball's compressed sprite sheet and palette when its tile tag is absent.

For processing indexes **6, 10 and 11** (Dive, Luxury and Premier Ball in the 0-based table), the extra shared VRAM decompression step is skipped; other ball variants decompress the shared ball effect graphics after loading.

`FreeBallGraphics` releases both tile and palette tags.

## Expansion direction

A Gen-10-ready ball presentation layer should:

- replace the fixed 12-entry table with a registry;
- preserve the original index mapping for Ruby saves;
- keep `MON_DATA_POKEBALL` compatibility conversion explicit;
- decouple capture math from presentation, as the original engine already largely does;
- move healthbox slide effects out of the ball-specific module;
- keep the original sprite/affine callbacks as a legacy renderer.

## Next module

`load_save` begins with `CheckForFlashMemory` at:

- Retail **0x08047CF0**
- Debug **0x0804BEBC**
- delta **+0x41CC**

The boundary is directly confirmed by the function sequence:

`IdentifyFlash -> gFlashMemoryPresent -> InitFlashTimer`.
