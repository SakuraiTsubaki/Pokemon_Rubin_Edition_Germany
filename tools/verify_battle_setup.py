#!/usr/bin/env python3
import argparse
import hashlib
from pathlib import Path

RETAIL=(0x81D94,0x83108)
DEBUG=(0x8915C,0x8A4D0)
RETAIL_SHA256="05518cd7d00fbd74e5ef75bafacac1f6a8702bb55c79afe703c2922d216a8a25"
DEBUG_SHA256="999ea36e9a5e9c88dcab89898cb32d11b39a30a34c997fd41b51eccbb42de798"
ENTRY=bytes.fromhex("30 b5 00 06 05 0e a8 00 40 19 c0 00 04 49 44 18 00 21 60 5e 00 28 05 d0 01 28 0e d0 1d e0 00 00")
LAST_RETAIL=(0x830EC,0x83108)
LAST_DEBUG=(0x8A4B4,0x8A4D0)
LAST_RETAIL_SHA256="ea98d544b95db961865f422b2162d64fddbfd9dddefcc759b77a5186c025d561"
LAST_DEBUG_SHA256="3da8b8fbc82b8e663b9cfc8382be145fb4d1fb25ede08e5c7cd0ad97599313fd"
NEXT_RETAIL=bytes.fromhex("70 b5 00 06 06 0e 09 06 0d 0e 0c 4c 20 1c")
NEXT_DEBUG=bytes.fromhex("00 b5 01 1c 02 48 81 42 04 d1 01 20")

def sha256(data): return hashlib.sha256(data).hexdigest()

def main():
    p=argparse.ArgumentParser(description="Verify German Pokemon Ruby battle_setup module")
    p.add_argument("--rev0",type=Path,required=True)
    p.add_argument("--rev1",type=Path,required=True)
    p.add_argument("--debug",type=Path,required=True)
    a=p.parse_args()
    r0=a.rev0.read_bytes(); r1=a.rev1.read_bytes(); dbg=a.debug.read_bytes()
    x0=r0[RETAIL[0]:RETAIL[1]]; x1=r1[RETAIL[0]:RETAIL[1]]; xd=dbg[DEBUG[0]:DEBUG[1]]
    assert len(x0)==len(x1)==len(xd)==0x1374
    assert x0==x1
    assert sha256(x0)==RETAIL_SHA256 and sha256(x1)==RETAIL_SHA256
    assert sha256(xd)==DEBUG_SHA256
    assert DEBUG[0]-RETAIL[0]==0x73C8 and DEBUG[1]-RETAIL[1]==0x73C8
    assert x0[:len(ENTRY)]==ENTRY and xd[:len(ENTRY)]==ENTRY
    assert sha256(r0[LAST_RETAIL[0]:LAST_RETAIL[1]])==LAST_RETAIL_SHA256
    assert sha256(dbg[LAST_DEBUG[0]:LAST_DEBUG[1]])==LAST_DEBUG_SHA256
    assert r0[RETAIL[1]:RETAIL[1]+len(NEXT_RETAIL)]==NEXT_RETAIL
    assert r1[RETAIL[1]:RETAIL[1]+len(NEXT_RETAIL)]==NEXT_RETAIL
    assert dbg[DEBUG[1]:DEBUG[1]+len(NEXT_DEBUG)]==NEXT_DEBUG
    print("German battle_setup verification passed")
    print("Retail Rev0/Rev1: 0x08081D94..0x08083108, 0x1374 bytes")
    print("Debug:            0x0808915C..0x0808A4D0, 0x1374 bytes")
    print("Accumulated Retail->Debug delta remains +0x73C8")
    print("Next: cable_club (Retail sub_8082CD4 / Debug debug_sub_808A4D0)")

if __name__=="__main__":
    main()
