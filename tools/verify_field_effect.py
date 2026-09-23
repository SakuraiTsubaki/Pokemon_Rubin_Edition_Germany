#!/usr/bin/env python3
import argparse
import hashlib
from pathlib import Path

RETAIL=(0x85ABC,0x899CC)
DEBUG=(0x92E88,0x96D98)
RETAIL_SHA256="e418e172cdc0829670b913fdf38594527b10e679132790a06b6851fbc43281aa"
DEBUG_SHA256="b7072798d60d961371bc0c636b19ae2afe6f00e950625f966666c4400eeb5bb3"
ENTRY=bytes.fromhex("30 b5 82 b0 04 1c 24 06 24 0e 20 1c")
TAIL_RETAIL=(0x89950,0x899CC)
TAIL_DEBUG=(0x96D1C,0x96D98)
TAIL_RETAIL_SHA256="863bbc7bc016752fa840645f1d4b41a06486dfd5f76f47fbe67235906cf662de"
TAIL_DEBUG_SHA256="f9f711a6e6face161e28afdddf007e5a1893985043b835c35597988b5039e942"
NEXT=bytes.fromhex("10 b5 0b 4c 00 20 60 75 0a 49 4a 89 0a 48 10 40 48 81 4a 89 09 48 10 40 48 81 48 89 20 7e ff 28 03 d0")

def sha256(data): return hashlib.sha256(data).hexdigest()

def main():
    p=argparse.ArgumentParser(description="Verify German Pokemon Ruby field_effect module")
    p.add_argument("--rev0",type=Path,required=True)
    p.add_argument("--rev1",type=Path,required=True)
    p.add_argument("--debug",type=Path,required=True)
    a=p.parse_args()
    r0=a.rev0.read_bytes(); r1=a.rev1.read_bytes(); dbg=a.debug.read_bytes()
    x0=r0[RETAIL[0]:RETAIL[1]]; x1=r1[RETAIL[0]:RETAIL[1]]; xd=dbg[DEBUG[0]:DEBUG[1]]
    assert len(x0)==len(x1)==len(xd)==0x3F10
    assert x0==x1
    assert sha256(x0)==RETAIL_SHA256 and sha256(x1)==RETAIL_SHA256
    assert sha256(xd)==DEBUG_SHA256
    assert DEBUG[0]-RETAIL[0]==0xD3CC and DEBUG[1]-RETAIL[1]==0xD3CC
    assert x0[:len(ENTRY)]==ENTRY and xd[:len(ENTRY)]==ENTRY
    assert sha256(r0[TAIL_RETAIL[0]:TAIL_RETAIL[1]])==TAIL_RETAIL_SHA256
    assert sha256(dbg[TAIL_DEBUG[0]:TAIL_DEBUG[1]])==TAIL_DEBUG_SHA256
    assert r0[RETAIL[1]:RETAIL[1]+len(NEXT)]==NEXT
    assert r1[RETAIL[1]:RETAIL[1]+len(NEXT)]==NEXT
    assert dbg[DEBUG[1]:DEBUG[1]+len(NEXT)]==NEXT
    print("German field_effect verification passed")
    print("Retail Rev0/Rev1: 0x08085ABC..0x080899CC, 0x3F10 bytes")
    print("Debug:            0x08092E88..0x08096D98, 0x3F10 bytes")
    print("Accumulated Retail->Debug delta remains +0xD3CC")
    print("Next: scanline_effect / ScanlineEffect_Stop")

if __name__=="__main__":
    main()
