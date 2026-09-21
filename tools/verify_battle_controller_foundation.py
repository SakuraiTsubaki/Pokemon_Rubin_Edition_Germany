#!/usr/bin/env python3
import argparse
import hashlib
from pathlib import Path

REV0_SHA1 = "1c2a53332382e14dab8815e3a6dd81ad89534050"
REV1_SHA1 = "424740be1fc67a5ddb954794443646e6aeee2c1b"
DEBUG_SHA1 = "ca5e3d415c4b47353a73a616878ba833f3648b7a"

RETAIL = (0xBA2C, 0xC7EC)
DEBUG = (0xBC0C, 0xCA08)

RETAIL_SHA256 = "ed1195f99f35a971e23d8018c26ccdd043155efacb7ec9b3fca5aba8fab1dd6c"
DEBUG_SHA256 = "39f0347ff1bd8a793d2f09bffe6d846fd71a399c279ad2a997924682406c304d"

FUNCTIONS = [
    (0xBA2C, 0xBC0C),
    (0xBA58, 0xBC38),
    (0xBB24, 0xBD40),
    (0xBB7C, 0xBD98),
    (0xBC4C, 0xBE68),
    (0xBF28, 0xC144),
    (0xC070, 0xC28C),
    (0xC0FC, 0xC318),
    (0xC1C4, 0xC3E0),
    (0xC37C, 0xC598),
    (0xC530, 0xC74C),
    (0xC650, 0xC86C),
    (0xC7EC, 0xCA08),
]

def sha1(data):
    return hashlib.sha1(data).hexdigest()

def sha256(data):
    return hashlib.sha256(data).hexdigest()

def main():
    p=argparse.ArgumentParser()
    p.add_argument("--rev0",type=Path,required=True)
    p.add_argument("--rev1",type=Path,required=True)
    p.add_argument("--debug",type=Path,required=True)
    a=p.parse_args()

    r0=a.rev0.read_bytes()
    r1=a.rev1.read_bytes()
    d=a.debug.read_bytes()

    assert sha1(r0)==REV0_SHA1
    assert sha1(r1)==REV1_SHA1
    assert sha1(d)==DEBUG_SHA1

    rs,re=RETAIL
    ds,de=DEBUG
    assert r0[rs:re] == r1[rs:re]
    assert sha256(r1[rs:re]) == RETAIL_SHA256
    assert sha256(d[ds:de]) == DEBUG_SHA256

    assert 0xBB24 - 0xBA58 == 204
    assert 0xBD40 - 0xBC38 == 264
    assert (0xBD40 - 0xBC38) - (0xBB24 - 0xBA58) == 60

    for i,(ro,do) in enumerate(FUNCTIONS):
        expected = 0x1E0 if i < 2 else 0x21C
        assert do-ro == expected, (hex(ro),hex(do),hex(do-ro))
        # Prologue identity where the same high-level routine begins.
        assert r1[ro:ro+2] == d[do:do+2], (hex(ro),hex(do))

    print("German battle-controller foundation verification passed")
    print("Debug-only SetUpBattleVars growth: 60 bytes")
    print("Post-growth address delta: +0x21C")

if __name__=="__main__":
    main()
