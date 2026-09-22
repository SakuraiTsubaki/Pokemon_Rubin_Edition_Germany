#!/usr/bin/env python3
import argparse, hashlib
from pathlib import Path

REV0_SHA1="1c2a53332382e14dab8815e3a6dd81ad89534050"
REV1_SHA1="424740be1fc67a5ddb954794443646e6aeee2c1b"
DEBUG_SHA1="ca5e3d415c4b47353a73a616878ba833f3648b7a"

R=(0x3BC00,0x3C51C)
D=(0x3FD7C,0x40698)
R_SHA="805c2ac86214fd252e5c33331c5b6d2de4b842216a4b150fca390fbf24412288"
D_SHA="34c128142c4201f5333f913fbbf677f57402b06052501d3abfc45b36e3a80006"

def sha1(x): return hashlib.sha1(x).hexdigest()
def sha256(x): return hashlib.sha256(x).hexdigest()

def main():
 p=argparse.ArgumentParser()
 p.add_argument("--rev0",type=Path,required=True)
 p.add_argument("--rev1",type=Path,required=True)
 p.add_argument("--debug",type=Path,required=True)
 a=p.parse_args()
 r0=a.rev0.read_bytes(); r1=a.rev1.read_bytes(); d=a.debug.read_bytes()
 assert sha1(r0)==REV0_SHA1 and sha1(r1)==REV1_SHA1 and sha1(d)==DEBUG_SHA1
 assert r0[R[0]:R[1]]==r1[R[0]:R[1]]
 assert sha256(r1[R[0]:R[1]])==R_SHA
 assert sha256(d[D[0]:D[1]])==D_SHA
 assert R[1]-R[0]==D[1]-D[0]==2332
 assert D[0]-R[0]==0x417C and D[1]-R[1]==0x417C
 assert r1[0x3C51C:0x3C51E]==bytes.fromhex("70 b5")
 assert d[0x40698:0x4069A]==bytes.fromhex("70 b5")
 print("German CalculateBaseDamage verification passed")
 print("Single function size: 0x91C")
 print("Next: pokemon_2 at +0x417C")

if __name__=="__main__": main()
