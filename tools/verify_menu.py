#!/usr/bin/env python3
import argparse
import hashlib
from pathlib import Path

RETAIL=(0x71F3C,0x731B8)
DEBUG=(0x791A8,0x7A424)
RETAIL_SHA256="399e9dd06ad7cab9c2062f0821b17453e8c5efb8833ff8edc5a8548d9dde1b97"
DEBUG_SHA256="e360c150e51a925e7f526ca26635819e77f2a4cb18895bc119596e71b0995160"

ENTRY=bytes.fromhex("00 b5 05 20 03 f0 88 fc")
FINAL_LITERAL=(0x020232CC).to_bytes(4,"little")

DE1_RETAIL=(0x73110,0x73174)
DE2_RETAIL=(0x73174,0x731B8)
DE1_DEBUG=(0x7A37C,0x7A3E0)
DE2_DEBUG=(0x7A3E0,0x7A424)
DE1_RETAIL_SHA="837325d4eecb84dfbe2b98addcc6c0ec4d5e27960d024da42f59c19c8d2e3f25"
DE2_RETAIL_SHA="418cf93955f6d1a33737aa82eff09e1ef07009ecf8772cd4fd62124df12cf80f"
DE1_DEBUG_SHA="f4e0163479d0ee994494c114d6eb5bce8d521f96c8814a49ba7824eab7e358d9"
DE2_DEBUG_SHA="bfd4b95344f538d822dcb7ec2aeda419eddc6efad47e998f0660d5f0694a4fef"

NEXT_PREFIX=bytes.fromhex("00 b5 81 b0 06 49 00 20 08 70 00 20 00 90 05 49 05 4a 68 46")
QUEUE_RETAIL=(0x030006C0).to_bytes(4,"little")
QUEUE_DEBUG=(0x030006E0).to_bytes(4,"little")
DMA_RETAIL=(0x0202E9D8).to_bytes(4,"little")
DMA_DEBUG=(0x0202EC7C).to_bytes(4,"little")

def sha256(data:bytes)->str:
    return hashlib.sha256(data).hexdigest()

def main()->None:
    p=argparse.ArgumentParser(description="Verify German Pokemon Ruby menu module")
    p.add_argument("--rev0",type=Path,required=True)
    p.add_argument("--rev1",type=Path,required=True)
    p.add_argument("--debug",type=Path,required=True)
    a=p.parse_args()
    rev0=a.rev0.read_bytes(); rev1=a.rev1.read_bytes(); debug=a.debug.read_bytes()
    r0=rev0[RETAIL[0]:RETAIL[1]]; r1=rev1[RETAIL[0]:RETAIL[1]]; dbg=debug[DEBUG[0]:DEBUG[1]]

    assert len(r0)==len(r1)==len(dbg)==0x127C
    assert r0==r1
    assert sha256(r0)==RETAIL_SHA256
    assert sha256(r1)==RETAIL_SHA256
    assert sha256(dbg)==DEBUG_SHA256
    assert DEBUG[0]-RETAIL[0]==0x726C
    assert DEBUG[1]-RETAIL[1]==0x726C
    assert r0.startswith(ENTRY) and dbg.startswith(ENTRY)
    assert r0[-4:]==FINAL_LITERAL and dbg[-4:]==FINAL_LITERAL

    assert sha256(rev0[DE1_RETAIL[0]:DE1_RETAIL[1]])==DE1_RETAIL_SHA
    assert sha256(rev0[DE2_RETAIL[0]:DE2_RETAIL[1]])==DE2_RETAIL_SHA
    assert sha256(debug[DE1_DEBUG[0]:DE1_DEBUG[1]])==DE1_DEBUG_SHA
    assert sha256(debug[DE2_DEBUG[0]:DE2_DEBUG[1]])==DE2_DEBUG_SHA

    assert rev0[RETAIL[1]:RETAIL[1]+len(NEXT_PREFIX)]==NEXT_PREFIX
    assert rev1[RETAIL[1]:RETAIL[1]+len(NEXT_PREFIX)]==NEXT_PREFIX
    assert debug[DEBUG[1]:DEBUG[1]+len(NEXT_PREFIX)]==NEXT_PREFIX

    assert rev0[RETAIL[1]+0x20:RETAIL[1]+0x24]==QUEUE_RETAIL
    assert debug[DEBUG[1]+0x20:DEBUG[1]+0x24]==QUEUE_DEBUG
    assert rev0[RETAIL[1]+0x24:RETAIL[1]+0x28]==DMA_RETAIL
    assert debug[DEBUG[1]+0x24:DEBUG[1]+0x28]==DMA_DEBUG

    print("German menu verification passed")
    print("Retail Rev0/Rev1: 0x08071F3C..0x080731B8, 0x127C bytes")
    print("Debug:            0x080791A8..0x0807A424, 0x127C bytes")
    print("Accumulated Retail->Debug delta remains +0x726C")
    print("Next: tileset_anim / ClearTilesetAnimDmas")

if __name__=="__main__":
    main()
