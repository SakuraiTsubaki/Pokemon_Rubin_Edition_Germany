#!/usr/bin/env python3
import argparse
import hashlib
from pathlib import Path

RETAIL = (0x69370, 0x696AC)
DEBUG = (0x6DA4C, 0x6DD88)
RETAIL_SHA256 = "706179f721a1edbf5291b5eb81b5fd905ee51efa61fd26aba2bb18cdcb927cbf"
DEBUG_SHA256 = "22efa675b3a33602a086d92deb5ddebd76c836857819c9873f4b12080558d377"

ENTRY_PREFIX = bytes.fromhex("10 b5 0c 4c 90 22 52 00 20 1c 00 21")
TEMP_RETAIL = (0x0202E8E2).to_bytes(4, "little")
TEMP_DEBUG = (0x0202EB86).to_bytes(4, "little")
WEATHER_IDS = [1,2,3,4,5,6,9,7,8,11,12,20,21]

def sha256(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()

def verify_init(data: bytes, start: int, temp_addr: bytes) -> None:
    assert data[start:start + len(ENTRY_PREFIX)] == ENTRY_PREFIX
    assert data[start + 0x38:start + 0x3C] == temp_addr

def verify_weather_wrappers(data: bytes, start: int) -> None:
    for i, weather_id in enumerate(WEATHER_IDS):
        fn = data[start + i * 12:start + (i + 1) * 12]
        assert len(fn) == 12
        assert fn[0:2] == bytes.fromhex("00 b5")
        assert fn[2:4] == bytes((weather_id, 0x20))
        assert fn[8:12] == bytes.fromhex("01 bc 00 47")

def main() -> None:
    p = argparse.ArgumentParser(description="Verify German Pokemon Ruby event_data module")
    p.add_argument("--rev0", type=Path, required=True)
    p.add_argument("--rev1", type=Path, required=True)
    p.add_argument("--debug", type=Path, required=True)
    a = p.parse_args()

    rev0 = a.rev0.read_bytes()
    rev1 = a.rev1.read_bytes()
    debug = a.debug.read_bytes()

    r0 = rev0[RETAIL[0]:RETAIL[1]]
    r1 = rev1[RETAIL[0]:RETAIL[1]]
    dbg = debug[DEBUG[0]:DEBUG[1]]

    assert len(r0) == len(r1) == len(dbg) == 0x33C
    assert r0 == r1
    assert sha256(r0) == RETAIL_SHA256
    assert sha256(r1) == RETAIL_SHA256
    assert sha256(dbg) == DEBUG_SHA256
    assert DEBUG[0] - RETAIL[0] == 0x46DC
    assert DEBUG[1] - RETAIL[1] == 0x46DC

    verify_init(rev0, RETAIL[0], TEMP_RETAIL)
    verify_init(rev1, RETAIL[0], TEMP_RETAIL)
    verify_init(debug, DEBUG[0], TEMP_DEBUG)

    verify_weather_wrappers(rev0, RETAIL[1])
    verify_weather_wrappers(rev1, RETAIL[1])
    verify_weather_wrappers(debug, DEBUG[1])

    print("German event_data verification passed")
    print("Retail Rev0/Rev1: 0x08069370..0x080696AC, 0x33C bytes")
    print("Debug:            0x0806DA4C..0x0806DD88, 0x33C bytes")
    print("Accumulated Retail->Debug delta remains +0x46DC")
    print("Next: coord_event_weather")

if __name__ == "__main__":
    main()
