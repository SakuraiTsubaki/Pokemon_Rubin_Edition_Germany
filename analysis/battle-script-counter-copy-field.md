# German battle script counters, copied moves and field rules

This slice maps opcodes 0xA0 through 0xBF and four internal helpers.

## Exact slice

| Profile | Start | End exclusive | Size | SHA-256 |
| --- | --- | --- | ---: | --- |
| Retail Rev 0 / Rev 1 | 0x08027B64 | 0x08029850 | 7,404 bytes | 6644ec154e3cd15bf0be45a27a6a3375dbb6b35228fb9c1d05ce3f15d1705065 |
| Debug | 0x0802B1C8 | 0x0802CEB4 | 7,404 bytes | 0befa4b0c047905478c820e4da840fef77e821d441db7e2755cfabfaeadc67cc |

Retail Rev 0 and Rev 1 are byte-identical. There are no new Debug-only insertions: the full slice remains at **+0x3664**.

## Opcode map

| Opcode | Function | Retail | Debug | Span | Role |
| ---: | --- | --- | --- | ---: | --- |
| 0xA0 | atkA0_psywavedamageeffect | 0x08027B64 | 0x0802B1C8 | 84 | Psywave damage at 50-150% of attacker level |
| 0xA1 | atkA1_counterdamagecalculator | 0x08027BB8 | 0x0802B21C | 248 | Counter: double recorded physical damage and choose source/follow-me target |
| 0xA2 | atkA2_mirrorcoatdamagecalculator | 0x08027CB0 | 0x0802B314 | 248 | Mirror Coat: double recorded special damage |
| 0xA3 | atkA3_disablelastusedattack | 0x08027DA8 | 0x0802B40C | 324 | Disable last used move for random 2-5 turns |
| 0xA4 | atkA4_trysetencore | 0x08027EEC | 0x0802B550 | 308 | Encore last move for random 3-6 turns |
| 0xA5 | atkA5_painsplitdmgcalc | 0x08028020 | 0x0802B684 | 248 | Pain Split average-HP delta calculation |
| 0xA6 | atkA6_settypetorandomresistance | 0x08028118 | 0x0802B77C | 504 | Conversion 2: choose a resistance type from type chart |
| 0xA7 | atkA7_setalwayshitflag | 0x08028310 | 0x0802B974 | 88 | set sure-hit battler/status3 state |
| 0xA8 | atkA8_copymovepermanently | 0x08028368 | 0x0802B9CC | 652 | Sketch permanent move copy; span includes two-turn/choice helpers |
| 0xA9 | atkA9_trychoosesleeptalkmove | 0x080285F4 | 0x0802BC58 | 312 | Sleep Talk choose one legal move from four slots |
| 0xAA | atkAA_setdestinybond | 0x0802872C | 0x0802BD90 | 144 | set Destiny Bond; span includes destiny-bond trigger helper |
| 0xAB | atkAB_trysetdestinybondtohappen | 0x080287BC | 0x0802BE20 | 24 | arm Destiny Bond hit marker when target qualifies |
| 0xAC | atkAC_remaininghptopower | 0x080287D4 | 0x0802BE38 | 104 | Flail/Reversal dynamic power from scaled HP |
| 0xAD | atkAD_tryspiteppreduce | 0x0802883C | 0x0802BEA0 | 496 | Spite remove random 2-5 PP from target's last move |
| 0xAE | atkAE_healpartystatus | 0x08028A2C | 0x0802C090 | 636 | Heal Bell/Aromatherapy party status healing with Soundproof behavior |
| 0xAF | atkAF_cursetarget | 0x08028CA8 | 0x0802C30C | 156 | Ghost Curse target status plus half-max-HP cost |
| 0xB0 | atkB0_trysetspikes | 0x08028D44 | 0x0802C3A8 | 140 | add Spikes layer up to three |
| 0xB1 | atkB1_setforesight | 0x08028DD0 | 0x0802C434 | 48 | set Foresight status |
| 0xB2 | atkB2_trysetperishsong | 0x08028E00 | 0x0802C464 | 184 | apply three-turn Perish Song except Soundproof/already affected |
| 0xB3 | atkB3_rolloutdamagecalculation | 0x08028EB8 | 0x0802C51C | 380 | five-hit Rollout scaling and Defense Curl doubling |
| 0xB4 | atkB4_jumpifconfusedandstatmaxed | 0x08029034 | 0x0802C698 | 104 | branch if confused and requested stat is already max |
| 0xB5 | atkB5_furycuttercalc | 0x0802909C | 0x0802C700 | 180 | Fury Cutter stacking power up to five-count state |
| 0xB6 | atkB6_happinesstodamagecalculation | 0x08029150 | 0x0802C7B4 | 132 | Return/Frustration power from friendship |
| 0xB7 | atkB7_presentdamagecalculation | 0x080291D4 | 0x0802C838 | 188 | Present choose 40/80/120 power or quarter-HP healing |
| 0xB8 | atkB8_setsafeguard | 0x08029290 | 0x0802C8F4 | 144 | start five-turn Safeguard |
| 0xB9 | atkB9_magnitudedamagecalculation | 0x08029320 | 0x0802C984 | 292 | Magnitude 4-10 weighted power selection |
| 0xBA | atkBA_jumpifnopursuitswitchdmg | 0x08029444 | 0x0802CAA8 | 376 | Pursuit interception of switching target |
| 0xBB | atkBB_setsunny | 0x080295BC | 0x0802CC20 | 88 | start five-turn temporary sun |
| 0xBC | atkBC_maxattackhalvehp | 0x08029614 | 0x0802CC78 | 128 | Belly Drum set Attack stage max at half-HP cost |
| 0xBD | atkBD_copyfoestats | 0x08029694 | 0x0802CCF8 | 72 | Psych Up copy all eight stat stages |
| 0xBE | atkBE_rapidspinfree | 0x080296DC | 0x0802CD40 | 324 | Rapid Spin clear Wrap, Leech Seed, then Spikes |
| 0xBF | atkBF_setdefensecurlbit | 0x08029820 | 0x0802CE84 | 48 | set Defense Curl status bit |

## Internal helpers

| Helper | Retail | Debug | Bytes | Role |
| --- | --- | --- | ---: | --- |
| IsTwoTurnsMove | 0x08028524 | 0x0802BB88 | 60 | identify charging/two-turn move effects |
| IsMoveUnchoosable | 0x08028560 | 0x0802BBC4 | 40 | reject Sleep Talk selection of empty/Sleep Talk/Assist/Mirror Move/Metronome |
| AttacksThisTurn | 0x08028588 | 0x0802BBEC | 108 | return charging turn versus attacking turn, including sunny SolarBeam |
| TrySetDestinyBondToHappen | 0x0802875C | 0x0802BDC0 | 96 | set Destiny Bond hit marker across opposing sides |

## Four-move constraints

Disable, Encore, Sketch, Sleep Talk and Spite all scan the battler's four move slots directly. Sleep Talk builds a four-bit unusable mask and requires the mask to differ from 0xF before selecting `Random() & 3`.

Sketch serializes exactly four 16-bit move IDs, four PP bytes and the PP-bonus byte through the controller.

## Timers and counters

- Disable duration: random 2..5 turns;
- Encore duration: random 3..6 turns;
- Spite PP loss: random 2..5;
- Spikes maximum layers: 3;
- Perish Song timers: 3;
- Rollout initial timer: 5;
- Fury Cutter counter cap: 5;
- Safeguard duration: 5 turns;
- Sunny Day duration: 5 turns.

## Damage formulas

- Psywave: attacker level × random 50..150% / 100;
- Counter / Mirror Coat: 2 × recorded physical/special damage;
- Super Fang: half current target HP, minimum 1;
- Ghost Curse: attacker max HP / 2 cost;
- Present: weighted 40/80/120 power or target max HP / 4 healing;
- Belly Drum: max Attack stage (12) at max HP / 2 cost.

## Legacy field and cleanup behavior

Rapid Spin removes effects in the original Ruby order: Wrap, then Leech Seed, then Spikes. It does not implement later-generation Rapid Spin effects.

Perish Song excludes Soundproof and already-affected battlers, then applies Pressure PP loss through the previously mapped Pressure helper.

## Next opcode

Opcode 0xC0 `atkC0_recoverbasedonsunlight` begins at Retail **0x08029850** / Debug **0x0802CEB4**, still at delta **+0x3664**.
