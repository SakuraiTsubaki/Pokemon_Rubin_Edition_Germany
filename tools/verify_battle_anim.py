#!/usr/bin/env python3
import argparse
import hashlib
from pathlib import Path

RETAIL = (0x759E4, 0x77E7C)
DEBUG = (0x7CC50, 0x7F0E8)
RETAIL_SHA256 = "c5eda52f36c5b7ff1bb83de262b3ceab7dbc7a6308933eeffa3aab014aa9c013"
DEBUG_SHA256 = "819df18b3733a0edb4ac128c409fdbd68cd179a0b0a2fdaa00be9471dd1a3c3f"

ENTRY = bytes.fromhex("f0 b5 4f 46 46 46 c0 b4 22 48 00 21 01 70 22 48 01 70 22 48 01 70 22 48 01 70 22 48 00 21 01 60")
NEXT = bytes.fromhex("30 b5 00 06 05 0e 09 06 0c 0e ff f7 8b f8 00 06 00 28 04 d0 03 2c 02 d1 03 2d 00 d1 01 24 04 2c")

TAIL_RETAIL = (0x77E54, 0x77E7C)
TAIL_DEBUG = (0x7F0C0, 0x7F0E8)
TAIL_RETAIL_SHA256 = "81068beb2dc357e1df150c04b3dcef59bcea3ff3742f251c80687e66ce18709a"
TAIL_DEBUG_SHA256 = "6f2e102be9c3376278954aad9011ac1640ad837ddfef390e9633e0d652eb06cc"

def sha256(data):
    return hashlib.sha256(data).hexdigest()

def main():
    p=argparse.ArgumentParser()
    p.add_argument("--rev0",type=Path,required=True)
    p.add_argument("--rev1",type=Path,required=True)
    p.add_argument("--debug",type=Path,required=True)
    a=p.parse_args()
    rev0=a.rev0.read_bytes(); rev1=a.rev1.read_bytes(); debug=a.debug.read_bytes()
    r0=rev0[RETAIL[0]:RETAIL[1]]; r1=rev1[RETAIL[0]:RETAIL[1]]; dbg=debug[DEBUG[0]:DEBUG[1]]
    assert len(r0)==len(r1)==len(dbg)==0x2498
    assert r0==r1
    assert sha256(r0)==RETAIL_SHA256 and sha256(r1)==RETAIL_SHA256
    assert sha256(dbg)==DEBUG_SHA256
    assert DEBUG[0]-RETAIL[0]==0x726C and DEBUG[1]-RETAIL[1]==0x726C
    assert r0[:32]==ENTRY and dbg[:32]==ENTRY
    tr=rev0[TAIL_RETAIL[0]:TAIL_RETAIL[1]]
    td=debug[TAIL_DEBUG[0]:TAIL_DEBUG[1]]
    assert sha256(tr)==TAIL_RETAIL_SHA256 and sha256(td)==TAIL_DEBUG_SHA256
    assert tr[-12:]==(0x030073D0).to_bytes(4,"little")+(0x03007410).to_bytes(4,"little")+(0x0202F7A4).to_bytes(4,"little")
    assert td[-12:]==(0x030074E0).to_bytes(4,"little")+(0x03007520).to_bytes(4,"little")+(0x0202FA48).to_bytes(4,"little")
    assert rev0[RETAIL[1]:RETAIL[1]+32]==NEXT
    assert rev1[RETAIL[1]:RETAIL[1]+32]==NEXT
    assert debug[DEBUG[1]:DEBUG[1]+32]==NEXT
    print("German battle_anim verification passed")
    print("Retail Rev0/Rev1: 0x080759E4..0x08077E7C, 0x2498 bytes")
    print("Debug:            0x0807CC50..0x0807F0E8, 0x2498 bytes")
    print("Accumulated Retail->Debug delta remains +0x726C")
    print("Next: rom_8077ABC / GetBattlerSpriteCoord")

if __name__=="__main__":
    main()
