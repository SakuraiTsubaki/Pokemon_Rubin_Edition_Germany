# German pokemon_1 core

The complete `pokemon_1` module is now mapped directly from the supplied German Retail, Rev 1 and Debug ROMs.

## Module boundary

| Profile | Start | End exclusive | Size | SHA-256 |
| --- | --- | --- | ---: | --- |
| Retail Rev 0 / Rev 1 | 0x0803A894 | 0x0803BC00 | 4,972 bytes (0x136C) | b1dcf9b7bf3072ad0ab17e2d85a1cbcea07df28f5a509be3ac41e502cb7ada2e |
| Debug | 0x0803E768 | 0x0803FD7C | 5,652 bytes (0x1614) | 8da5f12cbf393f7623b27b2c855447dde85c1fec05219e5e047aaf1c4f875027 |

Retail Rev 0 and Rev 1 are byte-identical throughout the entire module.

Debug is exactly **680 bytes (0x2A8)** larger. The sole extra function is `Nakamura_NakaGenderTest_RecalcStats`.

## Function map

| Function | Retail | Debug | Bytes | Delta | Role |
| --- | --- | --- | ---: | ---: | --- |
| ZeroBoxMonData | 0x0803A894 | 0x0803E768 | 24 | +0x3ED4 | clear all 0x50 bytes of BoxPokemon |
| ZeroMonData | 0x0803A8AC | 0x0803E780 | 128 | +0x3ED4 | clear BoxPokemon plus party-battle fields |
| ZeroPlayerPartyMons | 0x0803A92C | 0x0803E800 | 32 | +0x3ED4 | clear six player-party Pokemon records |
| ZeroEnemyPartyMons | 0x0803A94C | 0x0803E820 | 32 | +0x3ED4 | clear six enemy-party Pokemon records |
| CreateMon | 0x0803A96C | 0x0803E840 | 112 | +0x3ED4 | create BoxMon, set level/mail, calculate party stats |
| CreateBoxMon | 0x0803A9DC | 0x0803E8B0 | 724 | +0x3ED4 | initialize personality/OT/nickname/language/species/EXP/friendship/met data/IVs/ability/moves |
| CreateMonWithNature | 0x0803ACB0 | 0x0803EB84 | 104 | +0x3ED4 | reroll personality until requested nature |
| CreateMonWithGenderNatureLetter | 0x0803AD18 | 0x0803EBEC | 256 | +0x3ED4 | reroll personality until requested nature/gender/Unown letter |
| CreateMaleMon | 0x0803AE18 | 0x0803ECEC | 104 | +0x3ED4 | create male Pokemon with random personality/OT |
| CreateMonWithIVsPersonality | 0x0803AE80 | 0x0803ED54 | 64 | +0x3ED4 | create fixed-personality Pokemon then set packed IVs |
| CreateMonWithIVsOTID | 0x0803AEC0 | 0x0803ED94 | 116 | +0x3ED4 | create Pokemon then set six explicit IV bytes and fixed OT |
| CreateMonWithEVSpread | 0x0803AF34 | 0x0803EE08 | 136 | +0x3ED4 | distribute 510 EV points across selected six-stat mask |
| sub_803ADE8 | 0x0803AFBC | 0x0803EE90 | 400 | +0x3ED4 | import UnknownPokemonStruct into Pokemon including four moves/EVs/IVs/language |
| sub_803AF78 | 0x0803B14C | 0x0803F020 | 428 | +0x3ED4 | export Pokemon into UnknownPokemonStruct including four moves/EVs/IVs/personality |
| CalculateBoxMonChecksum | 0x0803B2F8 | 0x0803F1CC | 148 | +0x3ED4 | sum 24 decrypted 16-bit words across four personality-ordered substructs |
| CalculateMonStats | 0x0803B38C | 0x0803F260 | 764 | +0x3ED4 | derive level/HP/five stats from species, IVs, EVs and nature |
| ExpandBoxMon | 0x0803B688 | 0x0803F804 | 80 | +0x417C | expand boxed record into party Pokemon and calculate stats |
| GetLevelFromMonExp | 0x0803B6D8 | 0x0803F854 | 108 | +0x417C | derive level 1..100 from growth-rate EXP table |
| GetLevelFromBoxMonExp | 0x0803B744 | 0x0803F8C0 | 108 | +0x417C | boxed-record level derivation |
| GiveMoveToMon | 0x0803B7B0 | 0x0803F92C | 20 | +0x417C | party-mon wrapper for GiveMoveToBoxMon |
| GiveMoveToBoxMon | 0x0803B7C4 | 0x0803F940 | 112 | +0x417C | insert 16-bit move into first free of four slots or report duplicate/full |
| GiveMoveToBattleMon | 0x0803B834 | 0x0803F9B0 | 68 | +0x417C | insert move into first free BattlePokemon move slot |
| SetMonMoveSlot | 0x0803B878 | 0x0803F9F4 | 64 | +0x417C | set move and base PP for selected party-mon slot |
| SetBattleMonMoveSlot | 0x0803B8B8 | 0x0803FA34 | 48 | +0x417C | set move and base PP for selected BattlePokemon slot |
| GiveMonInitialMoveset | 0x0803B8E8 | 0x0803FA64 | 12 | +0x417C | party-mon wrapper for boxed initial moveset |
| GiveBoxMonInitialMoveset | 0x0803B8F4 | 0x0803FA70 | 168 | +0x417C | scan packed level-up learnset and retain latest four moves |
| MonTryLearningNewMove | 0x0803B99C | 0x0803FB18 | 268 | +0x417C | advance per-level learnset cursor and offer next move |
| DeleteFirstMoveAndGiveMoveToMon | 0x0803BAA8 | 0x0803FC24 | 172 | +0x417C | shift four move/PP slots left and append new move |
| DeleteFirstMoveAndGiveMoveToBoxMon | 0x0803BB54 | 0x0803FCD0 | 172 | +0x417C | boxed-record move/PP shift and append |

Debug-only:

| Function | Debug | Bytes | Role |
| --- | --- | ---: | --- |
| Nakamura_NakaGenderTest_RecalcStats | 0x0803F55C | 680 | recalculate level/HP/five stats for the development gender-test path |

Because that function is inserted immediately after `CalculateMonStats`, the Retail→Debug displacement changes from **+0x3ED4** to **+0x417C** at `ExpandBoxMon`.

## Core Pokémon record layout

The original boxed record is **0x50 bytes (80 bytes)**:

- personality: 32-bit;
- OT ID: 32-bit;
- nickname/language/flags/OT name/markings/checksum;
- secure payload: 48 bytes.

The secure payload is four **12-byte** substructs. Each substruct is also viewed as six 16-bit checksum words. Personality chooses one of 24 substruct orders.

The party `Pokemon` structure extends BoxPokemon with status, level, mail, HP, max HP, Attack, Defense, Speed, Special Attack and Special Defense, for an original total size of **0x64 bytes (100 bytes)**.

## Secure substruct contents

Substruct 0:

- species (16-bit);
- held item (16-bit);
- experience (32-bit);
- PP bonuses;
- friendship.

Substruct 1:

- exactly **four 16-bit moves**;
- exactly **four PP bytes**.

Substruct 2:

- six EV bytes: HP / Attack / Defense / Speed / Sp. Attack / Sp. Defense;
- five contest condition bytes plus sheen.

Substruct 3:

- Pokérus / met location / met level / game / ball / OT gender;
- six **5-bit IVs**;
- egg / alternate-ability bits;
- ribbon/event flags.

## Checksum

`CalculateBoxMonChecksum` sums exactly **24 unsigned 16-bit words**: six words from each of the four personality-ordered substructs.

This checksum sits directly on the encrypted boxed payload path. Expanding or replacing the secure layout therefore requires an explicit versioned save/box format rather than silently widening the existing structure.

## Creation and personality

`CreateBoxMon` establishes the original generation pipeline:

- personality generated as 32-bit value unless fixed;
- optional anti-shiny OT reroll uses the Generation III shiny XOR threshold `< 8`;
- nickname initialized from species name;
- language stored explicitly;
- EXP initialized from species growth-rate table and requested level;
- friendship from base stats;
- met location/level/game/Poké Ball/OT gender;
- six IVs, either one fixed value or two RNG words split into three 5-bit IVs each;
- alternate ability selected from personality bit 0 when species has ability 2;
- level-up initial moveset applied.

`CreateMonWithGenderNatureLetter` derives Unown form from four 2-bit personality fragments and modulo 28 while simultaneously enforcing requested nature and gender.

## Stats

`CalculateMonStats` uses the six original IV/EV values and nature modifiers. HP follows the Generation III formula and Shedinja is forced to 1 max HP.

The five non-HP stats use the familiar `(2 * base + IV + EV/4) * level / 100 + 5` basis before nature adjustment.

A preserved original bug allows current HP to become <= 0 when max HP drops after a recalculation; the comparison source only repairs this under a separate BUGFIX build flag, not in the German retail ROM.

## EV constraints

`CreateMonWithEVSpread` treats EV selection as a six-bit stat mask and divides **510 total EV points** among selected stats. Each EV field is stored as one byte in the secure record.

## Level / experience

`GetLevelFromMonExp` and `GetLevelFromBoxMonExp` walk the species growth-rate experience table from level 1 through the hard cap **100**.

## Move-storage constraints

The move helpers repeatedly prove the original **four-move** runtime model:

- four 16-bit move IDs;
- four one-byte PP values;
- insertion searches four slots;
- duplicate move detection searches four slots;
- initial level-up learnset keeps the newest four moves by deleting the first when full;
- delete/append helpers shift exactly three old entries then write slot 3.

Level-up learnset entries encode level in the upper bits and the move in a **9-bit move field (`0x1FF`)**. This is a particularly important Generation III limit for a Gen-10-ready data model: the modern move namespace cannot remain tied to this packed legacy encoding.

## Debug-only stat recalculation

`Nakamura_NakaGenderTest_RecalcStats` duplicates much of the stat calculation path for a development gender-test workflow. It is the complete reason `pokemon_1` grows by 0x2A8 in the supplied Debug ROM.

## Next module

`CalculateBaseDamage` begins the next linked module at:

- Retail **0x0803BC00**
- Debug **0x0803FD7C**
- new accumulated delta **+0x417C**.

The boundary is independently proven by the direct BL from `atk05_damagecalc` in each supplied ROM.
