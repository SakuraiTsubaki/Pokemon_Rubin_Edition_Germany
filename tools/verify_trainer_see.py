#!/usr/bin/env python3
import argparse
import hashlib
from pathlib import Path

RETAIL=(0x84410,0x84DCC)
DEBUG=(0x9177C,0x92138)
RETAIL_SHA256="47081b39ac7750874dc7441a768a4053b922dc7445d5b605e578062863d79b18"
DEBUG_SHA256="ce5879427fd13bf636c31ee85ccbc4f8f06c5dac625e81177c0a4bf532a7c748"
ENTRY=bytes.fromhex("30 b5 00 24 0a 4d e0 00 00 19 80 00 41 19 08 78 c0 07 00 28 0e d0 c8 79 01 28 01 d0 03 28 09 d1")
TAIL_RETAIL=(0x84D34,0x84DCC)
TAIL_DEBUG=(0x920A0,0x92138)
TAIL_RETAIL_SHA256="cfb42c98e9a778414924ecd58ee3107c724f6a2b64d3b56e5a3293bc93678792"
TAIL_DEBUG_SHA256="b17fc9ff4c4876e0024eee1759cd0adefbb711d949738d19ba7b316fb53f8553"
NEXT=bytes.fromhex("01 49 08 70 70 47 00 00")

def sha256(data): return hashlib.sha256(data).hexdigest()

def main():
    p=argparse.ArgumentParser(description="Verify German Pokemon Ruby trainer_see module")
    p.add_argument("--rev0",type=Path,required=True)
    p.add_argument("--rev1",type=Path,required=True)
    p.add_argument("--debug",type=Path,required=True)
    a=p.parse_args()
    r0=a.rev0.read_bytes(); r1=a.rev1.read_bytes(); dbg=a.debug.read_bytes()
    x0=r0[RETAIL[0]:RETAIL[1]]; x1=r1[RETAIL[0]:RETAIL[1]]; xd=dbg[DEBUG[0]:DEBUG[1]]
    assert len(x0)==len(x1)==len(xd)==0x9BC
    assert x0==x1
    assert sha256(x0)==RETAIL_SHA256 and sha256(x1)==RETAIL_SHA256
    assert sha256(xd)==DEBUG_SHA256
    assert DEBUG[0]-RETAIL[0]==0xD36C and DEBUG[1]-RETAIL[1]==0xD36C
    assert x0[:len(ENTRY)]==ENTRY and xd[:len(ENTRY)]==ENTRY
    assert sha256(r0[TAIL_RETAIL[0]:TAIL_RETAIL[1]])==TAIL_RETAIL_SHA256
    assert sha256(dbg[TAIL_DEBUG[0]:TAIL_DEBUG[1]])==TAIL_DEBUG_SHA256
    assert r0[RETAIL[1]:RETAIL[1]+8]==NEXT
    assert r1[RETAIL[1]:RETAIL[1]+8]==NEXT
    assert dbg[DEBUG[1]:DEBUG[1]+8]==NEXT
    assert int.from_bytes(r0[RETAIL[1]+8:RETAIL[1]+12],"little")==0x0202FF7C
    assert int.from_bytes(dbg[DEBUG[1]+8:DEBUG[1]+12],"little")==0x02030228
    print("German trainer_see verification passed")
    print("Retail Rev0/Rev1: 0x08084410..0x08084DCC, 0x9BC bytes")
    print("Debug:            0x0809177C..0x08092138, 0x9BC bytes")
    print("Accumulated Retail->Debug delta remains +0xD36C")
    print("Next: wild_encounter / DisableWildEncounters")

if __name__=="__main__":
    main()
