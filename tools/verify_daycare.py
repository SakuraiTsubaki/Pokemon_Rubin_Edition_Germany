#!/usr/bin/env python3
import argparse, hashlib
from pathlib import Path
R=(0x415D4,0x42BC8); D=(0x45750,0x46D44)
R_SHA="a10fe130a88cfa83f233a05e999082bcb943f7ed182b7dbdbf1535b4c55cc194"
D_SHA="9167ba6edee571b923b36ee2048ec086090c21b64d2e326fd9240ebd44e0ef65"
def h(x): return hashlib.sha256(x).hexdigest()
def main():
 p=argparse.ArgumentParser(); p.add_argument("--rev0",type=Path,required=True); p.add_argument("--rev1",type=Path,required=True); p.add_argument("--debug",type=Path,required=True)
 a=p.parse_args(); r0=a.rev0.read_bytes(); r1=a.rev1.read_bytes(); d=a.debug.read_bytes()
 assert r0[R[0]:R[1]]==r1[R[0]:R[1]]
 assert h(r1[R[0]:R[1]])==R_SHA and h(d[D[0]:D[1]])==D_SHA
 assert R[1]-R[0]==D[1]-D[0]==0x15F4
 assert D[0]-R[0]==0x417C and D[1]-R[1]==0x417C
 assert r1[0x42BC8:0x42BD0]==d[0x46D44:0x46D4C]
 print("German daycare verification passed")
 print("Module size: 0x15F4; stable Debug delta +0x417C")
 print("Next: egg_hatch / CreatedHatchedMon")
if __name__=="__main__": main()
