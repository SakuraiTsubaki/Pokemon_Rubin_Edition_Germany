#!/usr/bin/env python3
import argparse, hashlib
from pathlib import Path
R=(0x9D3C0,0x9D998); D=(0xAAC04,0xAB1DC)
RS="2fd41d5d628f62c828a537eea74fce8d51a105d30752d920aca70ca01571de63"; DS="c347fc84c44cde896ad7c0238c9f46c959596747c70b0990f83667962632ae9f"
ENTRY=bytes.fromhex("70 b5 46 46 40 b4 86 b0 1e 1c 0b 9b 00 04 00 0c 1b 06 1b 0e e8 46 17 4c")
NEXT_R=bytes.fromhex("00 b5 dd f7 03 fb 62 f7 93 ff 62 f7 b7 ff d6 f7 a9 fa 01 bc 00 47")
NEXT_D=bytes.fromhex("00 b5 81 b0 d7 f7 1a f8 55 f7 70 fb 55 f7 94 fb cf f7 bc ff")
def h(x): return hashlib.sha256(x).hexdigest()
def main():
 p=argparse.ArgumentParser(); p.add_argument("--rev0",type=Path,required=True); p.add_argument("--rev1",type=Path,required=True); p.add_argument("--debug",type=Path,required=True); a=p.parse_args()
 r0=a.rev0.read_bytes(); r1=a.rev1.read_bytes(); d=a.debug.read_bytes()
 x0=r0[R[0]:R[1]]; x1=r1[R[0]:R[1]]; xd=d[D[0]:D[1]]
 assert len(x0)==len(x1)==len(xd)==0x5D8 and x0==x1
 assert h(x0)==RS and h(x1)==RS and h(xd)==DS
 assert D[0]-R[0]==D[1]-R[1]==0xD844
 assert x0[:len(ENTRY)]==ENTRY and xd[:len(ENTRY)]==ENTRY
 assert r0[R[1]:R[1]+len(NEXT_R)]==NEXT_R and r1[R[1]:R[1]+len(NEXT_R)]==NEXT_R
 assert d[D[1]:D[1]+len(NEXT_D)]==NEXT_D
 print("German pokemon_icon verification passed")
 print("Retail Rev0/Rev1: 0x0809D3C0..0x0809D998, 0x5D8 bytes")
 print("Debug:            0x080AAC04..0x080AB1DC, 0x5D8 bytes")
 print("Accumulated Retail->Debug delta remains +0xD844")
 print("Next: pokemon_summary_screen / sub_809D844")
if __name__=="__main__": main()
