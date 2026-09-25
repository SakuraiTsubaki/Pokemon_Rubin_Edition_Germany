# German pokemon_storage_system module

The complete first `pokemon_storage_system` text module has been bounded directly in the German Retail Rev 0, Retail Rev 1 and Debug ROMs.

## Boundary

| Profile | Start | End exclusive | Size | SHA-256 |
| --- | --- | --- | ---: | --- |
| Retail Rev 0 / Rev 1 | 0x08095C2C | 0x08096908 | **3,292 bytes (0xCDC)** | `703092c567fa1305a37a5c6ce99e3ac33bae5b5483d203ca4a12125b12b467b0` |
| Debug | 0x080A317C | 0x080A3FB4 | **3,640 bytes (0xE38)** | `a14deaad84ad49a35a00d9e4126449a23beecf7a3e09355011b1d7a0d6749cd1` |

Retail Rev 0 and Rev 1 are byte-identical across the complete module.

Debug is **0x15C bytes larger**, changing the accumulated Retail-to-Debug text displacement from **+0xD550** at entry to **+0xD6AC** at exit.

## Entry

The first function is source-correlated as `CountPokemonInBoxN`.

Common first 32 bytes:

`70 B5 00 06 00 0E 00 24 00 25 81 00 09 18 08 01 40 1A 46 01 A0 00 00 19 00 01 0A 49 40 18 30 18`

It walks the 30 slots of the selected storage box and counts non-empty Pokémon.

## Runtime scope

This module owns the first layer of the Pokémon storage UI/runtime:

- box and party counting helpers;
- first-empty-slot and next-mon navigation;
- storage-system menu creation and field return;
- box-selection popup creation, drawing and teardown;
- current-box label construction;
- storage-system initialization;
- low-level tile-buffer copy/fill helpers;
- left/right box navigation.

## Debug-only text

The connected source contains one Debug-only naked function: `debug_sub_80A3904`.

German Debug range:

- **0x080A3904..0x080A3A60**
- size **0x15C bytes**
- SHA-256 `3c407fdd1d3a8c068ca9d137cad80e40e6b833d46af3619e5f0df22c075b7eaa`

This one function accounts for the **entire** module size increase.

Source correlation shows it mass-populates box Pokémon with randomized data for Debug testing.

## Tail

The final ordinary function is source-correlated as `sub_8096784`.

- Retail: **0x080968D4..0x08096908**
- Debug: **0x080A3F80..0x080A3FB4**
- size **0x34**
- SHA-256 in both profiles: `b736e4badd6f3bba4692a553241b2a130b73787c94d3cdd026658cce58aedf24`

It is byte-identical across Retail and Debug. It periodically nudges the sprite X offset and resets it after the animation cycle.

## Next module

`pokemon_storage_system_2` begins immediately afterward.

- Retail: **0x08096908**
- Debug: **0x080A3FB4**
- delta: **+0xD6AC**

The first function is `task_intro_29`.

Common first 16 bytes:

`00 B5 00 06 00 0E 04 49 08 70 04 49 48 71 04 48`

It stores the selected storage menu mode, writes the same value into the storage-system runtime state and installs the storage-system main callback.

The following function `sub_80967DC` independently anchors the transition by clearing all BG horizontal/vertical offsets.
