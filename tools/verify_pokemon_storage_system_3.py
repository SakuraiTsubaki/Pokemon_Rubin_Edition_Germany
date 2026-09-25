#!/usr/bin/env python3
import argparse, hashlib
from pathlib import Path
RETAIL=(0x98C90,0x99D4C); DEBUG=(0xA6498,0xA7554)
RS="2b83265be47e0550f0cb19b77f1d254e64bdc4cf294c319058bbab1f54b4ef24"
DS="581caea6528b19ab4c8e36957f663fad9abeacc98ff3bd3fecc654cdd086d2a5"
ENTRY=bytes.fromhex("01 48 00 78 70 47 00 00")
NEXT=bytes.fromhex("10 b5 81 b0 04 1c 24 06 24 0e 13 48 00 68 13 49 42 18 00 21 11 70")
def h(x): return hashlib.sha256(x).hexdigest()
def main():
 p=argparse.ArgumentParser(); p.add_argument("--rev0",type=Path,required=True); p.add_argument("--rev1",type=Path,required=True); p.add_argument("--debug",type=Path,required=True); a=p.parse_args()
 r0=a.rev0.read_bytes(); r1=a.rev1.read_bytes(); d=a.debug.read_bytes()
 x0=r0[RETAIL[0]:RETAIL[1]]; x1=r1[RETAIL[0]:RETAIL[1]]; xd=d[DEBUG[0]:DEBUG[1]]
 assert len(x0)==len(x1)==len(xd)==0x10BC and x0==x1
 assert h(x0)==RS and h(x1)==RS and h(xd)==DS
 assert DEBUG[0]-RETAIL[0]==DEBUG[1]-RETAIL[1]==0xD808
 assert x0[:8]==ENTRY and xd[:8]==ENTRY
 assert r0[RETAIL[1]:RETAIL[1]+len(NEXT)]==NEXT and r1[RETAIL[1]:RETAIL[1]+len(NEXT)]==NEXT and d[DEBUG[1]:DEBUG[1]+len(NEXT)]==NEXT
 print("German pokemon_storage_system_3 verification passed")
 print("Retail Rev0/Rev1: 0x08098C90..0x08099D4C, 0x10BC bytes")
 print("Debug:            0x080A6498..0x080A7554, 0x10BC bytes")
 print("Accumulated Retail->Debug delta remains +0xD808")
 print("Next: pokemon_storage_system_4 / sub_8099BF8")
if __name__=="__main__": main()
