# German battle_util item/target/disobedience tail

This slice completes the German battle_util module.

## Exact tail slice

| Profile | Start | End exclusive | Size | SHA-256 |
| --- | --- | --- | ---: | --- |
| Retail Rev 0 / Rev 1 | 0x0801A200 | 0x0801C1DC | 8,156 bytes | 89bba501313e49c894400ca736698e3c5b15ea142f28b0eddeeeea327b32429c |
| Debug | 0x0801D754 | 0x0801F754 | 8,192 bytes | 6a3350e10866d249f54ad7baa9939aa14766198460b93eb02171a4b3b0d8cce1 |

Retail Rev 0 and Rev 1 are byte-identical throughout the entire tail.

## Function map

| Function | Retail | Debug | Retail bytes | Debug bytes | Role |
| --- | --- | --- | ---: | ---: | --- |
| ItemBattleEffects | 0x0801A200 | 0x0801D754 | 5088 | 5088 | held-item effect dispatcher |
| unref_sub_801B40C | 0x0801B5E0 | 0x0801EB34 | 392 | 392 | unused double-battle combined-move matcher |
| sub_801B594 | 0x0801B768 | 0x0801ECBC | 44 | 44 | Battle Action 10; execute current battle-script opcode when controllers are idle |
| GetMoveTarget | 0x0801B794 | 0x0801ECE8 | 872 | 872 | resolve move target and redirections |
| IsMonDisobedient | 0x0801BAFC | 0x0801F050 | 1760 | 1796 | badge/level-based obedience and disobedience outcomes |

## ItemBattleEffects

ItemBattleEffects is equal-sized in Retail and Debug. The original dispatcher recognizes 27 held-item effect classes in this path:

- HOLD_EFFECT_DOUBLE_PRIZE
- HOLD_EFFECT_RESTORE_STATS
- HOLD_EFFECT_RESTORE_HP
- HOLD_EFFECT_RESTORE_PP
- HOLD_EFFECT_LEFTOVERS
- HOLD_EFFECT_CONFUSE_SPICY
- HOLD_EFFECT_CONFUSE_DRY
- HOLD_EFFECT_CONFUSE_SWEET
- HOLD_EFFECT_CONFUSE_BITTER
- HOLD_EFFECT_CONFUSE_SOUR
- HOLD_EFFECT_ATTACK_UP
- HOLD_EFFECT_DEFENSE_UP
- HOLD_EFFECT_SPEED_UP
- HOLD_EFFECT_SP_ATTACK_UP
- HOLD_EFFECT_SP_DEFENSE_UP
- HOLD_EFFECT_CRITICAL_UP
- HOLD_EFFECT_RANDOM_STAT_UP
- HOLD_EFFECT_CURE_PAR
- HOLD_EFFECT_CURE_PSN
- HOLD_EFFECT_CURE_BRN
- HOLD_EFFECT_CURE_FRZ
- HOLD_EFFECT_CURE_SLP
- HOLD_EFFECT_CURE_CONFUSION
- HOLD_EFFECT_CURE_STATUS
- HOLD_EFFECT_CURE_ATTRACT
- HOLD_EFFECT_FLINCH
- HOLD_EFFECT_SHELL_BELL

Recovered fixed-width assumptions include 16-bit held item IDs, byte-sized hold-effect IDs/parameters, eight stat stages and exactly four move slots for PP restoration.

## Resolved Battle Action 10

The German action table entry 10 is now fully identified:

- Retail sub_801B594 entry: 0x0801B768
- Retail Thumb pointer: 0x0801B769
- Debug entry: 0x0801ECBC
- Debug Thumb pointer: 0x0801ECBD
- Function size: 44 bytes

If gBattleControllerExecFlags is zero, this handler executes the battle-script function selected by the current opcode.

The historical source symbol name contains an address from another build; it is not the German binary address.

## GetMoveTarget

GetMoveTarget keeps a 16-bit move ID and returns an 8-bit battler index. It handles target overrides, Follow Me, random double-battle target selection, absent-battler fallback and Lightning Rod redirection. The topology assumes two sides with left/right active positions.

## IsMonDisobedient

Retail obedience thresholds are 10 / 30 / 50 / 70 by badge progression, with the eighth badge granting unconditional obedience. Disobedience can select another one of four moves, sleep, self-hit or loaf around. The function explicitly uses mask 0xF and Random() & 3 for the four move slots.

The Debug build adds a control-bit 0x40 path that forces obedienceLevel to 10 before badge processing.

- Retail size: 1,760 bytes
- Debug size: 1,796 bytes
- Debug growth: 36 bytes (0x24)
- accumulated delta changes from +0x3554 to +0x3578

## Complete battle_util module

| Profile | Start | End exclusive | Size | SHA-256 |
| --- | --- | --- | ---: | --- |
| Retail Rev 0 / Rev 1 | 0x08015324 | 0x0801C1DC | 28,344 bytes | d6faa3fa2b22fcfe2cfdb8ddabb9161558683a5d1bf64bc4781efefa427fe9c4 |
| Debug | 0x080183AC | 0x0801F754 | 29,608 bytes | 11f5c8a6cbece220bc932537185f4c892d61fbc71009dabafb322325c60b3807 |

Debug is exactly 1,264 bytes (0x4F0) larger. The difference is fully accounted for by AbilityBattleEffects (+0x4CC) and IsMonDisobedient (+0x24).

## Next module

battle_script_commands begins at Retail **0x0801C1DC** / Debug **0x0801F754**, with accumulated Debug delta **+0x3578**.
