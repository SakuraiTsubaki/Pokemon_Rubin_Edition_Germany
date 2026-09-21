#!/usr/bin/env python3
import argparse
import hashlib
import struct
from pathlib import Path

REV0_SHA1="1c2a53332382e14dab8815e3a6dd81ad89534050"
REV1_SHA1="424740be1fc67a5ddb954794443646e6aeee2c1b"
DEBUG_SHA1="ca5e3d415c4b47353a73a616878ba833f3648b7a"

RETAIL=(0xD858,0xE998)
DEBUG=(0xDA74,0xEC0C)
RETAIL_SHA256="1aa5d366a78ec31d9ad1b9e2a1d8a7e5dd972abaee607edb54685eb41d5b16a3"
DEBUG_SHA256="69cffde59be984b84836ae1e6e2f898c426ec713badf4af1a73ce8d7d2163331"

RETAIL_STARTS=[0xD858,0xD898,0xD8A8,0xD920,0xD98C,0xDC8C,0xDCCC,0xDDF8,0xE004,0xE410,0xE5E8]
DEBUG_STARTS =[0xDA74,0xDAB4,0xDAC4,0xDB3C,0xDBA8,0xDEA8,0xDF40,0xE06C,0xE278,0xE684,0xE85C]

RETAIL_TABLE=0x206528
DEBUG_TABLE=0x21F27C
TABLE_SHA256="64e4c4c2d165ac4e13e77623ddca80bbaf58ec1120e24418584dbfdf56393a0f"

def sha1(x): return hashlib.sha1(x).hexdigest()
def sha256(x): return hashlib.sha256(x).hexdigest()
def u32(data,off): return struct.unpack_from("<I",data,off)[0]

def main():
    p=argparse.ArgumentParser()
    p.add_argument("--rev0",type=Path,required=True)
    p.add_argument("--rev1",type=Path,required=True)
    p.add_argument("--debug",type=Path,required=True)
    a=p.parse_args()
    r0=a.rev0.read_bytes(); r1=a.rev1.read_bytes(); d=a.debug.read_bytes()

    assert sha1(r0)==REV0_SHA1
    assert sha1(r1)==REV1_SHA1
    assert sha1(d)==DEBUG_SHA1

    rs,re=RETAIL; ds,de=DEBUG
    assert r0[rs:re] == r1[rs:re]
    assert sha256(r1[rs:re]) == RETAIL_SHA256
    assert sha256(d[ds:de]) == DEBUG_SHA256
    assert re-rs == 4416
    assert de-ds == 4504

    for i,(ro,do) in enumerate(zip(RETAIL_STARTS,DEBUG_STARTS)):
        expected=0x21C if i <= 5 else 0x274
        assert do-ro == expected,(i,hex(ro),hex(do),hex(do-ro))
        assert r1[ro:ro+2] == d[do:do+2]

    # The debug-only expansion is wholly inside LoadBattleTextboxAndBackground.
    assert (0xDF40-0xDEA8) - (0xDCCC-0xDC8C) == 0x58

    rt=r1[RETAIL_TABLE:RETAIL_TABLE+200]
    dt=d[DEBUG_TABLE:DEBUG_TABLE+200]
    assert rt == dt
    assert sha256(rt) == TABLE_SHA256
    assert u32(r1,0xDB28) == 0x08206528
    assert u32(d,0xDD44) == 0x0821F27C

    # German link-result constants occur in PrintLinkBattleWinLossTie.
    f=r1[0xDDF8:0xE004]
    for b in (bytes.fromhex("22 a0 23 0d"), bytes.fromhex("22 ac 23 05"), bytes.fromhex("23 14")):
        assert b in f

    print("German battle_bg verification passed")
    print("Retail bytes:",re-rs)
    print("Debug-only growth: 0x58")
    print("Environment entries: 10")
    print("Next module: battle_main")

if __name__=="__main__":
    main()
