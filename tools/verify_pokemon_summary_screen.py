#!/usr/bin/env python3
import argparse, hashlib
from pathlib import Path

R=(0x9D998,0xA2224)
D=(0xAB1DC,0xAFAB4)
RS="7340ceeb3b69f3ff1fb65a3a64b0a29d89841b2decb3eac6d3ed0ee1ce66d94b"
DS="59eb2394e4ba40e321aa4f6654efa6d0ce358d3f6f85747dc6d6d11462ba2337"
FR=(0x9D998,0x9D9B0); FD=(0xAB1DC,0xAB220)
FRS="8bfa5e539a0f88e0d017278123bb240fe32c14bd337a95b92fa59ce1cb4dd539"
FDS="a952d10abc36c12d19d21859467541ff4b57851534d6dec83158dece17ee382e"
TR=(0xA21F8,0xA2224); TD=(0xAFA88,0xAFAB4)
TRS="9696dceaf51f770b406a676fb441b6ae3dbb275315a35ad88802dd35c5948e11"
TDS="436b6c9eb5c0bd0cc79f6b6c2e697a5c0e56a64e9b39b5c7bfc27dcfe520a3a5"
NEXT=bytes.fromhex("10 b5 81 b0 1c 1c 00 06 00 0e 09 06 09 0e 12 06 12 0e 6b 46")

def h(x): return hashlib.sha256(x).hexdigest()

def main():
 p=argparse.ArgumentParser(description="Verify German Pokemon Ruby pokemon_summary_screen")
 p.add_argument("--rev0",type=Path,required=True); p.add_argument("--rev1",type=Path,required=True); p.add_argument("--debug",type=Path,required=True)
 a=p.parse_args()
 r0=a.rev0.read_bytes(); r1=a.rev1.read_bytes(); d=a.debug.read_bytes()
 x0=r0[R[0]:R[1]]; x1=r1[R[0]:R[1]]; xd=d[D[0]:D[1]]
 assert len(x0)==0x488C and len(x1)==0x488C and len(xd)==0x48D8
 assert x0==x1 and h(x0)==RS and h(x1)==RS and h(xd)==DS
 assert D[0]-R[0]==0xD844 and D[1]-R[1]==0xD890
 assert len(xd)-len(x0)==0x4C
 assert h(r0[FR[0]:FR[1]])==FRS and h(d[FD[0]:FD[1]])==FDS
 assert (FD[1]-FD[0])-(FR[1]-FR[0])==0x2C
 assert 0x4C-0x2C==0x20
 assert h(r0[TR[0]:TR[1]])==TRS and h(d[TD[0]:TD[1]])==TDS
 assert len(r0[TR[0]:TR[1]])==len(d[TD[0]:TD[1]])==0x2C
 assert r0[R[1]:R[1]+len(NEXT)]==NEXT and r1[R[1]:R[1]+len(NEXT)]==NEXT and d[D[1]:D[1]+len(NEXT)]==NEXT
 print("German pokemon_summary_screen verification passed")
 print("Retail Rev0/Rev1: 0x0809D998..0x080A2224, 0x488C bytes")
 print("Debug:            0x080AB1DC..0x080AFAB4, 0x48D8 bytes")
 print("Debug growth: 0x4C")
 print("Accumulated Retail->Debug delta changes +0xD844 -> +0xD890")
 print("Next: script_movement / ScriptMovement_StartObjectMovementScript")

if __name__=="__main__": main()
