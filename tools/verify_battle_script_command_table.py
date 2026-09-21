#!/usr/bin/env python3
import argparse
import hashlib
import struct
from pathlib import Path

REV0_SHA1="1c2a53332382e14dab8815e3a6dd81ad89534050"
REV1_SHA1="424740be1fc67a5ddb954794443646e6aeee2c1b"
DEBUG_SHA1="ca5e3d415c4b47353a73a616878ba833f3648b7a"
TR=0x20770C; TD=0x2208A4; N=248
TR_SHA="ebba8be19326d32b19c90c944ff3085dc0d8f190c100479e6290e6d7835c0d56"
TD_SHA="18d9c5501e2f2d84cf9f8c2f1274248ad2a9e264816c8fad97c817a268e37258"

def sha1(x): return hashlib.sha1(x).hexdigest()
def sha256(x): return hashlib.sha256(x).hexdigest()
def u32(x,o): return struct.unpack_from("<I",x,o)[0]

def main():
    p=argparse.ArgumentParser()
    p.add_argument("--rev0",type=Path,required=True)
    p.add_argument("--rev1",type=Path,required=True)
    p.add_argument("--debug",type=Path,required=True)
    a=p.parse_args()
    r0=a.rev0.read_bytes(); r1=a.rev1.read_bytes(); d=a.debug.read_bytes()
    assert sha1(r0)==REV0_SHA1 and sha1(r1)==REV1_SHA1 and sha1(d)==DEBUG_SHA1
    tr=r1[TR:TR+N*4]; td=d[TD:TD+N*4]
    assert r0[TR:TR+N*4]==tr
    assert sha256(tr)==TR_SHA and sha256(td)==TD_SHA
    rp=[u32(r1,TR+4*i) for i in range(N)]
    dp=[u32(d,TD+4*i) for i in range(N)]
    assert rp[0]==0x0801BE25 and dp[0]==0x0801F39D
    assert rp[-1]==0x0802C129 and dp[-1]==0x0802F78D
    delta=lambda i:(dp[i]&~1)-(rp[i]&~1)
    assert all(delta(i)==0x3578 for i in range(0x00,0x16))
    assert all(delta(i)==0x35A4 for i in range(0x16,0x40))
    assert delta(0x40)==0x3578
    assert all(delta(i)==0x35A4 for i in range(0x41,0x9F))
    assert all(delta(i)==0x3664 for i in range(0x9F,0xF8))
    assert ((dp[0x16]&~1)-(dp[0x15]&~1))-((rp[0x16]&~1)-(rp[0x15]&~1))==0x2C
    assert ((dp[0x9F]&~1)-(dp[0x9E]&~1))-((rp[0x9F]&~1)-(rp[0x9E]&~1))==0xC0
    print("German battle-script command table verification passed")
    print("248 opcodes (0x00..0xF7)")
    print("Debug deltas: +0x3578 -> +0x35A4 -> +0x3664")

if __name__=="__main__":
    main()
