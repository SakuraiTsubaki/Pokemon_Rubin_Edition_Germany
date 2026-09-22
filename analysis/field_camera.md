# German field_camera module

The complete `field_camera` text module has been bounded directly in the supplied German Retail Rev 0, Retail Rev 1 and Debug ROMs.

## Module boundary

| Profile | Start | End exclusive | Size | SHA-256 |
| --- | --- | --- | ---: | --- |
| Retail Rev 0 / Rev 1 | 0x08057CFC | 0x080586B8 | **2,492 bytes (0x9BC)** | bb4fb3177a5165fad0cb6273029a5a6edf81c09cb8d753b4a4f4c70e8cd05461 |
| Debug | 0x0805C1E4 | 0x0805CBA0 | **2,492 bytes (0x9BC)** | 7656d3f28a00bd04749b5ea9c6cc6830c660b623de256a7a23e83d085b63daf2 |

Retail Rev 0 and Rev 1 are byte-identical across the entire module. Debug adds no `field_camera` code; the accumulated Retail-to-Debug displacement remains **+0x44E8** at both module entry and exit.

The different Retail / Debug SHA-256 values are caused by relocated references and branch displacements, not an extra Debug camera routine.

## Entry anchor

The module begins with the five-byte camera-offset initializer. The first 16 bytes are identical in all three German profiles:

`00 21 81 70 C1 70 01 70 41 70 01 21 01 71 70 47`

This clears the pixel/tile offset bytes, sets the copy-to-VRAM flag, and returns.

The source-correlated `FieldCameraOffset` runtime state consists of:

- X pixel offset
- Y pixel offset
- X tile offset
- Y tile offset
- copy-BG-to-VRAM flag

Historical function names are used only as semantic labels; any addresses embedded in names such as `sub_805xxxx` are not German addresses.

## Tilemap geometry

The camera renderer uses wrapped **32 x 32 tile** background maps. A field metatile is 2 x 2 BG tiles, so a full camera draw walks a **16 x 16 metatile** window.

Confirmed runtime constants used by the German module include:

- BG tilemap width/height: 32 tiles
- visible metatile width/height: 16 metatiles
- metatile tile footprint: 2 x 2 tiles
- tiles per metatile definition: 8 `u16` entries
- BG tilemap buffer transfer size: `0x800` bytes
- normal-layer BG3 fill tile: `0x3014`

`move_tilemap_camera_to_upper_left_corner` clears the BG1/BG2 tilemap buffers and fills BG3 with `0x3014`, then marks the map dirty for VRAM transfer.

## VRAM transfer

When the copy flag is set, the field camera copies the three 0x800-byte tilemap buffers to:

- BG1 map: VRAM + `0xE800`
- BG2 map: VRAM + `0xE000`
- BG3 map: VRAM + `0xF000`

The three destination literals are present inside the German Retail module at ROM offsets corresponding to `0x08057E44`, `0x08057E4C` and `0x08057E50`.

The camera also writes the horizontal/vertical scroll registers for BG1, BG2 and BG3 from the same pixel offsets and pan values, keeping the field layers synchronized.

## Whole-map and slice redraw

`DrawWholeMapView` renders the camera window by stepping through the 32 x 32 BG tilemap in increments of two tiles. Each step resolves one field metatile through `fieldmap`.

Camera tile movement does not redraw the entire map. The runtime redraws only the newly exposed north, south, east and/or west slices, then sets the VRAM-copy flag.

This is important for the GBA map compatibility layer: the backup map grid from `fieldmap` supplies metatile/collision/elevation state, while `field_camera` projects the currently visible 16 x 16 metatile region into the three hardware BG tilemaps.

## Metatile rendering layers

Each metatile resolves to eight tilemap entries: four bottom-layer tiles followed by four top-layer tiles. The layer type from `fieldmap` controls how those halves are placed onto BG1/BG2/BG3.

The source-correlated rendering policy is:

- layer type 2: bottom -> BG3, transparent -> BG2, top -> BG1
- layer type 1: bottom -> BG3, top -> BG2, transparent -> BG1
- layer type 0: `0x3014` fill -> BG3, bottom -> BG2, top -> BG1

Door animation has a dedicated draw path that can supply an explicit eight-entry metatile array while still using this same camera/tilemap projection.

## Camera tracking

The module owns the field-camera tracking state used by the overworld:

- callback pointer
- tracked sprite ID
- X/Y movement speed
- X/Y current movement offset

The camera object follows movement from the tracked sprite, moves the world camera at metatile boundaries, updates object events and rotating-gate state, resets berry-tree sparkle state, advances wrapped tilemap offsets, redraws exposed slices, and accumulates pixel offsets.

The pan layer is separate from map movement. A panning callback can adjust horizontal/vertical pan while `UpdateCameraPanning` converts the result into global sprite coordinate offsets.

## Source-correlated function inventory

The connected reference source contains 28 functions in this module. The German ROM is the address/boundary authority; these names are retained only to describe behavior:

1. `move_tilemap_camera_to_upper_left_corner_`
2. `tilemap_move_something`
3. `coords8_add`
4. `move_tilemap_camera_to_upper_left_corner`
5. `sub_8057A58`
6. `sub_8057B14`
7. `DrawWholeMapView`
8. `DrawWholeMapViewInternal`
9. `RedrawMapSlicesForCameraUpdate`
10. `RedrawMapSliceNorth`
11. `RedrawMapSliceSouth`
12. `RedrawMapSliceEast`
13. `RedrawMapSliceWest`
14. `CurrentMapDrawMetatileAt`
15. `DrawDoorMetatileAt`
16. `DrawMetatileAt`
17. `DrawMetatile`
18. `MapPosToBgTilemapOffset`
19. `CameraUpdateCallback`
20. `ResetCameraUpdateInfo`
21. `InitCameraUpdateCallback`
22. `CameraUpdate`
23. `MoveCameraAndRedrawMap`
24. `SetCameraPanningCallback`
25. `SetCameraPanning`
26. `InstallCameraPanAheadCallback`
27. `UpdateCameraPanning`
28. `CameraPanningCB_PanAhead`

## Tail and next-module anchor

The final camera-panning routine ends exactly at the module end-exclusive address.

`field_door` begins immediately after it:

- Retail: **0x080586B8**
- Debug: **0x0805CBA0**
- accumulated delta: **+0x44E8**

The first `field_door` routine is the door-tile VRAM copy helper. Its German entry bytes begin:

- Retail: `00 B5 03 49 40 22 95 F1 49 F8 01 BC 00 47`
- Debug: `00 B5 03 49 40 22 A9 F1 7F FC 01 BC 00 47`

The profile-specific branch displacement differs, but both functions use the literal `0x06007F00` immediately following the code. This independently anchors the `field_camera` end and the `field_door` start in the German binaries.
