#!/usr/bin/env python3
import argparse
import hashlib
from pathlib import Path

REV0_SHA1="1c2a53332382e14dab8815e3a6dd81ad89534050"
REV1_SHA1="424740be1fc67a5ddb954794443646e6aeee2c1b"
DEBUG_SHA1="ca5e3d415c4b47353a73a616878ba833f3648b7a"

ABILITY_R=(0x184F8,0x1A184)
ABILITY_D=(0x1B580,0x1D6D8)
EXEC_R=(0x1A184,0x1A1C0)
EXEC_D=(0x1D6D8,0x1D714)
PUSH_R=(0x1A1C0,0x1A200)
PUSH_D=(0x1D714,0x1D754)

ABILITY_R_SHA="bebef06996411234536f5acf13912386da5efa32b2c5e934d41b10106f0b577a"
ABILITY_D_SHA="6e414606a8371821ce31d9b66b4721ce57a25f1075587264c29864aff7703ab5"

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

    ar0=r0[ABILITY_R[0]:ABILITY_R[1]]
    ar1=r1[ABILITY_R[0]:ABILITY_R[1]]
    ad=d[ABILITY_D[0]:ABILITY_D[1]]
    assert ar0==ar1
    assert sha256(ar1)==ABILITY_R_SHA
    assert sha256(ad)==ABILITY_D_SHA

    assert len(ar1)==7308
    assert len(ad)==8536
    assert len(ad)-len(ar1)==0x4CC

    assert EXEC_D[0]-EXEC_R[0]==0x3554
    assert PUSH_D[0]-PUSH_R[0]==0x3554
    assert PUSH_R[1]-PUSH_R[0] == PUSH_D[1]-PUSH_D[0] == 64
    assert EXEC_R[1]-EXEC_R[0] == EXEC_D[1]-EXEC_D[0] == 60

    assert r1[0x1A200:0x1A202] == bytes.fromhex("f0 b5")
    assert d[0x1D754:0x1D756] == bytes.fromhex("f0 b5")

    print("German AbilityBattleEffects boundary verification passed")
    print("Retail bytes:",len(ar1))
    print("Debug bytes:",len(ad))
    print("Debug-only growth in dispatcher: 0x4CC")
    print("New accumulated Debug delta: +0x3554")

if __name__=="__main__":
    main()
