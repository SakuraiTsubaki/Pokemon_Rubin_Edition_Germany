# German menu module

The complete `menu` text module has been bounded directly in the supplied German Retail Rev 0, Retail Rev 1 and Debug ROMs.

## Module boundary

| Profile | Start | End exclusive | Size | SHA-256 |
| --- | --- | --- | ---: | --- |
| Retail Rev 0 / Rev 1 | 0x08071F3C | 0x080731B8 | **4,732 bytes (0x127C)** | `399e9dd06ad7cab9c2062f0821b17453e8c5efb8833ff8edc5a8548d9dde1b97` |
| Debug | 0x080791A8 | 0x0807A424 | **4,732 bytes (0x127C)** | `e360c150e51a925e7f526ca26635819e77f2a4cb18895bc119596e71b0995160` |

Retail Rev 0 and Rev 1 are byte-identical across the complete module. Debug adds no `menu` text, so the accumulated Retail-to-Debug displacement remains **+0x726C** at entry and exit.

## Entry anchor

The first function is `CloseMenu`.

The first eight bytes are identical in all three profiles:

`00 B5 05 20 03 F0 88 FC`

It plays the select sound, erases the screen, unfreezes object events, unlocks player controls and destroys the menu cursor.

## Runtime scope

The German module contains the normal menu/window/cursor layer:

- menu window initialization and multistep font/window setup;
- text printing, blanking and frame drawing;
- dialogue-frame display;
- wrapped/non-wrapped cursor movement;
- one- and multi-column menu input;
- yes/no menus;
- pixel-coordinate printing and text alignment;
- menu cursor creation/destruction.

The connected source has no `#if DEBUG` code in this module, consistent with the identical code size.

## German-specific tail

The German build contains two language-specific functions at the tail.

### de_sub_8073110

- Retail: **0x08073110..0x08073174**, size **0x64**
- Debug: **0x0807A37C..0x0807A3E0**, size **0x64**
- Retail SHA-256: `837325d4eecb84dfbe2b98addcc6c0ec4d5e27960d024da42f59c19c8d2e3f25`
- Debug SHA-256: `f4e0163479d0ee994494c114d6eb5bce8d521f96c8814a49ba7824eab7e358d9`

### de_sub_8073174

- Retail: **0x08073174..0x080731B8**, size **0x44**
- Debug: **0x0807A3E0..0x0807A424**, size **0x44**
- Retail SHA-256: `418cf93955f6d1a33737aa82eff09e1ef07009ecf8772cd4fd62124df12cf80f`
- Debug SHA-256: `bfd4b95344f538d822dcb7ec2aeda419eddc6efad47e998f0660d5f0694a4fef`

These helpers rewrite German formatted-name strings around control-code placeholders. Historical numeric names are semantic labels only; the German ROM establishes the addresses above.

The final literal is **0x020232CC**, shared by Retail and Debug, and belongs to the second German helper.

## Next-module anchor

`tileset_anim` begins immediately afterward:

- Retail Rev 0 / Rev 1: **0x080731B8**
- Debug: **0x0807A424**
- accumulated delta: **+0x726C**

Its first function is `ClearTilesetAnimDmas`. It clears the DMA queue count and zeroes the 20-entry DMA request array.

Stable function shape begins:

`00 B5 81 B0 06 49 00 20 08 70 00 20 00 90 05 49 05 4A 68 46`

Profile-specific state addresses in its literal pool are:

- queue count: Retail **0x030006C0**, Debug **0x030006E0**
- DMA array: Retail **0x0202E9D8**, Debug **0x0202EC7C**

This independently anchors the `menu` end and `tileset_anim` start.
