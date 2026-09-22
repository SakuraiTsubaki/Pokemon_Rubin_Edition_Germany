#!/usr/bin/env python3
import argparse
import hashlib
from pathlib import Path

RETAIL = (0x58AF4, 0x5AD90)
DEBUG = (0x5CFDC, 0x5F348)
RETAIL_SHA256 = "222f2eee68b4ca41ba6c9329b2691f18980b045715ba5926f149466f44c4dcfd"
DEBUG_SHA256 = "bb5acc900b4dc33878bceef76755552d5bde8752ac9b8d35e8b65476551858ad"

ENTRY_PREFIX = bytes.fromhex("00 b5 01 1c 2e 20 0a 5e d0 00 80 18 80 00 03 4a 80 18 03 4a")
EMPTY_CALLBACK = bytes.fromhex("00 20 70 47")
EMPTY_CALLBACK_OFFSET = 0x24

DEBUG_COMMON_END = 0x5F2B0
DEBUG_TAIL_END = 0x5F348
DEBUG_TAIL_SHA256 = "6cafd04d4c299ff17733bd4fa9083da2c28aaafecc7056a400f840d5e15193fd"
DEBUG_FUNC1 = (0x5F2B0, 0x5F2DC)
DEBUG_FUNC2 = (0x5F2DC, 0x5F348)
DEBUG_FUNC1_SHA256 = "f617e6afde734d0fe7db07543484fc9d95d658a6bb3da8505410ec3bfd4888bf"
DEBUG_FUNC2_SHA256 = "4e34a8b6306b1e55f192bf62a9c0be141b1c11b6c4a3afe352bb6b927e8d04e2"

NEXT_RETAIL = (0x5AD90, 0x5ADB0)
NEXT_DEBUG = (0x5F348, 0x5F368)
NEXT_PREFIX = bytes.fromhex("10 b5 04 1c 00 21 24 22")
NEXT_SUFFIX = bytes.fromhex("ff 20 20 72 01 20 40 42 60 72 a0 72 20 77 10 bc 01 bc 00 47")

def sha256(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()

def verify_next_function(data: bytes, bounds: tuple[int, int]) -> None:
    func = data[bounds[0]:bounds[1]]
    assert len(func) == 0x20
    assert func.startswith(NEXT_PREFIX)
    assert func.endswith(NEXT_SUFFIX)

def main() -> None:
    parser = argparse.ArgumentParser(description="Verify German Pokemon Ruby field_player_avatar module")
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

    assert RETAIL[1] - RETAIL[0] == 0x229C
    assert DEBUG[1] - DEBUG[0] == 0x236C
    assert len(dbg) - len(r0) == 0xD0
    assert r0 == r1
    assert sha256(r0) == RETAIL_SHA256
    assert sha256(r1) == RETAIL_SHA256
    assert sha256(dbg) == DEBUG_SHA256

    assert DEBUG[0] - RETAIL[0] == 0x44E8
    assert DEBUG[1] - RETAIL[1] == 0x45B8

    assert DEBUG_COMMON_END - DEBUG[0] == 0x22D4
    assert (DEBUG_COMMON_END - DEBUG[0]) - (RETAIL[1] - RETAIL[0]) == 0x38

    assert DEBUG_TAIL_END - DEBUG_COMMON_END == 0x98
    tail = debug[DEBUG_COMMON_END:DEBUG_TAIL_END]
    assert sha256(tail) == DEBUG_TAIL_SHA256
    assert DEBUG_FUNC1[1] - DEBUG_FUNC1[0] == 0x2C
    assert DEBUG_FUNC2[1] - DEBUG_FUNC2[0] == 0x6C
    assert sha256(debug[DEBUG_FUNC1[0]:DEBUG_FUNC1[1]]) == DEBUG_FUNC1_SHA256
    assert sha256(debug[DEBUG_FUNC2[0]:DEBUG_FUNC2[1]]) == DEBUG_FUNC2_SHA256

    assert r0.startswith(ENTRY_PREFIX)
    assert dbg.startswith(ENTRY_PREFIX)
    assert r0[EMPTY_CALLBACK_OFFSET:EMPTY_CALLBACK_OFFSET + 4] == EMPTY_CALLBACK
    assert dbg[EMPTY_CALLBACK_OFFSET:EMPTY_CALLBACK_OFFSET + 4] == EMPTY_CALLBACK

    verify_next_function(rev0, NEXT_RETAIL)
    verify_next_function(rev1, NEXT_RETAIL)
    verify_next_function(debug, NEXT_DEBUG)

    print("German field_player_avatar verification passed")
    print("Retail Rev0/Rev1: 0x08058AF4..0x0805AD90, 0x229C bytes")
    print("Debug:            0x0805CFDC..0x0805F348, 0x236C bytes")
    print("Debug growth: 0xD0 = 0x38 internal conditional growth + 0x98 Debug-only tail")
    print("Accumulated Retail->Debug delta changes +0x44E8 -> +0x45B8")
    print("Next: event_object_movement / ClearObjectEvent")

if __name__ == "__main__":
    main()
