#!/usr/bin/env python3
import argparse
import hashlib
from pathlib import Path

RETAIL=(0x73DD4,0x74F6C)
DEBUG=(0x7B040,0x7C1D8)
RETAIL_SHA256="00253a220123b34da98a8f730bbd40566732cd88f3062ed8535393bf98915e22"
DEBUG_SHA256="68f011f71b92e1c424fe5767d750d9ff8a32ad2db28a8c1cd7510d4cc4f2a3ba"

ENTRY=bytes.fromhex("70 b5 0c 1c 15 1c 24 04 24 0c 2d 04 0a 4e 31 1c")
UNFADED_RETAIL=(0x0202EAC8).to_bytes(4,"little")
UNFADED_DEBUG=(0x0202ED6C).to_bytes(4,"little")
FADED_RETAIL=(0x0202EEC8).to_bytes(4,"little")
FADED_DEBUG=(0x0202F16C).to_bytes(4,"little")
NEXT=bytes.fromhex("00 b5 03 49 00 20 08 70 00 f0 80 f8 01 bc 00 47")
DISABLE_RETAIL=(0x03004AFC).to_bytes(4,"little")
DISABLE_DEBUG=(0x03004BD4).to_bytes(4,"little")

def sha256(data:bytes)->str:
    return hashlib.sha256(data).hexdigest()

def main()->None:
    p=argparse.ArgumentParser(description="Verify German Pokemon Ruby palette module")
    p.add_argument("--rev0",type=Path,required=True); p.add_argument("--rev1",type=Path,required=True); p.add_argument("--debug",type=Path,required=True)
    a=p.parse_args()
    rev0=a.rev0.read_bytes(); rev1=a.rev1.read_bytes(); debug=a.debug.read_bytes()
    r0=rev0[RETAIL[0]:RETAIL[1]]; r1=rev1[RETAIL[0]:RETAIL[1]]; dbg=debug[DEBUG[0]:DEBUG[1]]

    assert len(r0)==len(r1)==len(dbg)==0x1198
    assert r0==r1
    assert sha256(r0)==RETAIL_SHA256 and sha256(r1)==RETAIL_SHA256 and sha256(dbg)==DEBUG_SHA256
    assert DEBUG[0]-RETAIL[0]==0x726C and DEBUG[1]-RETAIL[1]==0x726C
    assert r0.startswith(ENTRY) and dbg.startswith(ENTRY)

    assert UNFADED_RETAIL in r0[-0x100:] and FADED_RETAIL in r0[-0x100:]
    assert UNFADED_DEBUG in dbg[-0x100:] and FADED_DEBUG in dbg[-0x100:]

    assert rev0[RETAIL[1]:RETAIL[1]+len(NEXT)]==NEXT
    assert rev1[RETAIL[1]:RETAIL[1]+len(NEXT)]==NEXT
    assert debug[DEBUG[1]:DEBUG[1]+len(NEXT)]==NEXT
    assert rev0[RETAIL[1]+0x10:RETAIL[1]+0x14]==DISABLE_RETAIL
    assert debug[DEBUG[1]+0x10:DEBUG[1]+0x14]==DISABLE_DEBUG

    print("German palette verification passed")
    print("Retail Rev0/Rev1: 0x08073DD4..0x08074F6C, 0x1198 bytes")
    print("Debug:            0x0807B040..0x0807C1D8, 0x1198 bytes")
    print("Accumulated Retail->Debug delta remains +0x726C")
    print("Next: sound / InitMapMusic")

if __name__=="__main__":
    main()
