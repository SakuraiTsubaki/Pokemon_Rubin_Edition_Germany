# German battle background module

The complete battle-background module following decompression has been bounded and mapped directly from the supplied German ROMs.

## Exact module identity

| Profile | Start | End exclusive | Size | SHA-256 |
| --- | --- | --- | ---: | --- |
| Retail Rev 0 / Rev 1 | 0x0800D858 | 0x0800E998 | 4,416 bytes | 1aa5d366a78ec31d9ad1b9e2a1d8a7e5dd972abaee607edb54685eb41d5b16a3 |
| Debug | 0x0800DA74 | 0x0800EC0C | 4,504 bytes | 69cffde59be984b84836ae1e6e2f898c426ec713badf4af1a73ce8d7d2163331 |

Retail Rev 0 and Rev 1 are byte-identical across the complete module.

## Function map

| Function | Retail | Debug | Delta | Retail bytes | Debug bytes | Role |
| --- | --- | --- | ---: | ---: | ---: | --- |
| debug_sub_800D684 | 0x0800D858 | 0x0800DA74 | 0x21C | 64 | 64 | debug/utility sprite setup callback entry |
| sub_800D6C4 | 0x0800D898 | 0x0800DAB4 | 0x21C | 16 | 16 | animate sprites and build OAM buffer |
| sub_800D6D4 | 0x0800D8A8 | 0x0800DAC4 | 0x21C | 120 | 120 | initialize battle display registers/background controls |
| ApplyPlayerChosenFrameToBattleMenu | 0x0800D920 | 0x0800DB3C | 0x21C | 108 | 108 | load chosen window frame and battle-menu palette entries |
| DrawMainBattleBackground | 0x0800D98C | 0x0800DBA8 | 0x21C | 768 | 768 | select main battle tiles/tilemap/palette by battle flags, trainer class, map scene and environment |
| LoadBattleTextboxAndBackground | 0x0800DC8C | 0x0800DEA8 | 0x21C | 64 | 152 | load textbox graphics, frame and main battle background |
| sub_800DAF8 | 0x0800DCCC | 0x0800DF40 | 0x274 | 300 | 300 | build link-result window tile data |
| PrintLinkBattleWinLossTie | 0x0800DDF8 | 0x0800E06C | 0x274 | 524 | 524 | render localized link battle win/loss/tie messages |
| InitLinkBattleVsScreen | 0x0800E004 | 0x0800E278 | 0x274 | 1036 | 1036 | link VS-screen task/state machine |
| DrawBattleEntryBackground | 0x0800E410 | 0x0800E684 | 0x274 | 472 | 472 | load battle-entry animation background by battle context |
| LoadChosenBattleElement | 0x0800E5E8 | 0x0800E85C | 0x274 | 944 | 944 | incremental loader for textbox/background tiles, tilemap, palette and frame |

## Debug insertion

LoadBattleTextboxAndBackground is the only function in this module whose code size differs:

- Retail: 64 bytes
- Debug: 152 bytes
- Debug-only growth: **88 bytes (0x58)**

The extra Debug code is guarded by link-battle context and invokes Debug-only display helpers after the normal textbox/background setup.

Because of this insertion:

- functions through LoadBattleTextboxAndBackground begin at Retail + 0x21C in Debug;
- every later function begins at Retail + **0x274** in Debug.

No further size divergence occurs before the end of battle_bg.

## Battle environment table

The German ROMs contain a 10-entry table of five 32-bit pointers per environment.

- Retail table: **0x08206528**
- Debug table: **0x0821F27C**
- Table size: 200 bytes
- SHA-256 for both table contents: **64e4c4c2d165ac4e13e77623ddca80bbaf58ec1120e24418584dbfdf56393a0f**

The table is relocated in Debug, but every resource pointer inside it is byte-for-byte identical.

| ID | Environment | Tileset | Tilemap | Entry tiles | Entry map | Palette |
| ---: | --- | --- | --- | --- | --- | --- |
| 0 | GRASS | 0x08E5DED4 | 0x08E5E4BC | 0x08E63A7C | 0x08E64004 | 0x08E5E484 |
| 1 | LONG_GRASS | 0x08E5E76C | 0x08E5EE24 | 0x08E641C0 | 0x08E648D0 | 0x08E5EDE4 |
| 2 | SAND | 0x08E5F0D4 | 0x08E5F714 | 0x08E64B08 | 0x08E6504C | 0x08E5F6CC |
| 3 | UNDERWATER | 0x08E5F9C4 | 0x08E5FFC4 | 0x08E651F4 | 0x08E656C0 | 0x08E5FF7C |
| 4 | WATER | 0x08E60274 | 0x08E6088C | 0x08E65850 | 0x08E65E5C | 0x08E60848 |
| 5 | POND | 0x08E60B3C | 0x08E61124 | 0x08E66000 | 0x08E6654C | 0x08E610E4 |
| 6 | MOUNTAIN | 0x08E613D4 | 0x08E619D0 | 0x08E66698 | 0x08E66C78 | 0x08E61994 |
| 7 | CAVE | 0x08E61C80 | 0x08E622C0 | 0x08E66E0C | 0x08E67628 | 0x08E62278 |
| 8 | BUILDING | 0x08E625AC | 0x08E62B94 | 0x08E678D0 | 0x08E67CE0 | 0x08E636FC |
| 9 | PLAIN | 0x08E625AC | 0x08E62B94 | 0x08E678D0 | 0x08E67CE0 | 0x08E62570 |

BUILDING and PLAIN deliberately share the same tileset, tilemap and entry-animation resources while using different palette pointers.

## Background selection behavior

The module selects backgrounds from several independent dimensions:

- link / Battle Tower / e-Reader battle flags;
- Groudon/Kyogre special battle flag and game version;
- trainer class (notably Leader and Champion);
- map battle-scene category;
- generic environment ID 0..9.

The normal map-scene path indexes the 20-byte environment table directly by gBattleEnvironment.

## German-specific link result layout

PrintLinkBattleWinLossTie contains German layout constants directly in the binary:

- left message X = **5**
- right message X = **20**
- center message X = **13**
- win tile offset = **160**
- loss tile offset = **172**

The loss offset differs from the English-oriented layout and is preserved as German localization behavior.

## Expansion pressure points

Before adding newer battle environments or wider battle modes, this module needs deliberate expansion work:

- gBattleEnvironment indexing currently assumes exactly the original 10 table entries;
- LoadChosenBattleElement duplicates battle-scene/environment selection logic for tiles, tilemap and palette;
- trainer-class special cases are hard-coded;
- Groudon/Kyogre branching is version-specific;
- entry-background selection and main-background selection are separate code paths that must stay synchronized;
- the link VS result layout contains fixed German pixel/tile positioning.

This commit records original behavior only. No modernization has been applied yet.

## Next module

The next function begins at:

- Retail: **0x0800E998**
- Debug: **0x0800EC0C**

Link order identifies this as the start of battle_main.
