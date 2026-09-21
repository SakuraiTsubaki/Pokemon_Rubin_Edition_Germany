# German battle script accuracy, damage and type core

This slice maps opcode 0x01 through opcode 0x08 together with the internal damage/type helpers physically placed between them.

## Exact slice

| Profile | Start | End exclusive | Size | SHA-256 |
| --- | --- | --- | ---: | --- |
| Retail Rev 0 / Rev 1 | 0x0801C490 | 0x0801DAC0 | 5,680 bytes | 7bbe796fc3a53a0a91baac9b06a9534c0c70c213dd3e009516d8ee1c847a3061 |
| Debug | 0x0801FA08 | 0x08021038 | 5,680 bytes | 2e50618d4821ab4a88f1ab54ec0d8c72ffc4e118d7b6e9dcaea5005042ceed6b |

Retail Rev 0 and Rev 1 are byte-identical over the full slice. There is no Debug-only growth here; every mapped entry remains exactly **+0x3578** from Retail.

## Function map

| Function | Retail | Debug | Bytes | Role |
| --- | --- | --- | ---: | --- |
| atk01_accuracycheck | 0x0801C490 | 0x0801FA08 | 908 | accuracy/evasion, weather, ability and held-item hit calculation |
| atk02_attackstring | 0x0801C81C | 0x0801FD94 | 84 | emit move-use battle string |
| atk03_ppreduce | 0x0801C870 | 0x0801FDE8 | 476 | deduct PP with Pressure and sync PP through battle controller |
| atk04_critcalc | 0x0801CA4C | 0x0801FFC4 | 372 | calculate critical-hit stage and multiplier |
| atk05_damagecalc | 0x0801CBC0 | 0x08020138 | 268 | base damage calculation plus crit/damage multiplier/Charge/Helping Hand |
| AI_CalcDmg | 0x0801CCCC | 0x08020244 | 244 | AI-facing base damage calculation helper |
| ModulateDmgByType | 0x0801CDC0 | 0x08020338 | 216 | apply 0x/0.5x/2x type multiplier and result flags |
| atk06_typecalc | 0x0801CE98 | 0x08020410 | 632 | STAB/type chart/Levitate/Wonder Guard damage-type command |
| CheckWonderGuardAndLevitate | 0x0801D110 | 0x08020688 | 652 | pre-damage immunity/effectiveness helper for accuracy path |
| ModulateDmgByType2 | 0x0801D39C | 0x08020914 | 184 | type multiplier helper with explicit move/result arguments |
| TypeCalc | 0x0801D454 | 0x080209CC | 476 | general battle type calculation helper |
| AI_TypeCalc | 0x0801D630 | 0x08020BA8 | 280 | species/ability-based AI type effectiveness helper |
| Unused_ApplyRandomDmgMultiplier | 0x0801D748 | 0x08020CC0 | 60 | unused wrapper around 85-100% random damage multiplier |
| atk07_adjustnormaldamage | 0x0801D784 | 0x08020CFC | 432 | apply random damage, Focus Band, False Swipe and Endure survival |
| atk08_adjustnormaldamage2 | 0x0801D934 | 0x08020EAC | 396 | variant of atk07 without False Swipe handling |

## Accuracy pipeline — opcode 0x01

`atk01_accuracycheck` combines the original Ruby accuracy model:

- attacker accuracy stage and target evasion stage;
- Foresight override of target evasion;
- move accuracy;
- Thunder accuracy reduction to 50 in sun;
- Compound Eyes ×1.30;
- Sand Veil ×0.80 in sandstorm;
- Hustle ×0.80 for physical-type moves in the original type split;
- held-item evasion modifier;
- final random 1..100 roll.

The stage ratio table is the original 13-entry -6..+6 mapping. Accuracy/evasion remains byte-oriented while move IDs are 16-bit.

## PP / Pressure — opcode 0x03

`atk03_ppreduce` starts from one PP and adds Pressure costs according to the move target class. It synchronizes the changed one-byte PP value back through `BtlController_EmitSetMonData` unless the battler is transformed or the slot is treated as mimicked.

This is another direct four-move-slot integration point because controller PP requests are `REQUEST_PPMOVE1_BATTLE + gCurrMovePos`.

## Critical-hit model — opcode 0x04

The original critical stage is built from:

- Focus Energy: +2;
- selected high-critical move effects: +1;
- Scope Lens: +1;
- Lucky Punch on Chansey: +2;
- Stick on Farfetch'd: +2.

The stage is clamped to the five-entry critical table `{1/16, 1/8, 1/4, 1/3, 1/2}`. A successful critical uses multiplier 2. Battle Armor, Shell Armor and `STATUS3_CANT_SCORE_A_CRIT` suppress it.

## Base damage — opcode 0x05

`atk05_damagecalc` delegates the main Generation III formula to `CalculateBaseDamage`, then applies:

- critical multiplier;
- battle damage multiplier;
- Charge ×2 for Electric moves;
- Helping Hand ×1.5.

`AI_CalcDmg` mirrors the same post-base modifiers for AI evaluation.

## Type calculation — opcode 0x06

The type stage applies:

- STAB ×1.5;
- type-chart entries encoded as ×0, ×0.5 or ×2;
- Levitate immunity to Ground;
- Foresight handling;
- dual-type multiplication;
- Wonder Guard gating;
- move-result flags for immune / not very effective / super effective.

`TypeCalc` and `AI_TypeCalc` expose the same core concepts outside the main opcode path. The original interface still uses 16-bit move/species IDs and byte-sized type/ability/result fields.

## Random damage and survival — opcodes 0x07 / 0x08

The random damage helper multiplies final damage by a uniformly selected integer from **85 through 100 percent**.

`atk07_adjustnormaldamage` then handles:

- Focus Band activation;
- Substitute bypass of survival adjustment;
- False Swipe;
- Endure;
- Focus Band survival at 1 HP.

`atk08_adjustnormaldamage2` is the same survival path without the False Swipe check.

## Modernization pressure points

This slice is one of the strongest Generation III compatibility clusters. Later-generation battle rules should not be mixed directly into these functions without an explicit compatibility layer because changes touch:

- physical/special classification assumptions embedded in Hustle and damage calculation;
- critical-stage rules;
- weather-based accuracy;
- ability and item accuracy hooks;
- STAB/type effectiveness representation;
- immunity hooks;
- random damage range;
- survival effects and focus-item behavior.

The next command is opcode 0x09 `atk09_attackanimation` at Retail **0x0801DAC0** / Debug **0x08021038**.
