#!/usr/bin/env python3
import argparse
import hashlib
from pathlib import Path

REV0_SHA1="1c2a53332382e14dab8815e3a6dd81ad89534050"
REV1_SHA1="424740be1fc67a5ddb954794443646e6aeee2c1b"
DEBUG_SHA1="ca5e3d415c4b47353a73a616878ba833f3648b7a"

HELPER_R=(0x1041C,0x109F8)
HELPER_D=(0x132F0,0x138CC)
TOOLS_A=(0x10800,0x132F0)
TOOLS_B=(0x138CC,0x139E4)
CORE_R=(0x109F8,0x13AC4)
CORE_D=(0x139E4,0x16B4C)

HELPER_R_SHA="b159eaa8d62c47cfcbef24546a7b75595dbc7996ca7aff14d64a3a3693b6749f"
HELPER_D_SHA="6ad77a398be92d0eae95f4cebde9069cc52d66af998b417cf8657e0f6c00aa55"
TOOLS_A_SHA="c82b583df905cded349e3d5edc41f899d64175f2c848ae76cc7086d05dcb87f2"
TOOLS_B_SHA="d2d1d17bf6cc53d9dac48843ba154fef9033a8182598500188bfa1601962ca76"
CORE_R_SHA="f201eba9a43a5e002c5d166521c0dd6261d82fe9066ba1115f450cac9ef0f81c"
CORE_D_SHA="9d59402f778877241049f44590a8dc7606a24c968b59e0857804e6472094cf07"

HELPER_STARTS=[66588,66636,66688,66780,66784,66804,66904,67176,67316,67344,67400,67444,67456,67504,67516,67520,67560,67816,67972,68048,68052]
CORE_R_STARTS=[68088,68168,68956,69916,70804,70920,71000,71636,72052,72108,72148,72200,72344,72484,72516,72584,72764,72916,73628,73824,74236,74796,75000,78224,78276,79260,79920,80208,80288]
CORE_D_STARTS=[80356,80568,81380,82340,83228,83344,83424,84060,84476,84532,84572,84624,84768,84908,84940,85008,85188,85340,86052,86248,86660,87220,87424,90648,90700,91684,92344,92632,92712]

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

    assert r0[HELPER_R[0]:HELPER_R[1]] == r1[HELPER_R[0]:HELPER_R[1]]
    assert sha256(r1[HELPER_R[0]:HELPER_R[1]]) == HELPER_R_SHA
    assert sha256(d[HELPER_D[0]:HELPER_D[1]]) == HELPER_D_SHA
    assert sha256(d[TOOLS_A[0]:TOOLS_A[1]]) == TOOLS_A_SHA
    assert sha256(d[TOOLS_B[0]:TOOLS_B[1]]) == TOOLS_B_SHA

    for ro in HELPER_STARTS:
        do=ro+0x2ED4
        assert r1[ro:ro+2] == d[do:do+2], (hex(ro),hex(do))

    # BattleMainCB1 pointers embedded in CB2_HandleStartBattle.
    assert int.from_bytes(r1[0xF1F0:0xF1F4],"little") == 0x080109F9
    assert int.from_bytes(d[0xF4B0:0xF4B4],"little") == 0x080139E5

    assert r0[CORE_R[0]:CORE_R[1]] == r1[CORE_R[0]:CORE_R[1]]
    assert sha256(r1[CORE_R[0]:CORE_R[1]]) == CORE_R_SHA
    assert sha256(d[CORE_D[0]:CORE_D[1]]) == CORE_D_SHA

    for ro,do in zip(CORE_R_STARTS,CORE_D_STARTS):
        assert r1[ro:ro+2] == d[do:do+2], (hex(ro),hex(do))

    # Debug growth is isolated to the first two core functions.
    assert (0x13AB8-0x139E4) - (0x10A48-0x109F8) == 0x84
    assert (0x13DE4-0x13AB8) - (0x10D5C-0x10A48) == 0x18
    assert 0x16B4C-0x13AC4 == 0x3088

    print("German battle core correction/turn-order verification passed")
    print("BattleMainCB1 retail: 0x080109F8")
    print("BattleMainCB1 debug : 0x080139E4")
    print("Stable post-init Debug delta: +0x3088")

if __name__=="__main__":
    main()
