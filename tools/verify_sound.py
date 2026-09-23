#!/usr/bin/env python3
import argparse
import hashlib
from pathlib import Path

RETAIL = (0x74F6C, 0x759E4)
DEBUG = (0x7C1D8, 0x7CC50)
RETAIL_SHA256 = "5d126e677f92d1b169d5b26172bb83cb000e0899dbae11ea0d41688826fd531f"
DEBUG_SHA256 = "4c7e9d4d53eadc90f4424f77bf662c1426a9c70371f7aa6991e62d388ec67e30"

ENTRY = bytes.fromhex("00 b5 03 49 00 20 08 70 00 f0 80 f8 01 bc 00 47")
NEXT = bytes.fromhex("f0 b5 4f 46 46 46 c0 b4 22 48 00 21 01 70 22 48 01 70 22 48 01 70 22 48 01 70 22 48 00 21 01 60")

RETAIL_ADDRS = {
    0x030006D4: 11, 0x030006D6: 10, 0x030006D8: 12, 0x030006D9: 4, 0x030006DA: 3,
    0x03004AFC: 3, 0x0202F79C: 6, 0x0202F7A0: 4,
    0x03007390: 15, 0x030073D0: 4, 0x03007410: 4, 0x03007460: 1,
}
DEBUG_ADDRS = {
    0x030006F4: 11, 0x030006F6: 10, 0x030006F8: 12, 0x030006F9: 4, 0x030006FA: 3,
    0x03004BD4: 3, 0x0202FA40: 6, 0x0202FA44: 4,
    0x030074A0: 15, 0x030074E0: 4, 0x03007520: 4, 0x03007570: 1,
}

FANFARE_RETAIL = 0x3896DC
FANFARE_DEBUG = 0x3A386C
FANFARE = [
    (367,80),(370,160),(371,220),(372,220),(368,160),(369,340),
    (378,180),(387,120),(388,710),(389,250),(390,150),(391,160),
]
FANFARE_SHA256 = "b47a9578152cbf53851514486121001deccd59ee7f1d5b7ce0a0c5924f3a9ca8"

TAIL_RETAIL = (0x759BC, 0x759E4)
TAIL_DEBUG = (0x7CC28, 0x7CC50)

def sha256(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()

def verify_refs(chunk: bytes, refs: dict[int, int]) -> None:
    for addr, count in refs.items():
        assert chunk.count(addr.to_bytes(4, "little")) == count, (hex(addr), count)

def fanfare_bytes() -> bytes:
    out = bytearray()
    for song, duration in FANFARE:
        out += song.to_bytes(2, "little")
        out += duration.to_bytes(2, "little")
    return bytes(out)

def main() -> None:
    p = argparse.ArgumentParser(description="Verify German Pokemon Ruby sound module")
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

    assert len(r0) == len(r1) == len(dbg) == 0xA78
    assert r0 == r1
    assert sha256(r0) == RETAIL_SHA256
    assert sha256(r1) == RETAIL_SHA256
    assert sha256(dbg) == DEBUG_SHA256
    assert DEBUG[0] - RETAIL[0] == 0x726C
    assert DEBUG[1] - RETAIL[1] == 0x726C

    assert r0[:16] == ENTRY
    assert dbg[:16] == ENTRY
    verify_refs(r0, RETAIL_ADDRS)
    verify_refs(dbg, DEBUG_ADDRS)

    fan = fanfare_bytes()
    assert len(fan) == 48
    assert rev0[FANFARE_RETAIL:FANFARE_RETAIL+48] == fan
    assert rev1[FANFARE_RETAIL:FANFARE_RETAIL+48] == fan
    assert debug[FANFARE_DEBUG:FANFARE_DEBUG+48] == fan
    assert sha256(fan) == FANFARE_SHA256

    assert TAIL_RETAIL[1] == RETAIL[1]
    assert TAIL_DEBUG[1] == DEBUG[1]
    assert rev0[TAIL_RETAIL[0]:TAIL_RETAIL[1]][-8:] == bytes.fromhex("00 20 02 bc 08 47 00 00")
    assert debug[TAIL_DEBUG[0]:TAIL_DEBUG[1]][-8:] == bytes.fromhex("00 20 02 bc 08 47 00 00")

    assert rev0[RETAIL[1]:RETAIL[1]+len(NEXT)] == NEXT
    assert rev1[RETAIL[1]:RETAIL[1]+len(NEXT)] == NEXT
    assert debug[DEBUG[1]:DEBUG[1]+len(NEXT)] == NEXT

    print("German sound verification passed")
    print("Retail Rev0/Rev1: 0x08074F6C..0x080759E4, 0xA78 bytes")
    print("Debug:            0x0807C1D8..0x0807CC50, 0xA78 bytes")
    print("Fanfare table: 12 entries, byte-identical across profiles")
    print("Accumulated Retail->Debug delta remains +0x726C")
    print("Next: battle_anim / ClearBattleAnimationVars")

if __name__ == "__main__":
    main()
