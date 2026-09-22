#!/usr/bin/env python3
import argparse
import hashlib
from pathlib import Path

RETAIL = (0x65234, 0x656D4)
DEBUG = (0x69834, 0x69CD4)
RETAIL_SHA256 = "2c17ff26f0c817b1513a254d23c2e2a8fc2bdf195c201780fb0138ebd85a1123"
DEBUG_SHA256 = "0fdc59440c1b1401bd8a99183ff31f6ef60d804d43b352c7125bfc8f8b7baaff"

ENTRY = bytes.fromhex("00 04 00 0c 02 49 08 80 09 30 00 04 00 0c 70 47")
BASE_TILE_ADDR = (0x030005AC).to_bytes(4, "little")
DIALOGUE_TILE_ADDR = (0x030005AE).to_bytes(4, "little")
NEXT_PREFIX = bytes.fromhex(
    "00 b5 03 1c 00 20 58 70 98 60 18 70 58 60 d9 65 1a 66 "
    "00 22 03 21 18 1c 70 30 02 60 04 38 01 39 00 29 fa da "
    "19 1c 0c 31 00 22 18 1c 58 30 02 60"
)

def sha256(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()

def main() -> None:
    p = argparse.ArgumentParser(description="Verify German Pokemon Ruby text_window module")
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

    assert len(r0) == len(r1) == len(dbg) == 0x4A0
    assert r0 == r1
    assert sha256(r0) == RETAIL_SHA256
    assert sha256(r1) == RETAIL_SHA256
    assert sha256(dbg) == DEBUG_SHA256

    assert DEBUG[0] - RETAIL[0] == 0x4600
    assert DEBUG[1] - RETAIL[1] == 0x4600

    assert r0[:16] == ENTRY
    assert dbg[:16] == ENTRY
    assert r0[16:20] == BASE_TILE_ADDR
    assert dbg[16:20] == BASE_TILE_ADDR

    assert r0.count(BASE_TILE_ADDR) == 5
    assert dbg.count(BASE_TILE_ADDR) == 5
    assert r0.count(DIALOGUE_TILE_ADDR) == 4
    assert dbg.count(DIALOGUE_TILE_ADDR) == 4

    assert rev0[RETAIL[1]:RETAIL[1] + len(NEXT_PREFIX)] == NEXT_PREFIX
    assert rev1[RETAIL[1]:RETAIL[1] + len(NEXT_PREFIX)] == NEXT_PREFIX
    assert debug[DEBUG[1]:DEBUG[1] + len(NEXT_PREFIX)] == NEXT_PREFIX

    print("German text_window verification passed")
    print("Retail Rev0/Rev1: 0x08065234..0x080656D4, 0x4A0 bytes")
    print("Debug:            0x08069834..0x08069CD4, 0x4A0 bytes")
    print("Accumulated Retail->Debug delta remains +0x4600")
    print("Next: script / InitScriptContext")

if __name__ == "__main__":
    main()
