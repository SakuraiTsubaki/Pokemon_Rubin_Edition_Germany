#!/usr/bin/env python3
import argparse
import hashlib
from pathlib import Path

RETAIL=(0x7B114,0x7BA5C)
DEBUG=(0x82388,0x82CD0)
RETAIL_SHA256="4fc253119d97ce63c123ffcde3b7a20fc687881ae4d6f6b75efa671765ec6507"
DEBUG_SHA256="5478096f86521a4cda821e393ce4ba5ec2bd519de9f6cd6a7e56e2dc4a42aba0"
ENTRY=bytes.fromhex("70 47 00 00 00 b5 0d 4a 10 7a 80 21 08 43 10 72 00 20")
NEXT=bytes.fromhex("f0 b5 47 46 80 b4 04 1c 0d 1c 24 06 24 0e 2d 06 2d 0e 24 48 20 18 06 78 23 48 0a 21 ff f7")

def sha256(data):
    return hashlib.sha256(data).hexdigest()

def main():
    p=argparse.ArgumentParser(description="Verify German Pokemon Ruby reshow_battle_screen module")
    p.add_argument("--rev0",type=Path,required=True)
    p.add_argument("--rev1",type=Path,required=True)
    p.add_argument("--debug",type=Path,required=True)
    a=p.parse_args()
    r0=a.rev0.read_bytes(); r1=a.rev1.read_bytes(); dbg=a.debug.read_bytes()
    x0=r0[RETAIL[0]:RETAIL[1]]; x1=r1[RETAIL[0]:RETAIL[1]]; xd=dbg[DEBUG[0]:DEBUG[1]]
    assert len(x0)==len(x1)==len(xd)==0x948
    assert x0==x1
    assert sha256(x0)==RETAIL_SHA256 and sha256(x1)==RETAIL_SHA256
    assert sha256(xd)==DEBUG_SHA256
    assert DEBUG[0]-RETAIL[0]==0x7274 and DEBUG[1]-RETAIL[1]==0x7274
    assert x0[:len(ENTRY)]==ENTRY and xd[:len(ENTRY)]==ENTRY
    assert r0[RETAIL[1]:RETAIL[1]+len(NEXT)]==NEXT
    assert r1[RETAIL[1]:RETAIL[1]+len(NEXT)]==NEXT
    assert dbg[DEBUG[1]:DEBUG[1]+len(NEXT)]==NEXT
    print("German reshow_battle_screen verification passed")
    print("Retail Rev0/Rev1: 0x0807B114..0x0807BA5C, 0x948 bytes")
    print("Debug:            0x08082388..0x08082CD0, 0x948 bytes")
    print("Accumulated Retail->Debug delta remains +0x7274")
    print("Next: battle_anim_status_effects")

if __name__=="__main__":
    main()
