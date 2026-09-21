# German Debug battle-tool subsystem

The German Debug ROM contains a large development-only subsystem inside battle_main that is completely absent from both retail revisions.

## Exact range

- Start: **0x08010800**
- End exclusive: **0x080139E4**
- Size: **12,772 bytes (0x31E4)**
- SHA-256: **d5fdce32b2fc20101163c1b9c30f47c7aae94fafc126096e996eaf0f96dd14df**

The first function is debug_sub_8010800 at the address encoded by its historical symbol name. The final known Debug-only function begins at 0x080138CC as debug_sub_80138CC.

After this block, normal battle execution rejoins at:

- Retail BattleMainCB1: **0x0801041C**
- Debug BattleMainCB1: **0x080139E4**

The total displacement at rejoin is therefore **+0x35C8**.

## Exact anchored Debug entries

| Function | German Debug address |
| --- | --- |
| debug_sub_8010800 | 0x08010800 |
| debug_sub_8010818 | 0x08010818 |
| debug_sub_80108B8 | 0x080108B8 |
| debug_sub_8010A7C | 0x08010A7C |
| debug_sub_8010AAC | 0x08010AAC |
| debug_sub_8010B80 | 0x08010B80 |
| debug_sub_8010CAC | 0x08010CAC |
| debug_sub_8011498 | 0x08011498 |
| debug_sub_801174C | 0x0801174C |
| debug_sub_8011D40 | 0x08011D40 |
| debug_sub_8011E5C | 0x08011E5C |
| debug_sub_8011E74 | 0x08011E74 |
| debug_sub_8011EA0 | 0x08011EA0 |
| debug_sub_8012294 | 0x08012294 |
| debug_sub_80123D8 | 0x080123D8 |
| debug_sub_8012540 | 0x08012540 |
| debug_sub_80125A0 | 0x080125A0 |
| debug_sub_80125E4 | 0x080125E4 |
| debug_sub_8012628 | 0x08012628 |
| debug_sub_8012658 | 0x08012658 |
| debug_sub_8012688 | 0x08012688 |
| debug_sub_8012878 | 0x08012878 |
| debug_sub_8012D10 | 0x08012D10 |
| debug_sub_8013294 | 0x08013294 |
| debug_sub_80132C8 | 0x080132C8 |
| debug_sub_80138CC | 0x080138CC |

These symbol addresses were checked directly against the German Debug ROM. Several functions begin with non-PUSH Thumb instructions, so function discovery must not rely only on prologue scanning.

## Capabilities visible in the Debug source/binary block

The subsystem contains development paths for:

- battle animation selection/testing;
- audio/BGM/SE controls;
- battle text-buffer manipulation;
- species/gender/party parameter editing;
- direct sprite and affine-animation testing;
- controller/battle-buffer experiments;
- AI-cycle and automated battle input support;
- a dedicated Debug battle charmap/UI;
- direct battle state and link-test manipulation.

This block is preserved as a first-class Debug profile. It must not be merged into retail execution paths.

## Expansion significance

The Debug subsystem is useful as an instrumentation donor for the independent German project. It exposes internal battle state and test paths that can later be adapted into development diagnostics while keeping the Retail profiles clean.
