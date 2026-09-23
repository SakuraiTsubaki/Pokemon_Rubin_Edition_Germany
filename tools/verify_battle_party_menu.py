#!/usr/bin/env python3
import argparse, hashlib
from pathlib import Path
R=(0x94A78,0x95A54); D=(0xA1FC8,0xA2FA4)
R_SHA="02680c6402ce257154810b6eaef7d672e22e8f55a1df1edc23052fce4287a776"
D_SHA="1c48bbe28aa8b11afb25bed72bd5df2648ed6ad6bc1fb4765a0f330002c428a7"
TR=(0x95A14,0x95A54); TD=(0xA2F64,0xA2FA4)
TR_SHA="d2e230758f9d51fd25a3a448409cd19025d2e854b0cb8337ff60be58f3c3326d"
TD_SHA="dab4185229433a7fc779b1077bf0a065875f376db753ecc19ebcae13f7c39959"
NEXT=bytes.fromhex("f0 b5 57 46 4e 46 45 46 e0 b4 87 b0 00 90 0f 1c 14 1c 0f 98 24 06 24 0e 1b 04 1b 0c 01 93 00 06")
def h(x): return hashlib.sha256(x).hexdigest()
def main():
 p=argparse.ArgumentParser()
 p.add_argument("--rev0",type=Path,required=True); p.add_argument("--rev1",type=Path,required=True); p.add_argument("--debug",type=Path,required=True)
 a=p.parse_args(); r0=a.rev0.read_bytes(); r1=a.rev1.read_bytes(); d=a.debug.read_bytes()
 x0=r0[R[0]:R[1]]; x1=r1[R[0]:R[1]]; xd=d[D[0]:D[1]]
 assert len(x0)==len(x1)==len(xd)==0xFDC
 assert x0==x1 and h(x0)==R_SHA and h(x1)==R_SHA and h(xd)==D_SHA
 assert D[0]-R[0]==D[1]-R[1]==0xD550
 assert h(r0[TR[0]:TR[1]])==TR_SHA and h(d[TD[0]:TD[1]])==TD_SHA
 assert r0[R[1]:R[1]+len(NEXT)]==NEXT and r1[R[1]:R[1]+len(NEXT)]==NEXT and d[D[1]:D[1]+len(NEXT)]==NEXT
 print("German battle_party_menu verification passed")
 print("Retail Rev0/Rev1: 0x08094A78..0x08095A54, 0xFDC bytes")
 print("Debug:            0x080A1FC8..0x080A2FA4, 0xFDC bytes")
 print("Accumulated Retail->Debug delta remains +0xD550")
 print("Next: unk_text_8095904 / sub_8095904")
if __name__=="__main__": main()
