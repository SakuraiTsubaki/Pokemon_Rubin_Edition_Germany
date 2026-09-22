# German field_message_box module

The complete `field_message_box` text module has been bounded directly in the supplied German Retail Rev 0, Retail Rev 1 and Debug ROMs.

## Module boundary

| Profile | Start | End exclusive | Size | SHA-256 |
| --- | --- | --- | ---: | --- |
| Retail Rev 0 / Rev 1 | 0x08064DB4 | 0x08065000 | **588 bytes (0x24C)** | `8378e13d405471aebddbb2b6dfcff3c3d7ef1c76f1bf450bc8704384332f2e8a` |
| Debug | 0x080693B4 | 0x08069600 | **588 bytes (0x24C)** | `a342e8f71cccb346e8060b53addd3ff4bfb2ab0d3ab758b7feec746c5dc4648b` |

Retail Rev 0 and Rev 1 are byte-identical across the entire module.

Debug adds no `field_message_box` text. The accumulated Retail-to-Debug displacement remains **+0x4600** at both entry and exit. The Retail/Debug module hashes differ only because profile-specific code/data references are relocated.

## Entry anchor

The first function is source-correlated as `InitFieldMessageBox`. The first 16 bytes are identical in all three German profiles:

`00 B5 06 49 00 20 08 70 05 48 00 88 00 F0 A2 FB`

The function sets the message-box mode to hidden, reads the dialogue-frame base tile value, and initializes the field message window.

## Runtime state

The one-byte message-box mode is stored at the same IWRAM address in all profiles:

- `sMessageBoxMode`: **0x030005A8**

The complete module contains **11** literal references to this address in both Retail and Debug.

The EWRAM `Window` object is profile-relocated:

- Retail Rev 0 / Rev 1 `gFieldMessageBoxWindow`: **0x0202E87C**
- Debug `gFieldMessageBoxWindow`: **0x0202EB20**

Each complete module contains **9** literal references to its profile-specific window address.

## Message-box modes

Source correlation gives four mode values:

- 0: hidden
- 1: unused
- 2: normal
- 3: auto-scroll

The task state machine waits for frame setup and text completion, then resets the mode to hidden and destroys itself.

## Runtime path

The module contains **14 explicit source-correlated functions**:

1. `InitFieldMessageBox`
2. `Task_FieldMessageBox`
3. `CreateFieldMessageBoxTask`
4. `DestroyFieldMessageBoxTask`
5. `ShowFieldMessage`
6. `ShowFieldAutoScrollMessage`
7. `unref_sub_8064BB8`
8. `unref_sub_8064BD0`
9. `PrintFieldMessage`
10. `PrintFieldMessageFromStringVar4`
11. `HideFieldMessageBox`
12. `GetFieldMessageBoxMode`
13. `IsFieldMessageBoxHidden`
14. `unref_sub_8064CA0`

Historical numeric labels are semantic source names only; the German ROM establishes all addresses.

Normal and auto-scroll display paths share the same field message window and task. Text is expanded into the string variable buffer where required, printed into the field window, and the field-message task manages dialogue-frame drawing and completion.

## Next-module anchor

`event_object_lock` starts immediately afterward:

- Retail Rev 0 / Rev 1: **0x08065000**
- Debug: **0x08069600**
- accumulated delta: **+0x4600**

Its first function is source-correlated as `walkrun_is_standing_still`. It checks `gPlayerAvatar.tileTransitionState` and returns false only while a tile transition is active.

Stable German prefix:

`00 B5 03 48 C0 78 01 28 04 D0 01 20 03 E0`

The embedded `gPlayerAvatar` address is profile-specific:

- Retail: **0x0202E858**
- Debug: **0x0202EAFC**

Stable suffix after that literal:

`00 20 02 BC 08 47`

This independently anchors the end of `field_message_box` and the start of `event_object_lock`.
