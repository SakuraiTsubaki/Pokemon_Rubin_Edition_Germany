#!/usr/bin/env python3
import argparse, hashlib
from pathlib import Path

R=(0x89EC4,0x8BA64)
D=(0x97290,0x98E98)
R_SHA="e7d55eb1e9dc69dc936146d5b2a216b600fd5ebd714bd4547f4b8cb69f1dca15"
D_SHA="111c646d5e840c31bd107eec3a3f42a4c545b632c5d54422002c7e94a5496bd1"
ENTRY=bytes.fromhex("00 b5 05 48 01 7a 80 22 11 43 01 72 00 20 00 21")
DBG=(0x986AC,0x986F8)
DBG_SHA="6b4d3d6355598a0cafcc4fcd984c12dd624f33fe3e6eaa80392b3a88a49c1e51"
COND_R=(0x8B2E0,0x8B374)
COND_D=(0x986F8,0x987A8)
COND_R_SHA="236b1d716db3d90f560d64eb0c55ce8fe6466de34e3043e37270077d51ba16d1"
COND_D_SHA="bf2fdb0623dc87bb531a954e1c60e967230568abb609530313f6312ef880d8e1"
TAIL_R=(0x8BA38,0x8BA64)
TAIL_D=(0x98E6C,0x98E98)
TAIL_R_SHA="d80b13f226814e1420590161d80bdd9a8f7cc5f2c37f60c20394c4dc1e69b417"
TAIL_D_SHA="11429eac1fbb5db1e4afda21d3a79d20a45198f745abf417116b7de536b75299"
NEXT_R=bytes.fromhex("00 b5 ef f7 9d fa 74 f7 2d ff 74 f7 51 ff e8 f7 43 fa 01 bc 00 47")
NEXT_D=bytes.fromhex("00 b5 e9 f7 bd f9 67 f7 13 fd 67 f7 37 fd e2 f7 5f f9 01 bc 00 47")

def h(x): return hashlib.sha256(x).hexdigest()

def main():
 p=argparse.ArgumentParser()
 p.add_argument("--rev0",type=Path,required=True); p.add_argument("--rev1",type=Path,required=True); p.add_argument("--debug",type=Path,required=True)
 a=p.parse_args(); r0=a.rev0.read_bytes(); r1=a.rev1.read_bytes(); d=a.debug.read_bytes()
 x0=r0[R[0]:R[1]]; x1=r1[R[0]:R[1]]; xd=d[D[0]:D[1]]
 assert len(x0)==len(x1)==0x1BA0 and len(xd)==0x1C08
 assert x0==x1 and h(x0)==R_SHA and h(x1)==R_SHA and h(xd)==D_SHA
 assert D[0]-R[0]==0xD3CC and D[1]-R[1]==0xD434 and len(xd)-len(x0)==0x68
 assert x0[:len(ENTRY)]==ENTRY and xd[:len(ENTRY)]==ENTRY
 assert h(d[DBG[0]:DBG[1]])==DBG_SHA
 assert h(r0[COND_R[0]:COND_R[1]])==COND_R_SHA and h(d[COND_D[0]:COND_D[1]])==COND_D_SHA
 assert (COND_D[1]-COND_D[0])-(COND_R[1]-COND_R[0])==0x1C
 assert h(r0[TAIL_R[0]:TAIL_R[1]])==TAIL_R_SHA and h(d[TAIL_D[0]:TAIL_D[1]])==TAIL_D_SHA
 assert r0[R[1]:R[1]+len(NEXT_R)]==NEXT_R and r1[R[1]:R[1]+len(NEXT_R)]==NEXT_R and d[D[1]:D[1]+len(NEXT_D)]==NEXT_D
 print("German pokemon_menu verification passed")
 print("Retail Rev0/Rev1: 0x08089EC4..0x0808BA64, 0x1BA0 bytes")
 print("Debug:            0x08097290..0x08098E98, 0x1C08 bytes")
 print("Debug growth: 0x68 = waterfall helper 0x4C + TM/HM gate 0x1C")
 print("Accumulated Retail->Debug delta changes +0xD3CC -> +0xD434")
 print("Next: option_menu / MainCB")

if __name__=="__main__": main()
