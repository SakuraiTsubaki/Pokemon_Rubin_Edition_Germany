#!/usr/bin/env python3
import argparse
import hashlib
from pathlib import Path

REV0_SHA1 = "1c2a53332382e14dab8815e3a6dd81ad89534050"
REV1_SHA1 = "424740be1fc67a5ddb954794443646e6aeee2c1b"
DEBUG_SHA1 = "ca5e3d415c4b47353a73a616878ba833f3648b7a"

RETAIL_START = 0xA3C8
RETAIL_END = 0xB234
DEBUG_START = 0xA5A8
DEBUG_END = 0xB414
DELTA = 0x1E0

RETAIL_SHA256 = "8c81b39a88fe3b5d1a12eaee333692fee3d5ca87e1d52f2f62426572ba02e73e"
DEBUG_SHA256 = "f7c78291c4f9031b5585252d2e9a7099c7598c4a3dac258568ebf47f4aaf5938"

TASKS = [
    0xA3C8,
    0xA4B4,
    0xA52C,
    0xA59C,
    0xA5E8,
    0xA618,
    0xA68C,
    0xA6FC,
    0xA738,
    0xA780,
    0xA7F8,
    0xA83C,
    0xA8EC,
    0xA930,
    0xA970,
    0xA9A8,
    0xAA48,
    0xAAF0,
    0xAB48,
    0xAB88,
    0xABC0,
    0xAC80,
    0xACC0,
    0xAD0C,
    0xAD44,
    0xADF4,
    0xAE2C,
    0xAF1C,
    0xAFC8,
    0xB0A8,
    0xB158,
    0xB194,
    0xB208,
]

def sha1(data):
    return hashlib.sha1(data).hexdigest()

def sha256(data):
    return hashlib.sha256(data).hexdigest()

def main():
    p = argparse.ArgumentParser()
    p.add_argument("--rev0", required=True, type=Path)
    p.add_argument("--rev1", required=True, type=Path)
    p.add_argument("--debug", required=True, type=Path)
    args = p.parse_args()

    r0 = args.rev0.read_bytes()
    r1 = args.rev1.read_bytes()
    dbg = args.debug.read_bytes()

    assert sha1(r0) == REV0_SHA1
    assert sha1(r1) == REV1_SHA1
    assert sha1(dbg) == DEBUG_SHA1

    retail0 = r0[RETAIL_START:RETAIL_END]
    retail1 = r1[RETAIL_START:RETAIL_END]
    debug = dbg[DEBUG_START:DEBUG_END]

    assert retail0 == retail1
    assert len(retail1) == len(debug) == 3692
    assert sha256(retail1) == RETAIL_SHA256
    assert sha256(debug) == DEBUG_SHA256

    for addr in TASKS:
        daddr = addr + DELTA
        assert r1[addr:addr+4] == dbg[daddr:daddr+4], (hex(addr), hex(daddr))

    assert r1[0xB234:0xB238] == bytes.fromhex("30 b5 83 b0")
    assert dbg[0xB414:0xB418] == bytes.fromhex("30 b5 83 b0")

    print("German new-game speech verification passed")
    print("States:", len(TASKS))
    print("Retail SHA-256:", RETAIL_SHA256)
    print("Debug SHA-256:", DEBUG_SHA256)
    print("Debug address delta: +0x1E0")

if __name__ == "__main__":
    main()
