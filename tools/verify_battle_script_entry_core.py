#!/usr/bin/env python3
import argparse, hashlib
from pathlib import Path

REV0_SHA1="1c2a53332382e14dab8815e3a6dd81ad89534050"
REV1_SHA1="424740be1fc67a5ddb954794443646e6aeee2c1b"
DEBUG_SHA1="ca5e3d415c4b47353a73a616878ba833f3648b7a"
R=(0x1BE24,0x1C490); D=(0x1F39C,0x1FA08)
R_SHA="61c5916134fd94dd5c986bc366b380b3c41096fbf46ced2ce0344d7f65a5d7a0"
D_SHA="c141d790f54249b05d20c5b9bff60160616edf76c9e4285c08aaaaf1db69051e"
STARTS=[0x1BE24,0x1C1DC,0x1C26C,0x1C2DC,0x1C348,0x1C490]

def sha1(x): return hashlib.sha1(x).hexdigest()
def sha256(x): return hashlib.sha256(x).hexdigest()

def main():
 p=argparse.ArgumentParser()
 p.add_argument("--rev0",type=Path,required=True); p.add_argument("--rev1",type=Path,required=True); p.add_argument("--debug",type=Path,required=True)
 a=p.parse_args(); r0=a.rev0.read_bytes(); r1=a.rev1.read_bytes(); d=a.debug.read_bytes()
 assert sha1(r0)==REV0_SHA1 and sha1(r1)==REV1_SHA1 and sha1(d)==DEBUG_SHA1
 assert r0[R[0]:R[1]]==r1[R[0]:R[1]]
 assert sha256(r1[R[0]:R[1]])==R_SHA and sha256(d[D[0]:D[1]])==D_SHA
 for ro in STARTS:
  do=ro+0x3578
  assert r1[ro:ro+2]==d[do:do+2], (hex(ro),hex(do))
 print("German battle script entry core verification passed")
 print("atk00 + helpers mapped; initial Debug delta +0x3578")

if __name__=="__main__": main()
