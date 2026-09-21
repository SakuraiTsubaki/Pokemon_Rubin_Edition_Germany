# German battle_main initialization slice

The first battle_main slice has been mapped from the supplied German ROMs.

## Exact slice

| Profile | Start | End exclusive | Size | SHA-256 |
| --- | --- | --- | ---: | --- |
| Retail Rev 0 / Rev 1 | 0x0800E998 | 0x0800F200 | 2,152 bytes | d8753f7da7f3354ddd5839e7de318ec8c9f0f289789f5285fe44c05a4e69ca4e |
| Debug | 0x0800EC0C | 0x0800F4C0 | 2,228 bytes | 493145436c8a0f706ed56e4950e98e0b54aae0556d93754c06285174eaf0e89d |

Retail Rev 0 and Rev 1 are byte-identical across this entire initialization slice.

## Function map

| Function | Retail | Debug | Delta | Retail bytes | Debug bytes | Role |
| --- | --- | --- | ---: | ---: | ---: | --- |
| CB2_InitBattle | 0x0800E998 | 0x0800EC0C | +0x274 | 52 | 52 | battle init dispatcher; multi battle enters link setup path |
| CB2_InitBattleInternal | 0x0800E9CC | 0x0800EC40 | +0x274 | 500 | 532 | VRAM/window/scanline/background/sprite/task initialization and battle setup |
| BufferPartyVsScreenHealth_AtStart | 0x0800EBC0 | 0x0800EE54 | +0x294 | 192 | 192 | encode six-party health/status state for link VS screen |
| SetPlayerBerryDataInBattleStruct | 0x0800EC80 | 0x0800EF14 | +0x294 | 92 | 92 | copy local Enigma Berry data into link battle header |
| SetAllPlayersBerryData | 0x0800ECDC | 0x0800EF70 | +0x294 | 316 | 316 | populate per-player Enigma Berry battle records |
| TryCorrectShedinjaLanguage | 0x0800EE18 | 0x0800F0AC | +0x294 | 88 | 88 | repair Shedinja language flag when nickname matches localized default |
| CB2_HandleStartBattle | 0x0800EE70 | 0x0800F104 | +0x294 | 912 | 956 | link/non-link battle startup state machine and party exchange |

## Debug growth #1 — CB2_InitBattleInternal

Retail size: 500 bytes  
Debug size: 532 bytes  
Growth: **32 bytes (0x20)**

The Debug build adds checks around a debug-control flag before:

- selecting the battle environment, and
- creating the normal enemy trainer party / held-item setup path.

After this function, the accumulated Debug displacement changes:

- before: +0x274
- after: **+0x294**

This is direct evidence that Debug can preserve or inject battle-environment / opponent setup state instead of always rebuilding it from normal game context.

## Link VS health encoding

BufferPartyVsScreenHealth_AtStart packs the six player-party slots into two-bit states:

- 0: no usable/represented slot;
- 1: non-Egg, HP nonzero, no status;
- 2: HP nonzero and Egg or status condition;
- 3: non-Egg with zero HP.

The six two-bit states are then split into low/high bytes for the link VS header.

This fixed six-slot encoding is another original protocol constraint to preserve during compatibility work.

## Enigma Berry transfer

Two routines in this slice establish that battle initialization copies Enigma Berry metadata into battle/link structures:

- seven name bytes;
- eighteen item-effect bytes;
- hold effect;
- hold-effect parameter.

In link battles, remote berry records are read from received link blocks and indexed by link-player ID.

## Shedinja localization repair

TryCorrectShedinjaLanguage performs a localized compatibility correction:

- checks for Shedinja;
- checks language value;
- reads nickname;
- compares the nickname against a localized default-name resource;
- updates language when the expected localized name matches.

This routine must not be generalized or removed until the German text/name resource and language-ID semantics are fully reconstructed.

## Debug growth #2 — CB2_HandleStartBattle

Retail size: 912 bytes  
Debug size: 956 bytes  
Growth: **44 bytes (0x2C)**

The Debug-only path is gated by the same debug-control bit used by battle initialization. During link-start state 0 it can force two link-player records into a deterministic test arrangement, including link-player IDs and link type 0x2211.

After this function, accumulated Debug displacement becomes:

- previous: +0x294
- new: **+0x2C0**

## Expansion pressure points discovered already

This initialization slice exposes several structures that cannot be enlarged blindly:

- party count is hard-coded around six slots in VS-health packing and party exchange;
- early link-party transfer is performed as three groups of two Pokemon;
- Enigma Berry wire format has fixed field lengths;
- link startup assumes two-player and multi-player bit masks/state counts from the original protocol;
- localization repair logic relies on original species/language/name behavior;
- debug and retail setup paths intentionally diverge and must remain separate profiles.

No expansion changes are applied here yet.

## Next function

The next mapped function starts at:

- Retail: **0x0800F200**
- Debug: **0x0800F4C0**

The Debug displacement at this boundary is +0x2C0.
