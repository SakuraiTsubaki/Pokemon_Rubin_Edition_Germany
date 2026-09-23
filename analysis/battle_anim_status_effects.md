# German battle_anim_status_effects module

The complete `battle_anim_status_effects` text module has been bounded directly in the supplied German Retail Rev 0, Retail Rev 1 and Debug ROMs.

## Module boundary

| Profile | Start | End exclusive | Size | SHA-256 |
| --- | --- | --- | ---: | --- |
| Retail Rev 0 / Rev 1 | 0x0807BA5C | 0x0807C1C0 | **1,892 bytes (0x764)** | `96dff3d1c51f8c66be47915de60bee9d1b8aaba244d7ebbb8a0a2afa1b0d00d6` |
| Debug | 0x08082CD0 | 0x08083434 | **1,892 bytes (0x764)** | `6aa1736be3a4541ecd847d6368d3b806b5cdd085f37a64b87e6115396babe00b` |

Retail Rev 0 and Rev 1 are byte-identical across the complete module. Connected source contains no Debug-only text, matching the binary result: accumulated Retail-to-Debug displacement remains **+0x7274** at entry and exit.

## Entry anchor

The first function is source-correlated as `unref_sub_807B69C`.

Common first 30 bytes:

`F0 B5 47 46 80 B4 04 1C 0D 1C 24 06 24 0E 2D 06 2D 0E 24 48 20 18 06 78 23 48 0A 21 FF F7`

The function reads the battler sprite ID, creates a priority-10 task, loads status-animation sprite graphics and palette, initializes task state and creates a ring of status-effect sprites around the battler.

Historical `807B69C` naming is semantic/source correlation only and is not treated as the German ROM address.

## Status-effect runtime

The connected source contains **12 explicit functions**:

1. `unref_sub_807B69C`
2. `sub_807B7E0`
3. `sub_807B870`
4. `sub_807B8A4`
5. `sub_807B920`
6. `sub_807B9D8`
7. `sub_807BA24`
8. `sub_807BAD4`
9. `sub_807BB24`
10. `sub_807BB88`
11. `move_anim_start_t2`
12. `sub_807BDAC`

The module implements two major status-animation paths:

- orbiting/fading status sprites around a battler;
- large status-effect overlays and palette/alpha transitions.

It also translates status-condition selectors into battle-animation arguments, launches status-condition battle-animation scripts, and destroys the tracking task when the animation script becomes inactive.

## Last function anchor

The final function is source-correlated as `sub_807BDAC`.

| Profile | Start | End exclusive | Size | SHA-256 |
| --- | --- | --- | ---: | --- |
| Retail Rev 0 / Rev 1 | 0x0807C16C | 0x0807C1C0 | 0x54 | `e50efe904f1ab85cafe5ad0bbfb7729edb8421413cc1c14c728e7ab6bbd439ca` |
| Debug | 0x080833E0 | 0x08083434 | 0x54 | `3d4f5d4bf778b9ed40f8a92bc222c470540c86bb750ab200bf7ca54305854e4d` |

It invokes the battle-animation script callback and, when the script is no longer active, clears the battler healthbox status-animation flag and destroys the task.

## Next-module anchor

`title_screen` begins immediately afterward:

- Retail Rev 0 / Rev 1: **0x0807C1C0**
- Debug: **0x08083434**
- accumulated delta: **+0x7274**

The first function is source-correlated as `SpriteCallback_VersionBannerLeft`.

The first 48 bytes are identical in all three profiles:

`10 B5 02 1C 30 20 11 5E 88 00 40 18 C0 00 09 49 44 18 0A 21 60 5E 00 28 0E D0 51 78 0D 20 40 42 08 40 50 70 54 20 50 84 3E 32 11 78 59 38 08 40 10 70`

The next literal differs by profile because the German Debug build relocates `gTasks`; this is expected and independently confirms the boundary.
