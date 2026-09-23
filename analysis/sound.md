# German sound module

The complete `sound` text module has been bounded directly in the supplied German Retail Rev 0, Retail Rev 1 and Debug ROMs.

## Module boundary

| Profile | Start | End exclusive | Size | SHA-256 |
| --- | --- | --- | ---: | --- |
| Retail Rev 0 / Rev 1 | 0x08074F6C | 0x080759E4 | **2,680 bytes (0xA78)** | `5d126e677f92d1b169d5b26172bb83cb000e0899dbae11ea0d41688826fd531f` |
| Debug | 0x0807C1D8 | 0x0807CC50 | **2,680 bytes (0xA78)** | `4c7e9d4d53eadc90f4424f77bf662c1426a9c70371f7aa6991e62d388ec67e30` |

Retail Rev 0 and Rev 1 are byte-identical across the complete module. Debug adds no `sound` text, so the accumulated Retail-to-Debug displacement remains **+0x726C** at entry and exit.

## Entry anchor

The first function is source-correlated as `InitMapMusic`.

Common first 16 bytes:

`00 B5 03 49 00 20 08 70 00 F0 80 F8 01 BC 00 47`

The following literal is the profile-specific `gDisableMusic` byte:

- Retail Rev 0 / Rev 1: **0x03004AFC**
- Debug: **0x03004BD4**

The function clears the disable-music flag and resets the map-music state.

## Map-music state

The German binaries establish the internal map-music state addresses:

| State | Retail | Debug | Literal refs |
| --- | --- | --- | ---: |
| `sCurrentMapMusic` | 0x030006D4 | 0x030006F4 | 11 |
| `sNextMapMusic` | 0x030006D6 | 0x030006F6 | 10 |
| `sMapMusicState` | 0x030006D8 | 0x030006F8 | 12 |
| `sMapMusicFadeInSpeed` | 0x030006D9 | 0x030006F9 | 4 |
| `sFanfareCounter` | 0x030006DA | 0x030006FA | 3 |

Source correlation shows active map-music state values 0, 1, 2, 5, 6 and 7, covering idle, pending play, playing, fade-out stop, fade-out/play and fade-out/fade-in transitions.

## Music player globals

Profile-specific music-player references inside the German module are:

| Music player | Retail | Debug | Literal refs |
| --- | --- | --- | ---: |
| BGM | 0x03007390 | 0x030074A0 | 15 |
| SE1 | 0x030073D0 | 0x030074E0 | 4 |
| SE2 | 0x03007410 | 0x03007520 | 4 |
| SE3 | 0x03007460 | 0x03007570 | 1 |

The Pokemon-cry runtime state is also profile-relocated:

- `gMPlay_PokemonCry`: Retail **Œ‘ÎPÊŠ‹XYÈ
ŠŒŒ‘M
Šˆ8 %ˆ]\˜[™YœÂ‹HÔÚÙ[[ÛÜP‘ÓQXÚÚ[™ĞÛİ[\˜ˆ™]Z[
ŠŒŒ‘ĞL
Š‹XYÈ
Šƒƒ#$dCB¢¢(	BBÆ—FW&Â&Vg0 ¢22fæf&RF&ÆP ¥F†R6÷W&6RÖ6÷'&VÆFVBfæf&RF&ÆR†2¢£"VçG&–W2¢¢ÂV6‚‡Sb6öætçVÒÂSbGW&F–öâ–à ¤&–æ'’FG&W76W3  ¢Ò&WF–Â&Wbò&Wb¢¢£ƒƒ3ƒ“dD2¢ ¢ÒFV'Vs¢¢£ƒƒ43ƒd2¢  ¥F†R6ö×ÆWFRC‚Ö'—FRF&ÆR—2'—FRÖ–FVçF–6Â–âÆÂF‡&VR&öf–ÆW2v—F‚4„Ó#Sc  ¦#Cv“SsƒS&6&cS3ƒSSCCƒc#FV66CS–VSvcCV#v6S3S“#Fc6–6€ ¥F–ÂæBæW‡BÖÖöGVÆRæ6†÷"öÖ—GFVB†W&Rf÷"'&Wf—G’