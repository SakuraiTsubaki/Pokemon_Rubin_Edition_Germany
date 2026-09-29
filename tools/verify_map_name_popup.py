#!/usr/bin/env python3
import argparse
import hashlib
from pathlib import Path

RETAIL=(0xA3094,0xA3268)
DEBUG=(0xB0C58,0xB0E2C)
RETAIL_SHA256="b217476853bbcbe13fc7cd03a6e2fa7d3e11a8da30591a3307bb4f16d010f3f0"
DEBUG_SHA256="db6295fd772da9c7c31d1be82d8b6aa1c2ff72010af3b050169327a963554de6"
TAIL_R=(0xA3230,0xA3268)
TAIL_D=(0xB0DF4,0xB0E2C)
NEXT_R=bytes.fromhex("00 b5 5d f7 2d fb 5d f7 51 fb d7 f7 97 fe 04 f0 71 f9 d0 f7 3f fe 01 bc 00 47 00 00")
NEXT_D=bytes.fromhex("00 b5 4f f7 4b fd 4f f7 6f fd d1 f7 ef f9 04 f0 c3 f9 ca f7 93 f9 01 bc 00 47 00 00")

def sha256(data): return hashlib.sha256(data).hexdigest()

def main():
    p=argparse.ArgumentParser(description="Verify German Pokemon Ruby map_name_popup module")
    p.add_argument("--rev0",type=Path,required=True)
    p.add_argument("--rev1",type=Path,required=True)
    p.add_argument("--debug",type=Path,required=True)
    a=p.parse_args()
    r0=a.rev0.read_bytes(); r1=a.rev1.read_bytes(); d=a.debug.read_bytes()

    x0=r0[RETAIL[0]:RETAIL[1]]
    x1=r1[RETAIL[0]:RETAIL[1]]
    xd=d[DEBUG[0]:DEBUG[1]]

    assert len(x0)==len(x1)==len(xd)==0x1D4
    assert x0==x1
    assert sha256(x0)==RETAIL_SHA256
    assert sha256(x1)==RETAIL_SHA256
    assert sha256(xd)==DEBUG_SHA256
    assert DEBUG[0]-RETAIL[0]==DEBUG[1]-RETAIL[1]==0xDBC4

    assert r0[TAIL_R[0]:TAIL_R[1]][-4:]==(0x0202E828).to_bytes(4,"little")
    assert d[TAIL_D[0]:TAIL_D[1]][-4:]==(0x0202EACC).to_bytes(4,"little")

    assert r0[RETAIL[1]:RETAIL[1]+len(NEXT_R)]==NEXT_R
    assert r1[RETAIL[1]:RETAIL[1]+len(NEXT_R)]==NEXT_R
    assert d[DEBUG[1]:DEBUG[1]+len(NEXT_D)]==NEXT_D

    print("German map_name_popup verification passed")
    print("Retail Rev0/Rev1: 0x080A3094..0x080A3268, 0x1D4 bytes")
    print("Debug:            0x080B0C58..0x080B0E2C, 0x1D4 bytes")
    print("Accumulated Retail->Debug delta remains +0xDBC4")
    print("Next: item_menu / sub_80A3118")

if __name__=="__main__":
    main()
