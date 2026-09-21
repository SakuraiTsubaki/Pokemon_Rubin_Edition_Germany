#!/usr/bin/env python3
import argparse
import hashlib
from pathlib import Path

REV0_SHA1="1c2a53332382e14dab8815e3a6dd81ad89534050"
REV1_SHA1="424740be1fc67a5ddb954794443646e6aeee2c1b"
DEBUG_SHA1="ca5e3d415c4b47353a73a616878ba833f3648b7a"

RETAIL=(0xF200,0x1041C)
DEBUG_COMMON=(0xF4C0,0x10800)
DEBUG_TOOLS=(0x10800,0x139E4)

RETAIL_SHA256="6c564beca2daeb1b71704d16c159a71520419be68c11695e6b08de8320b785d7"
DEBUG_COMMON_SHA256="5f60c59e24fd5de5f02b3e431b6f47be3b114693de098cfca3072f8f38f3c44e"
DEBUG_TOOLS_SHA256="d5fdce32b2fc20101163c1b9c30f47c7aae94fafc126096e996eaf0f96dd14df"

COMMON=[
    (0xF200,0xF4C0,216,216),
    (0xF2D8,0xF598,404,452),
    (0xF46C,0xF75C,1392,1436),
    (0xF9DC,0xFCF8,48,248),
    (0xFA0C,0xFDF0,16,16),
    (0xFA1C,0xFE00,160,160),
    (0xFABC,0xFEA0,1004,1004),
    (0xFEA8,0x1028C,40,40),
    (0xFED0,0x102B4,176,176),
    (0xFF80,0x10364,4,4),
    (0xFF84,0x10368,112,112),
    (0xFFF4,0x103D8,32,32),
    (0x10014,0x103F8,468,468),
    (0x101E8,0x105CC,420,420),
    (0x1038C,0x10770,28,28),
    (0x103A8,0x1078C,116,116),
]

DEBUG_ANCHORS=[
    0x10800,
    0x10818,
    0x108B8,
    0x10A7C,
    0x10AAC,
    0x10B80,
    0x10CAC,
    0x11498,
    0x1174C,
    0x11D40,
    0x11E5C,
    0x11E74,
    0x11EA0,
    0x12294,
    0x123D8,
    0x12540,
    0x125A0,
    0x125E4,
    0x12628,
    0x12658,
    0x12688,
    0x12878,
    0x12D10,
    0x13294,
    0x132C8,
    0x138CC,
]

def sha1(x): return hashlib.sha1(x).hexdigest()
def sha256(x): return hashlib.sha256(x).hexdigest()

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

    rs,re=RETAIL
    ds,de=DEBUG_COMMON
    ts,te=DEBUG_TOOLS
    assert r0[rs:re] == r1[rs:re]
    assert sha256(r1[rs:re]) == RETAIL_SHA256
    assert sha256(d[ds:de]) == DEBUG_COMMON_SHA256
    assert sha256(d[ts:te]) == DEBUG_TOOLS_SHA256

    for ro,do,rsz,dsz in COMMON:
        assert any(r1[ro:ro+4])
        assert any(d[do:do+4])
        assert rsz > 0 and dsz > 0

    assert COMMON[1][3]-COMMON[1][2] == 48
    assert COMMON[2][3]-COMMON[2][2] == 44
    assert COMMON[3][3]-COMMON[3][2] == 200

    assert te-ts == 0x31E4
    for off in DEBUG_ANCHORS:
        assert any(d[off:off+8]), hex(off)

    # BattleMainCB1 rejoin points.
    assert r1[0x1041C:0x1041E] == bytes.fromhex("00 b5")
    assert d[0x139E4:0x139E6] == bytes.fromhex("30 b5")
    assert 0x139E4-0x1041C == 0x35C8

    print("German battle_main link/multi and Debug-tool verification passed")
    print("Common retail bytes:",re-rs)
    print("Debug-only tool bytes:",te-ts)
    print("BattleMainCB1 rejoin delta: +0x35C8")

if __name__=="__main__":
    main()
