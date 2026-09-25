#!/usr/bin/env python3
import argparse
import hashlib
from pathlib import Path

RETAIL=(0x95C2C,0x96908)
DEBUG=(0xA317C,0xA3FB4)
RETAIL_SHA256="703092c567fa1305a37a5c6ce99e3ac33bae5b5483d203ca4a12125b12b467b0"
DEBUG_SHA256="a14deaad84ad49a35a00d9e4126449a23beecf7a3e09355011b1d7a0d6749cd1"
ENTRY=bytes.fromhex("70 b5 00 06 00 0e 00 24 00 25 81 00 09 18 08 01 40 1a 46 01 a0 00 00 19 00 01 0a 49 40 18 30 18")
DBG=(0xA3904,0xA3A60)
DBG_SHA256="3c407fdd1d3a8c068ca9d137cad80e40e6b833d46af3619e5f0df22c075b7eaa"
TAIL_R=(0x968D4,0x96908)
TAIL_D=(0xA3F80,0xA3FB4)
TAIL_SHA256="b736e4badd6f3bba4692a553241b2a130b73787c94d3cdd026658cce58aedf24"
NEXT=bytes.fromhex("00 b5 00 06 00 0e 04 49 08 70 04 49 48 71 04 48")

def sha256(data): return hashlib.sha256(data).hexdigest()

def main():
    p=argparse.ArgumentParser(description="Verify German Pokemon Ruby pokemon_storage_system module")
    p.add_argument("--rev0",type=Path,required=True)
    p.add_argument("--rev1",type=Path,required=True)
    p.add_argument("--debug",type=Path,required=True)
    a=p.parse_args()
    r0=a.rev0.read_bytes(); r1=a.rev1.read_bytes(); d=a.debug.read_bytes()
    x0=r0[RETAIL[0]:RETAIL[1]]; x1=r1[RETAIL[0]:RETAIL[1]]; xd=d[DEBUG[0]:DEBUG[1]]
    assert len(x0)==len(x1)==0xCDC
    assert len(xd)==0xE38
    assert x0==x1
    assert sha256(x0)==RETAIL_SHA256 and sha256(x1)==RETAIL_SHA256
    assert sha256(xd)==DEBUG_SHA256
    assert DEBUG[0]-RETAIL[0]==0xD550
    assert DEBUG[1]-RETAIL[1]==0xD6AC
    assert len(xd)-len(x0)==0x15C
    assert x0[:len(ENTRY)]==ENTRY and xd[:len(ENTRY)]==ENTRY
    assert len(d[DBG[0]:DBG[1]])==0x15C
    assert sha256(d[DBG[0]:DBG[1]])==DBG_SHA256
    tr=r0[TAIL_R[0]:TAIL_R[1]]
    td=d[TAIL_D[0]:TAIL_D[1]]
    assert tr==td and sha256(tr)==TAIL_SHA256
    assert r0[RETAIL[1]:RETAIL[1]+len(NEXT)]==NEXT
    assert r1[RETAIL[1]:RETAIL[1]+len(NEXT)]==NEXT
    assert d[DEBUG[1]:DEBUG[1]+len(NEXT)]==NEXT
    print("German pokemon_storage_system verification passed")
    print("Retail Rev0/Rev1: 0x08095C2C..0x08096908, 0xCDC bytes")
    print("Debug:            0x080A317C..0x080A3FB4, 0xE38 bytes")
    print("Debug growth: 0x15C in debug_sub_80A3904")
    print("Accumulated Retail->Debug delta changes +0xD550 -> +0xD6AC")
    print("Next: pokemon_storage_system_2 / task_intro_29")

if __name__=="__main__":
    main()
