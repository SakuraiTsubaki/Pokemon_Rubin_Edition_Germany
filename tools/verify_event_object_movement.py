#!/usr/bin/env python3
import argparse
import hashlib
from pathlib import Path

RETAIL = (0x5AD90, 0x64DB4)
DEBUG = (0x5F348, 0x693B4)
RETAIL_SHA256 = "5828818871f2779b9f5a9500c2c1c4b5ffc02a06e928e9c8e1de3aa1c0b2e6f5"
DEBUG_SHA256 = "c7e94d987507ecc1dfee7ecfd442963054b5931d732be1fd2ef41f09e29a7609"

CLEAR_PREFIX = bytes.fromhex("10 b5 04 1c 00 21 24 22")
CLEAR_SUFFIX = bytes.fromhex("ff 20 20 72 01 20 40 42 60 72 a0 72 20 77 10 bc 01 bc 00 47")
CLEAR_SIZE = 0x20
TAIL_ANCHOR = bytes.fromhex("97 20 90 60 03 20 d0 60 05 20")
NEXT_PREFIX = bytes.fromhex("00 b5 06 49 00 20 08 70 05 48 00 88 00 f0 a2 fb")

def sha256(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()

def verify_clear(data: bytes, start: int) -> None:
    func = data[start:start + CLEAR_SIZE]
    assert len(func) == CLEAR_SIZE
    assert func.startswith(CLEAR_PREFIX)
    assert func.endswith(CLEAR_SUFFIX)

def main() -> None:
    p = argparse.ArgumentParser(description="Verify German Pokemon Ruby event_object_movement module")
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

    assert len(r0) == 0xA024
    assert len(dbg) == 0xA06C
    assert len(dbg) - len(r0) == 0x48
    assert r0 == r1
    assert sha256(r0) == RETAIL_SHA256
    assert sha256(r1) == RETAIL_SHA256
    assert sha256(dbg) == DEBUG_SHA256

    assert DEBUG[0] - RETAIL[0] == 0x45B8
    assert DEBUG[1] - RETAIL[1] == 0x4600

    verify_clear(rev0, RETAIL[0])
    verify_clear(rev1, RETAIL[0])
    verify_clear(debug, DEBUG[0])

    assert TAIL_ANCHOR in r0[-0x80:]
    assert TAIL_ANCHOR in dbg[-0x80:]

    assert rev0[RETAIL[1]:RETAIL[1] + len(NEXT_PREFIX)] == NEXT_PREFIX
    assert rev1[RETAIL[1]:RETAIL[1] + len(NEXT_PREFIX)] == NEXT_PREFIX
    assert debug[DEBUG[1]:DEBUG[1] + len(NEXT_PREFIX)] == NEXT_PREFIX

    print("German event_object_movement verification passed")
    print("Retail Rev0/Rev1: 0x0805AD90..0x08064DB4, 0xA024 bytes")
    print("Debug:            0x0805F348..0x080693B4, 0xA06C bytes")
    print("Debug text growth: 0x48")
    print("Accumulated Retail->Debug delta changes +0x45B8 -> +0x4600")
    print("Next: field_message_box / InitFieldMessageBox")

if __name__ == "__main__":
    main()
