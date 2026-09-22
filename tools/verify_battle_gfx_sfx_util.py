#!/usr/bin/env python3
import argparse, hashlib
from pathlib import Path

REV0_SHA1="1c2a53332382e14dab8815e3a6dd81ad89534050"
REV1_SHA1="424740be1fc67a5ddb954794443646e6aeee2c1b"
DEBUG_SHA1="ca5e3d415c4b47353a73a616878ba833f3648b7a"
R=(0x314C4,0x32CB0); D=(0x3527C,0x36A68)
R_SHA="232a9dc36ee0e1f7879e1f12c3d57c526001a486532b3f505b57fa0f5c3f5676"
D_SHA="b2f91dfeb5ce20260b34fb83911b76a16e92385034e7ec18446c88086b0d4e74"
PAIRS=[(0x314C4,0x3527C),(0x31538,0x352F0),(0x31574,0x3532C),(0x315A4,0x3535C)]

def sha1(x): return hashlib.sha1(x).hexdigest()
def sha256(x): return hashlib.sha256(x).hexdigest()

def main():
 p=argparse.ArgumentParser()
 p.add_argument("--rev0",type=Path,required=True); p.add_argument("--rev1",type=Path,required=True); p.add_argument("--debug",type=Path,required=True)
 a=p.parse_args(); r0=a.rev0.read_bytes(); r1=a.rev1.read_bytes(); d=a.debug.read_bytes()
 assert sha1(r0)==REV0_SHA1 and sha1(r1)==REV1_SHA1 and sha1(d)==DEBUG_SHA1
 assert r0[R[0]:R[1]]==r1[R[0]:R[1]]
 assert sha256(r1[R[0]:R[1]])==R_SHA and sha256(d[D[0]:D[1]])==D_SHA
 assert R[1]-R[0]==D[1]-D[0]==6124
 for ro,do in PAIRS:
  assert do-ro==0x3DB8
  assert r1[ro:ro+2]==d[do:do+2]
 assert r1[0x32CB0:0x32CB4]==bytes.fromhex("70 47 00 00")
 assert d[0x36A68:0x36A6C]==bytes.fromhex("70 47 00 00")
 print("German battle_gfx_sfx_util verification passed")
 print("Module size: 0x17EC; no Debug growth")
 print("Next: battle_controller_opponent at +0x3DB8")

if __name__=="__main__": main()
