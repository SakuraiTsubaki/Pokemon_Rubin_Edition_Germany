#!/usr/bin/env python3
import argparse, hashlib
from pathlib import Path
R=(0x40FE0,0x41110); D=(0x4515C,0x4528C)
R_SHA="0d60aa9e91ffd588e2d962a26e20f137a0e4b34fc6fc4eddde613c11890bca22"
D_SHA="d1c9e7698dc63c6b0e4a22b887172ed5aff2e9d91c5be92e4e2a64bd15d3d2bb"
STARTS=[0x40FE0,0x40FF4,0x4100C,0x41024,0x4110C]
def h(x): return hashlib.sha256(x).hexdigest()
def main():
 p=argparse.ArgumentParser(); p.add_argument("--rev0",type=Path,required=True); p.add_argument("--rev1",type=Path,required=True); p.add_argument("--debug",type=Path,required=True)
 a=p.parse_args(); r0=a.rev0.read_bytes(); r1=a.rev1.read_bytes(); d=a.debug.read_bytes()
 assert r0[R[0]:R[1]]==r1[R[0]:R[1]]
 assert h(r1[R[0]:R[1]])==R_SHA and h(d[D[0]:D[1]])==D_SHA
 assert R[1]-R[0]==D[1]-D[0]==0x130
 for ro in STARTS:
  do=ro+0x417C
  assert r1[ro:ro+2]==d[do:do+2]
 assert r1[0x41110:0x41114]==d[0x4528C:0x45290]
 print("German trainer-class localization module verification passed")
if __name__=="__main__": main()
