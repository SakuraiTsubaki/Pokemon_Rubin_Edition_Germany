# German AbilityBattleEffects and Debug divergence

AbilityBattleEffects is the first battle_util routine after the previously mapped end-turn/cancellation slice to introduce a large Retail/Debug size divergence.

## Function boundaries

| Function | Retail | Retail bytes | Debug | Debug bytes |
| --- | --- | ---: | --- | ---: |
| AbilityBattleEffects | 0x080184F8 | 7,308 | 0x0801B580 | 8,536 |
| BattleScriptExecute | 0x0801A184 | 60 | 0x0801D6D8 | 60 |
| BattleScriptPushCursorAndCallback | 0x0801A1C0 | 64 | 0x0801D714 | 64 |
| next: ItemBattleEffects | 0x0801A200 | — | 0x0801D754 | — |

Retail Rev 0 and Rev 1 are byte-identical over the complete Retail slice 0x080184F8..0x0801A1FF.

## Debug growth

At AbilityBattleEffects entry, Debug is still at the previous accumulated displacement of +0x3088.

AbilityBattleEffects sizes:

- Retail: 0x1C8C bytes (7,308)
- Debug: 0x2158 bytes (8,536)
- Debug growth: **0x4CC bytes (1,228)**

After this function, BattleScriptExecute and BattleScriptPushCursorAndCallback return to equal function sizes in both profiles. The accumulated Debug displacement is therefore now **+0x3554** and ItemBattleEffects begins at that new delta.

The supplied German Debug binary is authoritative for this difference. The currently consulted comparison source does not by itself explain the extra 0x4CC bytes, so the additional Debug behavior remains explicitly unclassified until statement-level Debug decompilation ties those bytes to concrete branches/functions. It is not silently attributed to Retail logic.

## Retail AbilityBattleEffects role

The Retail routine is the central Generation III ability-event dispatcher. Its case-based API covers switch-in, end-turn, move interaction, side/field queries and ability counting/checking. The observed logic includes or routes behavior for abilities such as:

- Drizzle, Sand Stream and Drought
- Intimidate
- Forecast / Castform
- Trace
- Rain Dish
- Shed Skin
- Speed Boost
- Soundproof
- Flash Fire
- Color Change
- Rough Skin
- Cute Charm
- Synchronize

It also performs field queries such as whether an ability exists on the opposing side, same side, whole field, or field excluding a specific battler.

## Architecture significance

This is a major modernization pressure point. The original design funnels many unrelated ability trigger classes through one large switch keyed by an ability-effect case ID, while individual ability IDs are switched again inside those cases.

For later-generation expansion, the German compatibility implementation should preserve this dispatcher as the original behavior layer, while new ability behavior should migrate toward explicit trigger categories / hook tables rather than continually extending one monolithic switch.

Existing move IDs passed to this dispatcher are 16-bit. Battler identity and ability IDs are byte-sized in this original interface.

## Battle-script bridge

BattleScriptExecute and BattleScriptPushCursorAndCallback establish two ways to enter battle scripting:

- replace battle-main execution while pushing the prior callback;
- push the current script cursor and callback, then continue through the script runner.

These two bridge functions remain equal-sized across Retail and Debug even though their literal addresses differ.

## Hashes

- Retail AbilityBattleEffects SHA-256: bebef06996411234536f5acf13912386da5efa32b2c5e934d41b10106f0b577a
- Debug AbilityBattleEffects SHA-256: 6e414606a8371821ce31d9b66b4721ce57a25f1075587264c29864aff7703ab5
- Retail full slice SHA-256: 3c73b59edc8cb2e5b7171b3281a73392103ec16f2695810fd9bc5cbf3c3e3cd6
- Debug full slice SHA-256: 9b641ffb25303d74075c179bbdd64aa072f0d2771738425fc5b59c27c5a8b2eb

## Next function

ItemBattleEffects begins at Retail **0x0801A200** / Debug **0x0801D754**, with the new accumulated Debug delta **+0x3554**.
