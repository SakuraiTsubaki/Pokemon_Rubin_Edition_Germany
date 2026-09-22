#!/usr/bin/env python3
import argparse
import hashlib
from pathlib import Path

RETAIL = (0x6B21C, 0x712D0)
DEBUG = (0x6FB44, 0x75C30)

RETAIL_SHA256 = "4e46edf06f57597e5be44b4ea4553baa12d7a5b0539a4ce4e9474d9132f0dd74"
DEBUG_SHA256 = "e9df2862b802125709c828573e1ab75fcaa5d3bb8d248bcd810cab15ecab0015"

ENTRY_RETAIL = bytes.fromhex("70 b5 81 b0 95 f7 52 fb 95 f7 76 fb")
ENTRY_DEBUG = bytes.fromhex("70 b5 81 b0 90 f7 be fe 90 f7 e2 fe")

RETAIL_ONLY_TAIL = (0x712AC, 0x712D0)
RETAIL_ONLY_TAIL_SHA256 = "9409d74a2cc3d04dd0fcd5304d4ec24d7695ffb470360ab3a1509646f727e04d"

NEXT_RETAIL = bytes.fromhex("00 b5 05 48 00 21 01 70 e3 f7 9e f9")
NEXT_DEBUG = bytes.fromhex("00 b5 03 f0 b9 fa 00 f0 b1 f8 01 20 02 bc 08 47")
DEBUG_COMMON_START = 0x75E5C
DEBUG_COMMON_PREFIX = bytes.fromhex("00 b5 05 48 00 21 01 70")

def sha256(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()

def main() -> None:
    p = argparse.ArgumentParser(description="Verify German Pokemon Ruby party_menu module")
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

    assert len(r0) == 0x60B4
    assert len(dbg) == 0x60EC
    assert len(dbg) - len(r0) == 0x38
    assert r0 == r1

    assert sha256(r0) == RETAIL_SHA256
    assert sha256(r1) == RETAIL_SHA256
    assert sha256(dbg) == DEBUG_SHA256

    assert DEBUG[0] - RETAIL[0] == 0x4928
    assert DEBUG[1] - RETAIL[1] == 0x4960

    assert r0.startswith(ENTRY_RETAIL)
    assert dbg.startswith(ENTRY_DEBUG)

    retail_tail = rev0[RETAIL_ONLY_TAIL[0]:RETAIL_ONLY_TAIL[1]]
    assert len(retail_tail) == 0x24
    assert sha256(retail_tail) == RETAIL_ONLY_TAIL_SHA256

    retail_common_size = RETAIL_ONLY_TAIL[0] - RETAIL[0]
    assert retail_common_size == 0x6090
    assert len(dbg) - retail_common_size == 0x5C

    assert rev0[RETAIL[1]:RETAIL[1] + len(NEXT_RETAIL)] == NEXT_RETAIL
    assert rev1[RETAIL[1]:RETAIL[1] + len(NEXT_RETAIL)] == NEXT_RETAIL
    assert debug[DEBUG[1]:DEBUG[1] + len(NEXT_DEBUG)] == NEXT_DEBUG

    assert debug[DEBUG_COMMON_START:DEBUG_COMMON_START + len(DEBUG_COMMON_PREFIX)] == DEBUG_COMMON_PREFIX

    print("German party_menu verification passed")
    print("Retail Rev0/Rev1: 0x0806B21C..0x080712D0, 0x60B4 bytes")
    print("Debug:            0x0806FB44..0x08075C30, 0x60EC bytes")
    print("Net Debug growth: 0x38 = +0x5C internal Debug code - 0x24 Retail-only tail")
    print("Accumulated Retail->Debug delta changes +0x4928 -> +0x4960")
    print("Next: start_menu")

if __name__ == "__main__":
    main()
