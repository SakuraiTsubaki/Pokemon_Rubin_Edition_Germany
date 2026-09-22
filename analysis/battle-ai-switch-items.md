# German battle AI switch/item module

The complete `battle_ai_switch_items` module has been mapped from the supplied German ROMs.

## Module boundary

| Profile | Start | End exclusive | Size | SHA-256 |
| --- | --- | --- | ---: | --- |
| Retail Rev 0 / Rev 1 | 0x080361C0 | 0x080376E0 | 5,408 bytes | 5f902540b54982bc30c68a089895b0f92fc449c9e0b9cd2463262d98cb6f1e85 |
| Debug | 0x0803A084 | 0x0803B5B4 | 5,424 bytes | eaec578391d7bbd235f7eef81816b8c6d914fb979270cbae1221acd1e460b2de |

Retail Rev 0 and Rev 1 are byte-identical across the module.

Debug is only **16 bytes (0x10)** larger. All functions through `AI_TrySwitchOrUseItem` start at inherited delta +0x3EC4. The Debug-only branch inside that function adds 0x10, so all following functions and the next module use **+0x3ED4**.

## Function map

| Function | Retail | Debug | Retail bytes | Debug bytes | Role |
| --- | --- | --- | ---: | ---: | --- |
| ShouldSwitchIfPerishSong | 0x080361C0 | 0x0803A084 | 104 | 104 | switch immediately when Perish Song timer reaches zero |
| ShouldSwitchIfWonderGuard | 0x08036228 | 0x0803A0EC | 404 | 404 | look for a reserve mon with super-effective coverage against Wonder Guard |
| FindMonThatAbsorbsOpponentsMove | 0x080363BC | 0x0803A280 | 552 | 552 | find reserve mon with an ability that absorbs/nullifies opponent move type |
| ShouldSwitchIfNaturalCure | 0x080365E4 | 0x0803A4A8 | 260 | 260 | consider Natural Cure switching under status/HP conditions |
| HasSuperEffectiveMoveAgainstOpponents | 0x080366E8 | 0x0803A5AC | 328 | 328 | test active AI battler for super-effective coverage |
| AreStatsRaised | 0x08036830 | 0x0803A6F4 | 72 | 72 | test whether active battler has sufficiently raised stat stages |
| FindMonWithFlagsAndSuperEffective | 0x08036878 | 0x0803A73C | 608 | 608 | find reserve mon matching AI flags plus super-effective coverage |
| ShouldSwitch | 0x08036AD8 | 0x0803A99C | 520 | 520 | ordered high-level switch heuristic dispatcher |
| AI_TrySwitchOrUseItem | 0x08036CE0 | 0x0803ABA4 | 320 | 336 | choose switch, trainer item, or default move action |
| ModulateByTypeEffectiveness | 0x08036E20 | 0x0803ACF4 | 136 | 136 | apply type-chart multiplier to AI suitability score |
| GetMostSuitableMonToSwitchInto | 0x08036EA8 | 0x0803AD7C | 860 | 860 | pick reserve mon by defensive typing then estimated damage |
| GetAI_ItemType | 0x08037204 | 0x0803B0D8 | 92 | 92 | classify trainer item into AI item category |
| ShouldUseItem | 0x08037260 | 0x0803B134 | 1152 | 1152 | select and consume one of up to four trainer items |

## Debug-only behavior

`AI_TrySwitchOrUseItem` contains one Debug control check. When Debug control bit 0x20 is set, trainer-item use is skipped. This adds exactly **16 bytes** to the Debug function:

- Retail: 320 bytes
- Debug: 336 bytes
- delta before: +0x3EC4
- delta after: +0x3ED4.

## Switch heuristics

The original AI switch layer explicitly considers:

- Perish Song at zero timer;
- Wonder Guard and super-effective coverage;
- reserve Pokémon whose abilities absorb or nullify expected move types;
- Natural Cure;
- whether the active battler already has a super-effective move;
- whether the active battler has accumulated useful stat boosts;
- reserve Pokémon with super-effective coverage and requested AI flags.

`ShouldSwitch` combines these heuristics in a fixed ordering. This ordering is part of the Generation III AI behavior and should be preserved as a legacy ruleset rather than silently mixed with later-generation heuristics.

## Reserve-mon selection

`GetMostSuitableMonToSwitchInto` first scores valid reserve Pokémon by defensive typing against the opposing battler's two types. It then requires at least one super-effective move. If no satisfactory typing candidate exists, it falls back to estimating damage across the candidate's four move slots.

The function directly assumes:

- six party slots;
- four moves per Pokémon;
- maximum four active battlers;
- three-slot party halves in Multi Battle.

The damage-comparison accumulator is byte-sized in the original implementation, another legacy AI quirk worth isolating before modernizing evaluation.

## Item AI

`ShouldUseItem` scans up to **four trainer items**. Recognized categories include:

- Full Restore;
- HP healing;
- status curing;
- X-stat style boosts;
- Guard Specs.

It also scans all six enemy-party slots to determine viable party count. Enigma Berry is handled through SaveBlock1's custom item-effect bytes.

## Modernization direction

For later-generation AI, this module is a good compatibility boundary:

- keep the original ordered switch/item heuristics for Ruby mode;
- expose party/move/item candidates through generalized iterators instead of fixed 6/4/4 loops;
- replace byte-sized damage scoring with a wider evaluation score;
- add modern switch triggers, abilities, hazards and item categories as separate policies.

## Next module

`battle_controller_link_opponent` begins at:

- Retail **0x080376E0**
- Debug **0x0803B5B4**
- delta **+0x3ED4**

with `nullsub_47` followed by the link-opponent controller setup.
