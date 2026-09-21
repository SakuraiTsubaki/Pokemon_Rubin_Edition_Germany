# German battle_util end-turn and move-cancellation core

This slice continues battle_util from DoFieldEndTurnEffects through CastformDataTypeChange.

## Exact slice

| Profile | Start | End exclusive | Size | SHA-256 |
| --- | --- | --- | ---: | --- |
| Retail Rev 0 / Rev 1 | 0x08015FD0 | 0x080184F8 | 9,512 bytes | f60d0efa94a631b184c9fe1b08ecd9a71752f648499ccb892a0efa7b7abc82fa |
| Debug | 0x08019058 | 0x0801B580 | 9,512 bytes | 5f92f831ecff7a256b50e990ba2f6e78dbcbd89a7d7b9700de8ed45c0b80da45 |

Retail Rev 0 and Rev 1 are byte-identical throughout the complete slice. Every Debug entry remains exactly +0x3088 from Retail.

## Function map

| Function | Retail | Debug | Bytes | Role |
| --- | --- | --- | ---: | --- |
| DoFieldEndTurnEffects | 0x08015FD0 | 0x08019058 | 1884 | field/side end-turn state machine for screens, Mist, Safeguard, Wish and weather |
| TurnBasedEffects | 0x0801672C | 0x080197B4 | 2948 | per-battler end-turn state machine for abilities, items, Leech Seed, poison, burn, Curse, Wrap and related effects |
| HandleWishPerishSongOnTurnEnd | 0x080172B0 | 0x0801A338 | 712 | Future Sight/Doom Desire and Perish Song end-turn processing |
| HandleFaintedMonActions | 0x08017578 | 0x0801A600 | 804 | experience, faint scripts, absence flags, abilities/items after fainting |
| TryClearRageStatuses | 0x0801789C | 0x0801A924 | 80 | clear Rage when a battler no longer selected Rage |
| AtkCanceller_UnableToUseMove | 0x080178EC | 0x0801A974 | 2304 | 14-stage pre-move inability/cancellation state machine |
| sub_8018018 | 0x080181EC | 0x0801B274 | 416 | party/battler availability helper used by fainted-mon processing |
| CastformDataTypeChange | 0x0801838C | 0x0801B414 | 364 | Forecast weather-driven Castform type/form selection |

## Field end-turn state machine

DoFieldEndTurnEffects is a staged state machine over the original field/side effects. Its tracked cases include:

- Reflect
- Light Screen
- Mist
- Safeguard
- Wish
- Rain
- Sandstorm
- Sun
- Hail

It first establishes battler turn order, then advances side/field counters and invokes the corresponding battle scripts as timers expire or weather continues.

The original implementation explicitly iterates exactly two battle sides for side timers. Later-generation screen/weather/terrain mechanics should therefore be added through a generalized field-effect layer rather than by extending this switch indefinitely.

## Per-battler end-turn state machine

TurnBasedEffects walks battlers in speed order and applies staged effects including:

- Ingrain healing
- end-turn abilities
- held-item effects
- Leech Seed
- poison and toxic poison
- burn
- Nightmare
- Curse
- Wrap/binding damage and expiration
- Disable/Encore and related timers

The function pauses whenever a script-producing effect occurs and resumes from its tracker, making tracker ordering part of Generation III compatibility behavior.

## Future Sight / Perish Song

HandleWishPerishSongOnTurnEnd keeps a separate state and battler cursor. Future Sight / Doom Desire uses per-battler counters, attacker IDs and stored damage; Perish Song uses per-battler timer fields and either decrements the displayed timer or applies lethal damage at zero.

## Fainted battler processing

HandleFaintedMonActions is an eight-state machine (states 0..7) that:

- clears stale absence flags where a replacement is available;
- grants experience;
- refreshes sent-party tracking;
- invokes fainted-Pokemon scripts;
- runs post-faint ability/item effects.

Its loops are bounded by gBattlersCount, but the surrounding arrays and bit tables remain the original four-active-battler model.

## Move cancellation

AtkCanceller_UnableToUseMove is the original 14-stage pre-move gate. It checks, among other states:

- sleep / Uproar wake-up / Early Bird
- freeze and thaw-on-hit interactions
- Truant
- recharge
- flinch
- Disable
- Taunt
- Imprison
- confusion
- paralysis
- infatuation
- Bide and other multi-turn state

Each stage may assign a battle script, set hit-marker/protect flags, or cancel the move. This function is one of the key modernization hooks for later-generation status, ability and move-prevention rules.

## Castform / Forecast

CastformDataTypeChange directly implements Forecast against the original weather bit model:

- no effective weather -> Normal
- Sun -> Fire
- Rain -> Water
- temporary Hail -> Ice

It mutates both battle type fields and returns a form-change code. Later-generation weather/form mechanics should not be bolted onto this Castform-specific switch; the German baseline should preserve this behavior while a generalized form-change layer is added separately.

## Next function

The next function starts at Retail **0x080184F8** / Debug **0x0801B580** and is AbilityBattleEffects.
