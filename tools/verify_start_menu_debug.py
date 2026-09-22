#!/usr/bin/env python3
import argparse
import hashlib
from pathlib import Path

DEBUG = (0x76AC8, 0x791A8)
DEBUG_SHA256 = "8e40baceb26a68d08faf009bdf0b4c64bd2aa7e8424d05304c684eb8293ec627"

ENTRY = bytes.fromhex(
    "10 b5 82 b0 00 06 00 0e 1b 4a 81 00 09 18 49 00 "
    "1a 48 09 18 11 60 00 24 08 78 ff 28 04 d0 01 34"
)
TAIL = (0x7918C, 0x791A8)
TAIL_SHA256 = "ec317a686616260b61ce4133187dc72d6bcbcb0d35cf554d98fef4cddc07caf5"
MENU_PREFIX = bytes.fromhex("00 b5 05 20 03 f0 88 fc")

RETAIL_MENU_START = 0x71F3C

def sha256(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()

def main() -> None:
    p = argparse.ArgumentParser(description="Verify German Pokemon Ruby Debug start-menu module")
    p.add_argument("--rev0", type=Path, required=True)
    p.add_argument("--rev1", type=Path, required=True)
    p.add_argument("--debug", type=Path, required=True)
    a = p.parse_args()

    rev0 = a.rev0.read_bytes()
    rev1 = a.rev1.read_bytes()
    debug = a.debug.read_bytes()

    dbg = debug[DEBUG[0]:DEBUG[1]]
    assert len(dbg) == 0x26E0
    assert sha256(dbg) == DEBUG_SHA256
    assert dbg.startswith(ENTRY)

    assert len(debug[TAIL[0]:TAIL[1]]) == 0x1C
    assert sha256(debug[TAIL[0]:TAIL[1]]) == TAIL_SHA256

    assert rev0[RETAIL_MENU_START:RETAIL_MENU_START + len(MENU_PREFIX)] == MENU_PREFIX
    assert rev1[RETAIL_MENU_START:RETAIL_MENU_START + len(MENU_PREFIX)] == MENU_PREFIX
    assert debug[DEBUG[1]:DEBUG[1] + len(MENU_PREFIX)] == MENU_PREFIX

    assert DEBUG[0] - 0x71F3C == 0x4B8C
    assert DEBUG[1] - RETAIL_MENU_START == 0x726C

    print("German Debug start_menu_debug verification passed")
    print("Retail Rev0/Rev1: module absent")
    print("Debug: 0x08076AC8..0x080791A8, 0x26E0 bytes")
    print("Accumulated Retail->Debug delta changes +0x4B8C -> +0x726C")
    print("Next/rejoin: menu / CloseMenu")

if __name__ == "__main__":
    main()
