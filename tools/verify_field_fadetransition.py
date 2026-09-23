#!/usr/bin/env python3
import argparse
import hashlib
from pathlib import Path

RETAIL=(0x80CA8,0x817A0)
DEBUG=(0x8805C,0x88B68)
RETAIL_SHA256="f96353b9c87675df5ce13131a1fca193b058f8dda2a2770fa1baedf49dc34068"
DEBUG_SHA256="1e8a0f4842a41da185180921af4747d6b63f0eb81bedae9b88edf0b01100a8dd"
ENTRY=bytes.fromhex("00 b5 81 b0 04 48 00 90 04 49 05 4a 68 46")
DEBUG_ONLY=(0x888D8,0x888EC)
DEBUG_ONLY_SHA256="ebf96fac7b416d1e95e002459d594edc90f429311a2468148935b698d33e3857"
LAST_RETAIL=(0x81768,0x817A0)
LAST_DEBUG=(0x88B30,0x88B68)
LAST_RETAIL_SHA256="bb3a28ad81d2475c472a45c8aca141095b78c2e80ea28a2001b0294f1c0d12aa"
LAST_DEBUG_SHA256="2ec098ec081f221e2158188eb5db786baed13fbce2bfa7049a60c889ccc0846e"
NEXT=bytes.fromhex("00 b5 a0 29 10 d8 00 2a 00 da 00 22 ff 2a 00 dd ff 22 00 2b 00 da 00 23 ff 2b 00 dd ff 23 49 00 09 18 10 02 18 43 08 80 01 bc 00 47 f0 b5 57 46")

def sha256(data): return hashlib.sha256(data).hexdigest()

def main():
    p=argparse.ArgumentParser(description="Verify German Pokemon Ruby field_fadetransition module")
    p.add_argument("--rev0",type=Path,required=True)
    p.add_argument("--rev1",type=Path,required=True)
    p.add_argument("--debug",type=Path,required=True)
    a=p.parse_args()
    r0=a.rev0.read_bytes(); r1=a.rev1.read_bytes(); dbg=a.debug.read_bytes()
    x0=r0[RETAIL[0]:RETAIL[1]]; x1=r1[RETAIL[0]:RETAIL[1]]; xd=dbg[DEBUG[0]:DEBUG[1]]
    assert len(x0)==len(x1)==0xAF8
    assert len(xd)==0xB0C
    assert x0==x1
    assert sha256(x0)==RETAIL_SHA256 and sha256(x1)==RETAIL_SHA256
    assert sha256(xd)==DEBUG_SHA256
    assert DEBUG[0]-RETAIL[0]==0x73B4
    assert DEBUG[1]-RETAIL[1]==0x73C8
    assert len(xd)-len(x0)==0x14
    assert x0[:len(ENTRY)]==ENTRY and xd[:len(ENTRY)]==ENTRY

    extra=dbg[DEBUG_ONLY[0]:DEBUG_ONLY[1]]
    assert len(extra)==0x14 and sha256(extra)==DEBUG_ONLY_SHA256
    assert extra[:2]==bytes.fromhex("00 b5")
    assert extra[-6:]==bytes.fromhex("01 bc 00 47 00 00")

    assert sha256(r0[LAST_RETAIL[0]:LAST_RETAIL[1]])==LAST_RETAIL_SHA256
    assert sha256(dbg[LAST_DEBUG[0]:LAST_DEBUG[1]])==LAST_DEBUG_SHA256

    assert r0[RETAIL[1]:RETAIL[1]+len(NEXT)]==NEXT
    assert r1[RETAIL[1]:RETAIL[1]+len(NEXT)]==NEXT
    assert dbg[DEBUG[1]:DEBUG[1]+len(NEXT)]==NEXT

    print("German field_fadetransition verification passed")
    print("Retail Rev0/Rev1: 0x08080CA8..0x080817A0, 0xAF8 bytes")
    print("Debug:            0x0808805C..0x08088B68, 0xB0C bytes")
    print("Debug growth: 0x14 bytes in debug_sub_80888D8")
    print("Accumulated Retail->Debug delta changes +0x73B4 -> +0x73C8")
    print("Next: field_screen_effect / SetFlashScanlineEffectWindowBoundary")

if __name__=="__main__":
    main()
