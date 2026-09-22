#!/usr/bin/env python3
import argparse, hashlib
from pathlib import Path

R=(0x47CF0,0x47FFC)
D=(0x4BEBC,0x4C1C8)
R_SHA="0a35f0a60d16a395c3537589d1f8db8d68a377de8ceab9e1b4b61738cdb5ad05"
D_SHA="3b756e289bf0492f340beb5657a7a83f668700c70c16d1b084046d95e08edd5a"

def h(x): return hashlib.sha256(x).hexdigest()

def contains_u32(data,start,end,value):
    return value.to_bytes(4,"little") in data[start:end]

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
 assert R[1]-R[0]==D[1]-D[0]==0x30C
 assert D[0]-R[0]==D[1]-R[1]==0x41CC

 # CheckForFlashMemory and first trade wrapper are Thumb functions.
 assert r1[R[0]:R[0]+2]==bytes.fromhex("00 b5")
 assert d[D[0]:D[0]+2]==bytes.fromhex("00 b5")
 assert r1[R[1]:R[1]+2]==bytes.fromhex("00 b5")
 assert d[D[1]:D[1]+2]==bytes.fromhex("00 b5")

 # German runtime save-block literals.
 assert contains_u32(r1,*R,0x02025734)
 assert contains_u32(d,*D,0x020259D8)
 assert contains_u32(r1,*R,0x02024EA4)
 assert contains_u32(d,*D,0x02025148)

 print("German load_save verification passed")
 print("Module size: 0x30C; stable Debug delta +0x41CC")
 print("SaveBlock1 Retail/Debug: 0x02025734 / 0x020259D8")
 print("Next: trade at 0x08047FFC / 0x0804C1C8")

if __name__=="__main__": main()
