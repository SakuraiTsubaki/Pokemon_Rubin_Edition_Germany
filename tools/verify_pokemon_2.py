#!/usr/bin/env python3
import argparse, hashlib
from pathlib import Path

REV0_SHA1="1c2a53332382e14dab8815e3a6dd81ad89534050"
REV1_SHA1="424740be1fc67a5ddb954794443646e6aeee2c1b"
DEBUG_SHA1="ca5e3d415c4b47353a73a616878ba833f3648b7a"

R=(0x3C51C,0x3E360)
D=(0x40698,0x424DC)
DELTA=0x417C
R_SHA="e7169aa097ab66e4027ca0ce3dc479548bcb4368acabb18ef6cad6453da636b8"
D_SHA="b9d4617ba309a7f5fc712553dea16be17def6632998b8bdf3d7e3e00c6a35879"
STARTS=[247068,247304,247436,247452,247544,247616,247668,247748,247784,247820,249140,249296,250832,251072,252644,252656,252780,252908,252976,253044,253160,253228,253280,253564,253624,253684,253736,253812,253888,253960,254020,254044]

def sha1(x): return hashlib.sha1(x).hexdigest()
def sha256(x): return hashlib.sha256(x).hexdigest()

def main():
 p=argparse.ArgumentParser()
 p.add_argument("--rev0",type=Path,required=True)
 p.add_argument("--rev1",type=Path,required=True)
 p.add_argument("--debug",type=Path,required=True)
 a=p.parse_args(); r0=a.rev0.read_bytes(); r1=a.rev1.read_bytes(); d=a.debug.read_bytes()
 assert sha1(r0)==REV0_SHA1 and sha1(r1)==REV1_SHA1 and sha1(d)==DEBUG_SHA1
 assert r0[R[0]:R[1]]==r1[R[0]:R[1]]
 assert sha256(r1[R[0]:R[1]])==R_SHA and sha256(d[D[0]:D[1]])==D_SHA
 assert R[1]-R[0]==D[1]-D[0]==7748
 for ro in STARTS:
  do=ro+DELTA
  assert r1[ro:ro+2]==d[do:do+2],(hex(ro),hex(do))
 assert r1[0x3E360:0x3E362]==bytes.fromhex("10 b5")
 assert d[0x424DC:0x424DE]==bytes.fromhex("10 b5")
 print("German pokemon_2 verification passed")
 print("32 functions; stable Debug delta +0x417C")
 print("Next: pokemon_item_effect")

if __name__=="__main__": main()
