#!/usr/bin/env python3
import argparse
import hashlib
import struct
from pathlib import Path

REV0_SHA1 = "1c2a53332382e14dab8815e3a6dd81ad89534050"
REV1_SHA1 = "424740be1fc67a5ddb954794443646e6aeee2c1b"
DEBUG_SHA1 = "ca5e3d415c4b47353a73a616878ba833f3648b7a"

RETAIL_START = 0x9890
RETAIL_END = 0xA3C8
DEBUG_START = 0x9A70
DEBUG_END = 0xA5A8

RETAIL_SLICE_SHA256 = "62bd4806097ce06e18050399c4221536613ffa164142b86ccad8433f0d355043"
DEBUG_SLICE_SHA256 = "4d8026c08d81e7f60d7d15bff838b0703b25d018ccafb6306e431ada5ff49a39"

def sha1(data):
    return hashlib.sha1(data).hexdigest()

def sha256(data):
    return hashlib.sha256(data).hexdigest()

def u32(data, off):
    return struct.unpack_from("<I", data, off)[0]

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
    assert sha256(retail1) == RETAIL_SLICE_SHA256
    assert sha256(debug) == DEBUG_SLICE_SHA256

    # Callback/function-entry fingerprints.
    assert r1[0x9890:0x9892] == b"\x00\xB5"
    assert r1[0x98A8:0x98AA] == b"\x00\xB5"
    assert r1[0x98D4:0x98D6] == b"\x30\xB5"
    assert r1[0x9A44:0x9A46] == b"\xF0\xB5"
    assert r1[0xA310:0xA312] == b"\x10\xB5"
    assert r1[0xA390:0xA392] == b"\x00\xB5"

    assert dbg[0x9A70:0x9A72] == b"\x00\xB5"
    assert dbg[0x9AB4:0x9AB6] == b"\x30\xB5"
    assert dbg[0x9C24:0x9C26] == b"\xF0\xB5"
    assert dbg[0xA4F0:0xA4F2] == b"\x10\xB5"
    assert dbg[0xA570:0xA572] == b"\x00\xB5"

    # SaveBlock2 base pointers used by PrintPlayerName.
    assert u32(r1, 0xA30C) == 0x02024EA4
    assert u32(dbg, 0xA4EC) == 0x02025148

    # German-only display geometry in PrintPlayTime.
    assert r1[0xA316:0xA31C] == bytes.fromhex("7c 21 18 22 01 23")
    assert dbg[0xA4F6:0xA4FC] == bytes.fromhex("7c 21 18 22 01 23")
    assert bytes.fromhex("28 22 01 23") in r1[0xA310:0xA350]
    assert bytes.fromhex("17 21 03 22") in r1[0xA310:0xA350]

    # German badge-label and badge-count pixel positions.
    assert r1[0xA396:0xA39C] == bytes.fromhex("7c 21 28 22 01 23")
    assert bytes.fromhex("cd 21 28 22 01 23") in r1[0xA390:0xA3C8]
    assert dbg[0xA576:0xA57C] == bytes.fromhex("7c 21 28 22 01 23")
    assert bytes.fromhex("cd 21 28 22 01 23") in dbg[0xA570:0xA5A8]

    print("German main-menu core verification passed")
    print("Retail core SHA-256:", RETAIL_SLICE_SHA256)
    print("Debug core SHA-256:", DEBUG_SLICE_SHA256)

if __name__ == "__main__":
    main()
