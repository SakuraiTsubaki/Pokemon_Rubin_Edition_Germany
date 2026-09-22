# German pokemon_3 metadata, evolution and infection core

The complete `pokemon_3` module has been mapped from the supplied German Retail, Rev 1 and Debug ROMs.

## Module boundary

| Profile | Start | End exclusive | Size | SHA-256 |
| --- | --- | --- | ---: | --- |
| Retail Rev 0 / Rev 1 | 0x0803F340 | 0x08040FE0 | 7,328 bytes (0x1CA0) | 41fa92dc097da2054ed5a8131e5a2694298634c2f82d6654b4b6b067b264dd48 |
| Debug | 0x080434BC | 0x0804515C | 7,328 bytes (0x1CA0) | 308529d87cffab0792d3e5db98c6eb6c39a82734829c34038f7182607fd6e18f |

Retail Rev 0 and Rev 1 are byte-identical throughout the module. There is **no Debug-only growth**; the inherited displacement remains **+0x417C** from start to end.

## Function inventory

- 1. HealStatusConditions
- 2. GetItemEffectParamOffset
- 3. sub_803F324
- 4. sub_803F378
- 5. GetNature
- 6. GetNatureFromPersonality
- 7. GetEvolutionTargetSpecies
- 8. HoennPokedexNumToSpecies
- 9. NationalPokedexNumToSpecies
- 10. NationalToHoennOrder
- 11. SpeciesToNationalPokedexNum
- 12. SpeciesToHoennPokedexNum
- 13. HoennToNationalOrder
- 14. SpeciesToCryId
- 15. unref_sub_803F938
- 16. DrawSpindaSpots
- 17. EvolutionRenameMon
- 18. sub_803FBBC
- 19. sub_803FBFC
- 20. sub_803FC34
- 21. sub_803FC58
- 22. nature_stat_mod
- 23. AdjustFriendship
- 24. MonGainEVs
- 25. GetMonEVCount
- 26. RandomlyGivePartyPokerus
- 27. CheckPartyPokerus
- 28. CheckPartyHasHadPokerus
- 29. UpdatePartyPokerusTime
- 30. PartySpreadPokerus
- 31. TryIncrementMonLevel
- 32. CanMonLearnTMHM
- 33. GetMoveTutorMoves
- 34. GetLevelUpMovesBySpecies
- 35. sub_8040574
- 36. SpeciesToPokedexNum
- 37. ClearBattleMonForms
- 38. GetMUS_ForBattle
- 39. sub_80408BC
- 40. current_map_music_set__default_for_battle
- 41. IsPokeSpriteNotFlipped
- 42. sub_8040A54
- 43. GetPokeFlavourRelation
- 44. IsTradedMon
- 45. IsOtherTrainer
- 46. MonRestorePP
- 47. BoxMonRestorePP
- 48. SetMonPreventsSwitchingString
- 49. SetWildMonHeldItem
- 50. IsShiny
- 51. IsShinyOtIdPersonality

## Nature model

`GetNature` and `GetNatureFromPersonality` define nature as:

`nature = personality % 25`

The stat-modifier path operates on the original five non-HP stats. This 25-nature / five-modified-stat model should remain a legacy rule interface rather than be inferred from localized strings.

## Evolution table

`GetEvolutionTargetSpecies` scans exactly **five evolution entries per species**.

Supported original branches include:

- friendship >= 220;
- friendship day: local hours 12..23;
- friendship night: local hours 0..11;
- level;
- Attack > Defense / = / <;
- Silcoon/Cascoon personality split;
- Ninjask level evolution;
- Beauty;
- trade;
- trade with held item;
- evolution item.

An Everstone-style `HOLD_EFFECT_PREVENT_EVOLVE` blocks ordinary evolution checks except the special item-check type that explicitly bypasses it.

This five-entry table is a hard schema limit for later-generation species with more evolution/form conditions.

## Pokédex mapping

The module owns conversions among species IDs, Hoenn Pokédex numbers and National Pokédex numbers, plus cry-ID mapping. These are separate namespaces in the original engine and should stay separate in an expanded registry.

## Spinda

`DrawSpindaSpots` derives the four facial/body spot offsets from personality bits. Personality is therefore visual-form provenance as well as nature/gender/shiny/evolution input in this generation.

## Friendship

`AdjustFriendship` divides friendship into three bands:

- 0..99;
- 100..199;
- 200..255.

Positive deltas receive the original Soothe Bell 1.5× modifier, plus +1 for Luxury Ball and +1 when the met location matches the current map. Result is clamped to 0..255.

## EV gain

`MonGainEVs` uses six EV stats and enforces:

- total EV cap: **510**;
- per-stat byte cap: **255**;
- Pokérus multiplier: ×2;
- Macho Brace multiplier: ×2;
- both multipliers can stack.

`GetMonEVCount` simply sums the six stored EV bytes.

## Pokérus

Random infection occurs only when the 16-bit RNG equals one of exactly three values:

- 0x4000;
- 0x8000;
- 0xC000.

That is **3 / 65,536** trigger values before party-slot selection and eligibility checks.

Party operations use exactly **six slots**. The low Pokérus nibble is the remaining contagious-day counter; elapsed days clear that low nibble while preserving the high-nibble 'has had Pokérus' history.

## TM/HM and level-up move schema

`CanMonLearnTMHM` treats TM/HM learnability as **two 32-bit words = 64 addressable bits per species**.

`GetLevelUpMovesBySpecies` enumerates at most **20 packed learnset entries** and masks each move ID with the already identified legacy **0x1FF (9-bit)** move-ID field.

These two constraints are independent expansion limits: modern move IDs and a larger move-teaching catalog need a new species-learnset representation.

## Wild held items

For non-trainer, non-legendary wild encounters where item1 != item2:

- RNG 0..44: no item (45%);
- 45..94: item1 (50%);
- 95..99: item2 (5%).

If item1 == item2, that item is always assigned.

## Shiny calculation

`IsShinyOtIdPersonality` uses the original Generation III XOR rule:

`TID_hi ^ TID_lo ^ PID_hi ^ PID_lo < 8`

giving the classic 8-in-65536 shiny threshold for a fixed OT/personality pair.

## Compatibility direction

`pokemon_3` is a strong schema boundary for modern expansion. Legacy mode should retain:

- 25 natures;
- five evolution records per species;
- 6-stat EV storage;
- 64-bit TM/HM learnability bitmap;
- 20-entry exported level-up list;
- personality-derived Spinda/shiny/nature behavior;
- six-slot Pokérus party loops.

A modern species/evolution/learnset registry should translate into these structures only when executing legacy Ruby logic.

## Next module

The German-only `de_rom_8040FE0` module starts exactly at its address-bearing symbol:

- Retail **0x08040FE0** (`de_sub_8040FE0`)
- Debug **0x0804515C**
- delta **+0x417C**.

The first eight bytes are byte-identical between the two profiles, confirming that `pokemon_3` ends immediately before this German localization helper module.
