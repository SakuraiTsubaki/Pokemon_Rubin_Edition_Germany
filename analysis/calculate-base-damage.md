# German CalculateBaseDamage module

The complete `calculate_base_damage` module contains a single large function and is byte-identical between German Retail Rev 0 and Rev 1.

## Boundary

| Profile | Start | End exclusive | Size | SHA-256 |
| --- | --- | --- | ---: | --- |
| Retail Rev 0 / Rev 1 | 0x0803BC00 | 0x0803C51C | 2,332 bytes (0x91C) | 805c2ac86214fd252e5c33331c5b6d2de4b842216a4b150fca390fbf24412288 |
| Debug | 0x0803FD7C | 0x08040698 | 2,332 bytes (0x91C) | 34c128142c4201f5333f913fbbf677f57402b06052501d3abfc45b36e3a80006 |

There is no Debug-only growth. The whole function stays at the inherited delta **+0x417C**.

## Physical/special split

The original Ruby engine chooses Attack/Defense or Special Attack/Special Defense from the **move type**, not from a per-move category:

- physical path: types below `TYPE_MYSTERY`;
- `TYPE_MYSTERY`: zero base damage;
- special path: types above `TYPE_MYSTERY`.

This is one of the largest Gen-4+ modernization boundaries. A Gen-10-ready ruleset needs a move-category field while keeping this type-based path as the legacy Ruby compatibility mode.

## Base formula

Both physical and special branches use the core Generation III shape:

`(((effectiveAttack * movePower * (2*level/5 + 2)) / effectiveDefense) / 50) + 2`

Stat-stage multipliers use the original 13-entry -6..+6 ratio table. Critical hits selectively ignore unfavorable attacker stages and favorable defender stages.

## Physical modifiers

The physical branch includes:

- Huge Power / Pure Power;
- badge Attack/Defense boosts;
- Choice Band;
- Thick Club;
- Hustle;
- Guts;
- Marvel Scale on defender;
- Explosion defense-halving;
- burn Attack penalty unless Guts;
- Reflect;
- spread-move Double Battle reduction.

Reflect uses half damage in singles and **2/3 damage** when two allied battlers are alive in a Double Battle.

## Special modifiers

The special branch includes:

- Soul Dew;
- Deep Sea Tooth / Scale;
- Light Ball;
- Plus / Minus;
- starter low-HP abilities Overgrow / Blaze / Torrent / Swarm through move-power modification;
- Light Screen;
- spread-move Double Battle reduction;
- rain and sun Fire/Water modifiers;
- SolarBeam penalty outside sun under rain/sand/hail;
- Flash Fire;
- Cloud Nine / Air Lock weather suppression.

Light Screen mirrors Reflect: half damage normally and 2/3 in the qualifying Double Battle case.

## Held-item type boosts

The function iterates a fixed table of **17 type-boosting held-item effects** and applies the item's parameter to Attack or Special Attack according to the original type-based physical/special classification.

## Badge boosts

Outside Link / Battle Tower / e-Reader Trainer battles, qualifying player-side trainer battles can receive the original 10% badge stat boosts for Attack, Defense, Special Attack and Special Defense.

This battle-only hidden stat behavior should remain restricted to the Ruby legacy ruleset.

## Data-width implications

- move argument: 32-bit parameter, but move IDs come from the existing 16-bit move namespace;
- side status: 16-bit;
- power override: 16-bit;
- type override: byte-sized, masked with `0x3F`;
- stat values: 16-bit fields promoted into wider arithmetic;
- final damage: signed 32-bit.

## Next module

`pokemon_2` begins with `CountAliveMons` at:

- Retail **0x0803C51C**
- Debug **0x08040698**
- delta **+0x417C**.

The boundary is visible as the next Thumb function prologue immediately after the return from `CalculateBaseDamage`.
