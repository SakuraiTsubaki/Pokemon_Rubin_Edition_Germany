# German pokemon_menu module

The complete `pokemon_menu` text module has been bounded directly in the supplied German Retail Rev 0, Retail Rev 1 and Debug ROMs.

## Boundary

- Retail Rev 0 / Rev 1: **0x08089EC4..0x0808BA64**, 0x1BA0 bytes, SHA-256 `e7d55eb1e9dc69dc936146d5b2a216b600fd5ebd714bd4547f4b8cb69f1dca15`
- Debug: **0x08097290..0x08098E98**, 0x1C08 bytes, SHA-256 `111c646d5e840c31bd107eec3a3f42a4c545b632c5d54422002c7e94a5496bd1`
- Retail Rev 0 / Rev 1 are byte-identical.
- Debug grows by **0x68 bytes**.
- accumulated displacement changes **+0xD3CC -> +0xD434**.

## Entry

The first function is source-correlated as `sub_8089A70`.

Common prefix:

`00 B5 05 48 01 7A 80 22 11 43 01 72 00 20 00 21`

It disables palette-buffer transfer during menu setup and opens the standard party menu.

## Runtime scope

The source-correlated file contains **83 explicit functions**.

It covers party-Pokémon context menus, summary/switch/item/mail flows, field-move selection and setup, Surf/Fly/Dive/Waterfall/Strength and related callbacks, item-use return flows and menu state restoration.

## Debug growth

Two guarded paths explain the complete growth.

### debug_sub_80986AC

- Debug: **0x080986AC..0x080986F8**
- size **0x4C**
- SHA-256 `6b4d3d6355598a0cafcc4fcd984c12dd624f33fe3e6eaa80392b3a88a49c1e51`

This is a Debug-only Waterfall helper.

### sub_808AE8C guarded condition

Retail:

- **0x0808B2E0..0x0808B374**
- size **0x94**
- SHA-256 `236b1d716db3d90f560d64eb0c55ce8fe6466de34e3043e37270077d51ba16d1`

Debug:

- **0x080986F8..0x080987A8**
- size **0xB0**
- SHA-256 `bf2fdb0623dc87bb531a954e1c60e967230568abb609530313f6312ef880d8e1`

Growth: **0x1C bytes**, matching the Debug-only `gUnknown_020297ED == 0` gate around TM/HM learnability status rendering.

Thus **0x4C + 0x1C = 0x68**.

## Tail

The final function is source-correlated as `sub_808B5E4`.

- Retail: **0x0808BA38..0x0808BA64**, size 0x2C, SHA-256 `d80b13f226814e1420590161d80bdd9a8f7cc5f2c37f60c20394c4dc1e69b417`
- Debug: **0x08098E6C..0x08098E98**, size 0x2C, SHA-256 `11429eac1fbb5db1e4afda21d3a79d20a45198f745abf417116b7de536b75299`

## Next

`option_menu` begins immediately afterward:

- Retail: **0x0808BA64**
- Debug: **0x08098E98**
- delta: **+0xD434**

Its first function is source-correlated as `MainCB`, a four-call frame callback running tasks, sprites, OAM build and palette fade update.
