#!/usr/bin/env python3
import argparse
import hashlib
from pathlib import Path

RETAIL = (0x6822C, 0x69370)
DEBUG = (0x6C82C, 0x6DA4C)

RETAIL_SHA256 = "24d30b6e9f0e240d2f9836789b64db8ff68502ad5130e61b0858e4ae5ec26d5b"
DEBUG_SHA256 = "e7cfd157fdd22d2de76d97f1c66c5721fdef4eccee7d05548f8f611c74cbe27f"

ENTRY = bytes.fromhex(
    "30 b5 02 21 49 42 03 23 5b 42 05 24 64 42 09 25 6d 42 "
    "00 22 02 70 42 78 11 40 19 40 21 40 29 40 41 70 00 21 "
    "81 70 30 bc 01 bc 00 47"
)

MAP_HEADER_RETAIL = (0x0202E828).to_bytes(4, "little")
MAP_HEADER_DEBUG = (0x0202EACC).to_bytes(4, "little")

NEXT_PREFIX = bytes.fromhex("10 b5 0c 4c 90 22 52 00 20 1c 00 21")
NEXT_TEMP_RETAIL = (0x0202E8E2).to_bytes(4, "little")
NEXT_TEMP_DEBUG = (0x0202EB86).to_bytes(4, "little")

def sha256(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()

def verify_next(data: bytes, start: int, temp_addr: bytes) -> None:
    assert data[start:start + len(NEXT_PREFIX)] == NEXT_PREFIX
    # InitEventData is 0x3C bytes including its literal pool.
    assert data[start + 0x38:start + 0x3C] == temp_addr

def main() -> None:
    p = argparse.ArgumentParser(description="Verify German Pokemon Ruby field_control_avatar module")
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

    assert len(r0) == 0x1144
    assert len(dbg) == 0x1220
    assert len(dbg) - len(r0) == 0xDC

    assert r0 == r1
    assert sha256(r0) == RETAIL_SHA256
    assert sha256(r1) == RETAIL_SHA256
    assert sha256(dbg) == DEBUG_SHA256

    assert DEBUG[0] - RETAIL[0] == 0x4600
    assert DEBUG[1] - RETAIL[1] == 0x46DC

    assert r0[:len(ENTRY)] == ENTRY
    assert dbg[:len(ENTRY)] == ENTRY

    assert r0[-4:] == MAP_HEADER_RETAIL
    assert dbg[-4:] == MAP_HEADER_DEBUG

    verify_next(rev0, RETAIL[1], NEXT_TEMP_RETAIL)
    verify_next(rev1, RETAIL[1], NEXT_TEMP_RETAIL)
    verify_next(debug, DEBUG[1], NEXT_TEMP_DEBUG)

    print("German field_control_avatar verification passed")
    print("Retail Rev0/Rev1: 0x0806822C..0x08069370, 0x1144 bytes")
    print("Debug:            0x0806C82C..0x0806DA4C, 0x1220 bytes")
    print("Debug growth: 0xDC")
    print("Accumulated Retail->Debug delta changes +0x4600 -> +0x46DC")
    print("Next: event_data / InitEventData")

if __name__ == "__main__":
    main()
