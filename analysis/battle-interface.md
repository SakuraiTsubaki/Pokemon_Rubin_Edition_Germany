# German battle interface / HUD module

> Boundary correction: an earlier repository snapshot ended this module at 0x08046234 by treating the historical source-name address `sub_8046234` as the German ROM address. Direct German-binary control-flow inspection shows that 0x08046234 is still inside `battle_interface`. The corrected German boundary is 0x08046558.

## Correct module boundary

| Profile | Start | End exclusive | Size | SHA-256 |
| --- | --- | --- | ---: | --- |
| Retail Rev 0 / Rev 1 | 0x08043A60 | 0x08046558 | 11,000 bytes (0x2AF8) | 3d9b4de9cf84eb5e822465da4d6da33b16f863c2171db1e45bc67a11c34c748b |
| Debug | 0x08047BDC | 0x0804A724 | 11,080 bytes (0x2B48) | c4ab84b3d9f3b3130081fe21e08026c878b28bdfb58fc1bdc5106a0e3c7f523a |

Retail Rev 0 and Rev 1 are byte-identical across the complete corrected module.

Debug is exactly **80 bytes (0x50)** larger.

## Why 0x08046234 was not the boundary

The code at Retail 0x080463EC is the four-argument test helper `sub_80460C8`: it calls the bar-step helper, tile-fill helper and `do_nothing`. It is followed by `sub_8046128`, `GetScaledExpFraction`, `GetScaledHPFraction` and `GetHPBarLevel`.

Only after `GetHPBarLevel` returns does the next module begin at **0x08046558**.

This correction is binary-first and avoids using historical function names as German addresses.

## Debug growth

The two source-level DEBUG blocks still account for the entire increase:

1. `sub_804454C`: opponent-side healthbox number-toggle allowance  
   - stable delta before block: **+0x417C**
   - stable delta after block: **+0x4188**
   - growth: **0x0C = 12 bytes**

2. `UpdateHealthboxAttribute`: optional opponent HP/max-HP number rendering  
   - delta before block: **+0x4188**
   - delta after block: **+0x41CC**
   - growth: **0x44 = 68 bytes**

Total: **0x50**.

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

## German HUD localization

The level display uses a **period** in the German build where the English build uses a colon.

## Legacy HUD dimensions

- HP bar: 6 tiles = 48 scaled pixels;
- EXP bar: 8 tiles = 64 scaled pixels;
- party summary: six party slots;
- level-100 EXP bar is rendered empty;
- HP thresholds use the 48-pixel scale: >=25 high, >=10 middle, >0 low, 0 empty.

## Correct next module

`smokescreen` starts at:

- Retail **0x08046558**
- Debug **0x0804A724**
- accumulated delta **+0x41CC**

The first function is the smoke-effect creator corresponding to source `sub_8046234`.
