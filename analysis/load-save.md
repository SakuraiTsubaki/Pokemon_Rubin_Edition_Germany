# German load/save staging and serialization module

The complete `load_save` text module is mapped from the supplied German Retail, Rev 1 and Debug ROMs.

## Module boundary

| Profile | Start | End exclusive | Size | SHA-256 |
| --- | --- | --- | ---: | --- |
| Retail Rev 0 / Rev 1 | 0x08047CF0 | 0x08047FFC | 780 bytes (0x30C) | 0a35f0a60d16a395c3537589d1f8db8d68a377de8ceab9e1b4b61738cdb5ad05 |
| Debug | 0x0804BEBC | 0x0804C1C8 | 780 bytes (0x30C) | 3b756e289bf0492f340beb5657a7a83f668700c70c16d1b084046d95e08edd5a |

Retail Rev 0 and Rev 1 are byte-identical. There is no Debug-only insertion; the complete module remains at accumulated delta **+0x41CC**.

## German function map

Historical source names are not treated as German addresses. The addresses below are the German binary entries.

| Function | Retail | Debug | Span | Role |
| --- | --- | --- | ---: | --- |
| CheckForFlashMemory | 0x08047CF0 | 0x0804BEBC | 44 | probe flash; set presence flag; initialize flash timer |
| GetSecretBase2Field_9 | 0x08047D1C | 0x0804BEE8 | 12 | read SaveBlock2 specialSaveWarp |
| ClearSecretBase2Field_9 | 0x08047D28 | 0x0804BEF4 | 12 | clear specialSaveWarp |
| SetSecretBase2Field_9 | 0x08047D34 | 0x0804BF00 | 12 | set specialSaveWarp |
| SetSecretBase2Field_9_AndHideBG | 0x08047D40 | 0x0804BF0C | 24 | hide BG then set specialSaveWarp |
| ClearSecretBase2Field_9_2 | 0x08047D58 | 0x0804BF24 | 12 | duplicate clear helper |
| SavePlayerParty | 0x08047D64 | 0x0804BF30 | 68 | serialize party count and six Pokemon to SaveBlock1 |
| LoadPlayerParty | 0x08047DA8 | 0x0804BF74 | 72 | restore party count and six Pokemon from SaveBlock1 |
| SaveObjectEvents | 0x08047DF0 | 0x0804BFBC | 56 | serialize sixteen object events |
| LoadObjectEvents | 0x08047E28 | 0x0804BFF4 | 56 | restore sixteen object events |
| SaveSerializedGame | 0x08047E60 | 0x0804C02C | 16 | SavePlayerParty plus SaveObjectEvents |
| LoadSerializedGame | 0x08047E70 | 0x0804C03C | 16 | LoadPlayerParty plus LoadObjectEvents |
| LoadPlayerBag | 0x08047E80 | 0x0804C04C | 188 | stage bag/mail arrays from SaveBlock1 into temporary EWRAM |
| SavePlayerBag | 0x08047F3C | 0x0804C108 | 192 | write staged bag/mail arrays back into SaveBlock1 |

## Runtime save-block addresses

The module's ROM literals directly identify the German EWRAM save blocks:

| Block | Retail | Debug | Debug shift |
| --- | --- | --- | ---: |
| gSaveBlock2 | **0x02024EA4** | **0x02025148** | +0x2A4 |
| gSaveBlock1 | **0x02025734** | **0x020259D8** | +0x2A4 |

This independently agrees with the already verified RTC offset:

- Retail local-time offset = SaveBlock2 +0x98 = **0x02024F3C**;
- Debug local-time offset = SaveBlock2 +0x98 = **0x020251E0**.

The ROM-code delta and EWRAM-data delta are therefore distinct quantities and must never be conflated.

## Serialized party

`SavePlayerParty` stores:

- player party count;
- exactly **six** 0x64-byte `Pokemon` records.

`LoadPlayerParty` restores the same fixed six-record region.

In SaveBlock1 these are:

- party count: +0x234;
- party array: +0x238.

This is the persistent counterpart to the six-slot party assumptions already found in battle, breeding, storage and AI code.

## Serialized object events

Exactly **16 ObjectEvent records** are copied between the live object-event array and SaveBlock1.

`SaveSerializedGame` is simply:

1. SavePlayerParty;
2. SaveObjectEvents.

`LoadSerializedGame` performs the inverse pair.

This module does not itself write flash sectors; it stages live runtime state into the save blocks used by the lower save/flash system.

## Bag/mail staging geometry

The temporary `LoadedSaveData` structure mirrors fixed SaveBlock1 pockets:

| Pocket/data | Entries | SaveBlock1 offset |
| --- | ---: | ---: |
| Items | **20** | +0x560 |
| Key Items | **20** | +0x5B0 |
| Poké Balls | **16** | +0x600 |
| TMs/HMs | **64** | +0x640 |
| Berries | **46** | +0x740 |
| Mail | **16** | +0x2B4C |

`LoadPlayerBag` copies all of those arrays from SaveBlock1 into temporary EWRAM. `SavePlayerBag` copies them back.

These are hard serialized capacities. A Gen-10-ready inventory should not widen these arrays in-place if legacy German saves must remain loadable; a versioned/extended inventory representation or translation layer is safer.

## specialSaveWarp

SaveBlock2 byte +0x09 is used as a Boolean `specialSaveWarp` flag.

The module provides:

- getter;
- setter;
- two clear helpers;
- a setter that also calls the BG-hide synchronization helper.

No code in this module stores values other than 0 or 1.

## Flash-presence probe

`CheckForFlashMemory` calls the flash-identification routine. A successful identification sets `gFlashMemoryPresent` and initializes the flash timer; failure clears the presence flag.

This is hardware/storage-device detection, distinct from the higher-level rotating-section save format already verified from the supplied 128-KiB SAV files.

## Expansion boundary

For later-generation expansion, keep three layers separate:

1. **live runtime structures** — party/object events/bag working data;
2. **legacy SaveBlock1/SaveBlock2 layout** — exact Ruby-compatible serialized schema;
3. **flash section transport** — rotating 14-section physical save system.

That separation allows a larger modern runtime model while preserving read/write compatibility with the original German format.

## Next module

`trade` begins at:

- Retail **0x08047FFC**
- Debug **0x0804C1C8**
- delta **+0x41CC**

The first function is source `sub_8047CD8`, a short wrapper that installs the trade main callback. Its historical name is not the German ROM address.
