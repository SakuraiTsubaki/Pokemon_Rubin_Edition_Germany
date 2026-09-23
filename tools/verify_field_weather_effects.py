#!/usr/bin/env python3
import argparse
import hashlib
from pathlib import Path

RETAIL=(0x7E2AC,0x80CA8)
DEBUG=(0x85660,0x8805C)
RETAIL_SHA256="98060a9865c5cb3ff0063d8a0690b12597ccf7f14faafefaff17c9aa954920e1"
DEBUG_SHA256="f6f8ba11e0c8e6d356c26ef7a053d68785e2699933f06176d6fdc76f8ee68780"
ENTRY=bytes.fromhex("00 b5 0d 48 00 68 0d 4a 81 18 00 22 0a 70 0c 49 43 18 14 21 19 70 0b 4b c1 18 0a 70 06 3b c1 18 0a 80 09 49 40 18 00 78 00 28 03 d1 00 20 10 21")
LAST_RETAIL=(0x80C88,0x80CA8)
LAST_DEBUG=(0x8803C,0x8805C)
LAST_RETAIL_SHA256="12e8879d7e0e70c121609d1eb1833fc782eea64c2f4eb6e7c4a1a0b45367780f"
LAST_DEBUG_SHA256="d247f4096e91cced24bf183ffc36cd1f94794531c676df80e46ad7eab01b9ac4"
WHITE_RETAIL=(0x80CA8,0x80CCC)
WHITE_DEBUG=(0x8805C,0x88080)
BLACK_RETAIL=(0x80CCC,0x80CEC)
BLACK_DEBUG=(0x88080,0x880A0)
WHITE_COMMON_HEAD=bytes.fromhex("00 b5 81 b0 04 48 00 90 04 49 05 4a 68 46")
WHITE_COMMON_TAIL=bytes.fromhex("01 b0 01 bc 00 47 ff 7f ff 7f")
BLACK_COMMON_HEAD=bytes.fromhex("00 b5 81 b0 00 20 00 90 03 49 04 4a 68 46")

def sha256(data): return hashlib.sha256(data).hexdigest()

def main():
    p=argparse.ArgumentParser(description="Verify German Pokemon Ruby field_weather_effects module")
    p.add_argument("--rev0",type=Path,required=True)
    p.add_argument("--rev1",type=Path,required=True)
    p.add_argument("--debug",type=Path,required=True)
    a=p.parse_args()
    r0=a.rev0.read_bytes(); r1=a.rev1.read_bytes(); dbg=a.debug.read_bytes()
    x0=r0[RETAIL[0]:RETAIL[1]]; x1=r1[RETAIL[0]:RETAIL[1]]; xd=dbg[DEBUG[0]:DEBUG[1]]
    assert len(x0)==len(x1)==len(xd)==0x29FC
    assert x0==x1
    assert sha256(x0)==RETAIL_SHA256 and sha256(x1)==RETAIL_SHA256
    assert sha256(xd)==DEBUG_SHA256
    assert DEBUG[0]-RETAIL[0]==0x73B4 and DEBUG[1]-RETAIL[1]==0x73B4
    assert x0[:len(ENTRY)]==ENTRY and xd[:len(ENTRY)]==ENTRY
    assert sha256(r0[LAST_RETAIL[0]:LAST_RETAIL[1]])==LAST_RETAIL_SHA256
    assert sha256(dbg[LAST_DEBUG[0]:LAST_DEBUG[1]])==LAST_DEBUG_SHA256

    wr=r0[WHITE_RETAIL[0]:WHITE_RETAIL[1]]
    wd=dbg[WHITE_DEBUG[0]:WHITE_DEBUG[1]]
    assert len(wr)==len(wd)==0x24
    assert wr[:14]==WHITE_COMMON_HEAD and wd[:14]==WHITE_COMMON_HEAD
    assert wr[18:28]==WHITE_COMMON_TAIL and wd[18:28]==WHITE_COMMON_TAIL
    assert wr[-8:]==bytes.fromhex("c8 ee 02 02 00 01 00 01")
    assert wd[-8:]==bytes.fromhex("6c f1 02 02 00 01 00 01")

    br=r0[BLACK_RETAIL[0]:BLACK_RETAIL[1]]
    bd=dbg[BLACK_DEBUG[0]:BLACK_DEBUG[1]]
    assert br[:14]==BLACK_COMMON_HEAD and bd[:14]==BLACK_COMMON_HEAD
    assert br[-8:]==bytes.fromhex("c8 ee 02 02 00 01 00 01")
    assert bd[-8:]==bytes.fromhex("6c f1 02 02 00 01 00 01")

    print("German field_weather_effects verification passed")
    print("Retail Rev0/Rev1: 0x0807E2AC..0x08080CA8, 0x29FC bytes")
    print("Debug:            0x08085660..0x0808805C, 0x29FC bytes")
    print("Accumulated Retail->Debug delta remains +0x73B4")
    print("Next: field_fadetransition / palette_bg_fill_white")

if __name__=="__main__":
    main()
