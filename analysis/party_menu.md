# German party_menu module

The complete `party_menu` text module has been bounded directly in the supplied German Retail Rev 0, Retail Rev 1 and Debug ROMs.

## Module boundary

| Profile | Start | End exclusive | Size | SHA-256 |
| --- | --- | --- | ---: | --- |
| Retail Rev 0 / Rev 1 | 0x0806B21C | 0x080712D0 | **24,756 bytes (0x60B4)** | `4e46edf06f57597e5be44b4ea4553baa12d7a5b0539a4ce4e9474d9132f0dd74` |
| Debug | 0x0806FB44 | 0x08075C30 | **24,812 bytes (0x60EC)** | `e9df2862b802125709c828573e1ab75fcaa5d3bb8d248bcd810cab15ecab0015` |

Retail Rev 0 and Rev 1 are byte-identical across the complete module.

Debug is **56 bytes (0x38)** larger overall. The accumulated Retail-to-Debug displacement changes from **+0x4928** at module entry to **+0x4960** at the next module.

## Entry anchor

The first function is source-correlated as `CB2_PartyMenuMain`.

Retail entry:

`70 B5 81 B0 95 F7 52 FB 95 F7 76 FB`

Debug entry:

`70 B5 81 B0 90 F7 BE FE 90 F7 E2 FE`

Both run the party-menu sprite/OAM update path and then process menu tasks/palette state. The Debug body additionally contains link diagnostics when the link is open.

## Debug / Retail conditional decomposition

The source contains three code-generating Debug conditionals inside otherwise common party-menu logic:

1. link receive-queue diagnostics in `CB2_PartyMenuMain`;
2. a Debug VRAM diagnostic path during party-menu initialization;
3. a Debug guard in the move-teaching path.

Their aggregate binary growth is **+0x5C** relative to the Retail common body.

Retail additionally contains one **Retail-only** tail function:

`unref_sub_8070F90` at **0x080712AC..0x080712D0**, size **0x24**.

Tail SHA-256:

`9409d74a2cc3d04dd0fcd5304d4ec24d7695ffb470360ab3a1509646f727e04d`

It sets the system Pokédex, Pokémon and PokéNav flags.

Therefore the net module-size change is:

`+0x5C Debug internal growth - 0x24 Retail-only tail = +0x38`

No guessed per-conditional byte split is recorded.

## Runtime scope

The module is the complete party-screen implementation layer. Source-correlated responsibilities include:

- party menu initialization and VBlank/main callbacks;
- single/double/link/multi party layouts;
- Pokémon icon and held-item sprites;
- nickname, level, HP/status and HP-bar rendering;
- menu selection and switching;
- field-move and item-use actions;
- move teaching and replacement;
- Rare Candy/stat-growth display;
- evolution-stone dispatch;
- party-menu messages and prompt handling;
- item-effect classification.

The connected source contains **180 explicit function definitions** in total, including the Retail-only tail function. Debug compiles the common 179-function set and omits that Retail-only function.

## Next-module anchor

The next module is `start_menu`, but its first compiled function differs by profile because `start_menu.c` begins with a Debug-only block.

Retail `start_menu` begins at:

- **0x080712D0**
- first compiled function: `BuildStartMenuActions`

Retail entry begins:

`00 B5 05 48 00 21 01 70 E3 F7 9E F9`

Debug `start_menu` begins at:

- **0x08075C30**
- first compiled function: `debug_sub_8075C30`

Debug entry begins:

`00 B5 03 F0 B9 FA 00 F0 B1 F8 01 20 02 BC 08 47`

The common `BuildStartMenuActions` function in Debug starts later at **0x08075E5C** after the Debug-only start-menu prefix.

This profile-specific first-function difference is intentional and independently anchors the party-menu end.
