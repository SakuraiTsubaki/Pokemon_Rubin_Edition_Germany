#!/usr/bin/env python3
import argparse
import hashlib
from pathlib import Path

REV0_SHA1="1c2a53332382e14dab8815e3a6dd81ad89534050"
REV1_SHA1="424740be1fc67a5ddb954794443646e6aeee2c1b"
DEBUG_SHA1="ca5e3d415c4b47353a73a616878ba833f3648b7a"

R=(0x1DAC0,0x1F8EC)
D=(0x21038,0x22E90)
R_SHA="c9edbc870e2acc0fb4c6301449f7693bc9058bcfd031262b061b944d8c320219"
D_SHA="d8e52c1c94d505e86f098244b379902377f947162e8406df6da98b3b5a714654"
R_STARTS=[0x1DAC0,0x1DC34,0x1DC54,0x1DD20,0x1E11C,0x1E170,0x1E240,0x1E3F0,0x1E430,0x1E474,0x1E4D0,0x1E524,0x1E588,0x1E5C0,0x1F7E8,0x1F8DC,0x1F8EC]

def sha1(x): return hashlib.sha1(x).hexdigest()
def sha256(x): return hashlib.sha256(x).hexdigest()

def main():
 p=argparse.ArgumentParser()
 p.add_argument("--rev0",type=Path,required=True); p.add_argument("--rev1",type=Path,required=True); p.add_argument("--debug",type=Path,required=True)
 a=p.parse_args(); r0=a.rev0.read_bytes(); r1=a.rev1.read_bytes(); d=a.debug.read_bytes()
 assert sha1(r0)==REV0_SHA1 and sha1(r1)==REV1_SHA1 and sha1(d)==DEBUG_SHA1
 assert r0[R[0]:R[1]]==r1[R[0]:R[1]]
 assert sha256(r1[R[0]:R[1]])==R_SHA and sha256(d[D[0]:D[1]])==D_SHA

 # Everything through SetMoveEffect and atk15 entry starts at +0x3578.
 for ro in R_STARTS[:15]:
  do=ro+0x3578
  assert r1[ro:ro+2]==d[do:do+2], (hex(ro),hex(do))

 # atk15 adds 0x2C, so atk16/atk17 use +0x35A4.
 assert 0x22D60-0x1F7E8==0x3578
 assert (0x22E80-0x22D60)-(0x1F8DC-0x1F7E8)==0x2C
 assert 0x22E80-0x1F8DC==0x35A4
 assert 0x22E90-0x1F8EC==0x35A4

 print("German animation/HP/move-effect core verification passed")
 print("SetMoveEffect retail/debug size: 4648")
 print("atk15 Debug growth: 0x2C")
 print("Next delta: +0x35A4")

if __name__=="__main__": main()
