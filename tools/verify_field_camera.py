#!/usr/bin/env python3
import argparse
import hashlib
from pathlib import Path

RETAIL = (0x57CFC, 0x586B8)
DEBUG = (0x5C1E4, 0x5CBA0)
RETAIL_SHA256 = "bb4fb3177a5165fad0cb6273029a5a6edf81c09cb8d753b4a4f4c70e8cd05461"
DEBUG_SHA256 = "7656d3f28a00bd04749b5ea9c6cc6830c660b623de256a7a23e83d085b63daf2"
ENTRY = bytes.fromhex("00 21 81 70 c1 70 01 70 41 70 01 21 01 71 70 47")
DOOR_RETAIL_ENTRY = bytes.fromhex("00 b5 03 49 40 22 95 f1 49 f8 01 bc 00 47")
DOOR_DEBUG_ENTRY = bytes.fromhex("00 b5 03 49 40 22 a9 f1 7f fc 01 bc 00 47")
DOOR_VRAM_LITERAL = (0x06007F00).to_bytes(4, "little")
VRAM_LITERALS = (
    (0x0600E800).to_bytes(4, "little"),
    (0x0600E000).to_bytes(4, "little"),
    (0x0600F000).to_bytes(4, "little"),
)
BG3_FILL_LITERAL = (0x00003014).to_bytes(4, "little")


def sha256(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def main() -> None:
    parser = argparse.ArgumentParser(description="Verify German Pokemon Ruby field_camera module")
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

    assert RETAIL[1] - RETAIL[0] == 0x9BC
    assert DEBUG[1] - DEBUG[0] == 0x9BC
    assert DEBUG[0] - RETAIL[0] == 0x44E8
    assert DEBUG[1] - RETAIL[1] == 0x44E8

    assert r0 == r1
    assert sha256(r0) == RETAIL_SHA256
    assert sha256(r1) == RETAIL_SHA256
    assert sha256(dbg) == DEBUG_SHA256

    assert r0[:16] == ENTRY
    assert dbg[:16] == ENTRY

    for literal in VRAM_LITERALS:
        assert literal in r0
        assert literal in dbg
    assert BG3_FILL_LITERAL in r0
    assert BG3_FILL_LITERAL in dbg

    # field_door begins immediately after field_camera. The first helper copies
    # door tiles to VRAM 0x06007F00; BL displacement differs between profiles.
    assert rev0[RETAIL[1]:RETAIL[1] + len(DOOR_RETAIL_ENTRY)] == DOOR_RETAIL_ENTRY
    assert rev1[RETAIL[1]:RETAIL[1] + len(DOOR_RETAIL_ENTRY)] == DOOR_RETAIL_ENTRY
    assert debug[DEBUG[1]:DEBUG[1] + len(DOOR_DEBUG_ENTRY)] == DOOR_DEBUG_ENTRY
    assert rev0[RETAIL[1] + 16:RETAIL[1] + 20] == DOOR_VRAM_LITERAL
    assert rev1[RETAIL[1] + 16:RETAIL[1] + 20] == DOOR_VRAM_LITERAL
    assert debug[DEBUG[1] + 16:DEBUG[1] + 20] == DOOR_VRAM_LITERAL

    print("German field_camera verification passed")
    print("Retail Rev0/Rev1: 0x08057CFC..0x080586B8, 0x9BC bytes")
    print("Debug:            0x0805C1E4..0x0805CBA0, 0x9BC bytes")
    print("Accumulated Retail->Debug delta remains +0x44E8")
    print("Next: field_door")


if __name__ == "__main__":
    main()
