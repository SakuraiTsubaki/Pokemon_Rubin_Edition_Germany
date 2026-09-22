# German pokemon_2 data access and storage core

The complete `pokemon_2` module has been mapped from the supplied German Retail, Rev 1 and Debug ROMs.

## Module boundary

| Profile | Start | End exclusive | Size | SHA-256 |
| --- | --- | --- | ---: | --- |
| Retail Rev 0 / Rev 1 | 0x0803C51C | 0x0803E360 | 7,748 bytes (0x1E44) | e7169aa097ab66e4027ca0ce3dc479548bcb4368acabb18ef6cad6453da636b8 |
| Debug | 0x08040698 | 0x080424DC | 7,748 bytes (0x1E44) | b9d4617ba309a7f5fc712553dea16be17def6632998b8bdf3d7e3e00c6a35879 |

Retail Rev 0 and Rev 1 are byte-identical across the complete module. There is **no Debug-only growth**; every mapped entry remains at **+0x417C**.

## Function map

| Function | Retail | Debug | Bytes | Role |
| --- | --- | --- | ---: | --- |
| CountAliveMons | 0x0803C51C | 0x08040698 | 236 | count living battlers for requested side/allied context |
| sub_803C434 | 0x0803C608 | 0x08040784 | 132 | choose opposing battler position with double-battle handling |
| GetMonGender | 0x0803C68C | 0x08040808 | 16 | party-mon wrapper for boxed gender calculation |
| GetBoxMonGender | 0x0803C69C | 0x08040818 | 92 | derive gender from species ratio and personality low byte |
| GetGenderFromSpeciesAndPersonality | 0x0803C6F8 | 0x08040874 | 72 | species/personality gender helper |
| SetMultiuseSpriteTemplateToPokemon | 0x0803C740 | 0x080408BC | 52 | prepare shared sprite template for Pokémon front/back graphics |
| SetMultiuseSpriteTemplateToTrainerBack | 0x0803C774 | 0x080408F0 | 80 | prepare shared trainer sprite template |
| EncryptBoxMon | 0x0803C7C4 | 0x08040940 | 36 | XOR 12 secure words with personality and OT ID |
| DecryptBoxMon | 0x0803C7E8 | 0x08040964 | 36 | reverse secure-payload XOR |
| GetSubstruct | 0x0803C80C | 0x08040988 | 1320 | map personality modulo 24 to one of four 12-byte secure substructs |
| GetMonData | 0x0803CD34 | 0x08040EB0 | 156 | read party-only fields or delegate boxed fields |
| GetBoxMonData | 0x0803CDD0 | 0x08040F4C | 1536 | decrypt/checksum/read boxed and secure data fields |
| SetMonData | 0x0803D3D0 | 0x0804154C | 240 | write party-only fields or delegate boxed fields |
| SetBoxMonData | 0x0803D4C0 | 0x0804163C | 1572 | decrypt/checksum/write boxed data then recalc checksum/re-encrypt |
| CopyMon | 0x0803DAE4 | 0x08041C60 | 12 | raw record copy wrapper |
| GiveMonToPlayer | 0x0803DAF0 | 0x08041C6C | 124 | fill first free party slot or send Pokémon to PC |
| SendMonToPC | 0x0803DB6C | 0x08041CE8 | 128 | scan 14 boxes × 30 slots for first free box slot |
| CalculatePlayerPartyCount | 0x0803DBEC | 0x08041D68 | 68 | count occupied player party slots |
| CalculateEnemyPartyCount | 0x0803DC30 | 0x08041DAC | 68 | count occupied enemy party slots |
| GetMonsStateToDoubles | 0x0803DC74 | 0x08041DF0 | 116 | summarize usable party state for double-battle decisions |
| GetAbilityBySpecies | 0x0803DCE8 | 0x08041E64 | 68 | select ability1/ability2 from species and altAbility bit |
| GetMonAbility | 0x0803DD2C | 0x08041EA8 | 52 | read species/altAbility and resolve ability |
| CreateSecretBaseEnemyParty | 0x0803DD60 | 0x08041EDC | 284 | build Secret Base enemy party from save decoration/trainer data |
| GetSecretBaseTrainerPicIndex | 0x0803DE7C | 0x08041FF8 | 60 | derive Secret Base trainer picture |
| GetSecretBaseTrainerNameIndex | 0x0803DEB8 | 0x08042034 | 60 | derive Secret Base trainer name class/index |
| PlayerPartyAndPokemonStorageFull | 0x0803DEF4 | 0x08042070 | 52 | test six party slots then PC capacity |
| PokemonStorageFull | 0x0803DF28 | 0x080420A4 | 76 | scan 14 boxes × 30 slots for any free slot |
| GetSpeciesName | 0x0803DF74 | 0x080420F0 | 76 | copy species name or species-0 fallback |
| CalculatePPWithBonus | 0x0803DFC0 | 0x0804213C | 72 | apply one of four packed PP Up counts to base PP |
| RemoveMonPPBonus | 0x0803E008 | 0x08042184 | 60 | clear selected two-bit PP Up field on boxed/party Pokémon |
| RemoveBattleMonPPBonus | 0x0803E044 | 0x080421C0 | 24 | clear selected PP Up field on BattlePokemon |
| CopyPlayerPartyMonToBattleData | 0x0803E05C | 0x080421D8 | 772 | materialize persistent party Pokémon into active BattlePokemon |

## Encryption / secure substruct access

`EncryptBoxMon` and `DecryptBoxMon` operate on exactly **12 32-bit secure words (48 bytes)**. Each word is XORed with both personality and OT ID; encryption and decryption differ only in XOR order, which is algebraically reversible.

`GetSubstruct` selects one of **24 permutations** using `personality % 24`, then maps logical substruct type 0..3 onto the physical four-substruct array.

This personality-dependent permutation is a fundamental part of the Gen III boxed-record format.

## GetBoxMonData integrity behavior

For fields inside the secure payload, `GetBoxMonData`:

1. resolves all four logical substruct pointers;
2. decrypts the payload;
3. recalculates the 24-word checksum;
4. if the checksum mismatches, marks `isBadEgg`, `isEgg`, and secure `isEgg`;
5. reads the requested field;
6. re-encrypts before returning.

Bad Egg therefore emerges from integrity validation in the ordinary data accessor itself, not from a separate save-loader pass.

Nickname reads also localize the visible result through stored language metadata, while Eggs and Bad Eggs substitute dedicated names.

## SetBoxMonData integrity behavior

For secure fields, `SetBoxMonData` decrypts and verifies the existing checksum before mutation. A checksum mismatch sets Bad Egg/Egg flags, re-encrypts immediately and rejects the write.

After a valid secure-field write, it recalculates the checksum and re-encrypts the 48-byte payload.

This makes `Get/SetBoxMonData` the critical compatibility boundary for any extended Pokémon/save format.

## Original packed-IV bug

The original `MON_DATA_IVS` setter reads only `*data` into the packed IV word unless the separate `BUGFIX_SETMONIVS` compile-time option is used. Consequently, only HP IV and the low three bits of Attack IV survive through that aggregate setter in the original behavior.

Individual six-IV field setters do not have that bug. The German retail ROM preserves the original path and should keep it in legacy compatibility mode.

## Party and PC storage

`GiveMonToPlayer` scans exactly **six party slots**. If full, `SendMonToPC` scans:

- **14 boxes**;
- **30 slots per box**;
- beginning from currentBox and wrapping around.

`PokemonStorageFull` uses the same 14×30 storage geometry.

This is a hard save/storage-layout constraint and should be versioned rather than widened in-place.

## Gender / ability

Gender is derived from the species gender ratio and the low byte of personality, except fixed male/female/genderless ratios.

Ability selection is the original two-ability model: `altAbility` selects ability2 when available, otherwise ability1.

This one-bit ability selector is another major later-generation schema limitation.

## PP Up packing

`CalculatePPWithBonus` uses four two-bit PP Up fields packed into one byte. Each count contributes 20% of base PP per PP Up, with a maximum of three PP Ups per move.

`RemoveMonPPBonus` and `RemoveBattleMonPPBonus` clear one of those four two-bit fields.

## Persistent → battle materialization

`CopyPlayerPartyMonToBattleData` copies persistent Pokémon data into the active `BattlePokemon` record:

- species/item;
- exactly four moves and four PP values;
- friendship/experience;
- six IVs;
- personality/status/level/HP/stats;
- egg/alternate-ability/OT fields;
- species types and resolved ability;
- nickname and OT name.

It then resets all **eight stat stages to neutral 6**, clears status2, updates sent-party tracking and refreshes battle sprite/substitute state.

## Next module

`pokemon_item_effect` begins at:

- Retail **0x0803E360**
- Debug **0x080424DC**
- delta **+0x417C**.

The first function is the wrapper `ExecuteTableBasedItemEffect_`, which immediately calls the larger item-effect interpreter.
