#!/usr/bin/env python3
import argparse
import hashlib
from pathlib import Path

RETAIL = (0x64DB4, 0x65000)
DEBUG = (0x693B4, 0x69600)
RETAIL_SHA256 = "8378e13d405471aebddbb2b6dfcff3c3d7ef1c76f1bf450bc8704384332f2e8a"
DEBUG_SHA256 = "a342e8f71cccb346e8060b53addd3ff4bfb2ab0d3ab758b7feec746c5dc4648b"

ENTRY = bytes.fromhex("00 b5 06 49 00 20 08 70 05 48 00 88 00 f0 a2 fb")
MODE_ADDR = (0x030005A8).to_bytes(4, "little")
WINDOW_RETAIL = (0x0202E87C).to_bytes(4, "little")
WINDOW_DEBUG = (0x0202EB20).to_bytes(4, "little")

NEXT_PREFIX = bytes.fromhex("00 b5 03 48 c0 78 01 28 04 d0 01 20 03 e0")
NEXT_SUFFIX = bytes.fromhex("00 20 02 bc 08 47")
PLAYER_AVATAR_RETAIL = 0x0202E858
PLAYER_AVATAR_DEBUG = 0x0202EAFC

def sha256(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()

def verify_next(data: bytes, start: int, player_avatar_addr: int) -> None:
    func = data[start:start + 0x1C]
    assert func[:14] == NEXT_PREFIX
    assert func[16:20] == player_avatar_addr.to_bytes(4, "little")
    assert func[20:26] == NEXT_SUFFIX

def main() -> None:
    p = argparse.ArgumentParser(description="Verify German Pokemon Ruby field_message_box module")
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

    assert len(r0) == len(r1) == len(dbg) == 0x24C
    assert r0 == r1
    assert sha256(r0) == RETAIL_SHA256
    assert sha256(r1) == RETAIL_SHA256
    assert sha256(dbg) == DEBUG_SHA256

    assert DEBUG[0] - RETAIL[0] == 0x4600
    assert DEBUG[1] - RETAIL[1] == 0x4600

    assert r0[:16] == ENTRY
    assert dbg[:16] == ENTRY

    assert r0.count(MODE_ADDR) == 11
    assert dbg.count(MODE_ADDR) == 11
    assert r0.count(WINDOW_RETAIL) == 9
    assert dbg.count(WINDOW_DEBUG) == 9

    verify_next(rev0, RETAIL[1], PLAYER_AVATAR_RETAIL)
    verify_next(rev1, RETAIL[1], PLAYER_AVATAR_RETAIL)
    verify_next(debug, DEBUG[1], PLAYER_AVATAR_DEBUG)

    print("German field_message_box verification passed")
    print("Retail Rev0/Rev1: 0x08064DB4..0x08065000, 0x24C bytes")
    print("Debug:            0x080693B4..0x08069600, 0x24C bytes")
    print("Accumulated Retail->Debug delta remains +0x4600")
    print("Next: event_object_lock / walkrun_is_standing_still")

if __name__ == "__main__":
    main()
