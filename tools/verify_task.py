#!/usr/bin/env python3
import argparse
import hashlib
from pathlib import Path

RETAIL=(0x7ADE8,0x7B114)
DEBUG=(0x82054,0x82388)
RETAIL_SHA256="68d30c1dfd7fa6d080cabae3fbfdf8e37dd0a8f08b53ade8b916dd1620772920"
DEBUG_SHA256="ceabbb2065c235e4d0dac09d37c5835886c406f1dfb86f1e498d970ecb482cc3"
RESET_PREFIX=bytes.fromhex("f0 b5 00 24 13 4e 37 1c 08 37 a0 00 00 19 c0 00 82 19 00 21 11 71 10 49 11 60 54 71 01 34 94 71 01 21 49 42 0d 1c ff 21 d1 71 c0 19 00 21 20 22")
CREATE_RETAIL=(0x7AE48,0x7AE9C)
CREATE_DEBUG=(0x820B4,0x82110)
CREATE_RETAIL_SHA256="f2013a49d64d7d8e490d9bbdbb6b8fd2355153b80dfc74005afe452084ac1154"
CREATE_DEBUG_SHA256="4b6b4aa00f2492030c4f6ffb0a686dede295fad9d55ca354fc0484da7eef00a7"
NEXT_DUMMY=bytes.fromhex("70 47 00 00")
NEXT_PREFIX=bytes.fromhex("00 b5 0d 4a 10 7a 80 21 08 43 10 72 00 20")

def sha256(data):
    return hashlib.sha256(data).hexdigest()

def main():
    p=argparse.ArgumentParser(description="Verify German Pokemon Ruby task module")
    p.add_argument("--rev0",type=Path,required=True)
    p.add_argument("--rev1",type=Path,required=True)
    p.add_argument("--debug",type=Path,required=True)
    a=p.parse_args()
    r0=a.rev0.read_bytes(); r1=a.rev1.read_bytes(); dbg=a.debug.read_bytes()
    x0=r0[RETAIL[0]:RETAIL[1]]; x1=r1[RETAIL[0]:RETAIL[1]]; xd=dbg[DEBUG[0]:DEBUG[1]]
    assert len(x0)==len(x1)==0x32C
    assert len(xd)==0x334
    assert x0==x1
    assert sha256(x0)==RETAIL_SHA256 and sha256(x1)==RETAIL_SHA256
    assert sha256(xd)==DEBUG_SHA256
    assert len(xd)-len(x0)==8
    assert DEBUG[0]-RETAIL[0]==0x726C
    assert DEBUG[1]-RETAIL[1]==0x7274
    assert x0[:0x30]==RESET_PREFIX and xd[:0x30]==RESET_PREFIX
    cr=r0[CREATE_RETAIL[0]:CREATE_RETAIL[1]]
    cd=dbg[CREATE_DEBUG[0]:CREATE_DEBUG[1]]
    assert len(cr)==0x54 and len(cd)==0x5C
    assert sha256(cr)==CREATE_RETAIL_SHA256
    assert sha256(cd)==CREATE_DEBUG_SHA256
    assert cd[-4:]==(0x083B8B18).to_bytes(4,"little")
    assert r0[RETAIL[1]:RETAIL[1]+4]==NEXT_DUMMY
    assert r1[RETAIL[1]:RETAIL[1]+4]==NEXT_DUMMY
    assert dbg[DEBUG[1]:DEBUG[1]+4]==NEXT_DUMMY
    assert r0[RETAIL[1]+4:RETAIL[1]+4+len(NEXT_PREFIX)]==NEXT_PREFIX
    assert dbg[DEBUG[1]+4:DEBUG[1]+4+len(NEXT_PREFIX)]==NEXT_PREFIX
    print("German task verification passed")
    print("Retail Rev0/Rev1: 0x0807ADE8..0x0807B114, 0x32C bytes")
    print("Debug:            0x08082054..0x08082388, 0x334 bytes")
    print("Debug growth: 0x8 bytes in CreateTask crash path")
    print("Accumulated Retail->Debug delta changes +0x726C -> +0x7274")
    print("Next: reshow_battle_screen / ReshowBattleScreenDummy")

if __name__=="__main__":
    main()
