#!/usr/bin/env python3
import argparse
import hashlib
from pathlib import Path

RETAIL=(0x731B8,0x73DD4)
DEBUG=(0x7A424,0x7B040)
RETAIL_SHA256="7011b493762e4c0d139d5131f086d25f350b721c508af6e1c703821d68a54ae3"
DEBUG_SHA256="f784aeb3924ed7c71106fdc69fc74202927ba96547673242fd4c76981f8393b9"

ENTRY=bytes.fromhex("00 b5 81 b0 06 49 00 20 08 70 00 20 00 90 05 49 05 4a 68 46")
QUEUE_RETAIL=(0x030006C0).to_bytes(4,"little")
QUEUE_DEBUG=(0x030006E0).to_bytes(4,"little")
DMA_RETAIL=(0x0202E9D8).to_bytes(4,"little")
DMA_DEBUG=(0x0202EC7C).to_bytes(4,"little")
TAIL_DEST=(0x06007E00).to_bytes(4,"little")
NEXT=bytes.fromhex("70 b5 0c 1c 15 1c 24 04 24 0c 2d 04 0a 4e 31 1c")

def sha256(data:bytes)->str:
    return hashlib.sha256(data).hexdigest()

def main()->None:
    p=argparse.ArgumentParser(description="Verify German Pokemon Ruby tileset_anim module")
    p.add_argument("--rev0",type=Path,required=True); p.add_argument("--rev1",type=Path,required=True); p.add_argument("--debug",type=Path,required=True)
    a=p.parse_args()
    rev0=a.rev0.read_bytes(); rev1=a.rev1.read_bytes(); debug=a.debug.read_bytes()
    r0=rev0[RETAIL[0]:RETAIL[1]]; r1=rev1[RETAIL[0]:RETAIL[1]]; dbg=debug[DEBUG[0]:DEBUG[1]]

    assert len(r0)==len(r1)==len(dbg)==0xC1C
    assert r0==r1
    assert sha256(r0)==RETAIL_SHA256 and sha256(r1)==RETAIL_SHA256 and sha256(dbg)==DEBUG_SHA256
    assert DEBUG[0]-RETAIL[0]==0x726C and DEBUG[1]-RETAIL[1]==0x726C
    assert r0.startswith(ENTRY) and dbg.startswith(ENTRY)

    assert r0[0x20:0x24]==QUEUE_RETAIL
    assert dbg[0x20:0x24]==QUEUE_DEBUG
    assert r0[0x24:0x28]==DMA_RETAIL
    assert dbg[0x24:0x28]==DMA_DEBUG
    assert r0[-4:]==TAIL_DEST and dbg[-4:]==TAIL_DEST

    assert rev0[RETAIL[1]:RETAIL[1]+len(NEXT)]==NEXT
    assert rev1[RETAIL[1]:RETAIL[1]+len(NEXT)]==NEXT
    assert debug[DEBUG[1]:DEBUG[1]+len(NEXT)]==NEXT

    print("German tileset_anim verification passed")
    print("Retail Rev0/Rev1: 0x080731B8..0x08073DD4, 0xC1C bytes")
    print("Debug:            0x0807A424..0x0807B040, 0xC1C bytes")
    print("Accumulated Retail->Debug delta remains +0x726C")
    print("Next: palette / LoadCompressedPalette")

if __name__=="__main__":
    main()
