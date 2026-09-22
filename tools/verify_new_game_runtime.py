#!/usr/bin/env python3
import argparse, hashlib
from pathlib import Path

R=(0x53040,0x5329C)
D=(0x57230,0x575AC)
R_SHA="ff8616201d0b9a71942cf375db42b9db673a2678deb42dcb3022ecdcfe76ec4c"
D_SHA="7055ef8767b612ce44f42a93fb0a12d04e051f53dc23774664777cdb43b99b66"

def h(x): return hashlib.sha256(x).hexdigest()

def main():
 p=argparse.ArgumentParser()
 p.add_argument("--rev0",type=Path,required=True)
 p.add_argument("--rev1",type=Path,required=True)
 p.add_argument("--debug",type=Path,required=True)
 a=p.parse_args()
 r0=a.rev0.read_bytes(); r1=a.rev1.read_bytes(); d=a.debug.read_bytes()

 assert r0[R[0]:R[1]] == r1[R[0]:R[1]]
 assert h(r1[R[0]:R[1]]) == R_SHA
 assert h(d[D[0]:D[1]]) == D_SHA
 assert R[1]-R[0] == 0x25C
 assert D[1]-D[0] == 0x37C
 assert (D[1]-D[0])-(R[1]-R[0]) == 0x120
 assert D[0]-R[0] == 0x41F0
 assert D[1]-R[1] == 0x4310

 # Common little-endian word writer is byte-identical.
 assert r1[0x53040:0x53050] == d[0x57230:0x57240]

 # Debug bootstrap and next module.
 assert d[0x57508:0x5750A] == bytes.fromhex("10 b5")
 assert r1[0x5329C:0x5329E] == bytes.fromhex("00 b5")
 assert d[0x575AC:0x575AE] == bytes.fromhex("00 b5")

 print("German new_game runtime verification passed")
 print("Retail 0x25C; Debug 0x37C; growth 0x120")
 print("Next: overworld at accumulated delta +0x4310")

if __name__=="__main__": main()
