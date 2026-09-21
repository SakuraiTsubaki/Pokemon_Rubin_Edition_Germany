#!/usr/bin/env python3
import argparse
import hashlib
import struct
from pathlib import Path

REV0_SHA1="1c2a53332382e14dab8815e3a6dd81ad89534050"
REV1_SHA1="424740be1fc67a5ddb954794443646e6aeee2c1b"
DEBUG_SHA1="ca5e3d415c4b47353a73a616878ba833f3648b7a"

RETAIL=(0x141BC,0x15324)
DEBUG=(0x17244,0x183AC)
DELTA=0x3088

RETAIL_SHA="20e994944adc5b1f3405a34ac8d07ae2ee405f492b5071c19dd328f77ce4a1d9"
DEBUG_SHA="e204ce288cf66d02e6ffee4d63b51bb5cf81c82c79b88d44bac49ed7cb93af6"

MODULE_RETAIL=(0xE998,0x15324)
MODULE_DEBUG=(0xEC0C,0x183AC)
MODULE_RETAIL_SHA="8e23208aa7693b31725b31dffa051c7808b82351ab40c591be8c41c746fd387b"
MODULE_DEBUG_SHA="db5388b194b192cfe68ef6ddf3b01638c19a938ed1b687acdbf707400532ebf5"

STARTS=[82364,84168,84340,85132,85448,85796,85868,85964,86160,86356,86416,86536,86580,86632]

RETAIL_ACTION_TABLE=0x207610
DEBUG_ACTION_TABLE=0x2207A8
RETAIL_ACTION_TABLE_SHA="325dc01ec5a02fb745118e57fa04eec5b43626f086af1db21eee8944c29e700c"
DEBUG_ACTION_TABLE_SHA="9f3eeb6e3a1f504da2c87f8c39c617441f6bfd011c8c7fbc26f13a6fa349de98"

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
    assert sha256(r1[rs:re]) == RETAIL_SHA
    assert sha256(d[ds:de]) == DEBUG_SHA
    assert re-rs == de-ds == 4456

    for off in STARTS:
        doff=off+DELTA
        assert r1[off:off+2] == d[doff:doff+2], (hex(off),hex(doff))

    mrt,mre=MODULE_RETAIL; mdt,mde=MODULE_DEBUG
    assert r0[mrt:mre] == r1[mrt:mre]
    assert sha256(r1[mrt:mre]) == MODULE_RETAIL_SHA
    assert sha256(d[mdt:mde]) == MODULE_DEBUG_SHA
    assert (mde-mdt)-(mre-mrt) == 11796

    rt=r1[RETAIL_ACTION_TABLE:RETAIL_ACTION_TABLE+56]
    dt=d[DEBUG_ACTION_TABLE:DEBUG_ACTION_TABLE+56]
    assert sha256(rt) == RETAIL_ACTION_TABLE_SHA
    assert sha256(dt) == DEBUG_ACTION_TABLE_SHA

    expected=[
        0x080141BD,0x08014975,0x080148C9,0x08014DC9,
        0x08014F25,0x08014F6D,0x08014FCD,0x08015091,
        0x08015155,0x08015191,0x0801B769,0x08015209,
        0x08015269,0x08015235
    ]
    assert [u32(r1,RETAIL_ACTION_TABLE+4*i) for i in range(14)] == expected

    assert any(r1[0x15324:0x1532C])
    assert any(d[0x183AC:0x183B4])

    print("German battle_main action/module verification passed")
    print("Action IDs: 0..13")
    print("battle_main retail bytes:",mre-mrt)
    print("battle_main debug extra bytes:",(mde-mdt)-(mre-mrt))
    print("Next module: battle_util")

if __name__=="__main__":
    main()
