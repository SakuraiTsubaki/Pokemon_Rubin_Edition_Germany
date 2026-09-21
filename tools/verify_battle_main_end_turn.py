#!/usr/bin/env python3
import argparse
import hashlib
from pathlib import Path

REV0_SHA1="1c2a53332382e14dab8815e3a6dd81ad89534050"
REV1_SHA1="424740be1fc67a5ddb954794443646e6aeee2c1b"
DEBUG_SHA1="ca5e3d415c4b47353a73a616878ba833f3648b7a"

RETAIL=(0x13AC4,0x141BC)
DEBUG=(0x16B4C,0x17244)
DELTA=0x3088

RETAIL_SHA256="2067deeccc15b2bd4a056bd4c9d76a3d1b32edc3da4ef1e4ce3d81aa32bedaaa"
DEBUG_SHA256="270e1c3605cec26515a6c387b0c12ac89884a0f4654eaadc5ab86cce2e22f666"

STARTS=[80580,80748,81208,81328,81436,81520,81788,81868,82012,82052,82216,82320]

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
    assert sha256(r1[rs:re]) == RETAIL_SHA256
    assert sha256(d[ds:de]) == DEBUG_SHA256
    assert re-rs == de-ds == 1784

    for off in STARTS:
        doff=off+DELTA
        assert r1[off:off+2] == d[doff:doff+2], (hex(off),hex(doff))

    # Next function begins with identical Thumb prologue in both profiles.
    assert r1[0x141BC:0x141BE] == d[0x17244:0x17246]

    print("German end-turn/post-battle lifecycle verification passed")
    print("Functions:",len(STARTS))
    print("Stable Debug delta: +0x3088")
    print("Next: HandleAction_UseMove")

if __name__=="__main__":
    main()
