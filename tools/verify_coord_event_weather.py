#!/usr/bin/env python3
import argparse
import hashlib
from pathlib import Path

RETAIL = (0x696AC, 0x6977C)
DEBUG = (0x6DD88, 0x6DE58)
RETAIL_SHA256 = "1feb1b8af8896d001a06e5ee56afc0c1241e27be57db500b24719aacb1a097ac"
DEBUG_SHA256 = "67d18d6dff683b8e4a2720e65b6a8157ade01b3deaaed66013778f292b26ac3b"

WEATHER_IDS = [1,2,3,4,5,6,9,7,8,11,12,20,21]
NEXT_PREFIX = bytes.fromhex(
    "00 b5 00 06 00 0e 07 4a 81 00 09 18 c9 00 89 18 "
    "08 22 89 5e 04 4a 89 00 89 18 09 68"
)

def sha256(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()

def verify_wrappers(data: bytes, start: int) -> None:
    for i, weather_id in enumerate(WEATHER_IDS):
        fn = data[start + i * 12:start + (i + 1) * 12]
        assert len(fn) == 12
        assert fn[0:2] == bytes.fromhex("00 b5")
        assert fn[2:4] == bytes((weather_id, 0x20))
        assert fn[8:12] == bytes.fromhex("01 bc 00 47")

def main() -> None:
    p = argparse.ArgumentParser(description="Verify German Pokemon Ruby coord_event_weather module")
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

    assert len(r0) == len(r1) == len(dbg) == 0xD0
    assert r0 == r1
    assert sha256(r0) == RETAIL_SHA256
    assert sha256(r1) == RETAIL_SHA256
    assert sha256(dbg) == DEBUG_SHA256
    assert DEBUG[0] - RETAIL[0] == 0x46DC
    assert DEBUG[1] - RETAIL[1] == 0x46DC

    verify_wrappers(rev0, RETAIL[0])
    verify_wrappers(rev1, RETAIL[0])
    verify_wrappers(debug, DEBUG[0])

    assert rev0[RETAIL[1]:RETAIL[1] + len(NEXT_PREFIX)] == NEXT_PREFIX
    assert rev1[RETAIL[1]:RETAIL[1] + len(NEXT_PREFIX)] == NEXT_PREFIX
    assert debug[DEBUG[1]:DEBUG[1] + len(NEXT_PREFIX)] == NEXT_PREFIX

    print("German coord_event_weather verification passed")
    print("Retail Rev0/Rev1: 0x080696AC..0x0806977C, 0xD0 bytes")
    print("Debug:            0x0806DD88..0x0806DE58, 0xD0 bytes")
    print("Accumulated Retail->Debug delta remains +0x46DC")
    print("Next: field_tasks / Task_RunPerStepCallback")

if __name__ == "__main__":
    main()
