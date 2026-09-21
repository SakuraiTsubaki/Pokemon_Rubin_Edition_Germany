# German battle_main end-turn and post-battle lifecycle

This slice begins at RunTurnActionsFunctions and ends immediately before HandleAction_UseMove.

## Exact slice

| Profile | Start | End exclusive | Size | SHA-256 |
| --- | --- | --- | ---: | --- |
| Retail Rev 0 / Rev 1 | 0x08013AC4 | 0x080141BC | 1,784 bytes | 2067deeccc15b2bd4a056bd4c9d76a3d1b32edc3da4ef1e4ce3d81aa32bedaaa |
| Debug | 0x08016B4C | 0x08017244 | 1,784 bytes | 270e1c3605cec26515a6c387b0c12ac89884a0f4654eaadc5ab86cce2e22f666 |

Retail Rev 0 and Rev 1 are byte-identical across the complete slice.

Every mapped Debug entry is exactly **+0x3088** from Retail and every function has the same code size in both profiles. No new Debug-only insertion occurs here.

## Function map

| Function | Retail | Debug | Bytes | Role |
| --- | --- | --- | ---: | --- |
| RunTurnActionsFunctions | 0x08013AC4 | 0x08016B4C | 168 | dispatch current action function and select end-turn handler when all battlers have acted |
| HandleEndTurn_BattleWon | 0x08013B6C | 0x08016BF4 | 460 | select link/tower/trainer/wild victory script and victory music |
| HandleEndTurn_BattleLost | 0x08013D38 | 0x08016DC0 | 120 | select link or local defeat script |
| HandleEndTurn_RanFromBattle | 0x08013DB0 | 0x08016E38 | 108 | select normal/Smoke Ball/ability escape message script |
| HandleEndTurn_MonFled | 0x08013E1C | 0x08016EA4 | 84 | prepare fleeing wild Pokemon nickname and flee script |
| HandleEndTurn_FinishBattle | 0x08013E70 | 0x08016EF8 | 268 | run final battle script or begin fade/music shutdown and post-battle transition |
| FreeResetData_ReturnToOvOrDoEvolutions | 0x08013F7C | 0x08017004 | 80 | reset sprite data after fade and select evolution processing or overworld return |
| TryEvolvePokemon | 0x08013FCC | 0x08017054 | 144 | scan six party bits and launch level-up evolution scenes |
| WaitForEvoSceneToFinish | 0x0801405C | 0x080170E4 | 40 | wait for evolution callback to return to BattleMainCB2 |
| ReturnFromBattleToOverworld | 0x08014084 | 0x0801710C | 164 | Pokerus/roamer/result cleanup and restore saved overworld callback |
| RunBattleScriptCommands_PopCallbacksStack | 0x08014128 | 0x080171B0 | 104 | resume stacked battle-main callback or run next script command |
| RunBattleScriptCommands | 0x08014190 | 0x08017218 | 44 | run current battle script command when controllers are idle |

The next function is HandleAction_UseMove:

- Retail: **0x080141BC**
- Debug: **0x08017244**

## End-of-turn dispatch

RunTurnActionsFunctions dispatches through the original action-function table. If a battle outcome is already set, it forces the finished-action path. Once gCurrentTurnActionNumber reaches gBattlersCount, it clears passive-HP-update state and selects the result handler from the battle-outcome table.

This establishes two original extensibility constraints:

- action dispatch is table/index based;
- outcome dispatch masks the outcome value to seven bits before indexing.

## Battle result branches

The German original distinguishes:

- link win/loss;
- Battle Tower / e-Reader trainer result;
- normal trainer victory;
- wild-battle post-processing;
- local defeat;
- normal escape;
- Smoke Ball escape;
- ability-based escape;
- wild Pokemon fleeing.

Trainer victory music is selected by trainer class. Elite Four/Champion, Team Aqua/Magma groups, Gym Leader and normal trainers use separate music branches.

## Final battle transition

HandleEndTurn_FinishBattle records battle-result Pokemon data for eligible non-link/non-special battles, then:

1. starts fast palette fade;
2. fades map music;
3. redirects the battle-main function to post-battle cleanup;
4. uses BattleMainCB2 as the evolution-scene return callback.

If final battle scripting is still running, it continues dispatching battle script commands instead.

## Evolution processing

TryEvolvePokemon scans **six party positions** using gLeveledUpInBattle as a bit field.

For each set party bit it:

- clears that party bit;
- asks for a level-up evolution target;
- enters EvolutionScene when a target exists;
- waits for the evolution scene to return;
- continues until no pending party bits remain.

This is another direct six-party assumption that must remain visible during expansion.

## Return to overworld

ReturnFromBattleToOverworld performs:

- Pokerus acquisition/spread for non-link battles;
- link-player disconnect wait;
- battle outcome export through gSpecialVar_Result;
- restoration of the pre-battle callback;
- roaming Pokemon HP/status persistence and deactivation on defeat/capture;
- battle BGM stop;
- restoration of gMain.savedCallback.

## Script dispatch

The two final functions re-enter the battle-script interpreter:

- one optionally pops the battle-main callback stack;
- one directly executes the current script opcode once all controller work is idle.

These functions form the bridge between battle_main action control and the battle scripting command table.
