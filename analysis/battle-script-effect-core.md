# German battle script animation, HP and move-effect core

This slice maps opcodes 0x09 through 0x16 together with the large SetMoveEffect helper.

## Exact slice

| Profile | Start | End exclusive | Size | SHA-256 |
| --- | --- | --- | ---: | --- |
| Retail Rev 0 / Rev 1 | 0x0801DAC0 | 0x0801F8EC | 7,724 bytes | c9edbc870e2acc0fb4c6301449f7693bc9058bcfd031262b061b944d8c320219 |
| Debug | 0x08021038 | 0x08022E90 | 7,768 bytes | d8e52c1c94d505e86f098244b379902377f947162e8406df6da98b3b5a714654 |

Retail Rev 0 and Rev 1 are byte-identical throughout this slice.

The only size divergence is opcode 0x15. Entries before atk15 remain at Debug delta +0x3578; atk16 begins at +0x35A4.

## Function map

| Function | Retail | Debug | Retail bytes | Debug bytes | Role |
| --- | --- | --- | ---: | ---: | --- |
| atk09_attackanimation | 0x0801DAC0 | 0x08021038 | 372 | 372 | emit move animation / pause fallback |
| atk0A_waitanimation | 0x0801DC34 | 0x080211AC | 32 | 32 | wait until controller animation work completes |
| atk0B_healthbarupdate | 0x0801DC54 | 0x080211CC | 204 | 204 | emit visual HP-bar delta |
| atk0C_datahpupdate | 0x0801DD20 | 0x08021298 | 1020 | 1020 | apply real HP/substitute damage and synchronize HP |
| atk0D_critmessage | 0x0801E11C | 0x08021694 | 84 | 84 | emit critical-hit message |
| atk0E_effectivenesssound | 0x0801E170 | 0x080216E8 | 208 | 208 | emit super/not-very/normal effectiveness sound |
| atk0F_resultmessage | 0x0801E240 | 0x080217B8 | 432 | 432 | select miss/effectiveness/OHKO/endure/failure message path |
| atk10_printstring | 0x0801E3F0 | 0x08021968 | 64 | 64 | print explicit string ID |
| atk11_printselectionstring | 0x0801E430 | 0x080219A8 | 68 | 68 | print selection string through controller |
| atk12_waitmessage | 0x0801E474 | 0x080219EC | 92 | 92 | wait configured frame count for active message |
| atk13_printfromtable | 0x0801E4D0 | 0x08021A48 | 84 | 84 | print string selected from pointer table / multichooser |
| atk14_printselectionstringfromtable | 0x0801E524 | 0x08021A9C | 100 | 100 | selection-string table variant |
| GetBattlerTurnOrderNum | 0x0801E588 | 0x08021B00 | 56 | 56 | map battler ID to current turn-order index |
| SetMoveEffect | 0x0801E5C0 | 0x08021B38 | 4648 | 4648 | central move-effect/status/stat/item/recoil dispatcher |
| atk15_seteffectwithchance | 0x0801F7E8 | 0x08022D60 | 244 | 288 | secondary-effect chance dispatcher; Debug can force eligible secondary effects |
| atk16_seteffectprimary | 0x0801F8DC | 0x08022E80 | 16 | 16 | apply move effect as primary/certain path |

## Animation and HP application

`atk09_attackanimation` sends the move-animation packet containing the 16-bit move ID, animation turn, move power, signed damage, friendship and the battler DisableStruct. Multi-target moves avoid replaying the full animation after the first target.

`atk0B_healthbarupdate` updates only the visual HP bar. `atk0C_datahpupdate` performs the authoritative HP/substitute mutation and then emits the actual 16-bit HP value through the battle controller.

The HP update path also records:

- total damage taken;
- attacker responsible for that damage;
- physical versus special damage history;
- Substitute HP and fade transition;
- passive-HP-update exclusions;
- damage for Bide/counter-style mechanics.

The original physical/special classification is type-based, not move-category based, which is a major later-generation modernization boundary.

## Result presentation

Opcodes 0x0D through 0x14 separate battle-state mutation from presentation:

- critical message;
- effectiveness sound;
- miss/effectiveness/OHKO/Endure/Focus Band result strings;
- direct string IDs;
- selection strings;
- timed message waits;
- multichooser string tables.

String IDs remain 16-bit in the script commands.

## SetMoveEffect — central Generation III effect dispatcher

`SetMoveEffect` is **4,648 bytes** and is the largest helper in this slice. It centralizes much of Generation III's move-side-effect behavior, including:

- primary status: sleep, poison, toxic, burn, freeze, paralysis;
- Shield Dust / Safeguard / Substitute prevention paths;
- Vital Spirit / Insomnia / Immunity / Own Tempo / Inner Focus / Sticky Hold interactions;
- confusion and flinch;
- Uproar / multi-turn locking;
- Pay Day;
- Tri Attack recursive status selection;
- charging, Wrap/binding and trapping metadata;
- recoil variants;
- stat raises and drops by one or two stages;
- recharge and Rage;
- item stealing and Knock Off;
- escape prevention and Nightmare;
- Rapid Spin cleanup routing;
- paralysis removal;
- Superpower-style Attack/Defense loss;
- Thrash lock/confusion setup;
- Overheat-style Special Attack drop.

This function also writes status changes back through the controller and prepares Synchronize follow-up state.

For Gen-10 expansion this should be treated as a legacy compatibility dispatcher, not as the place to keep appending every modern move effect.

## Debug-only secondary-effect forcing

`atk15_seteffectwithchance` is the first new Debug divergence inside battle_script_commands:

- Retail: 244 bytes
- Debug: 288 bytes
- Debug growth: **44 bytes (0x2C)**.

When Debug control bit 0x04 is enabled, eligible secondary effects can be forced instead of depending on the normal random chance.

After this function the accumulated Debug address delta becomes **+0x35A4**.

## Next opcode

Opcode 0x17 `atk17_seteffectsecondary` begins at Retail **0x0801F8EC** / Debug **0x08022E90**.
