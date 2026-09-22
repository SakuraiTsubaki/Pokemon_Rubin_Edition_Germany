#!/usr/bin/env python3
import argparse, hashlib
from pathlib import Path
R=(0x43A60,0x46558); D=(0x47BDC,0x4A724)
R_SHA="3d9b4de9cf84eb5e822465da4d6da33b16f863c2171db1e45bc67a11c34c748b"
D_SHA="c4ab84b3d9f3b3130081fe21e08026c878b28bdfb58fc1bdc5106a0e3c7f523a"
def h(x): return hashlib.sha256(x).hexdigest()
def main():
 p=argparse.ArgumentParser(); p.add_argument("--rev0",type=Path,required=True); p.add_argument("--rev1",type=Path,required=True); p.add_argument("--debug",type=Path,required=True)
 a=p.parse_args(); r0=a.rev0.read_bytes(); r1=a.rev1.read_bytes(); d=a.debug.read_bytes()
 assert r0[R[0]:R[1]]==r1[R[0]:R[1]]
 assert h(r1[R[0]:R[1]])==R_SHA and h(d[D[0]:D[1]])==D_SHA
 assert R[1]-R[0]==0x2AF8 and D[1]-D[0]==0x2B48
 assert (D[1]-D[0])-(R[1]-R[0])==0x50
 assert D[0]-R[0]==0x417C and D[1]-R[1]==0x41CC
 assert r1[0x43A60:0x43A64]==bytes.fromhex("09 20 70 47")
 assert r1[0x46558:0x46568]==d[0x4A724:0x4A734]
 print("German battle_interface corrected-boundary verification passed")
 print("Retail 0x2AF8; Debug 0x2B48; growth 0x50")
 print("Next: smokescreen at +0x41CC")
if __name__=="__main__": main()
