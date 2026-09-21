#!/usr/bin/env python3
import argparse
import hashlib
from pathlib import Path

REV0_SHA1="1c2a53332382e14dab8815e3a6dd81ad89534050"
REV1_SHA1="424740be1fc67a5ddb954794443646e6aeee2c1b"
DEBUG_SHA1="ca5e3d415c4b47353a73a616878ba833f3648b7a"

RETAIL=(0xE998,0xF200)
DEBUG=(0xEC0C,0xF4C0)
RETAIL_SHA256="d8753f7da7f3354ddd5839e7de318ec8c9f0f289789f5285fe44c05a4e69ca4e"
DEBUG_SHA256="493145436c8a0f706ed56e4950e98e0b54aae0556d93754c06285174eaf0e89d"

R=[0xE998,0xE9CC,0xEBC0,0xEC80,0xECDC,0xEE18,0xEE70,0xF200]
D=[0xEC0C,0xEC40,0xEE54,0xEF14,0xEF70,0xF0AC,0xF104,0xF4C0]

def sha1(x): return hashlib.sha1(x).hexdigest()
def sha256(x): return hashlib.sha256(x).hexdigest()

def main():
    p=argparse.ArgumentParser()
    p.add_argument("--rev0",type=Path,required=True)
    p.add_argument("--rev1",type=Path,required=True)
    p.add_argument("--debug",type=Path,required=True)
    a=p.parse_args()
    r0=a.rev0.read_bytes(); r1=a.rev1.read_bytes(); d=a.debug.read_bytes()

    assert sha1(r0)==REV0_SHA1
    assert sha1(r1)==REV1_SHA1
    assert sha1(d)==DEBUG_SHA1

    rs,re=RETAIL; ds,de=DEBUG
    assert r0[rs:re] == r1[rs:re]
    assert sha256(r1[rs:re]) == RETAIL_SHA256
    assert sha256(d[ds:de]) == DEBUG_SHA256

    # Function sizes and accumulated debug displacement.
    expected_deltas=[0x274,0x274,0x294,0x294,0x294,0x294,0x294]
    for i in range(7):
        assert D[i]-R[i] == expected_deltas[i]
        assert r1[R[i]:R[i]+2] == d[D[i]:D[i]+2]

    assert (D[2]-D[1])-(R[2]-R[1]) == 0x20
    assert (D[7]-D[6])-(R[7]-R[6]) == 0x2C
    assert D[7]-R[7] == 0x2C0

    print("German battle_main initialization verification passed")
    print("Debug growth: 0x20 + 0x2C = 0x4C")
    print("Next accumulated debug delta: +0x2C0")

if __name__=="__main__":
    main()
