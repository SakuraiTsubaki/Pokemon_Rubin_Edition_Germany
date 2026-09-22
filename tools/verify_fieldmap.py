#!/usr/bin/env python3
import argparse
import hashlib
from pathlib import Path

RETAIL = (0x562D0, 0x570DC)
DEBUG = (0x5A7B8, 0x5B5C4)
RETAIL_SHA256 = "437e6883063d29a9c67acba6402374456c7e3da2067129e483fbee6ed4b0b7f5"
DEBUG_SHA256 = "710a595e8e0b1594e27d27812fbc91fd480ecf538041ff855fbb2d5f9139b000"
ENTRY_PREFIX = bytes.fromhex("00 b5 02 7a 41 7a 10 1c")
NEXT_MODULE_ENTRY = bytes.fromhex("01 20 70 47")


def sha256(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def main() -> None:
    parser = argparse.ArgumentParser(description="Verify German Pokemon Ruby fieldmap module")
    parser.add_argument("--rev0", type=Path, required=True)
    parser.add_argument("--rev1", type=Path, required=True)
    parser.add_argument("--debug", type=Path, required=True)
    args = parser.parse_args()

    rev0 = args.rev0.read_bytes()
    rev1 = args.rev1.read_bytes()
    debug = args.debug.read_bytes()

    r0 = rev0[RETAIL[0]:RETAIL[1]]
    r1 = rev1[RETAIL[0]:RETAIL[1]]
    dbg = debug[DEBUG[0]:DEBUG[1]]

    assert RETAIL[1] - RETAIL[0] == 0xE0C
    assert DEBUG[1] - DEBUG[0] == 0xE0C
    assert DEBUG[0] - RETAIL[0] == 0x44E8
    assert DEBUG[1] - RETAIL[1] == 0x44E8

    assert r0 == r1
    assert sha256(r0) == RETAIL_SHA256
    assert sha256(r1) == RETAIL_SHA256
    assert sha256(dbg) == DEBUG_SHA256

    assert r0[:8] == ENTRY_PREFIX
    assert dbg[:8] == ENTRY_PREFIX

    # The next module is metatile_behavior. Its first function is the
    # four-byte Thumb leaf `MetatileBehavior_IsATile`: return TRUE.
    assert rev0[RETAIL[1]:RETAIL[1] + 4] == NEXT_MODULE_ENTRY
    assert rev1[RETAIL[1]:RETAIL[1] + 4] == NEXT_MODULE_ENTRY
    assert debug[DEBUG[1]:DEBUG[1] + 4] == NEXT_MODULE_ENTRY

    print("German fieldmap verification passed")
    print("Retail Rev0/Rev1: 0x080562D0..0x080570DC, 0xE0C bytes")
    print("Debug:             0x0805A7B8..0x0805B5C4, 0xE0C bytes")
    print("Accumulated Retail->Debug delta remains +0x44E8")
    print("Next: metatile_behavior / MetatileBehavior_IsATile")


if __name__ == "__main__":
    main()
