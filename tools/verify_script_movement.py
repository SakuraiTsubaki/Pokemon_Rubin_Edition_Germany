#!/usr/bin/env python3
import argparse, hashlib
from pathlib import Path
R=(0xA2224,0xA2654); D=(0xAFAB4,0xAFEE4)
RS="2f2790d8621ae2fe724a8dfd52479b24a91c4f9eed2c68782c0753d5f9c88750"; DS="5325c59d58f13c5a416f9e2cc57e0f2731664b11be16e1f1f40bd054b3fc29f4"
ENTRY=bytes.fromhex("10 b5 81 b0 1c 1c 00 06 00 0e 09 06 09 0e 12 06 12 0e 6b 46")
TR=(0xA25E0,0xA2654); TD=(0xAFE70,0xAFEE4)
TRS="0f3221843beaae8637a85ce0cabc224447f080f745aa2e91ef5f0079f7131066"; TDS="9917805dcfa0b391d9cff9c7080cccad65081f17107c6b286bf6d2e76df5e4b7"
NR=bytes.fromhex("f0 b5 47 46 80 b4 52 20 69 f0 34 f8 00 06 00 0e 01 28")
ND=bytes.fromhex("f0 b5 47 46 80 b4 52 20 70 f0 24 fc 00 06 00 0e 01 28")
def h(x): return hashlib.sha256(x).hexdigest()
def main():
 p=argparse.ArgumentParser(); p.add_argument("--rev0",type=Path,required=True); p.add_argument("--rev1",type=Path,required=True); p.add_argument("--debug",type=Path,required=True); a=p.parse_args()
 r0=a.rev0.read_bytes(); r1=a.rev1.read_bytes(); d=a.debug.read_bytes()
 x0=r0[R[0]:R[1]]; x1=r1[R[0]:R[1]]; xd=d[D[0]:D[1]]
 assert len(x0)==len(x1)==len(xd)==0x430 and x0==x1
 assert h(x0)==RS and h(x1)==RS and h(xd)==DS
 assert D[0]-R[0]==D[1]-R[1]==0xD890
 assert x0[:len(ENTRY)]==ENTRY and xd[:len(ENTRY)]==ENTRY
 assert h(r0[TR[0]:TR[1]])==TRS and h(d[TD[0]:TD[1]])==TDS
 assert r0[R[1]:R[1]+len(NR)]==NR and r1[R[1]:R[1]+len(NR)]==NR and d[D[1]:D[1]+len(ND)]==ND
 print("German script_movement verification passed")
 print("Retail Rev0/Rev1: 0x080A2224..0x080A2654, 0x430 bytes")
 print("Debug:            0x080AFAB4..0x080AFEE4, 0x430 bytes")
 print("Accumulated Retail->Debug delta remains +0xD890")
 print("Next: fldeff_cut")
if __name__=="__main__": main()
