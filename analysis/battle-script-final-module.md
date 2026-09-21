# German battle script final commands and complete module

This slice maps the final opcodes 0xE0 through 0xF7 and closes battle_script_commands.

## Final opcode slice

| Profile | Start | End exclusive | Size | SHA-256 |
| --- | --- | --- | ---: | --- |
| Retail Rev 0 / Rev 1 | 0x0802AE54 | 0x0802C144 | 4,848 bytes | 5f0c2a052fc9513f290c5cd3988c9468509211815bd88cd29d0ddaf3e884ead5 |
| Debug | 0x0802E4B8 | 0x0802F7A8 | 4,848 bytes | 80a072aa0e859189edb0bf58407561412377dd7b941581a8621ddd1037581d0a |

Retail Rev 0 and Rev 1 are byte-identical. Every final command remains at **+0x3664** in Debug.

## Opcode map

| Opcode | Function | Retail | Debug | Span | Role |
| ---: | --- | --- | --- | ---: | --- |
| 0xE0 | atkE0_trysetsnatch | 0x0802AE54 | 0x0802E4B8 | 124 | set Snatch interception state when turn ordering permits |
| 0xE1 | atkE1_trygetintimidatetarget | 0x0802AED0 | 0x0802E534 | 220 | find next valid opposing Intimidate target |
| 0xE2 | atkE2_switchoutabilities | 0x0802AFAC | 0x0802E610 | 132 | run switch-out ability behavior such as Natural Cure |
| 0xE3 | atkE3_jumpifhasnohp | 0x0802B030 | 0x0802E694 | 84 | branch if selected battler has zero HP |
| 0xE4 | atkE4_getsecretpowereffect | 0x0802B084 | 0x0802E6E8 | 184 | map battle environment to Secret Power effect |
| 0xE5 | atkE5_pickup | 0x0802B13C | 0x0802E7A0 | 236 | scan six-player party for Pickup item generation |
| 0xE6 | atkE6_docastformchangeanimation | 0x0802B228 | 0x0802E88C | 108 | emit Castform form-change animation |
| 0xE7 | atkE7_trycastformdatachange | 0x0802B294 | 0x0802E8F8 | 72 | run Forecast/Castform data change and callback script |
| 0xE8 | atkE8_settypebasedhalvers | 0x0802B2DC | 0x0802E940 | 184 | set Mud Sport or Water Sport status |
| 0xE9 | atkE9_setweatherballtype | 0x0802B394 | 0x0802E9F8 | 204 | Weather Ball type selection and 2x weather multiplier |
| 0xEA | atkEA_tryrecycleitem | 0x0802B460 | 0x0802EAC4 | 164 | restore previously consumed held item |
| 0xEB | atkEB_settypetoenvironment | 0x0802B504 | 0x0802EB68 | 176 | Camouflage type assignment from battle environment |
| 0xEC | atkEC_pursuitrelated | 0x0802B5B4 | 0x0802EC18 | 212 | double-battle Pursuit interception setup |
| 0xED | atkEF_snatchsetbattlers | 0x0802B688 | 0x0802ECEC | 104 | rotate attacker/target/scripting battler for Snatch |
| 0xEE | atkEE_removelightscreenreflect | 0x0802B6F0 | 0x0802ED54 | 156 | Brick Break removal of Reflect and Light Screen |
| 0xEF | atkEF_handleballthrow | 0x0802B78C | 0x0802EDF0 | 936 | Poké Ball catch-rate, ball-bonus and shake calculation |
| 0xF0 | atkF0_givecaughtmon | 0x0802BB34 | 0x0802F198 | 128 | give caught Pokémon to player and record battle result |
| 0xF1 | atkF1_trysetcaughtmondexflags | 0x0802BBB4 | 0x0802F218 | 176 | set Pokédex caught flags and Unown/Spinda personalities |
| 0xF2 | atkF2_displaydexinfo | 0x0802BC64 | 0x0802F2C8 | 512 | caught-Pokémon Pokédex display; span includes three UI helpers |
| 0xF3 | atkF3_trygivecaughtmonnick | 0x0802BE64 | 0x0802F4C8 | 608 | caught-Pokémon nickname yes/no/naming-screen state machine |
| 0xF4 | atkF4_subattackerhpbydmg | 0x0802C0C4 | 0x0802F728 | 48 | subtract current battle damage from attacker HP |
| 0xF5 | atkF5_removeattackerstatus1 | 0x0802C0F4 | 0x0802F758 | 40 | clear attacker primary status |
| 0xF6 | atkF6_finishaction | 0x0802C11C | 0x0802F780 | 12 | set action function to ActionFinished |
| 0xF7 | atkF7_finishturn | 0x0802C128 | 0x0802F78C | 28 | finish current action and force turn-action index to battler count |

## UI helpers embedded after opcode 0xF2

| Helper | Retail | Debug | Bytes | Role |
| --- | --- | --- | ---: | --- |
| sub_802BBD4 | 0x0802BDA8 | 0x0802F40C | 152 | draw/clear rectangular battle UI frame tiles |
| sub_802BC6C | 0x0802BE40 | 0x0802F4A4 | 32 | position yes/no menu cursor |
| nullsub_6 | 0x0802BE60 | 0x0802F4C4 | 4 | empty UI callback |

## Environment-driven commands

Secret Power, Weather Ball and Camouflage all directly depend on the original battle-environment ID model previously mapped as ten environment entries. Castform/Forecast also routes through the earlier CastformDataTypeChange helper.

This confirms that field environment, move behavior and form behavior are coupled across multiple modules.

## Pickup

Opcode 0xE5 scans exactly six player-party slots. Each eligible Pickup Pokémon with no held item receives a Pickup roll with a 10% trigger, followed by selection from the original Pickup item probability table.

## Capture core — opcode 0xEF

`atkEF_handleballthrow` is 936 bytes and contains the original Ruby capture algorithm.

Base odds are computed from:

`(catchRate * ballMultiplier / 10) * (3*maxHP - 2*HP) / (3*maxHP)`

Status modifiers:

- sleep/freeze: ×2;
- poison/burn/paralysis: ×1.5.

Ball behavior includes:

- Master Ball guaranteed capture;
- Net Ball Water/Bug bonus;
- Dive Ball map-type bonus;
- Nest Ball level-dependent bonus;
- Repeat Ball caught-before bonus;
- Timer Ball turn-count scaling capped at 4×;
- Luxury/Premier neutral multiplier;
- Safari Ball uses Safari catch factor.

When base odds exceed 254 the capture succeeds immediately; otherwise the original nested square-root shake threshold is evaluated for up to four shakes.

This is a major modernization boundary for later-generation ball modifiers and capture mechanics.

## Caught-Pokémon flow

Opcodes 0xF0..0xF3 cover:

- adding the captured Pokémon to player storage/party;
- Pokédex caught flag;
- preserving Unown and Spinda personalities for Pokédex display;
- fading to Pokédex information;
- restoring battle graphics;
- nickname yes/no UI;
- naming-screen transition;
- six-party-full decision.

## Complete battle_script_commands module

| Profile | Start | End exclusive | Size | SHA-256 |
| --- | --- | --- | ---: | --- |
| Retail Rev 0 / Rev 1 | 0x0801BE24 | 0x0802C144 | 66,336 bytes (0x10320) | 7cda4dc84fef6029645fb5fe6a6eceb05b02e582cf888663c2def8a4d42a6864 |
| Debug | 0x0801F39C | 0x0802F7A8 | 66,572 bytes (0x1040C) | 5938e9fa8bcfd0bf0ec3836249dc89afb2d2943188595188e98122da2ce763fe |

Retail Rev 0 and Rev 1 are byte-identical across the **entire module**.

Debug is exactly **236 bytes (0xEC)** larger. The entire size difference is accounted for:

- opcode 0x15 atk15_seteffectwithchance: +44 bytes (0x2C);
- opcode 0x9E atk9E_metronome: +192 bytes (0xC0);
- total: +236 bytes (0xEC).

The VM command table contains all **248 opcodes 0x00..0xF7**, now mapped across this repository's analysis slices.

## Next module boundary

The next linked source module is `battle_controller_player`.

Its first function `BattleControllerDummy` begins at:

- Retail: **0x0802C144**;
- Debug: **0x0802F7A8**;
- delta: **+0x3664**.

The first two bytes are `70 47` (`bx lr`) in both supplied profiles, directly confirming the boundary.
