#!/usr/bin/env python3
import argparse, hashlib
from pathlib import Path

REV0_SHA1="1c2a53332382e14dab8815e3a6dd81ad89534050"
REV1_SHA1="424740be1fc67a5ddb954794443646e6aeee2c1b"
DEBUG_SHA1="ca5e3d415c4b47353a73a616878ba833f3648b7a"
R=(0x361C0,0x376E0); D=(0x3A084,0x3B5B4)
R_SHA="5f902540b54982bc30c68a089895b0f92fc449c9e0b9cd2463262d98cb6f1e85"
D_SHA="eaec578391d7bbd235f7eef81816b8c6d914fb979270cbae1221acd1e460b2de"
R_STARTS=[0x361C0,0x36228,0x363BC,0x365E4,0x366E8,0x36830,0x36878,0x36AD8,0x36CE0,0x36E20,0x36EA8,0x37204,0x37260]
D_STARTS=[0x3A084,0x3A0EC,0x3A280,0x3A4A8,0x3A5AC,0x3A6F4,0x3A73C,0x3A99C,0x3ABA4,0x3ACF4,0x3AD7C,0x3B0D8,0x3B134]

def sha1(x): return hashlib.sha1(x).hexdigest()
def sha256(x): return hashlib.sha256(x).hexdigest()

def main():
 p=argparse.ArgumentParser()
 p.add_argument("--rev0",type=Path,required=True); p.add_argument("--rev1",type=Path,required=True); p.add_argument("--debug",type=Path,required=True)
 a=p.parse_args(); r0=a.rev0.read_bytes(); r1=a.rev1.read_bytes(); d=a.debug.read_bytes()
 assert sha1(r0)==REV0_SHA1 and sha1(r1)==REV1_SHA1 and sha1(d)==DEBUG_SHA1
 assert r0[R[0]:R[1]]==r1[R[0]:R[1]]
 assert sha256(r1[R[0]:R[1]])==R_SHA and sha256(d[D[0]:D[1]])==D_SHA
 assert (D[1]-D[0])-(R[1]-R[0])==0x10
 for i,(ro,do) in enumerate(zip(R_STARTS,D_STARTS)):
  expected=0x3EC4 if i<=8 else 0x3ED4
  assert do-ro==expected,(i,hex(do-ro))
  assert r1[ro:ro+2]==d[do:do+2]
 assert r1[0x376E0:0x376E4]==bytes.fromhex("70 47 00 00")
 assert d[0x3B5B4:0x3B5B8]==bytes.fromhex("70 47 00 00")
 print("German battle AI switch/item verification passed")
 print("13 functions; Debug growth 0x10")
 print("Next: battle_controller_link_opponent at +0x3ED4")

if __name__=="__main__": main()
