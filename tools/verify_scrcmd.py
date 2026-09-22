#!/usr/bin/env python3
import argparse
import hashlib
from pathlib import Path

RETAIL = (0x65BAC, 0x6822C)
DEBUG = (0x6A1AC, 0x6C82C)
RETAIL_SHA256 = "d9abe33055babd8e6e68fbb4838afb265c5475bfeb71b0a8a4fc3126ae34d372"
DEBUG_SHA256 = "de537d1d54882ba4d7ee7d9af4f581141a23ad320e6ba938a5312140eb207b5f"

ENTRY = bytes.fromhex("00 20 70 47 00 20 70 47 00 b5 ff f7 b5 fd 00 20 02 bc 08 47")
RESULT_RETAIL = (0x0202E8DC).to_bytes(4, "little")
RESULT_DEBUG = (0x0202EB80).to_bytes(4, "little")
NEXT = bytes.fromhex(
    "30 b5 02 21 49 42 03 23 5b 42 05 24 64 42 09 25 6d 42 "
    "00 22 02 70 42 78 11 40 19 40 21 40 29 40 41 70 00 21 "
    "81 70 30 bc 01 bc 00 47"
)

def sha256(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()

def main() -> None:
    p = argparse.ArgumentParser(description="Verify German Pokemon Ruby scrcmd module")
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

    assert len(r0) == len(r1) == len(dbg) == 0x2680
    assert r0 == r1
    assert sha256(r0) == RETAIL_SHA256
    assert sha256(r1) == RETAIL_SHA256
    assert sha256(dbg) == DEBUG_SHA256

    assert DEBUG[0] - RETAIL[0] == 0x4600
    assert DEBUG[1] - RETAIL[1] == 0x4600

    assert r0[:len(ENTRY)] == ENTRY
    assert dbg[:len(ENTRY)] == ENTRY

    assert r0[-4:] == RESULT_RETAIL
    assert dbg[-4:] == RESULT_DEBUG

    assert rev0[RETAIL[1]:RETAIL[1] + len(NEXT)] == NEXT
    assert rev1[RETAIL[1]:RETAIL[1] + len(NEXT)] == NEXT
    assert debug[DEBUG[1]:DEBUG[1] + len(NEXT)] == NEXT

    print("German scrcmd verification passed")
    print("Retail Rev0/Rev1: 0x08065BAC..0x0806822C, 0x2680 bytes")
    print("Debug:            0x0806A1AC..0x0806C82C, 0x2680 bytes")
    print("Accumulated Retail->Debug delta remains +0x4600")
    print("Next: field_control_avatar / ClearPlayerFieldInput")

if __name__ == "__main__":
    main()
