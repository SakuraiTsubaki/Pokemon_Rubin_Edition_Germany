# German sound module

The complete `sound` text module has been bounded directly in the supplied German Retail Rev 0, Retail Rev 1 and Debug ROMs.

## Module boundary

| Profile | Start | End exclusive | Size | SHA-256 |
| --- | --- | --- | ---: | --- |
| Retail Rev 0 / Rev 1 | 0x08074F6C | 0x080759E4 | **2,680 bytes (0xA78)** | `5d126e677f92d1b169d5b26172bb83cb000e0899dbae11ea0d41688826fd531f` |
| Debug | 0x0807C1D8 | 0x0807CC50 | **2,680 bytes (0xA78)** | `4c7e9d4d53eadc90f4424f77bf662c1426a9c70371f7aa6991e62d388ec67e30` |

Retail Rev 0 and Rev 1 are byte-identical across the complete module. Debug adds no `sound` text, so the accumulated Retail-to-Debug displacement remains **+0x726C** at entry and exit.

## Entry anchor

The first function is source-correlated as `InitMapMusic`.

Common first 16 bytes:

`00 B5 03 49 00 20 08 70 00 F0 80 F8 01 BC 00 47`

The following literal is the profile-specific `gDisableMusic` byte:

- Retail Rev 0 / Rev 1: **0x03004AFC**
- Debug: **0x03004BD4**

The function clears the disable-music flag and resets the map-music state.

## Map-music state

The German binaries establish the internal map-music state addresses:

| State | Retail | Debug | Literal refs |
| --- | --- | --- | ---: |
| `sCurrentMapMusic` | 0x030006D4 | 0x030006F4 | 11 |
| `sNextMapMusic` | 0x030006D6 | 0x030006F6 | 10 |
| `sMapMusicState` | 0x030006D8 | 0x030006F8 | 12 |
| `sMapMusicFadeInSpeed` | 0x030006D9 | 0x030006F9 | 4 |
| `sFanfareCounter` | 0x030006DA | 0x030006FA | 3 |

Source correlation shows active map-music state values 0, 1, 2, 5, 6 and 7, covering idle, pending play, playing, fade-out stop, fade-out/play and fade-out/fade-in transitions.

## Music player globals

Profile-specific music-player references inside the German module are:

| Music player | Retail | Debug | Literal refs |
| --- | --- | --- | ---: |
| BGM | 0x03007390 | 0x030074A0 | 15 |
| SE1 | 0x030073D0 | 0x030074E0 | 4 |
| SE2 | 0x03007410 | 0x03007520 | 4 |
| SE3 | 0x03007460 | 0x03007570 | 1 |

The Pokemon-cry runtime state is also profile-relocated:

- `gMPlay_PokemonCry`: Retail **0x0202F79C**, Debug **0x0202FA40** — 6 literal refs
- `gPokemonCryBGMDuckingCounter`: Retail **0x0202F7A0**, Debug **0x0202FA44** — 4 literal refs

## Fanfare table

The source-correlated fanfare table has **12 entries**, each `(u16 songNum, u16 duration)`.

Binary addresses:

- Retail Rev 0 / Rev 1: **0x083896DC**
- Debug: **0x083A386C**

The complete 48-byte table is byte-identical in all three profiles with SHA-256:

`b47a9578152cbf53851514486121001deccd59ee7f1d5b7ce0a0c5924f3a9ca8`

Durations are measured by the module's fanfare counter and the BGM is paused/resumed around fanfare playback.

## Cry path

The source-correlated cry layer supports six cry modes (`0..5`) and configures volume, pan, pitch, length, release, chorus and priority before selecting the cry tone table.

Normal cry playback ducks BGM volume and restores it through a task after the cry ends. The module tracks the current Pokemon-cry music player pointer and a short ducking counter.

## Public sound path

The source-correlated module contains **46 explicit functions** and no Debug-only text. It covers:

- map BGM state/reset/fade transitions;
- fanfare playback and fanfare task lifetime;
- Pokemon cry configuration and BGM ducking;
- BGM play/stop/fade helpers;
- SE1/SE2 panning and combined pan control;
- BGM/SE status queries.

Historical source labels are semantic correlation only; German addresses come from the German binaries.

## Tail anchor

The final function is source-correlated as `IsSpecialSEPlaying`.

Its 40-byte region begins:

`00 B5 05 48 41 68 00 29 0A DB 04 48 01 40 00 29 06 D0 01 20 05 E0`

and ends:

`00 20 02 BC 08 47 00 00`

The function's only profile-specific literal is the SE3 music-player address shown above. Including the final alignment halfword gives the exact module end.

## Next-module anchor

`battle_anim` begins immediately afterward:

- Retail Rev 0 / Rev 1: **0x080759E4**
- Debug: **0x0807CC50**
- accumulated delta: **+0x726C**

Its first function is source-correlated as `ClearBattleAnimationVars`.

Common first 32 bytes:

`F0 B5 4F 46 46 46 C0 B4 22 48 00 21 01 70 22 48 01 70 22 48 01 70 22 48 01 70 22 48 00 21 01 60`

This clears the battle-animation runtime globals and independently anchors the `sound` → `battle_anim` transition.
