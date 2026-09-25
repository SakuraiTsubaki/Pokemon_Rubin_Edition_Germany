#!/usr/bin/env python3
import argparse, hashlib
from pathlib import Path
R=(0x99D4C,0x9D3C0); D=(0xA7554,0xAAC04)
RS="fa563c2968cda273f355dbe20f353a7456a6248c35153e669e141f850c023440"; DS="2aa8bc2a89eb92b52cab450eb6c9760b5ffe20c3b78f598960c72a1ba446aebd"
ENTRY=bytes.fromhex("10 b5 81 b0 04 1c 24 06 24 0e 13 48 00 68 13 49 42 18 00 21 11 70")
DBG=(0xAA40C,0xAA434); DBGS="5d048de796db4afffef269f327ceb12176906d75266abf00fdbce48077d202b0"
TAIL_R=(0x9D318,0x9D3C0); TAIL_D=(0xAAB5C,0xAAC04); TAILS="d24bb1809f5e43ee4ef1bedad792a0dd54f8f37e21d2d4452564550db20ae012"
NEXT=bytes.fromhex("70 b5 46 46 40 b4 86 b0 1e 1c 0b 9b 00 04 00 0c 1b 06 1b 0e e8 46 17 4c")
def h(x): return hashlib.sha256(x).hexdigest()
def main():
 p=argparse.ArgumentParser(); p.add_argument("--rev0",type=Path,required=True); p.add_argument("--rev1",type=Path,required=True); p.add_argument("--debug",type=Path,required=True); a=p.parse_args()
 r0=a.rev0.read_bytes(); r1=a.rev1.read_bytes(); d=a.debug.read_bytes()
 x0=r0[R[0]:R[1]]; x1=r1[R[0]:R[1]]; xd=d[D[0]:D[1]]
 assert len(x0)==len(x1)==0x3674 and len(xd)==0x36B0 and x0==x1
 assert h(x0)==RS and h(x1)==RS and h(xd)==DS
 assert D[0]-R[0]==0xD808 and D[1]-R[1]==0xD844 and len(xd)-len(x0)==0x3C
 assert x0[:len(ENTRY)]==ENTRY and xd[:len(ENTRY)]==ENTRY
 assert len(d[DBG[0]:DBG[1]])==0x28 and h(d[DBG[0]:DBG[1]])==DBGS
 tr=r0[TAIL_R[0]:TAIL_R[1]]; td=d[TAIL_D[0]:TAIL_D[1]]; assert tr==td and h(tr)==TAILS
 assert r0[R[1]:R[1]+len(NEXT)]==NEXT and r1[R[1]:R[1]+len(NEXT)]==NEXT and d[D[1]:D[1]+len(NEXT)]==NEXT
 print("German pokemon_storage_system_4 verification passed")
 print("Retail Rev0/Rev1: 0x08099D4C..0x0809D3C0, 0x3674 bytes")
 print("Debug:            0x080A7554..0x080AAC04, 0x36B0 bytes")
 print("Debug growth: 0x3C")
 print("Accumulated Retail->Debug delta changes +0xD808 -> +0xD844")
 print("Next: pokemon_icon / unref_sub_809D26C")
if __name__=="__main__": main()
