#!/usr/bin/env python3
import argparse
import hashlib
from pathlib import Path

RETAIL = (0x570DC, 0x57CFC)
DEBUG = (0x5B5C4, 0x5C1E4)
RETAIL_SHA256 = "59c48f4631b4be59d63f8e5c72ace080955549f44bf7bda668cf08bd5ea8846f"
DEBUG_SHA256 = "d51e8243f9f4f8711253eeca9927b2d6be617a54d449865804470aba03f526bd"
TABLE_SHA256 = "cf25f69a32000022fe10be1c2fc9efec780d830e8eb0d6fe205cb4feb0d1badb"
RETAIL_TABLE = 0x314614
DEBUG_TABLE = 0x32D7BC
TABLE_SIZE = 0xF0
ENTRY = bytes.fromhex("01 20 70 47")
FIELD_CAMERA_ENTRY = bytes.fromhex(
    "00 21 81 70 c1 70 01 70 41 70 01 21 01 71 70 47"
)


def sha256(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def single_value_predicate(value: int) -> bytes:
    return bytes.fromhex("00 b5 00 06 00 0e") + bytes((value, 0x28)) + bytes.fromhex(
        "01 d0 00 20 00 e0 01 20 02 bc 08 47"
    )


def main() -> None:
    parser = argparse.ArgumentParser(description="Verify German Pokemon Ruby metatile_behavior")
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

    assert RETAIL[1] - RETAIL[0] == 0xC20
    assert DEBUG[1] - DEBUG[0] == 0xC20
    assert DEBUG[0] - RETAIL[0] == 0x44E8
    assert DEBUG[1] - RETAIL[1] == 0x44E8

    assert r0 == r1
    assert sha256(r0) == RETAIL_SHA256
    assert sha256(r1) == RETAIL_SHA256
    assert sha256(dbg) == DEBUG_SHA256
    assert r0[:4] == ENTRY
    assert dbg[:4] == ENTRY

    retail_table0 = rev0[RETAIL_TABLE:RETAIL_TABLE + TABLE_SIZE]
    retail_table1 = rev1[RETAIL_TABLE:RETAIL_TABLE + TABLE_SIZE]
    debug_table = debug[DEBUG_TABLE:DEBUG_TABLE + TABLE_SIZE]
    assert retail_table0 == retail_table1 == debug_table
    assert sha256(retail_table0) == TABLE_SHA256
    assert all((value & ~0x07) == 0 for value in retail_table0)

    # The source-correlated final seven predicates test IDs E0..E6 and are
    # consecutive in every German profile. Their end is the module boundary.
    tail = b"".join(single_value_predicate(value) for value in range(0xE0, 0xE7))
    assert r0.endswith(tail)
    assert dbg.endswith(tail)

    # field_camera begins immediately after the E6 / Blueprint predicate.
    assert rev0[RETAIL[1]:RETAIL[1] + 16] == FIELD_CAMERA_ENTRY
    assert rev1[RETAIL[1]:RETAIL[1] + 16] == FIELD_CAMERA_ENTRY
    assert debug[DEBUG[1]:DEBUG[1] + 16] == FIELD_CAMERA_ENTRY

    print("German metatile_behavior verification passed")
    print("Retail Rev0/Rev1: 0x080570DC..0x08057CFC, 0xC20 bytes")
    print("Debug:             0x0805B5C4..0x0805C1E4, 0xC20 bytes")
    print("Behavior table: 0xF0 bytes, identical across all three profiles")
    print("Accumulated Retail->Debug delta remains +0x44E8")
    print("Next: field_camera")


if __name__ == "__main__":
    main()
