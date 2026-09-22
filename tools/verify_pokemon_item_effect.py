#!/usr/bin/env python3
import argparse, hashlib
from pathlib import Path

REV0_SHA1="1c2a53332382e14dab8815e3a6dd81ad89534050"
REV1_SHA1="424740be1fc67a5ddb954794443646e6aeee2c1b"
DEBUG_SHA1="ca5e3d415c4b47353a73a616878ba833f3648b7a"

R=(0x3E360,0x3F340)
D=(0x424DC,0x434BC)
DELTA=0x417C
R_SHA="7ef952661f4ac95889a0eb8556f80aa32ddbad0289150c594dda1176122c6f05"
D_SHA="2e716b737731d48369942d58094840b418a1bee6c78e13954e371622556eb009"

def sha1(x): return hashlib.sha1(x).hexdigest()
def sha256(x): return hashlib.sha256(x).hexdigest()

def main():
 p=argparse.ArgumentParser()
 p.add_argument("--rev0",type=Path,required=True)
 p.add_argument("--rev1",type=Path,required=True)
 p.add_argument("--debug",type=Path,required=True)
 a=p.parse_args()
 r0=a.rev0.read_bytes(); r1=a.rev1.read_bytes(); d=a.debug.read_bytes()
 assert sha1(r0)==REV0_SHA1 and sha1(r1)==REV1_SHA1 and sha1(d)==DEBUG_SHA1
 assert r0[R[0]:R[1]]==r1[R[0]:R[1]]
 assert sha256(r1[R[0]:R[1]])==R_SHA
 assert sha256(d[D[0]:D[1]])==D_SHA
 assert R[1]-R[0]==D[1]-D[0]==0xFE0
 assert D[0]-R[0]==DELTA and D[1]-R[1]==DELTA
 assert r1[0x3E384:0x3E386]==bytes.fromhex("f0 b5")
 assert d[0x42500:0x42502]==bytes.fromhex("f0 b5")
 assert r1[0x3F340:0x3F342]==bytes.fromhex("70 b5")
 assert d[0x434BC:0x434BE]==bytes.fromhex("70 b5")
 print("German pokemon_item_effect verification passed")
 print("Module size: 0xFE0; stable Debug delta +0x417C")
 print("Next: pokemon_3 / HealStatusConditions")

if __name__=="__main__": main()
