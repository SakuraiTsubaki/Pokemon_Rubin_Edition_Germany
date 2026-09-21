# German battle script late Generation III mechanics core

This slice maps opcodes 0xC0 through 0xDF.

## Exact slice

| Profile | Start | End exclusive | Size | SHA-256 |
| --- | --- | --- | ---: | --- |
| Retail Rev 0 / Rev 1 | 0x08029850 | 0x0802AE54 | 5,636 bytes | 174eb2f5c256fe591be923bbd873e24d3121ff76af5306bafadcf47b9b9b7540 |
| Debug | 0x0802CEB4 | 0x0802E4B8 | 5,636 bytes | 54a42142ac9ed17d164c5186698419eebb41dc38219c608dbecc19631a92a736 |

Retail Rev 0 and Rev 1 are byte-identical and the Debug displacement remains **+0x3664** for every opcode in the slice.

## Opcode map

| Opcode | Function | Retail | Debug | Span | Role |
| ---: | --- | --- | --- | ---: | --- |
| 0xC0 | atkC0_recoverbasedonsunlight | 0x08029850 | 0x0802CEB4 | 264 | Morning Sun/Synthesis/Moonlight healing based on weather |
| 0xC1 | atkC1_hiddenpowercalc | 0x08029958 | 0x0802CFBC | 296 | Hidden Power type and power from six IV low bits |
| 0xC2 | atkC2_selectfirstvalidtarget | 0x08029A80 | 0x0802D0E4 | 116 | select first non-absent battler other than attacker |
| 0xC3 | atkC3_trysetfutureattack | 0x08029AF4 | 0x0802D158 | 296 | schedule Future Sight/Doom Desire with three-count delay and stored damage |
| 0xC4 | atkC4_trydobeatup | 0x08029C1C | 0x0802D280 | 528 | Beat Up six-party contributor scan and per-member damage |
| 0xC5 | atkC5_setsemiinvulnerablebit | 0x08029E2C | 0x0802D490 | 132 | set Fly/Bounce/Dig/Dive semi-invulnerable status |
| 0xC6 | atkC6_clearsemiinvulnerablebit | 0x08029EB0 | 0x0802D514 | 144 | clear Fly/Bounce/Dig/Dive status |
| 0xC7 | atkC7_setminimize | 0x08029F40 | 0x0802D5A4 | 64 | set Minimize status when obedience marker permits |
| 0xC8 | atkC8_sethail | 0x08029F80 | 0x0802D5E4 | 88 | start five-turn temporary Hail |
| 0xC9 | atkC9_jumpifattackandspecialattackcannotfall | 0x08029FD8 | 0x0802D63C | 156 | Memento gate and attacker self-KO setup |
| 0xCA | atkCA_setforcedtarget | 0x0802A074 | 0x0802D6D8 | 76 | Follow Me one-turn forced-target state |
| 0xCB | atkCB_setcharge | 0x0802A0C0 | 0x0802D724 | 100 | set Charge status and two-turn counters |
| 0xCC | atkCC_callenvironmentattack | 0x0802A124 | 0x0802D788 | 116 | Nature Power environment-to-move dispatch |
| 0xCD | atkCD_cureifburnedparalysedorpoisoned | 0x0802A198 | 0x0802D7FC | 132 | Refresh poison/burn/paralysis/toxic cure |
| 0xCE | atkCE_settorment | 0x0802A21C | 0x0802D880 | 88 | set Torment unless already active |
| 0xCF | atkCF_jumpifnodamage | 0x0802A274 | 0x0802D8D8 | 92 | branch according to recorded physical/special damage |
| 0xD0 | atkD0_settaunt | 0x0802A2D0 | 0x0802D934 | 116 | set two-turn Taunt timers |
| 0xD1 | atkD1_trysethelpinghand | 0x0802A344 | 0x0802D9A8 | 168 | set Helping Hand on live double-battle partner |
| 0xD2 | atkD2_tryswapitems | 0x0802A3EC | 0x0802DA50 | 664 | Trick item swap with mail/Enigma/Sticky Hold/Knock Off restrictions |
| 0xD3 | atkD3_trycopyability | 0x0802A684 | 0x0802DCE8 | 120 | Role Play copy target ability except none/Wonder Guard |
| 0xD4 | atkD4_trywish | 0x0802A6FC | 0x0802DD60 | 212 | Wish schedule/heal state with two-count timer and half-HP healing |
| 0xD5 | atkD5_trysetroots | 0x0802A7D0 | 0x0802DE34 | 88 | set Ingrain/Rooted status |
| 0xD6 | atkD6_doubledamagedealtifdamaged | 0x0802A828 | 0x0802DE8C | 104 | set 2x damage multiplier when attacker was damaged by target |
| 0xD7 | atkD7_setyawn | 0x0802A890 | 0x0802DEF4 | 112 | set Yawn two-turn status if target has no status/yawn |
| 0xD8 | atkD8_setdamagetohealthdifference | 0x0802A900 | 0x0802DF64 | 108 | Endeavor HP-difference damage |
| 0xD9 | atkD9_scaledamagebyhealthratio | 0x0802A96C | 0x0802DFD0 | 100 | Eruption/Water Spout power scaled by current/max HP |
| 0xDA | atkDA_tryswapabilities | 0x0802A9D0 | 0x0802E034 | 152 | Skill Swap abilities except Wonder Guard/no-effect invalid cases |
| 0xDB | atkDB_tryimprison | 0x0802AA68 | 0x0802E0CC | 256 | Imprison opposing move overlap with Pressure handling |
| 0xDC | atkDC_trysetgrudge | 0x0802AB68 | 0x0802E1CC | 88 | set Grudge status |
| 0xDD | atkDD_weightdamagecalculation | 0x0802ABC0 | 0x0802E224 | 152 | Low Kick power from target Pokédex weight table |
| 0xDE | atkDE_assistattackselect | 0x0802AC58 | 0x0802E2BC | 376 | Assist scan party moves and choose legal random move |
| 0xDF | atkDF_trysetmagiccoat | 0x0802ADD0 | 0x0802E434 | 132 | set Magic Coat bounce unless attacker is final turn action |

## Weather-dependent healing

Opcode 0xC0 heals the user by:

- no effective weather: max HP / 2;
- sun: 20/30 max HP (two thirds);
- other effective weather: max HP / 4;
- minimum healing value: 1.

## Hidden Power

Opcode 0xC1 derives power from the second-lowest bit of all six IVs and type from the lowest bit of all six IVs. Power is `30 + floor(bits * 40 / 63)`, while type maps the six-bit value across the original 15 non-Normal/non-Mystery type range.

This is strictly the Generation III Hidden Power model and should remain inside the legacy ruleset.

## Delayed effects

- Future Sight/Doom Desire counter: 3;
- Wish counter: 2, healing max HP / 2;
- Charge timer: 2;
- Yawn timer encoding: 2;
- Hail duration: 5;
- Follow Me timer: 1.

## Party/move fixed capacities

`atkC4_trydobeatup` scans exactly six party slots. `atkDB_tryimprison` compares the attacker's four moves against four move slots on opposing active battlers. `atkDE_assistattackselect` scans six party slots × four moves per eligible party member.

These are concrete runtime loops that must be generalized if storage or rules ever move beyond the original 6×4 topology.

## Item and ability mutation

`atkD2_tryswapitems` handles Trick-style item swapping while enforcing:

- ordinary trainer-battle restrictions;
- previously Knocked Off items;
- Enigma Berry exclusion;
- Mail exclusion;
- Sticky Hold;
- controller synchronization for both 16-bit item fields;
- Choice-move lock reset after the swap.

`atkD3_trycopyability` implements Role Play and refuses Wonder Guard. `atkDA_tryswapabilities` implements Skill Swap with the same Wonder Guard restriction.

## Environment dispatch

Nature Power directly indexes the existing 10-value battle-environment table mapped earlier. This couples battle-script behavior to the environment-ID model and should be routed through an extensible environment-effect registry for future expansion.

## Next opcode

Opcode 0xE0 `atkE0_trysetmagiccoat` begins at Retail **0x0802AE54** / Debug **0x0802E4B8**, still at delta **+0x3664**.
