#!/usr/bin/env python3
import argparse
import hashlib
from pathlib import Path

RETAIL=(0x7CC5C,0x7E2AC)
DEBUG=(0x83F14,0x85660)
RETAIL_SHA256="65ba9a03483a5b4582d2484bb26c8993ed8ce9d2f1eae56cb9b37ebc4b173cf8"
DEBUG_SHA256="e45bd520d56f26c9f5eac43dabde70ad7146e9182b06ff8929ea3dcae846e9c7"
ENTRY_START=bytes.fromhex("70 b5 30 48")
ENTRY_COMMON=bytes.fromhex("00 06 06 0e 00 2e 55 d1 90 20 40 01")
LAST_RETAIL=(0x7E29C,0x7E2AC)
LAST_DEBUG=(0x85554,0x85564)
LAST_RETAIL_SHA256="e9e2e88b835b73156afabff9d07d55285bc3a039572b43a6825791769ad2c33a"
LAST_DEBUG_SHA256="d0b6eb4feccd7aaa7170c0bb881baeaf364dd397f1640b40f516c2fd8e80e141"
DBG1=(0x85564,0x8560C)
DBG2=(0x8560C,0x85660)
DBG1_SHA256="ea49cdc926960635156453ff66e6fac79ac6f1b5dbc41994efd220211925950b"
DBG2_SHA256="75abe94de07942eec0e6b6998eb34861c6e62b9a609ff0b2a2d1620f20bd63a8"
NEXT_PREFIX=bytes.fromhex("00 b5 0d 48 00 68 0d 4a 81 18 00 22 0a 70 0c 49 43 18 14 21 19 70 0b 4b c1 18 0a 70 06 3b c1 18 0a 80 09 49 40 18 00 78 00 28 03 d1 00 20 10 21")

def sha256(b): return hashlib.sha256(b).hexdigest()

def main():
    p=argparse.ArgumentParser(description="Verify German Pokemon Ruby field_weather module")
    p.add_argument("--rev0",type=Path,required=True)
    p.add_argument("--rev1",type=Path,required=True)
    p.add_argument("--debug",type=Path,required=True)
    a=p.parse_args()
    r0=a.rev0.read_bytes(); r1=a.rev1.read_bytes(); dbg=a.debug.read_bytes()
    x0=r0[RETAIL[0]:RETAIL[1]]; x1=r1[RETAIL[0]:RETAIL[1]]; xd=dbg[DEBUG[0]:DEBUG[1]]
    assert len(x0)==len(x1)==0x1650
    assert len(xd)==0x174C
    assert x0==x1
    assert sha256(x0)==RETAIL_SHA256 and sha256(x1)==RETAIL_SHA256
    assert sha256(xd)==DEBUG_SHA256
    assert DEBUG[0]-RETAIL[0]==0x72B8
    assert DEBUG[1]-RETAIL[1]==0x73B4
    assert len(xd)-len(x0)==0xFC

    for data,start in ((r0,RETAIL[0]),(r1,RETAIL[0]),(dbg,DEBUG[0])):
        assert data[start:start+4]==ENTRY_START
        assert data[start+8:start+20]==ENTRY_COMMON

    assert sha256(r0[LAST_RETAIL[0]:LAST_RETAIL[1]])==LAST_RETAIL_SHA256
    assert sha256(dbg[LAST_DEBUG[0]:LAST_DEBUG[1]])==LAST_DEBUG_SHA256

    d1=dbg[DBG1[0]:DBG1[1]]
    d2=dbg[DBG2[0]:DBG2[1]]
    assert len(d1)==0xA8 and sha256(d1)==DBG1_SHA256
    assert len(d2)==0x54 and sha256(d2)==DBG2_SHA256
    assert len(d1)+len(d2)==0xFC

    assert r0[RETAIL[1]:RETAIL[1]+len(NEXT_PREFIX)]==NEXT_PREFIX
    assert r1[RETAIL[1]:RETAIL[1]+len(NEXT_PREFIX)]==NEXT_PREFIX
    assert dbg[DEBUG[1]:DEBUG[1]+len(NEXT_PREFIX)]==NEXT_PREFIX

    print("German field_weather verification passed")
    print("Retail Rev0/Rev1: 0x0807CC5C..0x0807E2AC, 0x1650 bytes")
    print("Debug:            0x08083F14..0x08085660, 0x174C bytes")
    print("Debug growth: 0xFC bytes = debug_sub_8085564 (0xA8) + debug_sub_808560C (0x54)")
    print("Accumulated Retail->Debug delta changes +0x72B8 -> +0x73B4")
    print("Next: field_weather_effects / Clouds_InitVars")

if __name__=="__main__": main()
