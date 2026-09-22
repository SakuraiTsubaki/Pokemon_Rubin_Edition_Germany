#!/usr/bin/env python3
import argparse
import hashlib
from pathlib import Path

RETAIL = (0x6A668, 0x6A7C0)
DEBUG = (0x6ED44, 0x6EE9C)

RETAIL_SHA256 = "f6a44a7060cc399cfa1c4b8ba180697d7f4a5e0ed52081c21dde417d006ee112"
DEBUG_SHA256 = "366852d55b6dc05ee1b5e64bdcaa07cf5529929790be452720451d038b1c775b"

ENTRY_PREFIX = bytes.fromhex("00 b5 09 48")
NEXT_PREFIX = bytes.fromhex("00 b5 03 1c 0a 4a 2e 20 19 5e 88 00 40 18 c0 00")
FUNCTION_OFFSETS = (0x000, 0x038, 0x068, 0x0CC, 0x124, 0x138)

def sha256(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()

def main() -> None:
    p = argparse.ArgumentParser(description="Verify German Pokemon Ruby clock module")
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

    assert len(r0) == len(r1) == len(dbg) == 0x158
    assert r0 == r1
    assert sha256(r0) == RETAIL_SHA256
    assert sha256(r1) == RETAIL_SHA256
    assert sha256(dbg) == DEBUG_SHA256

    assert DEBUG[0] - RETAIL[0] == 0x46DC
    assert DEBUG[1] - RETAIL[1] == 0x46DC

    assert r0.startswith(ENTRY_PREFIX)
    assert dbg.startswith(ENTRY_PREFIX)
    assert r0[0x28:0x2C] == (0x0835).to_bytes(4, "little")
    assert dbg[0x28:0x2C] == (0x0835).to_bytes(4, "little")
    assert r0[0x34:0x38] == (0x4040).to_bytes(4, "little")
    assert dbg[0x34:0x38] == (0x4040).to_bytes(4, "little")

    for off in FUNCTION_OFFSETS:
        assert r0[off:off + 2] in (
            bytes.fromhex("00 b5"),
            bytes.fromhex("10 b5"),
            bytes.fromhex("70 b5"),
        )
        assert dbg[off:off + 2] == r0[off:off + 2]

    assert rev0[RETAIL[1]:RETAIL[1] + len(NEXT_PREFIX)] == NEXT_PREFIX
    assert rev1[RETAIL[1]:RETAIL[1] + len(NEXT_PREFIX)] == NEXT_PREFIX
    assert debug[DEBUG[1]:DEBUG[1] + len(NEXT_PREFIX)] == NEXT_PREFIX

    print("German clock verification passed")
    print("Retail Rev0/Rev1: 0x0806A668..0x0806A7C0, 0x158 bytes")
    print("Debug:            0x0806ED44..0x0806EE9C, 0x158 bytes")
    print("Accumulated Retail->Debug delta remains +0x46DC")
    print("Next: reset_rtc_screen / SpriteCB_ResetRtcCusor0")

if __name__ == "__main__":
    main()
