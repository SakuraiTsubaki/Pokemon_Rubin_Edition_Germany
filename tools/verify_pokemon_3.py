#!/usr/bin/env python3
import argparse, hashlib
from pathlib import Path

REV0_SHA1="1c2a53332382e14dab8815e3a6dd81ad89534050"
REV1_SHA1="424740be1fc67a5ddb954794443646e6aeee2c1b"
DEBUG_SHA1="ca5e3d415c4b47353a73a616878ba833f3648b7a"

R=(0x3F340,0x40FE0)
D=(0x434BC,0x4515C)
DELTA=0x417C
R_SHA="41fa92dc097da2054ed5a8131e5a2694298634c2f82d6654b4b6b067b264dd48"
D_SHA="308529d87cffab0792d3e5db98c6eb6c39a82734829c34038f7182607fd6e18f"

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
 assert sha256(r1[R[0]:R[1]])==R_SHA
 assert sha256(d[D[0]:D[1]])==D_SHA
 assert R[1]-R[0]==D[1]-D[0]==0x1CA0
 assert D[0]-R[0]==DELTA and D[1]-R[1]==DELTA
 assert r1[0x40FE0:0x40FE2]==bytes.fromhex("00 b5")
 assert d[0x4515C:0x4515E]==bytes.fromhex("00 b5")
 print("German pokemon_3 verification passed")
 print("Module size: 0x1CA0; stable Debug delta +0x417C")
 print("Next: de_rom_8040FE0")

if __name__=="__main__": main()
