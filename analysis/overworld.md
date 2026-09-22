# German overworld runtime module

The complete `overworld` text module has been bounded directly in the supplied German Retail, Rev 1 and Debug ROMs.

## Module boundary

| Profile | Start | End exclusive | Size | SHA-256 |
| --- | --- | --- | ---: | --- |
| Retail Rev 0 / Rev 1 | 0x0805329C | 0x080562D0 | **12,340 bytes (0x3034)** | 357ca0add3b748d55f7849c99ab06da784968f5b4be7717916479fe9904962c9 |
| Debug | 0x080575AC | 0x0805A7B8 | **12,812 bytes (0x320C)** | 37705f2c85c5669fd49a96d2bf8089eba33c35e05fd07d95610b9fc607631dbc |

Retail Rev 0 and Rev 1 are byte-identical across the complete module.

Debug is **472 bytes (0x1D8)** larger. The accumulated code displacement changes from **+0x4310** at module entry to **+0x44E8** at the following `fieldmap` module.

The connected source identifies three Debug-only code areas responsible for the growth:

- test-menu initialization and its Debug callbacks;
- a Debug overworld-entry callback;
- the R-button Debug flag branch in `CB2_ContinueSavedGame`.

The total 0x1D8 binary growth is proven; this manifest intentionally does not invent per-block byte splits.

## Function inventory

The source-correlated implementation inventory contains 204 distinct functions. Historical `sub_805xxxx` labels are semantic source names only, not German addresses.

- 1. DoWhiteOut
- 2. Overworld_ResetStateAfterFly
- 3. Overworld_ResetStateAfterTeleport
- 4. Overworld_ResetStateAfterDigEscRope
- 5. Overworld_ResetStateAfterWhiteOut
- 6. sub_805308C
- 7. ResetGameStats
- 8. IncrementGameStat
- 9. GetGameStat
- 10. SetGameStat
- 11. LoadObjEventTemplatesFromHeader
- 12. LoadSaveblockObjEventScripts
- 13. Overworld_SetObjEventTemplateCoords
- 14. Overworld_SetObjEventTemplateMovementType
- 15. mapdata_load_assets_to_gpu_and_full_redraw
- 16. ApplyCurrentWarp
- 17. SetWarpData
- 18. IsDummyWarp
- 19. LoadCurrentMapData
- 20. LoadSaveblockMapHeader
- 21. SetPlayerCoordsFromWarp
- 22. WarpIntoMap
- 23. Overworld_SetWarpDestination
- 24. warp1_set_2
- 25. saved_warp2_set
- 26. saved_warp2_set_2
- 27. copy_saved_warp2_bank_and_enter_x_to_warp1
- 28. sub_8053538
- 29. Overworld_SetWarpDestToLastHealLoc
- 30. Overworld_SetHealLocationWarp
- 31. sub_80535C4
- 32. sub_805363C
- 33. sub_8053678
- 34. SetFixedDiveWarp
- 35. SetFixedDiveWarpAsDestination
- 36. SetFixedHoleWarp
- 37. SetFixedHoleWarpAsDestination
- 38. sub_8053778
- 39. unref_sub_8053790
- 40. sub_80537CC
- 41. gpu_sync_bg_hide
- 42. SetDiveWarp
- 43. SetDiveWarpEmerge
- 44. SetDiveWarpDive
- 45. LoadMapFromCameraTransition
- 46. sub_8053994
- 47. ResetInitialPlayerAvatarState
- 48. StoreInitialPlayerAvatarState
- 49. GetAdjustedInitialTransitionFlags
- 50. GetAdjustedInitialDirection
- 51. GetCenterScreenMetatileBehavior
- 52. Overworld_IsBikingAllowed
- 53. SetDefaultFlashLevel
- 54. Overworld_SetFlashLevel
- 55. Overworld_GetFlashLevel
- 56. sub_8053D14
- 57. GetLocationMusic
- 58. GetCurrLocationDefaultMusic
- 59. GetWarpDestinationMusic
- 60. Overworld_ResetMapMusic
- 61. Overworld_PlaySpecialMapMusic
- 62. Overworld_SetSavedMusic
- 63. Overworld_ClearSavedMusic
- 64. sub_8053F0C
- 65. Overworld_ChangeMusicToDefault
- 66. Overworld_ChangeMusicTo
- 67. GetMapMusicFadeoutSpeed
- 68. TryFadeOutOldMapMusic
- 69. BGMusicStopped
- 70. Overworld_FadeOutMapMusic
- 71. PlayAmbientCry
- 72. UpdateAmbientCry
- 73. ChooseAmbientCrySpecies
- 74. GetMapTypeByGroupAndId
- 75. GetMapTypeByWarpData
- 76. Overworld_GetMapTypeOfSaveblockLocation
- 77. GetLastUsedWarpMapType
- 78. is_map_type_1_2_3_5_or_6
- 79. Overworld_MapTypeAllowsTeleportAndFly
- 80. Overworld_MapTypeIsIndoors
- 81. unref_sub_8054260
- 82. sav1_map_get_name
- 83. sav1_map_get_battletype
- 84. CB2_InitTestMenu
- 85. debug_sub_80589D8
- 86. debug_sub_80589F4
- 87. debug_sub_8058A50
- 88. ResetSafariZoneFlag_
- 89. is_c1_link_related_active
- 90. DoCB1_Overworld
- 91. CB1_Overworld
- 92. OverworldBasic
- 93. CB2_OverworldBasic
- 94. CB2_Overworld
- 95. SetMainCallback1
- 96. sub_80543DC
- 97. RunFieldCallback
- 98. CB2_NewGame
- 99. debug_sub_8058C00
- 100. CB2_WhiteOut
- 101. CB2_LoadMap
- 102. CB2_LoadMap2
- 103. sub_8054534
- 104. sub_8054588
- 105. c2_80567AC
- 106. CB2_ReturnToField
- 107. CB2_ReturnToFieldLocal
- 108. CB2_ReturnToFieldLink
- 109. sub_805465C
- 110. c2_exit_to_overworld_1_sub_8080DEC
- 111. sub_80546B8
- 112. CB2_ReturnToFieldContinueScriptPlayMapMusic
- 113. sub_80546F0
- 114. sub_805470C
- 115. CB2_ContinueSavedGame
- 116. FieldClearVBlankHBlankCallbacks
- 117. SetFieldVBlankCallback
- 118. VBlankCB_Field
- 119. InitCurrentFlashLevelScanlineEffect
- 120. sub_805483C
- 121. sub_805493C
- 122. sub_8054A4C
- 123. sub_8054A9C
- 124. do_load_map_stuff_loop
- 125. sub_8054BA8
- 126. sub_8054C2C
- 127. InitOverworldGraphicsRegisters
- 128. sub_8054D4C
- 129. sub_8054D90
- 130. mli4_mapscripts_and_other
- 131. sub_8054E20
- 132. sub_8054E34
- 133. sub_8054E60
- 134. sub_8054E7C
- 135. sub_8054E98
- 136. sub_8054EC8
- 137. sub_8054F48
- 138. sub_8054F70
- 139. sub_8054F88
- 140. sub_8054FC0
- 141. sub_8054FF8
- 142. sub_8055218
- 143. sub_8055280
- 144. sub_80552B0
- 145. sub_805530C
- 146. sub_8055340
- 147. sub_8055354
- 148. sub_8055390
- 149. sub_80553E0
- 150. sub_80553E4
- 151. sub_8055408
- 152. sub_8055438
- 153. sub_8055468
- 154. sub_805546C
- 155. sub_80554A4
- 156. sub_80554B8
- 157. sub_80554BC
- 158. sub_80554E4
- 159. sub_80554F8
- 160. unref_sub_8055568
- 161. sub_8055574
- 162. sub_8055588
- 163. sub_805559C
- 164. sub_80555B0
- 165. sub_8055618
- 166. sub_8055630
- 167. sub_8055660
- 168. sub_8055758
- 169. sub_80557E8
- 170. sub_80557F4
- 171. sub_8055808
- 172. sub_8055824
- 173. sub_8055840
- 174. sub_805585C
- 175. sub_8055870
- 176. sub_80558AC
- 177. sub_8055910
- 178. sub_8055940
- 179. ClearLinkPlayerObjectEvent
- 180. ClearLinkPlayerObjectEvents
- 181. ClearObjectEvent
- 182. SpawnLinkPlayerObjectEvent
- 183. InitLinkPlayerObjectEventPos
- 184. unref_sub_8055A6C
- 185. unref_sub_8055A9C
- 186. sub_8055AE8
- 187. sub_8055B08
- 188. sub_8055B30
- 189. sub_8055B50
- 190. unref_sub_8055B74
- 191. GetLinkPlayerIdAt
- 192. sub_8055BFC
- 193. sub_8055C68
- 194. sub_8055C88
- 195. sub_8055C8C
- 196. sub_8055CAC
- 197. sub_8055CB0
- 198. sub_8055D18
- 199. sub_8055D30
- 200. sub_8055D38
- 201. npc_something3
- 202. LinkPlayerDetectCollision
- 203. CreateLinkPlayerSprite
- 204. SpriteCB_LinkPlayer

## Entry / White Out

`DoWhiteOut` is binary-proven at:

- Retail **0x0805329C**
- Debug **0x080575AC**

It:

1. runs the White Out event script;
2. halves SaveBlock1 money;
3. heals the player's party;
4. clears transient overworld movement/mode state;
5. targets the last heal location;
6. warps into that map.

The Fly, Teleport, Dig/Escape Rope and White Out reset helpers all clear the transient cycling/cruise/Safari/Strength/Flash state appropriate to a field transition.

## Game statistics

Game statistics are stored in SaveBlock1 and are indexed through a byte-sized statistic ID.

`IncrementGameStat` saturates each statistic at:

**0xFFFFFF**

rather than wrapping.

Invalid indices are ignored by the setter/incrementer and read as zero by the getter.

## Saved object-event templates

The overworld keeps **64 saved ObjectEventTemplate slots**.

The module can:

- clear/copy current map object templates into SaveBlock1;
- restore script pointers from the current map header;
- update a saved template's coordinates;
- update its movement type.

This 64-template save representation is separate from the **16 live ObjectEvent records** serialized by `load_save`. The two capacities must not be conflated.

## Map header / layout ownership

The overworld module owns the high-level map identity and warp transition:

- `gSaveBlock1.location` identifies current map/warp;
- `gWarpDestination` identifies destination;
- `gLastUsedWarp` preserves the source;
- `gFixedDiveWarp` and `gFixedHoleWarp` are special transition targets;
- `gMapHeader` is loaded from map group + map number;
- SaveBlock1 stores the selected map-layout ID.

`WarpIntoMap` performs the core chain:

`ApplyCurrentWarp -> LoadCurrentMapData -> SetPlayerCoordsFromWarp`

Player coordinates come from the destination warp event when valid, otherwise explicit warp coordinates, otherwise the map-layout center.

## Warp model

A `WarpData` destination carries:

- map group;
- map number;
- warp ID;
- X;
- Y.

The all--1 tuple is treated as the dummy/invalid warp.

Separate SaveBlock1 warp records are used for dynamic warp, last heal, warp1 and warp4-style transition bookkeeping.

Dive/emerge transitions can use map connections or the fixed dive warp fallback.

## Map loading pipeline

The field-loading callbacks are split into staged state machines rather than one blocking load.

The main staged loader performs a sequence including:

- clear field VBlank/HBlank callbacks;
- initialize scripts/control;
- map/warp setup;
- object/event initialization;
- map scripts;
- flash scanline effect;
- graphics registers and text window;
- camera positioning;
- primary tileset copy;
- secondary tileset copy;
- palette load;
- full map draw;
- tileset post-load functions;
- field callback.

The staged design is useful for preserving exact GBA behavior while exposing a higher-level modern map-loading transaction.

## New game / continue / return-to-field

`CB2_NewGame` calls the already mapped `NewGameInitData`, starts the play-time counter, initializes scripts and loads the truck map before installing the normal overworld callbacks.

`CB2_ContinueSavedGame`:

- stops field callbacks/music;
- reloads the saved map header and object-event scripts;
- runs time-based events;
- initializes map state from the saved game;
- restarts play-time counting;
- handles the specialSaveWarp recovery path from SaveBlock2;
- otherwise returns to the normal field.

The Debug build adds an R-button path that marks the Debug working flag during continue.

## Music and ambient sound

Map music is selected from map header plus special cases such as legendary/weather locations, Surf and Underwater.

The special saved-music field in SaveBlock1 can override ordinary location music.

Ambient cries are probabilistic and can be restricted to water/underwater metatile behavior, tying overworld audio to fieldmap behavior queries.

## Map type policy

The module owns high-level map-type decisions including:

- whether Teleport/Fly are allowed;
- indoor/outdoor classification;
- transition music behavior;
- biking restrictions;
- current/destination map type lookup.

Modern map metadata should expose these as named policies rather than relying on the original numeric map-type cases, while the legacy adapter preserves exact Ruby behavior.

## Link-player overworld

The overworld supports exactly **four LinkPlayerObjectEvent records**.

The link-player collision check scans the **16 live ObjectEvent slots** and falls back to map-grid collision.

Link player sprites, positions, movement modes and visibility are therefore layered on the same object-event and fieldmap collision system as local overworld entities.

## Debug-only overworld tooling

The Debug profile includes:

- a test-menu graphics/task bootstrap;
- Debug palette/task callbacks;
- a Debug field-entry callback that can choose truck-sequence versus normal field callback based on R;
- a saved-game R-button path setting the Debug working flag.

These are kept as an explicit Debug profile rather than being promoted into Retail German behavior.

## Next module

`fieldmap` starts at:

- Retail **0x080562D0**
- Debug **0x0805A7B8**
- accumulated delta **+0x44E8**

The first function is `GetMapHeaderFromConnection`. Its German binary fingerprint loads `mapGroup` and `mapNum` from connection offsets +8/+9 and calls the overworld map-header lookup. `InitMap` follows immediately.
