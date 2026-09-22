#!/usr/bin/env python3
import argparse, hashlib
from pathlib import Path

R=(0x43A60,0x46234)
D=(0x47BDC,0x4A400)
R_SHA="cf178beb5a639d1932696c9eba1385bd0735b64e70c8cd05c7bf96d5a7061b0f"
D_SHA="4dbf0b7b85a017c2b041e40247d484cc9edb84c0eb5f65d9012bd3f4308366f1"

def h(x): return hashlib.sha256(x).hexdigest()

def main():
 p=argparse.ArgumentParser()
 p.add_argument("--rev0",type=Path,required=True)
 p.add_argument("--rev1",type=Path,required=True)
 p.add_argument("--debug",type=Path,required=True)
 a=p.parse_args()
 r0=a.rev0.read_bytes(); r1=a.rev1.read_bytes(); d=a.debug.read_bytes()

 assert r0[R[0]:R[1]]==r1[R[0]:R[1]]
 assert h(r1[R[0]:R[1]])==R_SHA
 assert h(d[D[0]:D[1]])==D_SHA

 assert R[1]-R[0]==0x27D4
 assert D[1]-D[0]==0x2824
 assert (D[1]-D[0])-(R[1]-R[0])==0x50

 assert D[0]-R[0]==0x417C
 assert D[1]-R[1]==0x41CC

 # First battle-interface function: return 9.
 assert r1[0x43A60:0x43A64]==bytes.fromhex("09 20 70 47")
 assert d[0x47BDC:0x47BE0]==bytes.fromhex("09 20 70 47")

 # smokescreen boundary / first function prefix
 assert r1[0x46234:0x46244]==d[0x4A400:0x4A410]

 print("German battle_interface verification passed")
 print("Retail size 0x27D4; Debug size 0x2824")
 print("Debug growth 0x50 = 0x0C + 0x44")
 print("Next: smokescreen at accumulated delta +0x41CC")

if __name__=="__main__": main()
