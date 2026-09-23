# German Debug menu block

This block records the profile split immediately after `cable_club` and the point where Retail and Debug converge again at `trainer_see`.

## Module sequence

### Retail Rev 0 / Rev 1

Retail skips the globally DEBUG-guarded Tomomichi, Nohara and Taya modules. It contains only the unguarded Mori module:

- `mori_debug_menu`: **0x08084144..0x08084410**, size **0x2CC**

Then `trainer_see` starts at **0x08084410**.

### Debug

Debug contains all four menu modules:

- `tomomichi_debug_menu`: **0x0808B85C..0x0808F3C4**, size **0x3B68**
- `nohara_debug_menu`: **0x0808F3C4..0x08090454**, size **0x1090**
- `mori_debug_menu`: **0x08090454..0x08090720**, size **0x2CC**
- `taya_debug_window`: **0x08090720..0x0809177C**, size **0x105C**

Then `trainer_see` starts at **0x0809177C**.

## SHA-256

- Tomomichi Debug: `8382ed4234377c500d28fa69ad170d7dd9c6eeef46b045b4286a7ddd70b22b91`
- Nohara Debug: `1858b8fb291d3f7c9a1e1e114fbaaa159221ef499d3a42aef0195bc176fc2a98`
- Mori Retail: `f060b11a1bf4848bacf58419c38441f6c25d44850c8cbc10129c5a2c417b5663`
- Mori Debug: `ed44baed947a6c5cb01c4a7c7ac5305c33070cf572cf536fc5ebb95df2670b52`
- Taya Debug: `87df792ed184eb1dc86755a576a045247dc87e3a9f88097dad80a0f827c5d48d`
- complete Debug menu block `0x0808B85C..0x0809177C`: `0d8a1167d6047c0f2bef58ff748db967bc45955bda4fa299f46eb874008deb14`

Retail Rev 0 and Rev 1 Mori text are byte-identical.

## Tomomichi

The connected source contains **181 explicit functions** and is globally `#if DEBUG`.

Entry:

- **0x0808B85C** `InitTomomichiDebugWindow`
- **0x0808B868** `debug_sub_808B868`

The first function calls the Debug-window initializer and returns FALSE.

The final function is `debug_nullsub_66`:

- **0x0808F3C0..0x0808F3C4**
- bytes `70 47 00 00`

The next module, Nohara, starts at **0x0808F3C4**.

## Nohara

The connected source contains **40 explicit functions** and is globally `#if DEBUG`.

Entry:

- **0x0808F3C4** `InitNoharaDebugMenu`
- **0x0808F414** `debug_sub_808F414`

The module exposes TV, fan-club, Petalburg Gym, Sootopolis, Mr. Briney, ash-count, legendary-flag and Battle Tower streak Debug actions.

The final function is source-correlated as `NoharaDebugMenu_AddNumWinningStreaks` and occupies:

- **0x080903F4..0x08090454**
- size **0x60**
- SHA-256 `ae7015bc658696b5a1c00351b47e0685c8f31ae72778c998d62c370854d24bc1`

The next module, Mori, begins at **0x08090454**.

## Mori

The connected source contains **13 explicit functions** and is not globally DEBUG-guarded, so it appears in Retail and Debug.

Retail:

- **0x08084144..0x08084410**
- size **0x2CC**

Debug:

- **0x08090454..0x08090720**
- size **0x2CC**

The size is identical across profiles. The Retail-to-Debug displacement through Mori is therefore constant at **+0xC310**.

The first function is source-correlated as `unref_sub_8083CF0`. It reads the multiplayer ID from SIOCNT and builds a diagnostic input-state string.

The final function is `InitMoriDebugMenu`:

- Retail **0x080843C0..0x08084410**
- Debug **0x080906D0..0x08090720**
- size **0x50** in both profiles

Mori exposes daycare/egg, step-count, move-tutor, long-name and Pokéblock Debug actions.

Retail proceeds directly to `trainer_see`; Debug proceeds to Taya.

## Taya

The connected source contains **24 explicit functions** and is globally `#if DEBUG`.

Debug range:

- **0x08090720..0x0809177C**
- size **0x105C**

Entry `TayaDebugMenu_Trend` starts at **0x08090720**.

The second function begins at **0x08090808**, matching source label `debug_sub_8090808`.

The final function `debug_sub_80916AC` occupies:

- **0x080916AC..0x0809177C**
- size **0xD0**
- SHA-256 `2e6c6830c85834f86d18265190b9ceee84afc6e93bd789c105519a7f7ecefc4e`

## Divergence accounting

Debug-only menu text after `cable_club` totals:

- Tomomichi: 0x3B68
- Nohara: 0x1090
- Taya: 0x105C

Total Debug-only menu text: **0x5C54**

Mori contributes the same **0x2CC** in both profiles.

At Mori entry the Retail-to-Debug displacement is **+0xC310**. After Taya, at `trainer_see`, it becomes:

**+0xD36C**

## trainer_see convergence anchor

Retail `trainer_see`:

- **0x08084410**

Debug `trainer_see`:

- **0x0809177C**

Both begin with the same `CheckTrainers` instruction prefix:

`30 B5 00 24 0A 4D E0 00 00 19 80 00 41 19 08 78 C0 07 00 28 0E D0 C8 79 01 28 01 D0 03 28 09 D1`

This independently establishes the end of the Debug-menu divergence block.
