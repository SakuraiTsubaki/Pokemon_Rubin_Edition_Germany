#!/usr/bin/env python3
import argparse
import hashlib
from pathlib import Path

RETAIL=(0x7C1C0,0x7CC5C)
DEBUG=(0x83434,0x83F14)
RETAIL_SHA256="04b39c6221fdf7b12a2d274b0ced8c35d99e4c82490808b8a38b0d2c9368b2b4"
DEBUG_SHA256="e301c3aec31b83cd9038880e95e02f1e8908c5dfe8606b5920a8fc928e5f3a9f"
ENTRY=bytes.fromhex("10 b5 02 1c 30 20 11 5e 88 00 40 18 c0 00 09 49 44 18 0a 21 60 5e 00 28 0e d0 51 78 0d 20 40 42 08 40 50 70 54 20 50 84 3e 32 11 78 59 38 08 40 10 70")
PHASE3_RETAIL=(0x7CA78,0x7CBA8)
PHASE3_DEBUG=(0x83CEC,0x83E44)
PHASE3_RETAIL_SHA256="05e0926eaa6ed0d93e2aaab3eacfd9f5cb9b0858db308c7ed519a544281bc92c"
PHASE3_DEBUG_SHA256="0629023932f881ccc4abd12caf3993305dc3cd3616f6ad2cc35258ad2bf6eb62"
TESTMENU_DEBUG=(0x83E60,0x83E7C)
TESTMENU_DEBUG_SHA256="6b016e7833466b735eddf30f9b9caeef4b22049bc75beea7a5b77ebd35d49927"
UPDATE_RETAIL=(0x7CC18,0x7CC5C)
UPDATE_DEBUG=(0x83ED0,0x83F14)
UPDATE_RETAIL_SHA256="3b955f0ccfcac7c4dedc1be663e9b68d00c430d4a23fa37125866b658e5a8fff"
UPDATE_DEBUG_SHA256="cbffa9a9f56a5d8887f77cbc55b40371fee05178f919d4615845cd30fd3831d9"
NEXT_START=bytes.fromhex("70 b5 30 48")
NEXT_COMMON_8_20=bytes.fromhex("00 06 06 0e 00 2e 55 d1 90 20 40 01")

def sha256(b): return hashlib.sha256(b).hexdigest()

def main():
    p=argparse.ArgumentParser(description="Verify German Pokemon Ruby title_screen module")
    p.add_argument("--rev0",type=Path,required=True)
    p.add_argument("--rev1",type=Path,required=True)
    p.add_argument("--debug",type=Path,required=True)
    a=p.parse_args()
    r0=a.rev0.read_bytes(); r1=a.rev1.read_bytes(); dbg=a.debug.read_bytes()
    x0=r0[RETAIL[0]:RETAIL[1]]; x1=r1[RETAIL[0]:RETAIL[1]]; xd=dbg[DEBUG[0]:DEBUG[1]]
    assert len(x0)==len(x1)==0xA9C
    assert len(xd)==0xAE0
    assert x0==x1
    assert sha256(x0)==RETAIL_SHA256 and sha256(x1)==RETAIL_SHA256
    assert sha256(xd)==DEBUG_SHA256
    assert DEBUG[0]-RETAIL[0]==0x7274
    assert DEBUG[1]-RETAIL[1]==0x72B8
    assert len(xd)-len(x0)==0x44
    assert x0[:len(ENTRY)]==ENTRY and xd[:len(ENTRY)]==ENTRY

    pr=r0[PHASE3_RETAIL[0]:PHASE3_RETAIL[1]]
    pd=dbg[PHASE3_DEBUG[0]:PHASE3_DEBUG[1]]
    assert len(pr)==0x130 and len(pd)==0x158
    assert sha256(pr)==PHASE3_RETAIL_SHA256
    assert sha256(pd)==PHASE3_DEBUG_SHA256
    assert len(pd)-len(pr)==0x28

    tm=dbg[TESTMENU_DEBUG[0]:TESTMENU_DEBUG[1]]
    assert len(tm)==0x1C and sha256(tm)==TESTMENU_DEBUG_SHA256

    assert sha256(r0[UPDATE_RETAIL[0]:UPDATE_RETAIL[1]])==UPDATE_RETAIL_SHA256
    assert sha256(dbg[UPDATE_DEBUG[0]:UPDATE_DEBUG[1]])==UPDATE_DEBUG_SHA256

    for data,start in ((r0,RETAIL[1]),(r1,RETAIL[1]),(dbg,DEBUG[1])):
        assert data[start:start+4]==NEXT_START
        assert data[start+8:start+20]==NEXT_COMMON_8_20

    print("German title_screen verification passed")
    print("Retail Rev0/Rev1: 0x0807C1C0..0x0807CC5C, 0xA9C bytes")
    print("Debug:            0x08083434..0x08083F14, 0xAE0 bytes")
    print("Debug growth: 0x44 bytes = Task_TitleScreenPhase3 +0x28, CB2_GoToTestMenu +0x1C")
    print("Accumulated Retail->Debug delta changes +0x7274 -> +0x72B8")
    print("Next: field_weather / StartWeather")

if __name__=="__main__": main()
