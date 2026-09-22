#!/usr/bin/env python3
import argparse
import hashlib
import struct
from pathlib import Path

RETAIL = (0x6977C, 0x6A668)
DEBUG = (0x6DE58, 0x6ED44)
RETAIL_SHA256 = "71549fd25ff83140a1e90464aff4a3db7d3ca0092fc533c4feafa7b3a8f370ca"
DEBUG_SHA256 = "be1aee30a11d8ceba061f45a3c54d4da36cf5ad198a97f146f1864774ec75e46"

ENTRY_PREFIX = bytes.fromhex(
    "00 b5 00 06 00 0e 07 4a 81 00 09 18 c9 00 89 18 "
    "08 22 89 5e 04 4a 89 00 89 18 09 68"
)
TAIL = bytes.fromhex("01 b0 08 bc 98 46 f0 bc 01 bc 00 47")
CLOCK_PREFIX = bytes.fromhex("00 b5 09 48")

CALLBACK_TABLE_RETAIL = 0x08381B4C
CALLBACK_TABLE_DEBUG = 0x0839ACF4
MODULE_OWNED_CALLBACK_INDICES = (0, 1, 2, 3, 4, 7)

def sha256(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()

def read_rom_table(data: bytes, address: int, count: int) -> tuple[int, ...]:
    offset = address - 0x08000000
    return struct.unpack("<" + "I" * count, data[offset:offset + count * 4])

def main() -> None:
    p = argparse.ArgumentParser(description="Verify German Pokemon Ruby field_tasks module")
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

    assert len(r0) == len(r1) == len(dbg) == 0xEEC
    assert r0 == r1
    assert sha256(r0) == RETAIL_SHA256
    assert sha256(r1) == RETAIL_SHA256
    assert sha256(dbg) == DEBUG_SHA256

    assert DEBUG[0] - RETAIL[0] == 0x46DC
    assert DEBUG[1] - RETAIL[1] == 0x46DC

    assert r0.startswith(ENTRY_PREFIX)
    assert dbg.startswith(ENTRY_PREFIX)
    assert r0.endswith(TAIL)
    assert dbg.endswith(TAIL)

    assert struct.unpack("<I", r0[0x28:0x2C])[0] == CALLBACK_TABLE_RETAIL
    assert struct.unpack("<I", dbg[0x28:0x2C])[0] == CALLBACK_TABLE_DEBUG

    retail_callbacks = read_rom_table(rev0, CALLBACK_TABLE_RETAIL, 8)
    debug_callbacks = read_rom_table(debug, CALLBACK_TABLE_DEBUG, 8)
    for i in MODULE_OWNED_CALLBACK_INDICES:
        assert (debug_callbacks[i] & ~1) - (retail_callbacks[i] & ~1) == 0x46DC

    assert rev0[RETAIL[1]:RETAIL[1] + 4] == CLOCK_PREFIX
    assert rev1[RETAIL[1]:RETAIL[1] + 4] == CLOCK_PREFIX
    assert debug[DEBUG[1]:DEBUG[1] + 4] == CLOCK_PREFIX

    assert rev0[RETAIL[1] + 0x28:RETAIL[1] + 0x2C] == (0x0835).to_bytes(4, "little")
    assert debug[DEBUG[1] + 0x28:DEBUG[1] + 0x2C] == (0x0835).to_bytes(4, "little")
    assert rev0[RETAIL[1] + 0x34:RETAIL[1] + 0x38] == (0x4040).to_bytes(4, "little")
    assert debug[DEBUG[1] + 0x34:DEBUG[1] + 0x38] == (0x4040).to_bytes(4, "little")

    print("German field_tasks verification passed")
    print("Retail Rev0/Rev1: 0x0806977C..0x0806A668, 0xEEC bytes")
    print("Debug:            0x0806DE58..0x0806ED44, 0xEEC bytes")
    print("Accumulated Retail->Debug delta remains +0x46DC")
    print("Next: clock / InitTimeBasedEvents")

if __name__ == "__main__":
    main()
