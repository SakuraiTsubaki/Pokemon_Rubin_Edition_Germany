# German battle interface / HUD module

The complete `battle_interface` module has been bounded directly in the supplied German Retail, Rev 1 and Debug ROMs.

## Module boundary

| Profile | Start | End exclusive | Size | SHA-256 |
| --- | --- | --- | ---: | --- |
| Retail Rev 0 / Rev 1 | 0x08043A60 | 0x08046234 | 10,196 bytes (0x27D4) | cf178beb5a639d1932696c9eba1385bd0735b64e70c8cd05c7bf96d5a7061b0f |
| Debug | 0x08047BDC | 0x0804A400 | 10,276 bytes (0x2824) | 4dbf0b7b85a017c2b041e40247d484cc9edb84c0eb5f65d9012bd3f4308366f1 |

Retail Rev 0 and Rev 1 are byte-identical across the complete module.

Debug is exactly **80 bytes (0x50)** larger.

## Debug growth

The two source-level DEBUG blocks account for the entire increase.

1. `sub_804454C`: opponent-side healthbox number-toggle allowance  
   - stable delta before block: **+0x417C**
   - stable delta after block: **+0x4188**
   - growth: **0x0C = 12 bytes**

2. `UpdateHealthboxAttribute`: optional opponent HP/max-HP number rendering in Debug  
   - delta before block: **+0x4188**
   - delta after block: **+0x41CC**
   - growth: **0x44 = 68 bytes**

Total: **0x0C + 0x44 = 0x50**.

The next module therefore begins at accumulated Debug displacement **+0x41CC**.

## Function inventory

- 1. do_nothing
- 2. sub_8043740
- 3. unref_sub_80438E0
- 4. battle_make_oam_normal_battle
- 5. battle_make_oam_safari_battle
- 6. sub_8043CEC
- 7. sub_8043D5C
- 8. SetBattleBarStruct
- 9. SetHealthboxSpriteInvisible
- 10. SetHealthboxSpriteVisible
- 11. sub_8043E50
- 12. unref_sub_8043E70
- 13. nullsub_11
- 14. UpdateOamPriorityInAllHealthboxes
- 15. sub_8043F44
- 16. UpdateHpTextInHealthbox
- 17. sub_8044210
- 18. PrintSafariMonInfo
- 19. sub_804454C
- 20. CreatePartyStatusSummarySprites
- 21. sub_8044CA0
- 22. sub_8044E74
- 23. sub_8044ECC
- 24. sub_8044F70
- 25. sub_8045030
- 26. sub_8045048
- 27. sub_804507C
- 28. sub_8045110
- 29. sub_8045180
- 30. sub_8045458
- 31. sub_80457E8
- 32. UpdateHealthboxAttribute
- 33. MoveBattleBar
- 34. sub_8045D58
- 35. sub_8045F58
- 36. CalcBarFilledPixels
- 37. sub_80460C8
- 38. sub_8046128
- 39. GetScaledExpFraction
- 40. GetScaledHPFraction
- 41. GetHPBarLevel

## German-specific HUD localization

The level display has an explicit regional compile-time difference:

- English: level separator = colon;
- **German: level separator = period**.

This is direct evidence that German battle UI differences are embedded in rendering code, not only in localized text data.

Together with the previously mapped German `BattleText_OtherMenu` tile offset, this confirms a recurring pattern: German localization changes both text assets and HUD geometry/rendering details.

## Healthbox architecture

The module owns the visible battle HUD layer:

- normal single/double battle healthbox sprite construction;
- Safari healthbox construction;
- HP and maximum-HP text;
- level text;
- status ailment graphics;
- HP bar;
- EXP bar;
- Safari nature/catch/flee display;
- party-status summary sprites;
- healthbox visibility and OAM priority;
- healthbox attribute refresh.

The battle controllers therefore remain protocol endpoints while this module is the shared visual representation of battler state.

## HP bar model

The HP bar is rendered as **6 tiles × 8 pixels = 48 scaled pixels**.

`GetScaledHPFraction(hp, maxhp, 48)` guarantees at least one visible pixel for positive HP.

`GetHPBarLevel` returns:

- 4: HP == max HP;
- 3: scaled fraction >= 25;
- 2: scaled fraction >= 10;
- 1: scaled fraction > 0;
- 0: zero HP.

The corresponding bar graphics use the same threshold boundaries:

- 25..48 pixels: high/green range;
- 10..24 pixels: middle/yellow range;
- 1..9 pixels: low/red range;
- 0: empty.

These exact integer thresholds are legacy rendering behavior, not percentages calculated in floating point.

## EXP bar model

The EXP bar is **8 tiles × 8 pixels = 64 scaled pixels**.

At level **100**, all eight EXP-bar tile fill values are forced to zero.

The update path derives current-level progress from the species growth-rate table and animates the bar using a scaled step size rather than immediately replacing the graphics.

## Healthbox animation state

`SetBattleBarStruct` stores:

- healthbox sprite ID;
- maximum value;
- old/current source value;
- received delta;
- animation cursor initialized to **-0x8000**.

`MoveBattleBar` then advances HP or EXP over time and redraws the relevant tile strip.

For very small maxima, the animation path uses fixed-point state so the visual bar can still advance at sub-unit precision.

## Safari HUD

`PrintSafariMonInfo` replaces ordinary opponent health information with:

- the wild Pokémon's Nature name;
- Safari catch factor;
- Safari flee rate.

This is another case where battle mode changes the semantic content of the healthbox rather than only its style.

## Party summary

`CreatePartyStatusSummarySprites` iterates exactly **six** `HpAndStatus` entries and creates the six Poké Ball/status icons used in trainer-battle party summaries.

The six-slot party assumption is therefore embedded directly in battle presentation as well as party data/storage logic.

## Debug HUD behavior

The Debug build can expose opponent HP numbers that retail normally hides.

The first Debug branch relaxes the opponent-side restriction used by the healthbox-number toggle. The second branch makes `UpdateHealthboxAttribute` render current/max HP text for an opponent when the Debug control byte is enabled.

These are development inspection features, not retail German UI behavior.

## Expansion direction

For a Gen-10-ready renderer, the safest separation is:

- preserve this exact module as the legacy GBA HUD renderer;
- expose battler UI state through a larger presentation model;
- remove fixed six-party assumptions from modern party-summary rendering;
- keep the 48-pixel HP and 64-pixel EXP bars only as legacy skins;
- make opponent HP visibility and special modes policy-driven rather than compile-time Debug branches;
- keep German punctuation/layout rules in locale-specific presentation assets.

## Next module

`smokescreen` begins with `sub_8046234` at:

- Retail **0x08046234**
- Debug **0x0804A400**
- accumulated delta **+0x41CC**

The first 16 bytes are byte-identical in the two profiles, confirming the boundary immediately after `GetHPBarLevel`.
