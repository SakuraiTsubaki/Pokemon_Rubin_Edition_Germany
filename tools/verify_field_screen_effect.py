#!/usr/bin/env python3
import argparse
import hashlib
from pathlib import Path

RETAIL=(0x817A0,0x81D94)
DEBUG=(0x88B68,0x8915C)
RETAIL_SHA256="dc3058ebd07b7a27a381d1b75b9f095c3bdc9d94e70d90076d608ca68cf6782d"
DEBUG_SHA256="131727fd66761d42156daeb30b806f7312f912673d8d4aa4d5cba54b5024c2a1"
ENTRY=bytes.fromhex("00 b5 a0 29 10 d8 00 2a 00 da 00 22 ff 2a 00 dd ff 22 00 2b 00 da 00 23 ff 2b 00 dd ff 23 49 00 09 18 10 02 18 43 08 80 01 bc 00 47")
LAST_RETAIL=(0x81D70,0x81D94)
LAST_DEBUG=(0x89138,0x8915C)
LAST_RETAIL_SHA256="3c94a205e2b9de6a41b71323c3dd1c575fd09bd542c3e173a3602e163d90c8dc"
LAST_DEBUG_SHA256="c68c8330ca0f2db300e043aeef5a6b859eedbfaab9e6c56a1722ba96364e026a"
NEXT=bytes.fromhex("30 b5 00 06 05 0e a8 00 40 19 c0 00 04 49 44 18 00 21 60 5e 00 28 05 d0 01 28 0e d0 1d e0 00 00")

def sha256(data): return hashlib.sha256(data).hexdigest()

def main():
    p=argparse.ArgumentParser(description="Verify German Pokemon Ruby field_screen_effect module")
    p.add_argument("--rev0",type=Path,required=True)
    p.add_argument("--rev1",type=Path,required=True)
    p.add_argument("--debug",type=Path,required=True)
    a=p.parse_args()
    r0=a.rev0.read_bytes(); r1=a.rev1.read_bytes(); dbg=a.debug.read_bytes()
    x0=r0[RETAIL[0]:RETAIL[1]]; x1=r1[RETAIL[0]:RETAIL[1]]; xd=dbg[DEBUG[0]:DEBUG[1]]
    assert len(x0)==len(x1)==len(xd)==0x5F4
    assert x0==x1
    assert sha256(x0)==RETAIL_SHA256 and sha256(x1)==RETAIL_SHA256
    assert sha256(xd)==DEBUG_SHA256
    assert DEBUG[0]-RETAIL[0]==0x73C8 and DEBUG[1]-RETAIL[1]==0x73C8
    assert x0[:len(ENTRY)]==ENTRY and xd[:len(ENTRY)]==ENTRY
    assert sha256(r0[LAST_RETAIL[0]:LAST_RETAIL[1]])==LAST_RETAIL_SHA256
    assert sha256(dbg[LAST_DEBUG[0]:LAST_DEBUG[1]])==LAST_DEBUG_SHA256
    assert r0[RETAIL[1]:RETAIL[1]+len(NEXT)]==NEXT
    assert r1[RETAIL[1]:RETAIL[1]+len(NEXT)]==NEXT
    assert dbg[DEBUG[1]:DEBUG[1]+len(NEXT)]==NEXT
    print("German field_screen_effect verification passed")
    print("Retail Rev0/Rev1: 0x080817A0..0x08081D94, 0x5F4 bytes")
    print("Debug:            0x08088B68..0x0808915C, 0x5F4 bytes")
    print("Accumulated Retail->Debug delta remains +0x73C8")
    print("Next: battle_setup / Task_BattleStart")

if __name__=="__main__":
    main()
