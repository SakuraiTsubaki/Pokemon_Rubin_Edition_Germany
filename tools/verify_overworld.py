#!/usr/bin/env python3
import argparse, hashlib
from pathlib import Path

R=(0x5329C,0x562D0)
D=(0x575AC,0x5A7B8)
R_SHA="357ca0add3b748d55f7849c99ab06da784968f5b4be7717916479fe9904962c9"
D_SHA="37705f2c85c5669fd49a96d2bf8089eba33c35e05fd07d95610b9fc607631dbc"

def h(x): return hashlib.sha256(x).hexdigest()

def main():
 p=argparse.ArgumentParser()
 p.add_argument("--rev0",type=Path,required=True)
 p.add_argument("--rev1",type=Path,required=True)
 p.add_argument("--debug",type=Path,required=True)
 a=p.parse_args()
 r0=a.rev0.read_bytes(); r1=a.rev1.read_bytes(); d=a.debug.read_bytes()

 assert r0[R[0]:R[1]] == r1[R[0]:R[1]]
 assert h(r1[R[0]:R[1]]) == R_SHA
 assert h(d[D[0]:D[1]]) == D_SHA
 assert R[1]-R[0] == 0x3034
 assert D[1]-D[0] == 0x320C
 assert (D[1]-D[0])-(R[1]-R[0]) == 0x1D8
 assert D[0]-R[0] == 0x4310
 assert D[1]-R[1] == 0x44E8

 # DoWhiteOut entry.
 assert r1[0x5329C:0x5329E] == bytes.fromhex("00 b5")
 assert d[0x575AC:0x575AE] == bytes.fromhex("00 b5")

 # fieldmap GetMapHeaderFromConnection fingerprint before profile-specific BL displacement.
 assert r1[0x562D0:0x562D8] == bytes.fromhex("00 b5 02 7a 41 7a 10 1c")
 assert d[0x5A7B8:0x5A7C0] == bytes.fromhex("00 b5 02 7a 41 7a 10 1c")

 print("German overworld verification passed")
 print("Retail 0x3034; Debug 0x320C; growth 0x1D8")
 print("Next: fieldmap at accumulated delta +0x44E8")

if __name__=="__main__": main()
