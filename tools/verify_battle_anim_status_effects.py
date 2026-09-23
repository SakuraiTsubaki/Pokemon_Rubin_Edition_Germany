#!/usr/bin/env python3
import argparse
import hashlib
from pathlib import Path

RETAIL=(0x7BA5C,0x7C1C0)
DEBUG=(0x82CD0,0x83434)
RETAIL_SHA256="96dff3d1c51f8c66be47915de60bee9d1b8aaba244d7ebbb8a0a2afa1b0d00d6"
DEBUG_SHA256="6aa1736be3a4541ecd847d6368d3b806b5cdd085f37a64b87e6115396babe00b"
ENTRY_PREFIX=bytes.fromhex("f0 b5 47 46 80 b4 04 1c 0d 1c 24 06 24 0e 2d 06 2d 0e 24 48 20 18 06 78 23 48 0a 21 ff f7")
LAST_RETAIL=(0x7C16C,0x7C1C0)
LAST_DEBUG=(0x833E0,0x83434)
LAST_RETAIL_SHA256="e50efe904f1ab85cafe5ad0bbfb7729edb8421413cc1c14c728e7ab6bbd439ca"
LAST_DEBUG_SHA256="3d4f5d4bf778b9ed40f8a92bc222c470540c86bb750ab200bf7ca54305854e4d"
NEXT_PREFIX=bytes.fromhex("10 b5 02 1c 30 20 11 5e 88 00 40 18 c0 00 09 49 44 18 0a 21 60 5e 00 28 0e d0 51 78 0d 20 40 42 08 40 50 70 54 20 50 84 3e 32 11 78 59 38 08 40 10 70 25 e0")

def sha256(b): return hashlib.sha256(b).hexdigest()

def main():
    p=argparse.ArgumentParser(description="Verify German Pokemon Ruby battle_anim_status_effects module")
    p.add_argument("--rev0",type=Path,required=True)
    p.add_argument("--rev1",type=Path,required=True)
    p.add_argument("--debug",type=Path,required=True)
    a=p.parse_args()
    r0=a.rev0.read_bytes(); r1=a.rev1.read_bytes(); dbg=a.debug.read_bytes()
    x0=r0[RETAIL[0]:RETAIL[1]]; x1=r1[RETAIL[0]:RETAIL[1]]; xd=dbg[DEBUG[0]:DEBUG[1]]
    assert len(x0)==len(x1)==len(xd)==0x764
    assert x0==x1
    assert sha256(x0)==RETAIL_SHA256 and sha256(x1)==RETAIL_SHA256
    assert sha256(xd)==DEBUG_SHA256
    assert DEBUG[0]-RETAIL[0]==0x7274 and DEBUG[1]-RETAIL[1]==0x7274
    assert x0[:len(ENTRY_PREFIX)]==ENTRY_PREFIX
    assert xd[:len(ENTRY_PREFIX)]==ENTRY_PREFIX
    assert sha256(r0[LAST_RETAIL[0]:LAST_RETAIL[1]])==LAST_RETAIL_SHA256
    assert sha256(dbg[LAST_DEBUG[0]:LAST_DEBUG[1]])==LAST_DEBUG_SHA256
    assert r0[RETAIL[1]:RETAIL[1]+len(NEXT_PREFIX)]==NEXT_PREFIX
    assert r1[RETAIL[1]:RETAIL[1]+len(NEXT_PREFIX)]==NEXT_PREFIX
    assert dbg[DEBUG[1]:DEBUG[1]+len(NEXT_PREFIX)]==NEXT_PREFIX
    print("German battle_anim_status_effects verification passed")
    print("Retail Rev0/Rev1: 0x0807BA5C..0x0807C1C0, 0x764 bytes")
    print("Debug:            0x08082CD0..0x08083434, 0x764 bytes")
    print("Accumulated Retail->Debug delta remains +0x7274")
    print("Next: title_screen / SpriteCallback_VersionBannerLeft")

if __name__=="__main__": main()
