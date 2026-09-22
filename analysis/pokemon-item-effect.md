# German pokemon item-effect interpreter

The complete `pokemon_item_effect` module is mapped from the supplied German Retail, Rev 1 and Debug ROMs.

## Module boundary

| Profile | Start | End exclusive | Size | SHA-256 |
| --- | --- | --- | ---: | --- |
| Retail Rev 0 / Rev 1 | 0x0803E360 | 0x0803F340 | 4,064 bytes (0xFE0) | 7ef952661f4ac95889a0eb8556f80aa32ddbad0289150c594dda1176122c6f05 |
| Debug | 0x080424DC | 0x080434BC | 4,064 bytes (0xFE0) | 2e716b737731d48369942d58094840b418a1bee6c78e13954e371622556eb009 |

Retail Rev 0 and Rev 1 are byte-identical. There is no Debug-only growth; the full module remains at **+0x417C**.

## Functions

- `ExecuteTableBasedItemEffect_`: Retail 0x0803E360 / Debug 0x080424DC, 36 bytes. Thin wrapper that normalizes arguments and enters the interpreter.
- `PokemonUseItemEffects`: Retail 0x0803E384 / Debug 0x08042500, 4,028 bytes. Main item-effect interpreter.

## Effect-table format

Normal items resolve their effect record through `gItemEffectTable[itemId - 13]`. Enigma Berry bypasses that table and uses its custom effect bytes from battle/save data.

Each effect begins with **six command bytes** followed by variable parameters:

### Effect byte 0

- low nibble: X Attack stage amount;
- Dire Hit / Focus Energy-style effect;
- Sacred Ash;
- infatuation cure.

### Effect byte 1

- X Speed;
- X Defend.

### Effect byte 2

- X Special Attack;
- X Accuracy.

### Effect byte 3

- confusion;
- paralysis;
- freeze;
- burn;
- poison/toxic;
- sleep;
- level up;
- Guard Spec / five-turn Mist.

### Effect byte 4

- HP EV;
- Attack EV;
- HP healing;
- PP healing;
- single-move PP healing;
- PP Up;
- Revive;
- evolution-stone behavior.

### Effect byte 5

- Defense EV;
- Speed EV;
- Special Defense EV;
- Special Attack EV;
- PP Max;
- low/mid/high friendship modifiers.

Parameters begin at byte 6 and are consumed conditionally according to the active bits.

## Battle stat items

X-item style effects write directly into the existing eight-stage battle stat model and clamp stages to **12**, with neutral still 6.

Dire Hit sets the original Focus Energy status, and Guard Spec starts the original Mist side timer at **5 turns**.

## Status cures

Primary status cures delegate to `HealStatusConditions` in the next module. Sleep healing also clears Nightmare when used on an active battler.

Infatuation is cleared from status2 directly in this interpreter.

## Level-up item behavior

The level-up effect refuses use at level **100**. Otherwise it sets EXP directly to the species growth-table threshold for the next level and recalculates stats.

This is the original Rare Candy behavior, not a generic 'add one level' abstraction.

## EV items

The interpreter uses six original EV fields and enforces:

- total EV cap: **510**;
- vitamin-style per-stat cap: **100**;
- item parameters may add or subtract EVs;
- stats are recalculated after a successful EV change.

These caps are embedded in item execution, not only in Pokémon creation.

## HP healing / Revive

HP recovery supports parameter sentinels for:

- full HP;
- half max HP;
- level-up HP delta;
- ordinary explicit HP amounts.

Revive effects require zero HP, restore the battler into active battle state when applicable, update absent-battler flags, rematerialize BattlePokemon data and increment battle-result revive statistics.

## PP healing and PP Ups

The interpreter operates on exactly **four move slots**.

PP restoration supports all-move and one-move paths. PP Up/PP Max behavior uses the already mapped four packed two-bit PP-Up fields and recalculates current PP relative to the new maximum.

## Evolution stones

The evolution-stone bit calls `GetEvolutionTargetSpecies` using item evolution mode and the current item ID. On success it can enter the evolution scene directly.

This tightly couples item IDs, effect-table records and the legacy evolution-method table.

## Friendship

Three separate friendship bands are encoded:

- low: <100;
- middle: 100..199;
- high: >=200.

Positive friendship changes receive the original Soothe Bell 1.5× modifier and can gain +1 bonuses for matching Poké Ball/met-location conditions. Final friendship is clamped to 0..255.

## Expansion pressure points

For a Gen-10-ready item system, the six-byte bitfield interpreter should be treated as a legacy codec rather than extended indefinitely. Major constraints are:

- fixed six command bytes;
- conditional parameter stream with positional coupling;
- four-move PP logic;
- six-stat EV model;
- level cap 100;
- byte-sized friendship;
- hard-coded battle-stage/status effects;
- item-ID-offset table lookup (`itemId - 13`).

A modern item-effect registry can translate legacy six-byte records into structured effects while preserving exact Ruby behavior.

## Next module

`pokemon_3` starts with `HealStatusConditions` at:

- Retail **0x0803F340**
- Debug **0x080434BC**
- delta **+0x417C**.

The exact module boundary is visible at the `PokemonUseItemEffects` epilogue ending at 0x0803F33F, followed immediately by the `HealStatusConditions` Thumb prologue.
