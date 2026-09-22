# German daycare / breeding module

The complete `daycare` module has been bounded directly in the supplied German ROMs.

## Module boundary

| Profile | Start | End exclusive | Size | SHA-256 |
| --- | --- | --- | ---: | --- |
| Retail Rev 0 / Rev 1 | 0x080415D4 | 0x08042BC8 | 5,620 bytes (0x15F4) | a10fe130a88cfa83f233a05e999082bcb943f7ed182b7dbdbf1535b4c55cc194 |
| Debug | 0x08045750 | 0x08046D44 | 5,620 bytes (0x15F4) | 9167ba6edee571b923b36ee2048ec086090c21b64d2e326fd9240ebd44e0ef65 |

Retail Rev 0 and Rev 1 are byte-identical. There is no conditional Debug insertion in this module; the full text keeps the inherited displacement **+0x417C**.

The function named `Debug_AddDaycareSteps` exists in the normal code path as well; it is not evidence of a Debug-ROM-only insertion.

## Function inventory

- 1. CountPokemonInDaycare
- 2. InitDaycareMailRecordMixing
- 3. Daycare_FindEmptySpot
- 4. StorePokemonInDaycare
- 5. StoreSelectedPokemonInDaycare
- 6. ShiftDaycareSlots
- 7. ApplyDaycareExperience
- 8. TakeSelectedPokemonFromDaycare
- 9. TakePokemonFromDaycare
- 10. GetLevelAfterDaycareSteps
- 11. GetNumLevelsGainedFromSteps
- 12. GetNumLevelsGainedForDaycareSlot
- 13. GetDaycareCostForSelectedMon
- 14. GetDaycareCost
- 15. Debug_AddDaycareSteps
- 16. GetNumLevelsGainedFromDaycare
- 17. ClearDaycareMail
- 18. unref_sub_8041824
- 19. GetEggSpecies
- 20. _TriggerPendingDaycareEgg
- 21. _TriggerPendingDaycareMaleEgg
- 22. TriggerPendingDaycareEgg
- 23. TriggerPendingDaycareMaleEgg
- 24. RemoveIVIndexFromList
- 25. InheritIVs
- 26. GetEggMoves
- 27. BuildEggMoveset
- 28. RemoveEggFromDayCare
- 29. RejectEggFromDayCare
- 30. AlterEggSpeciesWithIncenseItem
- 31. DetermineEggSpeciesAndParentSlots
- 32. _GiveEggFromDaycare
- 33. CreateEgg
- 34. SetInitialEggData
- 35. GiveEggFromDaycare
- 36. _ShouldEggHatch
- 37. ShouldEggHatch
- 38. IsEggPending
- 39. _GetDaycareMonNicknames
- 40. GetSelectedDaycareMonNickname
- 41. GetDaycareMonNicknames
- 42. GetDaycareState
- 43. EggGroupsOverlap
- 44. GetDaycareCompatibilityScore
- 45. GetDaycareCompatibilityScoreFromSave
- 46. SetDaycareCompatibilityString
- 47. NameHasGenderSymbol
- 48. AppendGenderSymbol
- 49. AppendMonGenderSymbol
- 50. GetDaycareLevelMenuText
- 51. GetDaycareLevelMenuLevelText
- 52. HandleDaycareLevelMenuInput
- 53. ShowDaycareLevelMenu
- 54. ChooseSendDaycareMon

## Daycare storage and experience

The daycare has exactly **two deposited Pokémon slots**.

Depositing a Pokémon copies its BoxPokemon record, restores PP, resets that slot's step counter and removes the party record. Mail is preserved in a separate daycare-mail structure.

Each occupied daycare slot accumulates one step count. On withdrawal, accumulated steps are added directly to EXP. The engine repeatedly applies level increases up to the normal level cap and automatically processes level-up moves.

If a Pokémon already knows four moves while learning a daycare level-up move, the original routine removes the first move and appends the new one. This is another direct four-move compatibility rule.

Withdrawal cost is:

`100 + 100 * levelsGained`

## Compatibility score

The original breeding compatibility score is one of **0, 20, 50 or 70**.

Rules:

- Undiscovered Egg Group -> 0;
- Ditto + Ditto -> 0;
- Ditto + other, same OT -> 20;
- Ditto + other, different OT -> 50;
- same gender or either genderless without Ditto -> 0;
- no Egg Group overlap -> 0;
- same species + same OT -> 50;
- same species + different OT -> 70;
- different compatible species + different OT -> 50;
- different compatible species + same OT -> 20.

Every 256-step compatibility opportunity (the code checks slot-1 steps modulo 256 == 255), if no egg is already pending, the score is compared against a 16-bit RNG scaled to 0..100.

The pending egg personality low half is then set to a nonzero random value from **1..65534**.

## Parent slots and Ditto

The two parent slots are assigned as conceptual mother/father inputs.

- a female non-Ditto becomes the mother slot;
- when one parent is Ditto, the other normally provides the egg species;
- if the non-Ditto partner is not female, Ditto is swapped into the internal “mother” slot after species determination so move inheritance uses the expected parent roles.

Nidoran F/M and Illumise/Volbeat use bit **0x8000** of the pending egg personality to select the paired species.

## Base egg species

`GetEggSpecies` walks backward through the evolution graph up to **five passes**. Each species is searched through the already identified **five evolution entries per species**.

This couples breeding ancestry to the same five-entry evolution schema and is a major expansion limit.

## Incense species exceptions

Generation III has two incense baby exceptions in this module:

- Wynaut requires Lax Incense; otherwise the egg species becomes Wobbuffet;
- Azurill requires Sea Incense; otherwise the egg species becomes Marill.

Either parent holding the required incense is sufficient in this implementation.

## IV inheritance

Exactly **three distinct IV stats** are inherited.

The routine:

1. builds the six-stat IV index list;
2. selects three different stat indexes without replacement;
3. independently chooses parent 0 or parent 1 for each selected stat;
4. copies that parent's 5-bit IV for the selected stat.

There is no Destiny Knot/Power Item-style modern inheritance logic here.

## Egg move inheritance

The breeding move builder works around the original four-move Pokémon structure.

It reads four moves from each parent and then adds, in this order:

1. father's Egg Moves recognized for the baby species;
2. father's TM/HM moves that the baby can learn;
3. moves known by **both parents** that also occur in the baby's level-up learnset.

The Egg Move lookup reads at most **10 Egg Moves** for the species. Parent buffers are four moves each. If adding a move overflows the baby's four slots, the oldest move is deleted and the new move appended.

This is strongly Generation III-specific: later games changed which parent may pass moves, TM inheritance, Egg Move transfer, and move-slot handling.

## Egg construction

The daycare-created egg:

- uses the determined base species after incense rules;
- combines the stored pending-personality low half with a fresh RNG high half;
- is created at the fixed egg-hatch level;
- inherits three IVs;
- receives the breeding moveset;
- is marked as an Egg;
- is placed into party slot 5 before party compaction.

The original constructor stores a Poké Ball, zero met level, the species egg-cycle value in the friendship field, and the internal Japanese Egg nickname/language marker used by the Gen III data format.

## Hatch-cycle stepping

`_ShouldEggHatch` increments the daycare parent step counters on each call.

The egg-cycle step byte is incremented and checked against **255**. At each cycle boundary, each party Egg's friendship/egg-cycle byte is decremented. If an Egg is already at zero, its party index is returned as the hatch candidate.

Party traversal is bounded by the current player-party count, with the global party topology still capped at six.

## Modernization direction

For a Gen-10-ready system, this module should become a legacy breeding ruleset behind a generalized breeding engine. Hard constraints to isolate include:

- two daycare parents;
- 0/20/50/70 compatibility scoring;
- three inherited IVs;
- four moves per parent/egg;
- father-centric Egg Move and TM/HM inheritance;
- ten Egg Moves scanned per species;
- five evolution records per species;
- two incense-baby exceptions;
- 256-step egg-generation checks;
- byte-sized egg-cycle counter.

## Next module

`egg_hatch` starts with `CreatedHatchedMon` at:

- Retail **0x08042BC8**
- Debug **0x08046D44**
- delta **+0x417C**

The boundary is directly visible from the large Thumb prologue at 0x08042BC8 and the first hatch conversion flow's calls into `GetMonData` and `CreateMon`.
