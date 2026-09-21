#!/usr/bin/env python3
import argparse
import hashlib
from pathlib import Path

REV0_SHA1="1c2a53332382e14dab8815e3a6dd81ad89534050"
REV1_SHA1="424740be1fc67a5ddb954794443646e6aeee2c1b"
DEBUG_SHA1="ca5e3d415c4b47353a73a616878ba833f3648b7a"

R=(0x1C490,0x1DAC0)
D=(0x1FA08,0x21038)
DELTA=0x3578
R_SHA="7bbe796fc3a53a0a91baac9b06a9534c0c70c213dd3e009516d8ee1c847a3061"
D_SHA="2e50618d4821ab4a88f1ab54ec0d8c72ffc4e118d7b6e9dcaea5005042ceed6b"
STARTS=[0x1C490,0x1C81C,0x1C870,0x1CA4C,0x1CBC0,0x1CCCC,0x1CDC0,0x1CE98,0x1D110,0x1D39C,0x1D454,0x1D630,0x1D748,0x1D784,0x1D934,0x1DAC0]

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
    assert r0[R[0]:R[1]] == r1[R[0]:R[1]]
    assert sha256(r1[R[0]:R[1]]) == R_SHA
    assert sha256(d[D[0]:D[1]]) == D_SHA
    assert (R[1]-R[0]) == (D[1]-D[0]) == 5680

    for ro in STARTS:
        do=ro+DELTA
        assert r1[ro:ro+2] == d[do:do+2], (hex(ro),hex(do))

    print("German accuracy/damage/type core verification passed")
    print("Functions/helpers:",len(STARTS)-1)
    print("Stable Debug delta: +0x3578")
    print("Next opcode: 0x09 atk09_attackanimation")

if __name__=="__main__":
    main()
