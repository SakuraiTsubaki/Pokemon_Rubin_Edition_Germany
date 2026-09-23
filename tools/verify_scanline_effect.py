#!/usr/bin/env python3
import argparse
import hashlib
from pathlib import Path

RETAIL=(0x899CC,0x89EC4)
DEBUG=(0x96D98,0x97290)
RETAIL_SHA256="96bc747002423e226b44f4b0cc7152350f42b579daa3437b32acb0fcb8995522"
DEBUG_SHA256="f21a414215e96ff73766c4f4a72d0895fb6dd8b2536768c411bf093e3663795c"
ENTRY=bytes.fromhex("10 b5 0b 4c 00 20 60 75 0a 49 4a 89 0a 48 10 40 48 81 4a 89 09 48 10 40 48 81 48 89 20 7e ff 28 03 d0")
TAIL_R=(0x89D98,0x89EC4)
TAIL_D=(0x97164,0x97290)
TAIL_R_SHA="2cb3c4a1583878673bc356e585587bc6aaf5b0307bf048245054fb1b77498e9d"
TAIL_D_SHA="daecf910e078672460d5f3678f5f7c946c50bb6ac6f583bfbbe67cd730d35b36"
NEXT=bytes.fromhex("00 b5 05 48 01 7a 80 22 11 43 01 72 00 20 00 21")

def h(x): return hashlib.sha256(x).hexdigest()

def main():
    p=argparse.ArgumentParser()
    p.add_argument("--rev0",type=Path,required=True)
    p.add_argument("--rev1",type=Path,required=True)
    p.add_argument("--debug",type=Path,required=True)
    a=p.parse_args()
    r0=a.rev0.read_bytes(); r1=a.rev1.read_bytes(); d=a.debug.read_bytes()
    x0=r0[RETAIL[0]:RETAIL[1]]; x1=r1[RETAIL[0]:RETAIL[1]]; xd=d[DEBUG[0]:DEBUG[1]]
    assert len(x0)==len(x1)==len(xd)==0x4F8
    assert x0==x1
    assert h(x0)==RETAIL_SHA256 and h(x1)==RETAIL_SHA256 and h(xd)==DEBUG_SHA256
    assert DEBUG[0]-RETAIL[0]==DEBUG[1]-RETAIL[1]==0xD3CC
    assert x0[:len(ENTRY)]==ENTRY and xd[:len(ENTRY)]==ENTRY
    assert h(r0[TAIL_R[0]:TAIL_R[1]])==TAIL_R_SHA
    assert h(d[TAIL_D[0]:TAIL_D[1]])==TAIL_D_SHA
    assert r0[RETAIL[1]:RETAIL[1]+len(NEXT)]==NEXT
    assert r1[RETAIL[1]:RETAIL[1]+len(NEXT)]==NEXT
    assert d[DEBUG[1]:DEBUG[1]+len(NEXT)]==NEXT
    assert int.from_bytes(r0[RETAIL[1]+24:RETAIL[1]+28],"little")==0x0202F388
    assert int.from_bytes(d[DEBUG[1]+24:DEBUG[1]+28],"little")==0x0202F62C
    print("German scanline_effect verification passed")
    print("Retail Rev0/Rev1: 0x080899CC..0x08089EC4, 0x4F8 bytes")
    print("Debug:            0x08096D98..0x08097290, 0x4F8 bytes")
    print("Accumulated Retail->Debug delta remains +0xD3CC")
    print("Next: pokemon_menu / sub_8089A70")

if __name__=="__main__":
    main()
