#!/usr/bin/env python3
import argparse, hashlib, struct
from pathlib import Path
REV0_SHA1="1c2a53332382e14dab8815e3a6dd81ad89534050"
REV1_SHA1="424740be1fc67a5ddb954794443646e6aeee2c1b"
DEBUG_SHA1="ca5e3d415c4b47353a73a616878ba833f3648b7a"
MR=(0x376E0,0x3A894); MD=(0x3B5B4,0x3E768); TR=0x208018; TD=0x2211B0; N=57
MR_SHA="be0ae41d9a3ac32369d15f31fc5c4f72491b238c6b48bdca06e8dd117d73357d"
MD_SHA="7b481172fd4c9d3ae43e56c0151c323a02fa9dc70244d103e8b49d6f1d5bc09b"
TR_SHA="ab46af9102042f243e39cda3b3586461130ce252ddcb16fc1ef80c65ee85d959"
TD_SHA="e86c03defee73f1b93445225d3f8071ae611ffdf52a61f922267afcef2b9b6d3"
def sha1(x): return hashlib.sha1(x).hexdigest()
def sha256(x): return hashlib.sha256(x).hexdigest()
def u32(x,o): return struct.unpack_from("<I",x,o)[0]
def main():
 p=argparse.ArgumentParser(); p.add_argument("--rev0",type=Path,required=True); p.add_argument("--rev1",type=Path,required=True); p.add_argument("--debug",type=Path,required=True)
 a=p.parse_args(); r0=a.rev0.read_bytes(); r1=a.rev1.read_bytes(); d=a.debug.read_bytes()
 assert sha1(r0)==REV0_SHA1 and sha1(r1)==REV1_SHA1 and sha1(d)==DEBUG_SHA1
 assert r0[MR[0]:MR[1]]==r1[MR[0]:MR[1]]
 assert sha256(r1[MR[0]:MR[1]])==MR_SHA and sha256(d[MD[0]:MD[1]])==MD_SHA
 assert MR[1]-MR[0]==MD[1]-MD[0]==12724
 tr=r1[TR:TR+N*4]; td=d[TD:TD+N*4]
 assert r0[TR:TR+N*4]==tr and sha256(tr)==TR_SHA and sha256(td)==TD_SHA
 for i in range(N):
  assert (u32(d,TD+4*i)&~1)-(u32(r1,TR+4*i)&~1)==0x3ED4
 assert r1[0x3A890:0x3A894]==bytes.fromhex("70 47 00 00")
 assert d[0x3E764:0x3E768]==bytes.fromhex("70 47 00 00")
 print("German link-opponent controller verification passed")
 print("57 commands; no Debug growth; next pokemon_1 at +0x3ED4")
if __name__=="__main__": main()
