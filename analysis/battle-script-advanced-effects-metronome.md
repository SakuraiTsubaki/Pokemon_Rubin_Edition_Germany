# German battle script advanced move-effects and Metronome core

This slice maps opcodes 0x80 through 0x9F together with four physically embedded helpers.

## Exact slice

| Profile | Start | End exclusive | Size | SHA-256 |
| --- | --- | --- | ---: | --- |
| Retail Rev 0 / Rev 1 | 0x08025A70 | 0x08027B64 | 8,436 bytes | 4ff38ee3cd2d99b00c61ac34cd1ce77e206fdfc8c240cf20bf1216b8fa4ab805 |
| Debug | 0x08029014 | 0x0802B1C8 | 8,628 bytes | 64e2ac7d35bed453b2c3ee3b6d6531e04ad38ace1a7dd9d4829f8643cc5726ff |

Retail Rev 0 and Rev 1 are byte-identical. The 192-byte size difference is entirely the Debug-only path inside opcode 0x9E.

## Opcode map

| Opcode | Function | Retail | Debug | Span | Delta | Role |
| ---: | --- | --- | --- | ---: | ---: | --- |
| 0x80 | atk80_manipulatedamage | 0x08025A70 | 0x08029014 | 128 | +0x35A4 | negate, halve/cap, or double current battle damage |
| 0x81 | atk81_trysetrest | 0x08025AF0 | 0x08029094 | 208 | +0x35A4 | Rest full heal setup and fixed sleep status |
| 0x82 | atk82_jumpifnotfirstturn | 0x08025BC0 | 0x08029164 | 72 | +0x35A4 | branch unless attacker is on first turn |
| 0x83 | atk83_nop | 0x08025C08 | 0x080291AC | 172 | +0x35A4 | one-byte no-op; physical span includes UproarWakeUpCheck |
| 0x84 | atk84_jumpifcantmakeasleep | 0x08025CB4 | 0x08029258 | 124 | +0x35A4 | reject sleep under Uproar, Insomnia or Vital Spirit |
| 0x85 | atk85_stockpile | 0x08025D30 | 0x080292D4 | 124 | +0x35A4 | increment Stockpile counter up to three |
| 0x86 | atk86_stockpiletobasedamage | 0x08025DAC | 0x08029350 | 296 | +0x35A4 | Spit Up-style damage using Stockpile count |
| 0x87 | atk87_stockpiletohpheal | 0x08025ED4 | 0x08029478 | 236 | +0x35A4 | Swallow-style healing from Stockpile count |
| 0x88 | atk88_negativedamage | 0x08025FC0 | 0x08029564 | 1240 | +0x35A4 | set healing/recoil-style negative half of dealt HP; span includes ChangeStatBuffs |
| 0x89 | atk89_statbuffchange | 0x08026498 | 0x08029A3C | 84 | +0x35A4 | apply encoded stat change through ChangeStatBuffs |
| 0x8A | atk8A_normalisebuffs | 0x080264EC | 0x08029A90 | 84 | +0x35A4 | Haze: reset eight stat stages of all battlers to neutral 6 |
| 0x8B | atk8B_setbide | 0x08026540 | 0x08029AE4 | 112 | +0x35A4 | initialize Bide multi-turn state and damage accumulator |
| 0x8C | atk8C_confuseifrepeatingattackends | 0x080265B0 | 0x08029B54 | 64 | +0x35A4 | queue confusion after locked repeating attack ends |
| 0x8D | atk8D_setmultihitcounter | 0x080265F0 | 0x08029B94 | 76 | +0x35A4 | initialize explicit or random multi-hit count |
| 0x8E | atk8E_initmultihitstring | 0x0802663C | 0x08029BE0 | 296 | +0x35A4 | initialize multi-hit text count; span includes forced-switch level helper |
| 0x8F | atk8F_forcerandomswitch | 0x08026764 | 0x08029D08 | 764 | +0x35A4 | Roar/Whirlwind-style forced switch with trainer/wild level rules |
| 0x90 | atk90_tryconversiontypechange | 0x08026A60 | 0x0802A004 | 420 | +0x35A4 | Conversion: randomly adopt a type from one of four known moves |
| 0x91 | atk91_givepaydaymoney | 0x08026C04 | 0x0802A1A8 | 144 | +0x35A4 | award accumulated Pay Day money outside link battles |
| 0x92 | atk92_setlightscreen | 0x08026C94 | 0x0802A238 | 184 | +0x35A4 | start five-turn Light Screen |
| 0x93 | atk93_tryKO | 0x08026D4C | 0x0802A2F0 | 736 | +0x35A4 | OHKO calculation with Sturdy, Focus Band, level and accuracy logic |
| 0x94 | atk94_damagetohalftargethp | 0x0802702C | 0x0802A5D0 | 60 | +0x35A4 | set damage to half target current HP, minimum one |
| 0x95 | atk95_setsandstorm | 0x08027068 | 0x0802A60C | 88 | +0x35A4 | start five-turn temporary Sandstorm |
| 0x96 | atk96_weatherdamage | 0x080270C0 | 0x0802A664 | 376 | +0x35A4 | apply Sandstorm/Hail residual damage and immunities |
| 0x97 | atk97_tryinfatuating | 0x08027238 | 0x0802A7DC | 468 | +0x35A4 | Attract gender/personality check with Oblivious handling |
| 0x98 | atk98_updatestatusicon | 0x0802740C | 0x0802A9B0 | 272 | +0x35A4 | emit one or both allied status icon updates |
| 0x99 | atk99_setmist | 0x0802751C | 0x0802AAC0 | 148 | +0x35A4 | start five-turn Mist |
| 0x9A | atk9A_setfocusenergy | 0x080275B0 | 0x0802AB54 | 92 | +0x35A4 | set Focus Energy once |
| 0x9B | atk9B_transformdataexecution | 0x0802760C | 0x0802ABB0 | 416 | +0x35A4 | Transform battle data, four moves and PP capped to five |
| 0x9C | atk9C_setsubstitute | 0x080277AC | 0x0802AD50 | 260 | +0x35A4 | create quarter-max-HP Substitute |
| 0x9D | atk9D_mimicattackcopy | 0x080278B0 | 0x0802AE54 | 476 | +0x35A4 | Mimic last move into current move slot with five-PP cap |
| 0x9E | atk9E_metronome | 0x08027A8C | 0x0802B030 | 168 | +0x35A4 | choose legal random move; Debug adds sequential move-test path |
| 0x9F | atk9F_dmgtolevel | 0x08027B34 | 0x0802B198 | 48 | +0x3664 | set damage equal to attacker level |

## Embedded helper map

| Helper | Retail | Debug | Bytes | Role |
| --- | --- | --- | ---: | --- |
| UproarWakeUpCheck | 0x08025C18 | 0x080291BC | 156 | scan active battlers for Uproar unless sleeper has Soundproof |
| ChangeStatBuffs | 0x08025FF4 | 0x08029598 | 1188 | central stat-stage change helper with Mist/Protect/ability/Shield Dust handling |
| ForceSwitchLevelCheck (sub_80264C0) | 0x08026694 | 0x08029C38 | 208 | trainer/wild forced-switch level and random success helper |
| IsMoveUncopyable | 0x08027868 | 0x0802AE0C | 72 | check Mimic/Metronome forbidden move list |

These helper starts were verified against the supplied German binaries. They are not inferred from historical source symbol addresses.

## Stat-stage compatibility core

`ChangeStatBuffs` is 1,188 bytes and enforces the original stat-stage model:

- eight stat stages per battler;
- range 0..12;
- neutral value 6;
- Mist prevention;
- Protect interaction;
- Clear Body / White Smoke;
- Keen Eye protecting Accuracy;
- Hyper Cutter protecting Attack;
- Shield Dust blocking secondary-effect stat changes;
- separate failure scripts/messages for capped or blocked changes.

Opcode 0x8A Haze resets all eight stages for all active battlers to neutral 6.

## Stockpile / multi-hit

Stockpile is capped at **3**. Spit Up multiplies base damage by the counter, while Swallow heals:

- 1 Stockpile -> max HP / 4;
- 2 -> max HP / 2;
- 3 -> full max HP.

The original random multi-hit command uses the Generation III 2-to-5-hit selection routine and stores the result in a byte counter.

## Forced switching

`atk8F_forcerandomswitch` assumes:

- six party slots;
- three-slot halves in Multi Battle;
- maximum four active battlers;
- random replacement selection from valid non-Egg, non-fainted party members;
- a level-dependent failure calculation for the wild-battle path.

## Conversion / Transform / Mimic

Conversion samples from exactly four move slots. Transform copies the first 0x24 bytes of the target BattlePokemon state and then rewrites the copied four PP values to at most 5. Mimic also scans exactly four slots, copies a 16-bit move ID and caps copied PP at 5.

These are strong runtime-level four-move constraints, not just UI constants.

## Weather and side effects

- Light Screen duration: 5 turns;
- Sandstorm duration: 5 turns;
- Mist duration: 5 turns;
- Sandstorm/Hail residual damage: max HP / 16, minimum 1 when applicable;
- Substitute cost/HP: max HP / 4, minimum 1.

## OHKO

`atk93_tryKO` combines original Ruby OHKO behavior with:

- Sturdy immunity;
- Focus Band survival;
- attacker/target level comparison;
- move accuracy plus level difference;
- semi-invulnerable state checks;
- Endure/Focus Band survival result flags.

## Debug Metronome path

Opcode 0x9E is the second major Debug-only growth inside battle_script_commands.

Retail Metronome randomly samples `(Random() & 0x1FF) + 1`, rejects IDs outside `NUM_MOVES`, and rejects the forbidden-copy list.

The Debug build adds a deterministic test mode when move slot 1 is empty while slots 2 and 3 are populated. A shared 16-bit test cursor walks the configured move-ID range, redirects directly to the selected move-effect script, suppresses PP deduction and recomputes the target.

- Retail opcode span: 168 bytes
- Debug opcode span: 360 bytes
- Debug-only growth: **192 bytes (0xC0)**
- delta through opcode 0x9E entry: +0x35A4
- delta from opcode 0x9F onward: **+0x3664**

This Debug path is particularly useful as a future move-effect regression-test donor.

## Next opcode

Opcode 0xA0 `atkA0_psywavedamageeffect` begins at Retail **0x08027B64** / Debug **0x0802B1C8**, with the new stable Debug delta **+0x3664**.
