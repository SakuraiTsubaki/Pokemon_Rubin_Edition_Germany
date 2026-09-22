#!/usr/bin/env python3
import argparse
import hashlib
from pathlib import Path

RETAIL = (0x656D4, 0x65BAC)
DEBUG = (0x69CD4, 0x6A1AC)
RETAIL_SHA256 = "4b56a2c1b4a0c91db332dffcf8e65e87224c4537ee058c459c13aab7467a7b1f"
DEBUG_SHA256 = "95e62a9bfde97ee285c346060870dde56d3c0b285e5df1060db1aa133dde25e6"

ENTRY = bytes.fromhex(
    "00 b5 03 1c 00 20 58 70 98 60 18 70 58 60 d9 65 1a 66 "
    "00 22 03 21 18 1c 70 30 02 60 04 38 01 39 00 29 fa da "
    "19 1c 0c 31 00 22 18 1c 58 30 02 60"
)
NEXT = bytes.fromhex("00 20 70 47 00 20 70 47 00 b5 ff f7 b5 fd 00 20 02 bc 08 47")

RAM_RET_RETAIL = (0x02028DC8).to_bytes(4, "little")
RAM_RET_DEBUG = (0x0202906C).to_bytes(4, "little")
SAVE1_RETAIL = (0x0202E8AC).to_bytes(4, "little")
SAVE1_DEBUG = (0x0202EB50).to_bytes(4, "little")

def sha256(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()

def main() -> None:
    p = argparse.ArgumentParser(description="Verify German Pokemon Ruby script module")
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

    assert len(r0) == len(r1) == len(dbg) == 0x4D8
    assert r0 == r1
    assert sha256(r0) == RETAIL_SHA256
    assert sha256(r1) == RETAIL_SHA256
    assert sha256(dbg) == DEBUG_SHA256

    assert DEBUG[0] - RETAIL[0] == 0x4600
    assert DEBUG[1] - RETAIL[1] == 0x4600

    assert r0[:len(ENTRY)] == ENTRY
    assert dbg[:len(ENTRY)] == ENTRY

    assert bytes.fromhex("33 28") in r0[-0x80:]
    assert bytes.fromhex("33 28") in dbg[-0x80:]
    assert RAM_RET_RETAIL in r0[-0x80:]
    assert RAM_RET_DEBUG in dbg[-0x80:]
    assert SAVE1_RETAIL in r0[-0x80:]
    assert SAVE1_DEBUG in dbg[-0x80:]

    assert rev0[RETAIL[1]:RETAIL[1] + len(NEXT)] == NEXT
    assert rev1[RETAIL[1]:RETAIL[1] + len(NEXT)] == NEXT
    assert debug[DEBUG[1]:DEBUG[1] + len(NEXT)] == NEXT

    print("German script verification passed")
    print("Retail Rev0/Rev1: 0x080656D4..0x08065BAC, 0x4D8 bytes")
    print("Debug:            0x08069CD4..0x0806A1AC, 0x4D8 bytes")
    print("Accumulated Retail->Debug delta remains +0x4600")
    print("Next: scrcmd / ScrCmd_nop")

if __name__ == "__main__":
    main()
