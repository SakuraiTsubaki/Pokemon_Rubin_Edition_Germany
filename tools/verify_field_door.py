#!/usr/bin/env python3
import argparse
import hashlib
from pathlib import Path

RETAIL = (0x586B8, 0x58AF4)
DEBUG = (0x5CBA0, 0x5CFDC)
RETAIL_SHA256 = "48f3f9760b961707a5eae1e176979ede3bf23afdd0e3cab1ef1dd33381b4af09"
DEBUG_SHA256 = "46a519981bec8252ca0efa2c10927a871e21210815d42e2ac66f68d84fc30029"
RETAIL_ENTRY = bytes.fromhex("00 b5 03 49 40 22 95 f1 49 f8 01 bc 00 47")
DEBUG_ENTRY = bytes.fromhex("00 b5 03 49 40 22 a9 f1 7f fc 01 bc 00 47")
DOOR_VRAM = (0x06007F00).to_bytes(4, "little")

RETAIL_FRAMES = 0x31B064
DEBUG_FRAMES = 0x33420C
FRAME_BYTES = 0x28
FRAME_SHA256 = "367d6e93a7e2d4d98d29434fdb45021b48b6fb74ca94906805b43ccebd6d0504"
EXPECTED_FRAMES = [
    (4, 0xFFFF), (4, 0x0000), (4, 0x0100), (4, 0x0200), (0, 0x0000),
    (4, 0x0200), (4, 0x0100), (4, 0x0000), (4, 0xFFFF), (0, 0x0000),
]

RETAIL_GRAPHICS = 0x31B19C
DEBUG_GRAPHICS = 0x334344
GRAPHICS_ENTRY_SIZE = 12
GRAPHICS_COUNT = 35
GRAPHICS_BYTES = GRAPHICS_ENTRY_SIZE * GRAPHICS_COUNT
RETAIL_GRAPHICS_SHA256 = "d69a7de97722fc00b2f51c53b6fc44a4b3c7b3c1d0a8ffb2022a5ac0c28ddd41"
DEBUG_GRAPHICS_SHA256 = "48ec5ca7ce3fd0f25a08b818c6cc97fd72fe7da993e4aa8a1505b1510ca3613d"
DEBUG_DATA_DELTA = 0x191A8

PLAYER_ENTRY_COMMON_PREFIX = bytes.fromhex("00 b5 01 1c 2e 20 0a 5e d0 00 80 18 80 00 03 4a 80 18 03 4a")
PLAYER_EMPTY_CALLBACK = bytes.fromhex("00 20 70 47")


def sha256(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def parse_frames(data: bytes):
    return [(data[i], int.from_bytes(data[i + 2:i + 4], "little")) for i in range(0, len(data), 4)]


def parse_graphics(data: bytes):
    result = []
    for i in range(0, len(data), GRAPHICS_ENTRY_SIZE):
        result.append((
            int.from_bytes(data[i:i + 2], "little"),
            data[i + 2],
            int.from_bytes(data[i + 4:i + 8], "little"),
            int.from_bytes(data[i + 8:i + 12], "little"),
        ))
    return result


def main() -> None:
    parser = argparse.ArgumentParser(description="Verify German Pokemon Ruby field_door module")
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

    assert RETAIL[1] - RETAIL[0] == 0x43C
    assert DEBUG[1] - DEBUG[0] == 0x43C
    assert DEBUG[0] - RETAIL[0] == 0x44E8
    assert DEBUG[1] - RETAIL[1] == 0x44E8
    assert r0 == r1
    assert sha256(r0) == RETAIL_SHA256
    assert sha256(r1) == RETAIL_SHA256
    assert sha256(dbg) == DEBUG_SHA256

    assert r0[:len(RETAIL_ENTRY)] == RETAIL_ENTRY
    assert dbg[:len(DEBUG_ENTRY)] == DEBUG_ENTRY
    assert rev0[RETAIL[0] + 16:RETAIL[0] + 20] == DOOR_VRAM
    assert rev1[RETAIL[0] + 16:RETAIL[0] + 20] == DOOR_VRAM
    assert debug[DEBUG[0] + 16:DEBUG[0] + 20] == DOOR_VRAM

    frame_sets = [
        rev0[RETAIL_FRAMES:RETAIL_FRAMES + FRAME_BYTES],
        rev1[RETAIL_FRAMES:RETAIL_FRAMES + FRAME_BYTES],
        debug[DEBUG_FRAMES:DEBUG_FRAMES + FRAME_BYTES],
    ]
    assert frame_sets[0] == frame_sets[1] == frame_sets[2]
    assert sha256(frame_sets[0]) == FRAME_SHA256
    assert parse_frames(frame_sets[0]) == EXPECTED_FRAMES

    retail_graphics0 = rev0[RETAIL_GRAPHICS:RETAIL_GRAPHICS + GRAPHICS_BYTES]
    retail_graphics1 = rev1[RETAIL_GRAPHICS:RETAIL_GRAPHICS + GRAPHICS_BYTES]
    debug_graphics = debug[DEBUG_GRAPHICS:DEBUG_GRAPHICS + GRAPHICS_BYTES]
    assert retail_graphics0 == retail_graphics1
    assert sha256(retail_graphics0) == RETAIL_GRAPHICS_SHA256
    assert sha256(debug_graphics) == DEBUG_GRAPHICS_SHA256

    rg = parse_graphics(retail_graphics0)
    dg = parse_graphics(debug_graphics)
    assert rg[-1] == (0, 0, 0, 0)
    assert dg[-1] == (0, 0, 0, 0)
    assert len(rg[:-1]) == 34
    assert all(entry[1] in (0, 1) for entry in rg[:-1])
    assert [(x[0], x[1]) for x in rg] == [(x[0], x[1]) for x in dg]
    for retail_entry, debug_entry in zip(rg[:-1], dg[:-1]):
        assert debug_entry[2] - retail_entry[2] == DEBUG_DATA_DELTA
        assert debug_entry[3] - retail_entry[3] == DEBUG_DATA_DELTA

    # field_player_avatar begins immediately after field_door.
    assert rev0[RETAIL[1]:RETAIL[1] + len(PLAYER_ENTRY_COMMON_PREFIX)] == PLAYER_ENTRY_COMMON_PREFIX
    assert rev1[RETAIL[1]:RETAIL[1] + len(PLAYER_ENTRY_COMMON_PREFIX)] == PLAYER_ENTRY_COMMON_PREFIX
    assert debug[DEBUG[1]:DEBUG[1] + len(PLAYER_ENTRY_COMMON_PREFIX)] == PLAYER_ENTRY_COMMON_PREFIX
    assert rev0[RETAIL[1] + 0x24:RETAIL[1] + 0x28] == PLAYER_EMPTY_CALLBACK
    assert rev1[RETAIL[1] + 0x24:RETAIL[1] + 0x28] == PLAYER_EMPTY_CALLBACK
    assert debug[DEBUG[1] + 0x24:DEBUG[1] + 0x28] == PLAYER_EMPTY_CALLBACK

    print("German field_door verification passed")
    print("Retail Rev0/Rev1: 0x080586B8..0x08058AF4, 0x43C bytes")
    print("Debug:            0x0805CBA0..0x0805CFDC, 0x43C bytes")
    print("Door graphics: 34 entries + terminator; frame data identical across profiles")
    print("Accumulated Retail->Debug text delta remains +0x44E8")
    print("Next: field_player_avatar")


if __name__ == "__main__":
    main()
