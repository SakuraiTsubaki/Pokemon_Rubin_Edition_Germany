#!/usr/bin/env python3
import argparse
import hashlib
from pathlib import Path

RETAIL=(0x83108,0x84144)
DEBUG=(0x8A4D0,0x8B85C)
RETAIL_SHA256="28df0fa5ac7207668dede82697ea774f85b995f712444400e1b7c1c93ad649a7"
DEBUG_SHA256="df55b1561074d791e2a2c732d41bfef302d3776f04d2041fd7c95c6cdc87df99"

RETAIL_ENTRY=bytes.fromhex("70 b5 00 06 06 0e 09 06 0d 0e 0c 4c 20 1c")
DEBUG_ENTRY=bytes.fromhex("00 b5 01 1c 02 48 81 42 04 d1 01 20")

DEBUG_TOP1=(0x8A4D0,0x8A55C)
DEBUG_TOP2=(0x8A55C,0x8A750)
DEBUG_TOP1_SHA256="022822ad831619a3069865a269423fcc32eb534e327e0ff69161e66f36b80482"
DEBUG_TOP2_SHA256="c8404998421573d153e599dd0abf5d0205d8dd1177f7fabe4a790c6b13d75081"

RETAIL_FIRST_NORMAL=(0x83108,0x8314C)
DEBUG_FIRST_NORMAL=(0x8A750,0x8A7BC)
RETAIL_FIRST_NORMAL_SHA256="6a67084008b40a22cbb73da645e63a144cffbd644b17fd70dd5b4649153a728e"
DEBUG_FIRST_NORMAL_SHA256="27301ae7ac7f1335f056fb7620ef8d820ba7381182864a2aefe585bb96b03730"

DEBUG_TAIL_A=(0x8B778,0x8B7E0)
DEBUG_TAIL_B=(0x8B82C,0x8B85C)

RETAIL_LAST=(0x8411C,0x84144)
DEBUG_LAST=(0x8B804,0x8B82C)
RETAIL_LAST_SHA256="8fdec746d51f056630c7a5b4db917ca1ee1fe5e88eff23e5125b2df67201b69b"
DEBUG_LAST_SHA256="3afb605797adc47c917e49ce80b074044ba86c85c6b129033fe3bb8d4b972725"

NEXT_RETAIL=bytes.fromhex("f0 b5 11 48 04 68 a4 06 a4 0f 10 48 ff 21 01 70 0f 49")
NEXT_DEBUG=bytes.fromhex("00 b5 00 f0 09 f8 00 20 02 bc 08 47 00 b5")

def sha256(data):
    return hashlib.sha256(data).hexdigest()

def main():
    p=argparse.ArgumentParser(description="Verify German Pokemon Ruby cable_club module")
    p.add_argument("--rev0",type=Path,required=True)
    p.add_argument("--rev1",type=Path,required=True)
    p.add_argument("--debug",type=Path,required=True)
    a=p.parse_args()
    r0=a.rev0.read_bytes()
    r1=a.rev1.read_bytes()
    dbg=a.debug.read_bytes()

    x0=r0[RETAIL[0]:RETAIL[1]]
    x1=r1[RETAIL[0]:RETAIL[1]]
    xd=dbg[DEBUG[0]:DEBUG[1]]

    assert len(x0)==len(x1)==0x103C
    assert len(xd)==0x138C
    assert x0==x1
    assert sha256(x0)==RETAIL_SHA256 and sha256(x1)==RETAIL_SHA256
    assert sha256(xd)==DEBUG_SHA256
    assert DEBUG[0]-RETAIL[0]==0x73C8
    assert DEBUG[1]-RETAIL[1]==0x7718
    assert len(xd)-len(x0)==0x350

    assert x0[:len(RETAIL_ENTRY)]==RETAIL_ENTRY
    assert xd[:len(DEBUG_ENTRY)]==DEBUG_ENTRY

    assert sha256(dbg[DEBUG_TOP1[0]:DEBUG_TOP1[1]])==DEBUG_TOP1_SHA256
    assert sha256(dbg[DEBUG_TOP2[0]:DEBUG_TOP2[1]])==DEBUG_TOP2_SHA256

    assert sha256(r0[RETAIL_FIRST_NORMAL[0]:RETAIL_FIRST_NORMAL[1]])==RETAIL_FIRST_NORMAL_SHA256
    assert sha256(dbg[DEBUG_FIRST_NORMAL[0]:DEBUG_FIRST_NORMAL[1]])==DEBUG_FIRST_NORMAL_SHA256
    assert len(dbg[DEBUG_FIRST_NORMAL[0]:DEBUG_FIRST_NORMAL[1]]) - len(r0[RETAIL_FIRST_NORMAL[0]:RETAIL_FIRST_NORMAL[1]]) == 0x28

    assert len(dbg[DEBUG_TAIL_A[0]:DEBUG_TAIL_A[1]])==0x68
    assert len(dbg[DEBUG_TAIL_B[0]:DEBUG_TAIL_B[1]])==0x30

    assert sha256(r0[RETAIL_LAST[0]:RETAIL_LAST[1]])==RETAIL_LAST_SHA256
    assert sha256(dbg[DEBUG_LAST[0]:DEBUG_LAST[1]])==DEBUG_LAST_SHA256

    assert r0[RETAIL[1]:RETAIL[1]+len(NEXT_RETAIL)]==NEXT_RETAIL
    assert r1[RETAIL[1]:RETAIL[1]+len(NEXT_RETAIL)]==NEXT_RETAIL
    assert dbg[DEBUG[1]:DEBUG[1]+len(NEXT_DEBUG)]==NEXT_DEBUG

    print("German cable_club verification passed")
    print("Retail Rev0/Rev1: 0x08083108..0x08084144, 0x103C bytes")
    print("Debug:            0x0808A4D0..0x0808B85C, 0x138C bytes")
    print("Debug growth: 0x350 bytes")
    print("Accumulated Retail->Debug delta changes +0x73C8 -> +0x7718")
    print("Next Retail: mori_debug_menu / unref_sub_8083CF0")
    print("Next Debug:  tomomichi_debug_menu / InitTomomichiDebugWindow")

if __name__=="__main__":
    main()
