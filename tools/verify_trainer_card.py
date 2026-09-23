#!/usr/bin/env python3
import argparse, hashlib
from pathlib import Path

R=(0x93260,0x94710); D=(0xA0694,0xA1C60)
R_SHA="914172d616e63504c6322025b7e281bf630fe89fdfe5d6d170c44394b95ff1d1"
D_SHA="c52635154eecab15c54d75afeda752b5469de06a2bdcae02c347ee52483ac4cf"
DBG1=(0xA0710,0xA073C,"8f528e340a14ea981588f8f5c9432f011e6d2a21e0dd5faa9b5688746b883696")
DBG2=(0xA073C,0xA0780,"ef2a3c703f49824838ca426f494cdd001903b8f0b1be9e949010450acf92e158")
DBG3=(0xA0780,0xA07A8,"ac51fa79059dfd66ceb364c9408e65e5181b65b5f1ad8384276db535549dfc5f")
TAIL_R=(0x946D8,0x94710); TAIL_D=(0xA1C28,0xA1C60)
TAIL_R_SHA="3b6bd699d5cb5173691d9705a313c7717e50e4fe45650a5386b85c3b4742f8d9"
TAIL_D_SHA="f931a40fb2767b7e2213f725b98520c9a744140b5909f67b54579d9c13b0de1c"
NEXT=bytes.fromhex("70 b5 00 04 05 0c 09 04 0c 0c 0c 26")

def h(x): return hashlib.sha256(x).hexdigest()

def main():
 p=argparse.ArgumentParser()
 p.add_argument("--rev0",type=Path,required=True); p.add_argument("--rev1",type=Path,required=True); p.add_argument("--debug",type=Path,required=True)
 a=p.parse_args(); r0=a.rev0.read_bytes(); r1=a.rev1.read_bytes(); d=a.debug.read_bytes()
 x0=r0[R[0]:R[1]]; x1=r1[R[0]:R[1]]; xd=d[D[0]:D[1]]
 assert len(x0)==len(x1)==0x14B0 and len(xd)==0x15CC
 assert x0==x1 and h(x0)==R_SHA and h(x1)==R_SHA and h(xd)==D_SHA
 assert D[0]-R[0]==0xD434 and D[1]-R[1]==0xD550
 assert len(xd)-len(x0)==0x11C
 for a0,b0,sha in (DBG1,DBG2,DBG3):
  assert h(d[a0:b0])==sha
 assert h(r0[TAIL_R[0]:TAIL_R[1]])==TAIL_R_SHA
 assert h(d[TAIL_D[0]:TAIL_D[1]])==TAIL_D_SHA
 assert r0[R[1]:R[1]+len(NEXT)]==NEXT and r1[R[1]:R[1]+len(NEXT)]==NEXT and d[D[1]:D[1]+len(NEXT)]==NEXT
 print("German trainer_card verification passed")
 print("Retail Rev0/Rev1: 0x08093260..0x08094710, 0x14B0 bytes")
 print("Debug:            0x080A0694..0x080A1C60, 0x15CC bytes")
 print("Debug growth: 0x11C bytes; delta +0xD434 -> +0xD550")
 print("Next: save_menu_util / HandleDrawSaveWindowInfo")

if __name__=="__main__": main()
