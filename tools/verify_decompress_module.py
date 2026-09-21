#!/usr/bin/env python3
import argparse
import hashlib
from pathlib import Path

REV0_SHA1="1c2a53332382e14dab8815e3a6dd81ad89534050"
REV1_SHA1="424740be1fc67a5ddb954794443646e6aeee2c1b"
DEBUG_SHA1="ca5e3d415c4b47353a73a616878ba833f3648b7a"

RETAIL_START=0xD40C
RETAIL_END=0xD858
DEBUG_START=0xD628
DEBUG_END=0xDA74
DELTA=0x21C

RETAIL_SHA256="8214643be8cafdff49ca26dfa48cdbce01e99cedf26e6143d5e5754625190feb"
DEBUG_SHA256="b49b41f45d0812ec8342a6a77345cc789f9e0ed6ce76dbadd3855ecd1248a8fd"

STARTS=[0xD40C,0xD418,0xD424,0xD450,0xD478,0xD4AC,0xD4DC,0xD508,0xD54C,0xD5F4,0xD600]

def sha1(x):
    return hashlib.sha1(x).hexdigest()

def sha256(x):
    return hashlib.sha256(x).hexdigest()

def main():
    p=argparse.ArgumentParser()
    p.add_argument("--rev0",type=Path,required=True)
    p.add_argument("--rev1",type=Path,required=True)
    p.add_argument("--debug",type=Path,required=True)
    a=p.parse_args()

    r0=a.rev0.read_bytes()
    r1=a.rev1.read_bytes()
    d=a.debug.read_bytes()

    assert sha1(r0)==REV0_SHA1
    assert sha1(r1)==REV1_SHA1
    assert sha1(d)==DEBUG_SHA1

    assert r0[RETAIL_START:RETAIL_END] == r1[RETAIL_START:RETAIL_END]
    assert sha256(r1[RETAIL_START:RETAIL_END]) == RETAIL_SHA256
    assert sha256(d[DEBUG_START:DEBUG_END]) == DEBUG_SHA256

    for off in STARTS:
        doff=off+DELTA
        assert r1[off:off+2] == d[doff:doff+2], (hex(off),hex(doff))

    assert RETAIL_END-RETAIL_START == 1100
    assert DEBUG_END-DEBUG_START == 1100

    print("German decompress module verification passed")
    print("Functions:",len(STARTS))
    print("Debug address delta: +0x21C")
    print("Next module: battle_bg")

if __name__=="__main__":
    main()
