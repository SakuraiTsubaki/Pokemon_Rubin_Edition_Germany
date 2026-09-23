#!/usr/bin/env python3
import argparse, hashlib
from pathlib import Path

R=(0x94710,0x94A78); D=(0xA1C60,0xA1FC8)
R_SHA="0a9d4d825cd91a353ea71b0efb13671f13106a4b9af8da1cdef58207bc38f13f"
D_SHA="bad9adc07eade99b078687abc0d749a8215e9dffccac1bb899d10f906ee943c8"
TAIL_R=(0x94A34,0x94A78); TAIL_D=(0xA1F84,0xA1FC8)
TAIL_R_SHA="d612081b2b477c5d3de1379d5e13ccbbd79b6684352d04f422e6664c0c7e1bfc"
TAIL_D_SHA="c2f9f543aa71125de78cc00f46c0351d375482b6afb0f380c0f1dd81e1202e8f"
NEXT=bytes.fromhex("00 b5 03 49 03 4a")

def h(x): return hashlib.sha256(x).hexdigest()

def main():
 p=argparse.ArgumentParser()
 p.add_argument("--rev0",type=Path,required=True); p.add_argument("--rev1",type=Path,required=True); p.add_argument("--debug",type=Path,required=True)
 a=p.parse_args(); r0=a.rev0.read_bytes(); r1=a.rev1.read_bytes(); d=a.debug.read_bytes()
 x0=r0[R[0]:R[1]]; x1=r1[R[0]:R[1]]; xd=d[D[0]:D[1]]
 assert len(x0)==len(x1)==len(xd)==0x368
 assert x0==x1 and h(x0)==R_SHA and h(x1)==R_SHA and h(xd)==D_SHA
 assert D[0]-R[0]==D[1]-R[1]==0xD550
 assert h(r0[TAIL_R[0]:TAIL_R[1]])==TAIL_R_SHA and h(d[TAIL_D[0]:TAIL_D[1]])==TAIL_D_SHA
 assert r0[R[1]:R[1]+len(NEXT)]==NEXT and r1[R[1]:R[1]+len(NEXT)]==NEXT and d[D[1]:D[1]+len(NEXT)]==NEXT
 print("German save_menu_util verification passed")
 print("Retail Rev0/Rev1: 0x08094710..0x08094A78, 0x368 bytes")
 print("Debug:            0x080A1C60..0x080A1FC8, 0x368 bytes")
 print("Accumulated Retail->Debug delta remains +0xD550")
 print("Next: battle_party_menu / unref_sub_8094928")

if __name__=="__main__": main()
