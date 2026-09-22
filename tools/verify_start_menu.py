#!/usr/bin/env python3
import argparse
import hashlib
from pathlib import Path

RETAIL = (0x712D0, 0x71F3C)
DEBUG = (0x75C30, 0x76AC8)

RETAIL_SHA256 = "0bd17feffa3874c6540ebb08928be1b9110dcf2c6960f6e4eccc6caf0a710a58"
DEBUG_SHA256 = "7e26e68bee12d4aa582c831bf90b6b87b4e2df21119b308409607e7dc31e4d0f"

RETAIL_ENTRY = bytes.fromhex("00 b5 05 48 00 21 01 70 e3 f7 9e f9")
DEBUG_ENTRY = bytes.fromhex("00 b5 03 f0 b9 fa 00 f0 b1 f8 01 20 02 bc 08 47")

DEBUG_COMMON_START = 0x75E5C
DEBUG_COMMON_PREFIX = bytes.fromhex("00 b5 05 48 00 21 01 70")

DEBUG_PREFIX = (0x75C30, 0x75E5C)
DEBUG_PREFIX_SHA256 = "69afdd1b92fc99c5287650915d4d422f107e77365c356bd1e9c934fb9e499bf6"
DEBUG_FUNCTIONS = (
    (0x75C30, 0x75C40, "fdc3517658f7a66b128155de08291e05ed35ca02c03c11abcee98c3e26e3a42f"),
    (0x75C40, 0x75D9C, "dfe24c9787a1d35cd9812b41d88f4c42e456f8600cce8421c3c1315fea1733e9"),
    (0x75D9C, 0x75DB4, "dcba1dd32bcd7ebd2f18b781ab6f1c52be503d4345e6ae3626f4932e47b183d2"),
    (0x75DB4, 0x75E38, "8ca7fd6db939a01b67f8f967df3ac6482d074f5e1aebf2dad7fc3ac73f9b9a31"),
    (0x75E38, 0x75E5C, "4007784d0fb970efb51a70324a3cd40b7035ebaf9a632dd7ddee31ae409320fc"),
)

NEXT_RETAIL = bytes.fromhex("00 b5 05 20 03 f0 88 fc")
NEXT_DEBUG = bytes.fromhex("10 b5 82 b0 00 06 00 0e 1b 4a 81 00 09 18 49 00")

def sha256(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()

def main() -> None:
    p = argparse.ArgumentParser(description="Verify German Pokemon Ruby start_menu module")
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

    assert len(r0) == 0xC6C
    assert len(dbg) == 0xE98
    assert len(dbg) - len(r0) == 0x22C

    assert r0 == r1
    assert sha256(r0) == RETAIL_SHA256
    assert sha256(r1) == RETAIL_SHA256
    assert sha256(dbg) == DEBUG_SHA256

    assert DEBUG[0] - RETAIL[0] == 0x4960
    assert DEBUG[1] - RETAIL[1] == 0x4B8C

    assert r0.startswith(RETAIL_ENTRY)
    assert dbg.startswith(DEBUG_ENTRY)

    prefix = debug[DEBUG_PREFIX[0]:DEBUG_PREFIX[1]]
    assert len(prefix) == 0x22C
    assert sha256(prefix) == DEBUG_PREFIX_SHA256
    for start, end, expected_hash in DEBUG_FUNCTIONS:
        assert sha256(debug[start:end]) == expected_hash

    assert DEBUG[1] - DEBUG_COMMON_START == len(r0)
    assert debug[DEBUG_COMMON_START:DEBUG_COMMON_START + len(DEBUG_COMMON_PREFIX)] == DEBUG_COMMON_PREFIX

    assert rev0[RETAIL[1]:RETAIL[1] + len(NEXT_RETAIL)] == NEXT_RETAIL
    assert rev1[RETAIL[1]:RETAIL[1] + len(NEXT_RETAIL)] == NEXT_RETAIL
    assert debug[DEBUG[1]:DEBUG[1] + len(NEXT_DEBUG)] == NEXT_DEBUG

    print("German start_menu verification passed")
    print("Retail Rev0/Rev1: 0x080712D0..0x08071F3C, 0xC6C bytes")
    print("Debug:            0x08075C30..0x08076AC8, 0xE98 bytes")
    print("Debug-only prefix: 0x22C bytes")
    print("Accumulated Retail->Debug delta changes +0x4960 -> +0x4B8C")
    print("Next Retail: menu / CloseMenu")
    print("Next Debug: debug/start_menu_debug / debug_sub_8076AC8")

if __name__ == "__main__":
    main()
