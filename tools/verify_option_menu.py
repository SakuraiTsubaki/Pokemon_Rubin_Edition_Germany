#!/usr/bin/env python3
import argparse, hashlib
from pathlib import Path

R=(0x8BA64,0x8C430)
D=(0x98E98,0x99864)
R_SHA="1efa501a7455ed6c5fe575bb962f9ac8ecb94717bd872f704d5027819d3a8614"
D_SHA="673d41e14bbbe9d80e8f473de6b7209a1cdec157cac0b4b64e2152ce12ea7b5c"
TAIL_R=(0x8C3DC,0x8C430)
TAIL_D=(0x99810,0x99864)
TAIL_R_SHA="4cfcde4898d967ad8f61dc3d80b0a112988c24064b2576923640ad2d50604667"
TAIL_D_SHA="dba036b2229f5ddc91e2f854f3b67d6a96d7070a8d7c90813d352d9ec764ac0e"
NEXT36=bytes.fromhex("70 b5 16 48 00 21 01 80 15 4a 40 20 10 70 15 48 01 70 15 4c 00 20 61 76 21 76 a1 76 e1 76 e0 61 20 62 60 62")
LOOP=bytes.fromhex("48 1c 00 04 01 0c 33 29 f2 d9")

def h(x): return hashlib.sha256(x).hexdigest()

def main():
 p=argparse.ArgumentParser()
 p.add_argument("--rev0",type=Path,required=True)
 p.add_argument("--rev1",type=Path,required=True)
 p.add_argument("--debug",type=Path,required=True)
 a=p.parse_args()
 r0=a.rev0.read_bytes(); r1=a.rev1.read_bytes(); d=a.debug.read_bytes()
 x0=r0[R[0]:R[1]]; x1=r1[R[0]:R[1]]; xd=d[D[0]:D[1]]
 assert len(x0)==len(x1)==len(xd)==0x9CC
 assert x0==x1
 assert h(x0)==R_SHA and h(x1)==R_SHA and h(xd)==D_SHA
 assert D[0]-R[0]==D[1]-R[1]==0xD434
 assert h(r0[TAIL_R[0]:TAIL_R[1]])==TAIL_R_SHA
 assert h(d[TAIL_D[0]:TAIL_D[1]])==TAIL_D_SHA
 assert r0[R[1]:R[1]+len(NEXT36)]==NEXT36
 assert r1[R[1]:R[1]+len(NEXT36)]==NEXT36
 assert d[D[1]:D[1]+len(NEXT36)]==NEXT36
 assert r0[R[1]+0x4A:R[1]+0x54]==LOOP
 assert d[D[1]+0x4A:D[1]+0x54]==LOOP
 print("German option_menu verification passed")
 print("Retail Rev0/Rev1: 0x0808BA64..0x0808C430, 0x9CC bytes")
 print("Debug:            0x08098E98..0x08099864, 0x9CC bytes")
 print("Accumulated Retail->Debug delta remains +0xD434")
 print("Next: pokedex / ResetPokedex")

if __name__=="__main__": main()
