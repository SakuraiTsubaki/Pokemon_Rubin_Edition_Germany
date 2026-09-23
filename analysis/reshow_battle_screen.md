# German reshow_battle_screen module

The complete `reshow_battle_screen` text module has been bounded directly in the supplied German Retail Rev 0, Retail Rev 1 and Debug ROMs.

## Module boundary

| Profile | Start | End exclusive | Size | SHA-256 |
| --- | --- | --- | ---: | --- |
| Retail Rev 0 / Rev 1 | 0x0807B114 | 0x0807BA5C | **2,376 bytes (0x948)** | `4fc253119d97ce63c123ffcde3b7a20fc687881ae4d6f6b75efa671765ec6507` |
| Debug | 0x08082388 | 0x08082CD0 | **2,376 bytes (0x948)** | `5478096f86521a4cda821e393ce4ba5ec2bd519de9f6cd6a7e56e2dc4a42aba0` |

Retail Rev 0 and Rev 1 are byte-identical across the complete module. Debug adds no `reshow_battle_screen` text, so the accumulated Retail-to-Debug displacement remains **+0x7274**.

## Entry anchor

The module begins with `ReshowBattleScreenDummy`:

`70 47 00 00`

Immediately after it, `ReshowBattleScreenAfterMenu` begins with the common prefix:

`00 B5 0D 4A 10 7A 80 21 08 43 10 72 00 20`

The setup disables palette-buffer transfer, clears HBlank/VBlank callbacks, clears MOSAIC, resets the reshow/helper state and installs the reshow callback.

## Battle-screen reconstruction

The central state machine reconstructs the battle scene after returning from a menu. Its source-correlated flow includes:

- scanline-effect reset;
- battle text-window restoration;
- palette fade reset;
- clearing VRAM;
- incremental battle-element loading;
- sprite-data reset;
- sprite-palette reset and reserved palette count restoration;
- battle graphics setup;
- battler sprite reload for up to four battlers;
- battler OAM/state reconstruction;
- healthbox reconstruction;
- opponent sprite/species refresh;
- battle-selection cursor restoration;
- HBlank/VBlank callback restoration;
- hardware palette fade back into the active battle screen.

The code handles ordinary, Safari and Wally-tutorial battle paths separately where their back sprites/healthboxes differ.

## Battler sprite reload

`LoadAppropiateBankSprite` restores a battler's graphics according to side and battle type:

- opponent Pokémon or substitute;
- player Pokémon or substitute;
- Safari player back sprite;
- Wally tutorial back sprite.

The subsequent battler-sprite reconstruction restores palette number, callback, battler ID, species/form animation and invisibility state.

## Healthbox reload

The final helper rebuilds the appropriate normal/Safari healthbox, updates healthbox attributes from the correct party Pokémon, applies double-battle layout adjustment and hides zero-HP battlers.

## Source-correlated function inventory

The module contains seven semantic functions when the public `ReshowBattleScreenAfterMenu` wrapper is included:

1. `ReshowBattleScreenDummy`
2. `ReshowBattleScreenAfterMenu`
3. `CB2_ReshowBattleScreenAfterMenu`
4. `sub_807B06C`
5. `LoadAppropiateBankSprite`
6. `sub_807B184`
7. `sub_807B508`

There is no Debug-only text.

## Next-module anchor

`battle_anim_status_effects` begins immediately afterward:

- Retail Rev 0 / Rev 1: **0x0807BA5C**
- Debug: **0x08082CD0**
- accumulated delta: **+0x7274**

The first function is source-correlated as `unref_sub_807B69C`. The first 30 bytes are identical across profiles before the relocated branch:

`F0 B5 47 46 80 B4 04 1C 0D 1C 24 06 24 0E 2D 06 2D 0E 24 48 20 18 06 78 23 48 0A 21 FF F7`

It reads the battler sprite ID, creates a priority-10 task and then loads the status-animation sprite graphics/palette, independently anchoring the module transition.
