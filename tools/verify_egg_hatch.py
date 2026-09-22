#!/usr/bin/env python3
import argparse, hashlib
from pathlib import Path
R=(0x42BC8,0x43A60); D=(0x46D44,0x47BDC)
R_SHA="f588c592f49c79df973673fae1a61b27e72ade82e4e4f83c2c8b7c5f46112749"
D_SHA="2c9dea76d3666146f7d70064330d2ca25a3996912f475fea3cf9663602f0986b"
def h(x): return hashlib.sha256(x).hexdigest()
def main():
 p=argparse.ArgumentParser(); p.add_argument("--rev0",type=Path,required=True); p.add_argument("--rev1",type=Path,required=True); p.add_argument("--debug",type=Path,required=True)
 a=p.parse_args(); r0=a.rev0.read_bytes(); r1=a.rev1.read_bytes(); d=a.debug.read_bytes()
 assert r0[R[0]:R[1]]==r1[R[0]:R[1]]
 assert h(r1[R[0]:R[1]])==R_SHA and h(d[D[0]:D[1]])==D_SHA
 assert R[1]-R[0]==D[1]-D[0]==0xE98
 assert D[0]-R[0]==0x417C and D[1]-R[1]==0x417C
 assert r1[0x43A60:0x43A64]==bytes.fromhex("09 20 70 47")
 assert d[0x47BDC:0x47BE0]==bytes.fromhex("09 20 70 47")
 print("German egg_hatch verification passed")
 print("Module size: 0xE98; stable Debug delta +0x417C")
 print("Next: battle_interface / do_nothing")
if __name__=="__main__": main()
