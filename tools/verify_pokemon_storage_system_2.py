#!/usr/bin/env python3
import argparse
import hashlib
from pathlib import Path

RETAIL=(0x96908,0x98C90)
DEBUG=(0xA3FB4,0xA6498)
RETAIL_SHA256="eeef7c2b7e2abc0fcae65e71e5ba650b1894a6bf6043df93d5c6ae1cf557dd58"
DEBUG_SHA256="2c576e8a2aba3aa8a7b2d6972656ac485cfa2e5e730bc4036d80e555bb7a6f0b"
ENTRY=bytes.fromhex("00 b5 00 06 00 0e 04 49 08 70 04 49 48 71 04 48")
DEBUG_FUNCS=[
 (0xA4300,0xA433C,"0984327cafb08159a22d50312193b0bf4f3c346d670889585e9298c468268eb2"),
 (0xA433C,0xA435C,"b2a54853b5c67a97b7d32f80134f952bc3b7b9c8f9ad261e8c1857f022f8beb9"),
 (0xA435C,0xA43B4,"6b58e42c5765e0913697b2d9487df7d0f117bce422012527ac29f537d55a4264"),
]
NEXT=bytes.fromhex("01 48 00 78 70 47 00 00")

def sha256(data): return hashlib.sha256(data).hexdigest()

def main():
    p=argparse.ArgumentParser(description="Verify German Pokemon Ruby pokemon_storage_system_2")
    p.add_argument("--rev0",type=Path,required=True); p.add_argument("--rev1",type=Path,required=True); p.add_argument("--debug",type=Path,required=True)
    a=p.parse_args()
    r0=a.rev0.read_bytes(); r1=a.rev1.read_bytes(); d=a.debug.read_bytes()
    x0=r0[RETAIL[0]:RETAIL[1]]; x1=r1[RETAIL[0]:RETAIL[1]]; xd=d[DEBUG[0]:DEBUG[1]]
    assert len(x0)==len(x1)==0x2388 and len(xd)==0x24E4
    assert x0==x1
    assert sha256(x0)==RETAIL_SHA256 and sha256(x1)==RETAIL_SHA256 and sha256(xd)==DEBUG_SHA256
    assert DEBUG[0]-RETAIL[0]==0xD6AC and DEBUG[1]-RETAIL[1]==0xD808
    assert len(xd)-len(x0)==0x15C
    assert x0[:len(ENTRY)]==ENTRY and xd[:len(ENTRY)]==ENTRY
    total=0
    for s,e,h in DEBUG_FUNCS:
        c=d[s:e]; assert sha256(c)==h; total += len(c)
    assert total==0xB4 and 0x15C-total==0xA8
    for data,start in ((r0,RETAIL[1]),(r1,RETAIL[1]),(d,DEBUG[1])):
        assert data[start:start+8]==NEXT
    print("German pokemon_storage_system_2 verification passed")
    print("Retail Rev0/Rev1: 0x08096908..0x08098C90, 0x2388 bytes")
    print("Debug:            0x080A3FB4..0x080A6498, 0x24E4 bytes")
    print("Debug growth: 0x15C")
    print("Accumulated Retail->Debug delta changes +0xD6AC -> +0xD808")
    print("Next: pokemon_storage_system_3 / get_preferred_box")

if __name__=="__main__": main()
