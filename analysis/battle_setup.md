# German battle_setup module

The complete `battle_setup` text module has been bounded directly in the supplied German Retail Rev 0, Retail Rev 1 and Debug ROMs.

## Module boundary

| Profile | Start | End exclusive | Size | SHA-256 |
| --- | --- | --- | ---: | --- |
| Retail Rev 0 / Rev 1 | 0x08081D94 | 0x08083108 | **4,980 bytes (0x1374)** | `05518cd7d00fbd74e5ef75bafacac1f6a8702bb55c79afe703c2922d216a8a25` |
| Debug | 0x0808915C | 0x0808A4D0 | **4,980 bytes (0x1374)** | `999ea36e9a5e9c88dcab89898cb32d11b39a30a34c997fd41b51eccbb42de798` |

Retail Rev 0 and Rev 1 are byte-identical across the complete module. Connected source contains no Debug-only text in `battle_setup`, matching the binary result: accumulated Retail-to-Debug displacement remains **+0x73C8** at entry and exit.

## Entry anchor

The first function is source-correlated as `Task_BattleStart`.

Common first 32 bytes:

`30 B5 00 06 05 0E A8 00 40 19 C0 00 04 49 44 18 00 21 60 5E 00 28 05 D0 01 28 0E D0 1D E0 00 00`

The function indexes the 0x28-byte task record, reads the battle-start state, waits for the field poison effect to be inactive, launches the selected transition and, once it finishes, switches to the battle initializer and clears encounter/poison step state.

## Runtime scope

The connected source contains **71 explicit functions** and no `#if DEBUG` text.

The module covers:

- wild-battle startup;
- roamer battle startup;
- Safari battle startup;
- scripted legendary/special wild battles;
- Wally tutorial battle;
- trainer battle startup and transition selection;
- battle-end return callbacks;
- trainer-battle parameter loading/clearing;
- trainer defeated/fought flags;
- trainer intro/defeat/cannot-battle speech selection;
- trainer object-event lookup;
- trainer battle scripts and return addresses;
- wild/trainer transition selection by map type and levels;
- Trainer Eye rematch lookup and progression;
- badge-gated rematch step counting;
- random rematch activation;
- rematch ID selection and clearing.

Historical numeric names remain semantic/source correlation only; German addresses come from the supplied German binaries.

## Tail anchor

The final function is source-correlated as `SetTrainerFlagsAfterTrainerEyeRematch`.

- Retail Rev 0 / Rev 1: **0x080830EC..0x08083108**
- Debug: **0x0808A4B4..0x0808A4D0**
- size: **0x1C bytes**

SHA-256:

- Retail: `ea98d544b95db961865f422b2162d64fddbfd9dddefcc759b77a5186c025d561`
- Debug: `3da8b8fbc82b8e663b9cfc8382be145fb4d1fb25ede08e5c7cd0ad97599313fd`

It clears the current trainer's Trainer Eye rematch flag and then marks the current trainer as battled.

## Next-module anchor

`cable_club` begins immediately afterward:

- Retail Rev 0 / Rev 1: **0x08083108**
- Debug: **0x0808A4D0**
- accumulated delta at module boundary: **+0x73C8**

The profile entries intentionally differ because `cable_club` itself contains Debug-only functions at its beginning.

### Retail entry

The first Retail function is source-correlated as `sub_8082CD4`.

Prefix:

`70 B5 00 06 06 0E 09 06 0D 0E 0C 4C 20 1C`

It looks for the cable-club task; if absent it creates the priority-80 task and stores the two arguments into task data.

### Debug entry

The Debug build begins `cable_club` with source-correlated `debug_sub_808A4D0`.

Prefix:

`00 B5 01 1C 02 48 81 42 04 D1 01 20`

It maps cable-club task functions to Debug state IDs before the ordinary cable-club runtime begins.

Thus the different next-module prefixes are expected and do not indicate a `battle_setup` size difference.
