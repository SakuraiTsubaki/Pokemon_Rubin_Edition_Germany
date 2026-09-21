#!/usr/bin/env python3
import argparse
import hashlib
from pathlib import Path

REV0_SHA1 = "1c2a53332382e14dab8815e3a6dd81ad89534050"
REV1_SHA1 = "424740be1fc67a5ddb954794443646e6aeee2c1b"
DEBUG_SHA1 = "ca5e3d415c4b47353a73a616878ba833f3648b7a"

HELPER_RETAIL = (0xB234, 0xBA2C)
HELPER_DEBUG = (0xB414, 0xBC0C)
MODULE_RETAIL = (0x9890, 0xBA2C)
MODULE_DEBUG = (0x9A70, 0xBC0C)

HELPER_RETAIL_SHA256 = "844fad2a520d6b7b769786399de8d3c5a5e351cb0f97a7465f67df53e430d031"
HELPER_DEBUG_SHA256 = "74260300a0830783b57573d9defeafaa4084e65025418d2631ba9508bd5a3757"
MODULE_RETAIL_SHA256 = "6aab6354e6342ade67758f5a293db2e45a9c27a0adbe983487eb28f752f0ea06"
MODULE_DEBUG_SHA256 = "86c703c4790622849580374f46b5bb0a2974757e0d6b0afbf66925c98e2307c7"

HELPERS = [
    0xB234,
    0xB410,
    0xB414,
    0xB430,
    0xB4A0,
    0xB5C0,
    0xB62C,
    0xB69C,
    0xB708,
    0xB77C,
    0xB7E8,
    0xB828,
    0xB894,
    0xB8D4,
    0xB934,
    0xB944,
    0xB9CC,
    0xB9DC,
]

def sha1(data):
    return hashlib.sha1(data).hexdigest()

def sha256(data):
    return hashlib.sha256(data).hexdigest()

def main():
    p = argparse.ArgumentParser()
    p.add_argument("--rev0", type=Path, required=True)
    p.add_argument("--rev1", type=Path, required=True)
    p.add_argument("--debug", type=Path, required=True)
    args = p.parse_args()

    r0 = args.rev0.read_bytes()
    r1 = args.rev1.read_bytes()
    dbg = args.debug.read_bytes()

    assert sha1(r0) == REV0_SHA1
    assert sha1(r1) == REV1_SHA1
    assert sha1(dbg) == DEBUG_SHA1

    a,b = HELPER_RETAIL
    da,db = HELPER_DEBUG
    assert r0[a:b] == r1[a:b]
    assert sha256(r1[a:b]) == HELPER_RETAIL_SHA256
    assert sha256(dbg[da:db]) == HELPER_DEBUG_SHA256

    a,b = MODULE_RETAIL
    da,db = MODULE_DEBUG
    assert r0[a:b] == r1[a:b]
    assert sha256(r1[a:b]) == MODULE_RETAIL_SHA256
    assert sha256(dbg[da:db]) == MODULE_DEBUG_SHA256
    assert sum(x != y for x,y in zip(r1[a:b], dbg[da:db])) == 899

    for off in HELPERS:
        doff = off + 0x1E0
        # Function-entry forms align. BL immediates in tiny wrappers may differ.
        if off not in (0xB934, 0xB9CC):
            assert r1[off:off+4] == dbg[doff:doff+4], (hex(off), hex(doff))

    # Main-menu ends before the next module.
    assert r1[0xBA2C:0xBA2E] == bytes.fromhex("00 b5")
    assert dbg[0xBC0C:0xBC0E] == bytes.fromhex("00 b5")

    print("German main-menu module verification passed")
    print("Retail module bytes:", MODULE_RETAIL[1] - MODULE_RETAIL[0])
    print("Debug module bytes:", MODULE_DEBUG[1] - MODULE_DEBUG[0])
    print("Next module starts at retail 0x0800BA2C / debug 0x0800BC0C")

if __name__ == "__main__":
    main()
