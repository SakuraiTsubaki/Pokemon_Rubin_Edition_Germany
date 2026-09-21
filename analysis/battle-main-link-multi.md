# German battle_main link/multi and pre-debug slice

This slice continues immediately after the first battle_main initialization block.

## Exact common slice

| Profile | Start | End exclusive | Size | SHA-256 |
| --- | --- | --- | ---: | --- |
| Retail Rev 0 / Rev 1 | 0x0800F200 | 0x0801041C | 4,636 bytes | 6c564beca2daeb1b71704d16c159a71520419be68c11695e6b08de8320b785d7 |
| Debug | 0x0800F4C0 | 0x08010800 | 4,928 bytes | 5f60c59e24fd5de5f02b3e431b6f47be3b114693de098cfca3072f8f38f3c44e |

Retail Rev 0 and Rev 1 are byte-identical over the complete slice.

## Function map

| Function | Retail | Debug | Retail bytes | Debug bytes | Extra Debug | Delta |
| --- | --- | --- | ---: | ---: | ---: | ---: |
| PrepareOwnMultiPartnerBuffer | 0x0800F200 | 0x0800F4C0 | 216 | 216 | 0 | +0x2C0 |
| sub_800F104 | 0x0800F2D8 | 0x0800F598 | 404 | 452 | 48 | +0x2C0 |
| CB2_HandleStartMultiBattle | 0x0800F46C | 0x0800F75C | 1392 | 1436 | 44 | +0x2F0 |
| BattleMainCB2 | 0x0800F9DC | 0x0800FCF8 | 48 | 248 | 200 | +0x31C |
| sub_800F828 | 0x0800FA0C | 0x0800FDF0 | 16 | 16 | 0 | +0x3E4 |
| sub_800F838 | 0x0800FA1C | 0x0800FE00 | 160 | 160 | 0 | +0x3E4 |
| CreateNPCTrainerParty | 0x0800FABC | 0x0800FEA0 | 1004 | 1004 | 0 | +0x3E4 |
| sub_800FCD4 | 0x0800FEA8 | 0x0801028C | 40 | 40 | 0 | +0x3E4 |
| sub_800FCFC | 0x0800FED0 | 0x080102B4 | 176 | 176 | 0 | +0x3E4 |
| nullsub_36 | 0x0800FF80 | 0x08010364 | 4 | 4 | 0 | +0x3E4 |
| sub_800FDB0 | 0x0800FF84 | 0x08010368 | 112 | 112 | 0 | +0x3E4 |
| sub_800FE20 | 0x0800FFF4 | 0x080103D8 | 32 | 32 | 0 | +0x3E4 |
| sub_800FE40 | 0x08010014 | 0x080103F8 | 468 | 468 | 0 | +0x3E4 |
| c2_8011A1C | 0x080101E8 | 0x080105CC | 420 | 420 | 0 | +0x3E4 |
| sub_80101B8 | 0x0801038C | 0x08010770 | 28 | 28 | 0 | +0x3E4 |
| c2_081284E0 | 0x080103A8 | 0x0801078C | 116 | 116 | 0 | +0x3E4 |

## Debug growth inside common battle flow

Three common functions contain Debug-only logic.

### sub_800F104

Debug adds **48 bytes**.

The added branch can force all four link-player IDs and link types into a deterministic Debug test layout before multi-battle party exchange.

Accumulated Debug displacement:

- before: +0x2C0
- after: **+0x2F0**

### CB2_HandleStartMultiBattle

Debug adds **44 bytes**.

It contains the equivalent four-player link test setup in the actual multi-battle startup path.

Accumulated displacement:

- before: +0x2F0
- after: **+0x31C**

### BattleMainCB2

Retail is only 48 bytes, while Debug is 248 bytes.

Debug adds **200 bytes (0xC8)** including:

- an R+SELECT battle-abort/test shortcut;
- forced battle outcome/result handling;
- restoration of pre-battle callback state;
- Debug-only link/battle status rendering calls.

Accumulated displacement:

- before: +0x31C
- after: **+0x3E4**

Every remaining common function through c2_081284E0 has the same code size in Retail and Debug.

## Multi-battle fixed-format findings

The original code hard-codes several capacities:

- four link players;
- three Pokemon summaries per multi-battle participant;
- party reconstruction into six-slot player/enemy arrays;
- two-Pokemon and one-Pokemon transfer phases;
- two-bit health/status representation for six slots.

CreateNPCTrainerParty also assumes the original trainer-party formats, four moves per Pokemon, and original item/species indexing.

These are recorded as compatibility constraints before any expansion work.

## Divergence boundary

At the end of c2_081284E0:

- Retail next address: **0x0801041C**
- Debug next address: **0x08010800**

Retail proceeds directly to the normal battle core.

Debug instead enters a large Debug-only battle-tool subsystem before eventually rejoining normal battle execution.
