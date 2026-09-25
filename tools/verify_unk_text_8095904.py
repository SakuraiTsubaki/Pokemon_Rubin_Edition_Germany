#!/usr/bin/env python3
import argparse
import hashlib
from pathlib import Path

RETAIL=(0x95A54,0x95C2C)
DEBUG=(0xA2FA4,0xA317C)
RETAIL_SHA256="7c97512f9b583eaab1ba4494db45187ac232d32f869c332429e3f50473beba3a"
DEBUG_SHA256="fab4730ceb6435ea9f6ecbe2c321d83f4557bca896e0564a8e085698b1305a4c"
ENTRY=bytes.fromhex("f0 b5 57 46 4e 46 45 46 e0 b4 87 b0 00 90 0f 1c 14 1c 0f 98 24 06 24 0e 1b 04 1b 0c 01 93 00 06")
SECOND_R=(0x95B98,0x95C2C)
SECOND_D=(0xA30E8,0xA317C)
SECOND_SHA256="08470fd10cdfb958daf4abd90a4e9bbd3f70a8dbaf8309af09de31d5a57770f8"
NEXT=bytes.fromhex("70 b5 00 06 00 0e 00 24 00 25 81 00 09 18 08 01 40 1a 46 01 a0 00 00 19 00 01 0a 49 40 18 30 18")

def sha256(data): return hashlib.sha256(data).hexdigest()

def main():
    p=argparse.ArgumentParser(description="Verify German Pokemon Ruby unk_text_8095904 module")
    p.add_argument("--rev0",type=Path,required=True)
    p.add_argument("--rev1",type=Path,required=True)
    p.add_argument("--debug",type=Path,required=True)
    a=p.parse_args()
    r0=a.rev0.read_bytes(); r1=a.rev1.read_bytes(); d=a.debug.read_bytes()
    x0=r0[RETAIL[0]:RETAIL[1]]; x1=r1[RETAIL[0]:RETAIL[1]]; xd=d[DEBUG[0]:DEBUG[1]]
    assert len(x0)==len(x1)==len(xd)==0x1D8
    assert x0==x1
    assert sha256(x0)==RETAIL_SHA256 and sha256(x1)==RETAIL_SHA256
    assert sha256(xd)==DEBUG_SHA256
    assert DEBUG[0]-RETAIL[0]==DEBUG[1]-RETAIL[1]==0xD550
    assert x0[:len(ENTRY)]==ENTRY and xd[:len(ENTRY)]==ENTRY
    s0=r0[SECOND_R[0]:SECOND_R[1]]
    sd=d[SECOND_D[0]:SECOND_D[1]]
    assert s0==sd and sha256(s0)==SECOND_SHA256
    assert r0[RETAIL[1]:RETAIL[1]+len(NEXT)]==NEXT
    assert r1[RETAIL[1]:RETAIL[1]+len(NEXT)]==NEXT
    assert d[DEBUG[1]:DEBUG[1]+len(NEXT)]==NEXT
    print("German unk_text_8095904 verification passed")
    print("Retail Rev0/Rev1: 0x08095A54..0x08095C2C, 0x1D8 bytes")
    print("Debug:            0x080A2FA4..0x080A317C, 0x1D8 bytes")
    print("Accumulated Retail->Debug delta remains +0xD550")
    print("Next: pokemon_storage_system / CountPokemonInBoxN")

if __name__=="__main__":
    main()
