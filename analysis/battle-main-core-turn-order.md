# German battle core through turn ordering

This slice begins at the actual BattleMainCB1 entry and ends immediately before RunTurnActionsFunctions.

## Exact slice

| Profile | Start | End exclusive | Size | SHA-256 |
| --- | --- | --- | ---: | --- |
| Retail Rev 0 / Rev 1 | 0x080109F8 | 0x08013AC4 | 12,492 bytes | f201eba9a43a5e002c5d166521c0dd6261d82fe9066ba1115f450cac9ef0f81c |
| Debug | 0x080139E4 | 0x08016B4C | 12,648 bytes | 9d59402f778877241049f44590a8dc7606a24c968b59e0857804e6472094cf07 |

Retail Rev 0 and Rev 1 are byte-identical across the complete slice.

## Function map

| Function | Retail | Debug | Retail bytes | Debug bytes | Extra Debug | Delta |
| --- | --- | --- | ---: | ---: | ---: | ---: |
| BattleMainCB1 | 0x080109F8 | 0x080139E4 | 80 | 212 | 132 | +0x2FEC |
| BattleStartClearSetData | 0x08010A48 | 0x08013AB8 | 788 | 812 | 24 | +0x3070 |
| SwitchInClearSetData | 0x08010D5C | 0x08013DE4 | 960 | 960 | 0 | +0x3088 |
| UndoEffectsAfterFainting | 0x0801111C | 0x080141A4 | 888 | 888 | 0 | +0x3088 |
| bc_8012FAC | 0x08011494 | 0x0801451C | 116 | 116 | 0 | +0x3088 |
| BattlePrepIntroSlide | 0x08011508 | 0x08014590 | 80 | 80 | 0 | +0x3088 |
| sub_8011384 | 0x08011558 | 0x080145E0 | 636 | 636 | 0 | +0x3088 |
| bc_801333C | 0x080117D4 | 0x0801485C | 416 | 416 | 0 | +0x3088 |
| bc_battle_begin_message | 0x08011974 | 0x080149FC | 56 | 56 | 0 | +0x3088 |
| bc_8013568 | 0x080119AC | 0x08014A34 | 40 | 40 | 0 | +0x3088 |
| sub_8011800 | 0x080119D4 | 0x08014A5C | 52 | 52 | 0 | +0x3088 |
| sub_8011834 | 0x08011A08 | 0x08014A90 | 144 | 144 | 0 | +0x3088 |
| bc_801362C | 0x08011A98 | 0x08014B20 | 140 | 140 | 0 | +0x3088 |
| unref_sub_8011950 | 0x08011B24 | 0x08014BAC | 32 | 32 | 0 | +0x3088 |
| sub_8011970 | 0x08011B44 | 0x08014BCC | 68 | 68 | 0 | +0x3088 |
| sub_80119B4 | 0x08011B88 | 0x08014C10 | 180 | 180 | 0 | +0x3088 |
| unref_sub_8011A68 | 0x08011C3C | 0x08014CC4 | 152 | 152 | 0 | +0x3088 |
| BattleBeginFirstTurn | 0x08011CD4 | 0x08014D5C | 712 | 712 | 0 | +0x3088 |
| bc_8013B1C | 0x08011F9C | 0x08015024 | 196 | 196 | 0 | +0x3088 |
| BattleTurnPassed | 0x08012060 | 0x080150E8 | 412 | 412 | 0 | +0x3088 |
| CanRunFromBattle | 0x080121FC | 0x08015284 | 560 | 560 | 0 | +0x3088 |
| sub_8012258 | 0x0801242C | 0x080154B4 | 204 | 204 | 0 | +0x3088 |
| sub_8012324 | 0x080124F8 | 0x08015580 | 3224 | 3224 | 0 | +0x3088 |
| SwapTurnOrder | 0x08013190 | 0x08016218 | 52 | 52 | 0 | +0x3088 |
| GetWhoStrikesFirst | 0x080131C4 | 0x0801624C | 984 | 984 | 0 | +0x3088 |
| SetActionsAndBanksTurnOrder | 0x0801359C | 0x08016624 | 660 | 660 | 0 | +0x3088 |
| TurnValuesCleanUp | 0x08013830 | 0x080168B8 | 288 | 288 | 0 | +0x3088 |
| SpecialStatusesClear | 0x08013950 | 0x080169D8 | 80 | 80 | 0 | +0x3088 |
| CheckFocusPunch_ClearVarsBeforeTurnStarts | 0x080139A0 | 0x08016A28 | 292 | 292 | 0 | +0x3088 |

The next function is RunTurnActionsFunctions:

- Retail: **0x08013AC4**
- Debug: **0x08016B4C**

## Debug divergences in this slice

Only two functions grow in Debug.

### BattleMainCB1

- Retail: 80 bytes
- Debug: 212 bytes
- Extra: **132 bytes (0x84)**

Debug can run debug_sub_80138CC for player-side battlers before normal battle-main/controller dispatch when its automated-input flag is active.

### BattleStartClearSetData

- Retail: 788 bytes
- Debug: 812 bytes
- Extra: **24 bytes (0x18)**

Debug additionally clears the two-byte AI-cycle move-tracker state in shared battle memory.

After BattleStartClearSetData, the accumulated Retail->Debug address displacement is **+0x3088** and remains constant through RunTurnActionsFunctions.

## Original engine capacities exposed here

BattleStartClearSetData directly establishes several fixed Generation III dimensions:

- four battler slots;
- two battle sides;
- eight stat stages per battler;
- four moves per battler elsewhere in action selection;
- six party slots in party-status and switching logic;
- arrays of last move / landed move / result / lock data indexed by four battlers.

SwitchInClearSetData and UndoEffectsAfterFainting clear or preserve per-battler status, DisableStruct, ProtectStruct and move-history state using those fixed dimensions.

## Battle intro flow

The mapped intro chain covers:

- retrieving battler Pokemon data from controllers;
- intro slide;
- constructing gBattleMons;
- trainer pictures;
- wild/opponent sprite loading;
- Pokedex-seen updates;
- six-entry party-status summaries;
- trainer ball throws;
- first-turn transition.

The party-status summary continues to use exactly six HpAndStatus records.

## Action-selection state machine

sub_8012324 is the largest routine in this slice:

- 3,224 bytes in both Retail and Debug.

It manages per-battler action-selection states for:

- fight / move choice;
- item;
- switch;
- run;
- Safari actions;
- selection battle scripts;
- link standby/confirmation.

The routine advances to SetActionsAndBanksTurnOrder only after the confirmed-action count equals gBattlersCount.

## Strike-order mechanics

GetWhoStrikesFirst is 984 bytes and implements the original Ruby ordering model, including:

- Swift Swim and Chlorophyll weather speed multipliers;
- stat-stage speed ratio;
- player's badge speed boost outside link battles;
- Macho Brace speed reduction;
- paralysis speed reduction;
- Quick Claw activation;
- move priority;
- speed comparison;
- random 50/50 tie resolution.

Move IDs used for ordering are already 16-bit in this original path.

## Turn ordering

SetActionsAndBanksTurnOrder:

1. gives run-away handling its dedicated early path;
2. places item and switch actions before remaining actions;
3. fills remaining battlers;
4. pairwise sorts eligible actions using GetWhoStrikesFirst;
5. transitions to CheckFocusPunch_ClearVarsBeforeTurnStarts.

The ordering arrays are still sized for the original maximum of four active battlers.

## Expansion significance

Before introducing later-generation mechanics or more active battlers, the independent German project must audit:

- all four-battler arrays and bit masks;
- six-party assumptions;
- action-selection communication slots;
- priority/speed mechanics;
- status-speed modifiers;
- item/ability ordering hooks;
- battle-script selection state;
- fixed party/status packet formats already mapped earlier.

No modern mechanics are inserted by this commit; this is the German original baseline.
