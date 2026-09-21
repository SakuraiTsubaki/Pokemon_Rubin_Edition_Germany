#!/usr/bin/env python3
import argparse
import hashlib
from pathlib import Path

REV0_SHA1="1c2a53332382e14dab8815e3a6dd81ad89534050"
REV1_SHA1="424740be1fc67a5ddb954794443646e6aeee2c1b"
DEBUG_SHA1="ca5e3d415c4b47353a73a616878ba833f3648b7a"

RETAIL=(0x15FD0,0x184F8)
DEBUG=(0x19058,0x1B580)
DELTA=0x3088
RETAIL_SHA="f60d0efa94a631b184c9fe1b08ecd9a71752f648499ccb892a0efa7b7abc82fa"
DEBUG_SHA="5f92f831ecff7a256b50e990ba2f6e78dbcbd89a7d7b9700de8ed45c0b80da45"

STARTS=[90064,91948,94896,95608,96412,96492,98796,99212]

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
    assert re-rs == de-ds == 9512

    for off in STARTS:
        doff=off+DELTA
        assert r1[off:off+2] == d[doff:doff+2], (hex(off),hex(doff))

    assert r1[0x184F8:0x184FA] == bytes.fromhex("f0 b5")
    assert d[0x1B580:0x1B582] == bytes.fromhex("f0 b5")

    print("German battle_util end-turn/cancellation verification passed")
    print("Functions:",len(STARTS))
    print("Stable Debug delta: +0x3088")
    print("Next: AbilityBattleEffects")

if __name__=="__main__":
    main()
