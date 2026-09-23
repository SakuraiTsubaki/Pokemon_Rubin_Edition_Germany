# German cable_club module

The complete `cable_club` text module has been bounded directly in the supplied German Retail Rev 0, Retail Rev 1 and Debug ROMs.

## Module boundary

| Profile | Start | End exclusive | Size | SHA-256 |
| --- | --- | --- | ---: | --- |
| Retail Rev 0 / Rev 1 | 0x08083108 | 0x08084144 | **4,156 bytes (0x103C)** | `28df0fa5ac7207668dede82697ea774f85b995f712444400e1b7c1c93ad649a7` |
| Debug | 0x0808A4D0 | 0x0808B85C | **5,004 bytes (0x138C)** | `df55b1561074d791e2a2c732d41bfef302d3776f04d2041fd7c95c6cdc87df99` |

Retail Rev 0 and Rev 1 are byte-identical across the complete module.

The Debug module is **0x350 bytes larger**, so the accumulated Retail-to-Debug text displacement changes from **+0x73C8** at module entry to **+0x7718** at module exit.

## Profile-specific entry

### Retail

Retail begins directly with source-correlated `sub_8082CD4`:

`70 B5 00 06 06 0E 09 06 0D 0E 0C 4C 20 1C`

The routine finds/creates the cable-club task and stores the requested link-mode arguments.

### Debug

Debug begins with `debug_sub_808A4D0`:

`00 B5 01 1C 02 48 81 42 04 D1 01 20`

The historical Debug label happens to match the German Debug ROM address exactly. It maps cable-club task functions to compact Debug state IDs.

The next Debug-only function is `debug_sub_808A55C`, which renders live link-state diagnostics.

## Debug growth decomposition

The binary growth is **0x350 bytes** and can be fully reconciled with source-correlated Debug paths.

### Debug-only prefix: 0x280 bytes

- `debug_sub_808A4D0`: **0x0808A4D0..0x0808A55C**, 0x8C bytes
  - SHA-256 `022822ad831619a3069865a269423fcc32eb534e327e0ff69161e66f36b80482`
- `debug_sub_808A55C`: **0x0808A55C..0x0808A750**, 0x1F4 bytes
  - SHA-256 `c8404998421573d153e599dd0abf5d0205d8dd1177f7fabe4a790c6b13d75081`

Total: **0x280 bytes**

### Debug instrumentation in sub_8082CD4: +0x28 bytes

Retail version:

- **0x08083108..0x0808314C**
- size 0x44
- SHA-256 `6a67084008b40a22cbb73da645e63a144cffbd644b17fd70dd5b4649153a728e`

Debug version:

- **0x0808A750..0x0808A7BC**
- size 0x6C
- SHA-256 `27301ae7ac7f1335f056fb7620ef8d820ba7381182864a2aefe585bb96b03730`

Source correlation explains the extra initialization of the link-test background plus creation of the live Debug diagnostic task.

### Debug instrumentation in sub_80831F8: +0x10 bytes

The source has one additional Debug-only call in this ordinary task: it updates the displayed link-player count via `sub_8082D60`.

After accounting for the directly bounded Debug-only functions and the `sub_8082CD4` growth, the remaining ordinary-code growth is exactly **0x10 bytes**, matching this second source-guarded instrumentation path.

### Debug-only tail: 0x98 bytes

First tail block:

- `debug_sub_808B778` + `debug_sub_808B7A8`
- **0x0808B778..0x0808B7E0**
- size **0x68**

Second tail block:

- `debug_sub_808B82C`
- `debug_sub_808B838`
- `debug_sub_808B850`
- **0x0808B82C..0x0808B85C**
- size **0x30**

Total tail Debug growth: **0x98 bytes**

Therefore:

**0x280 + 0x28 + 0x10 + 0x98 = 0x350**

## Runtime scope

The source contains **61 explicit functions including 7 Debug-only functions**, leaving 54 ordinary/retail functions.

The module handles:

- timed and ordinary link opening;
- master/client player-count negotiation;
- link error and cancellation paths;
- link-player data exchange;
- link battle setup;
- single/double/multi battle type selection;
- link battle music selection;
- party/bag save/restore around link battles;
- record mixing;
- trainer-card viewing and color-name formatting;
- link timeout/error handling;
- script-context handoff;
- link shutdown and return-to-field sequencing.

German-specific source logic in `sub_808303C` treats link type `0x2255` specially: more than one player is sufficient; other link types use the task's configured minimum-player count.

The German trainer-card color strings include `KUPFER` for copper.

Historical numeric source labels remain semantic identifiers only unless independently verified against the German binary.

## Last ordinary functions

The final ordinary functions are source-correlated as `sub_8083CA4` and `unref_sub_8083CC8`.

`unref_sub_8083CC8` occupies:

- Retail: **0x0808411C..0x08084144**, size 0x28
- Debug: **0x0808B804..0x0808B82C**, size 0x28

SHA-256:

- Retail: `8fdec746d51f056630c7a5b4db917ca1ee1fe5e88eff23e5125b2df67201b69b`
- Debug: `3afb605797adc47c917e49ce80b074044ba86c85c6b129033fe3bb8d4b972725`

It installs the close-link callback and replaces the task function with the script-resume watcher.

The Debug-only 0x30-byte tail follows it; Retail ends immediately.

## Next-module anchors

The next executable module differs by profile.

### Retail next: mori_debug_menu

Retail skips the DEBUG-guarded Tomomichi and Nohara modules, but `mori_debug_menu.c` itself is not globally DEBUG-guarded.

It begins at:

**0x08084144**

The first function is source-correlated as `unref_sub_8083CF0`.

Common entry shape:

`F0 B5 11 48 04 68 A4 06 A4 0F 10 48 FF 21 01 70 0F 49`

The routine reads the multiplayer ID from SIOCNT, builds a diagnostic string and appends button-state labels.

### Debug next: tomomichi_debug_menu

Debug begins the first dedicated Debug-menu module immediately at:

**0x0808B85C**

The first function is `InitTomomichiDebugWindow`:

`00 B5 00 F0 09 F8 00 20 02 BC 08 47`

It calls the Debug-window initializer and returns FALSE.

The following function begins at **0x0808B868**, matching source label `debug_sub_808B868`.

This profile split is deliberate and is why a single post-`cable_club` delta cannot be carried across the Debug-menu block.
