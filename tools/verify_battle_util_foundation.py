#!/usr/bin/env python3
import argparse
import hashlib
from pathlib import Path

REV0_SHA1="1c2a53332382e14dab8815e3a6dd81ad89534050"
REV1_SHA1="424740be1fc67a5ddb954794443646e6aeee2c1b"
DEBUG_SHA1="ca5e3d415c4b47353a73a616878ba833f3648b7a"

RETAIL=(0x15324,0x15FD0)
DEBUG=(0x183AC,0x19058)
DELTA=0x3088
RETAIL_SHA="f1292d07e15d28e091d388c71f989ba613c06f45d5d2ec118cb625d41576d374"
DEBUG_SHA="8280b41942af994c9ae1979d2a785dc62b13c75e4bdba295b6d15fa59535a05e"

STARTS=[86820,86952,87152,87460,87736,87848,87928,88008,88116,88204,88240,88340,88472,88576,88608,88644,88680,89196,89700,89904]

def sha1(x): return hashlib.sha1(x).hexdigest()
def sha256(x): return hashlib.sha256(x).hexdigest()

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
    assert sha256(r1[rs:re]) == RETAIL_SHA
    assert sha256(d[ds:de]) == DEBUG_SHA
    assert re-rs == de-ds == 3244

    for off in STARTS:
        doff=off+DELTA
        assert r1[off:off+2] == d[doff:doff+2], (hex(off),hex(doff))

    # Tiny stack operations intentionally do not require a PUSH prologue.
    assert r1[0x15A20:0x15A22] == d[0x18AA8:0x18AAA]
    assert r1[0x15A44:0x15A46] == d[0x18ACC:0x18ACE]

    # DoFieldEndTurnEffects is the next routine.
    assert r1[0x15FD0:0x15FD2] == bytes.fromhex("f0 b5")
    assert d[0x19058:0x1905A] == bytes.fromhex("f0 b5")

    print("German battle_util foundation verification passed")
    print("Functions:",len(STARTS))
    print("Move slots: 4 / all-unusable mask: 0xF")
    print("Stable Debug delta: +0x3088")

if __name__=="__main__":
    main()
