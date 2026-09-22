#!/usr/bin/env python3
import argparse
import hashlib
from pathlib import Path

RETAIL = (0x6A7C0, 0x6B21C)
DEBUG = (0x6EE9C, 0x6FB44)

RETAIL_SHA256 = "77007b88f74c8d930d9ca9a753bb307fee59a46903a68276d4a183e80057d9f9"
DEBUG_SHA256 = "ba808e9fe207c8925504f661ae8ff1e6c19079a15eff92e50319d112e0f43914"

ENTRY = bytes.fromhex(
    "00 b5 03 1c 0a 4a 2e 20 19 5e 88 00 40 18 c0 00 "
    "80 18 0c 22 81 5e 30 22 98 5e 81 42 7b d0 19 86"
)

DEBUG_COMMON_END = 0x6F8F8
DEBUG_TAIL_SHA256 = "15903c364ae087117620114b83df44d784f8e2ded4f3177516fbd4c0db3aeccb"
DEBUG_FUNCTIONS = (
    (0x6F8F8, 0x6F908, "b9d46c8666dc6f80f76512bbb1f37a39d6138b241016bf33b02dd9058a03c673"),
    (0x6F908, 0x6F99C, "3b79039f0fae18532c2e87e45a8e09cd5f8e5c50c615b1d315b4e27f75d5b52b"),
    (0x6F99C, 0x6F9B8, "95685efd13811c1e99ec0d2275589c0f9c557ba76f15b42a506096e2de3f3fa5"),
    (0x6F9B8, 0x6F9E4, "33a72a98a81c617bdbff0da2962378a04404e79c7e9561848448f4086fad1c16"),
    (0x6F9E4, 0x6FB44, "69ffc50642ac5d2b7ba661e3045389c007b3426f49e56243afd2242a39b0b5c0"),
)

PARTY_RETAIL = bytes.fromhex("70 b5 81 b0 95 f7 52 fb 95 f7 76 fb")
PARTY_DEBUG = bytes.fromhex("70 b5 81 b0 90 f7 be fe 90 f7 e2 fe")

def sha256(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()

def main() -> None:
    p = argparse.ArgumentParser(description="Verify German Pokemon Ruby reset_rtc_screen module")
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

    assert len(r0) == len(r1) == 0xA5C
    assert len(dbg) == 0xCA8
    assert len(dbg) - len(r0) == 0x24C

    assert r0 == r1
    assert sha256(r0) == RETAIL_SHA256
    assert sha256(r1) == RETAIL_SHA256
    assert sha256(dbg) == DEBUG_SHA256

    assert DEBUG[0] - RETAIL[0] == 0x46DC
    assert DEBUG[1] - RETAIL[1] == 0x4928

    assert r0.startswith(ENTRY)
    assert dbg.startswith(ENTRY)

    assert DEBUG_COMMON_END - DEBUG[0] == len(r0)
    tail = debug[DEBUG_COMMON_END:DEBUG[1]]
    assert len(tail) == 0x24C
    assert sha256(tail) == DEBUG_TAIL_SHA256

    for start, end, expected_hash in DEBUG_FUNCTIONS:
        assert sha256(debug[start:end]) == expected_hash

    assert rev0[RETAIL[1]:RETAIL[1] + len(PARTY_RETAIL)] == PARTY_RETAIL
    assert rev1[RETAIL[1]:RETAIL[1] + len(PARTY_RETAIL)] == PARTY_RETAIL
    assert debug[DEBUG[1]:DEBUG[1] + len(PARTY_DEBUG)] == PARTY_DEBUG

    print("German reset_rtc_screen verification passed")
    print("Retail Rev0/Rev1: 0x0806A7C0..0x0806B21C, 0xA5C bytes")
    print("Debug:            0x0806EE9C..0x0806FB44, 0xCA8 bytes")
    print("Debug-only tail:  0x0806F8F8..0x0806FB44, 0x24C bytes")
    print("Accumulated Retail->Debug delta changes +0x46DC -> +0x4928")
    print("Next: party_menu / CB2_PartyMenuMain")

if __name__ == "__main__":
    main()
