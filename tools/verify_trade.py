#!/usr/bin/env python3
import argparse, hashlib
from pathlib import Path

R=(0x47FFC,0x4E5FC)
D=(0x4C1C8,0x527C8)
R_SHA="dcfc40527a81508441e9e0c457be2ae8554345218ca21f0b79f81423f555586c"
D_SHA="557436d7f90a9543e7ce0e1fdd05fae54f83ecbe2538d28258d4bc31fd10bef1"

def h(x): return hashlib.sha256(x).hexdigest()

def main():
 p=argparse.ArgumentParser()
 p.add_argument("--rev0",type=Path,required=True)
 p.add_argument("--rev1",type=Path,required=True)
 p.add_argument("--debug",type=Path,required=True)
 a=p.parse_args()
 r0=a.rev0.read_bytes(); r1=a.rev1.read_bytes(); d=a.debug.read_bytes()

 assert r0[R[0]:R[1]]==r1[R[0]:R[1]]
 assert h(r1[R[0]:R[1]])==R_SHA
 assert h(d[D[0]:D[1]])==D_SHA
 assert R[1]-R[0]==D[1]-D[0]==0x6600
 assert D[0]-R[0]==D[1]-R[1]==0x41CC

 # First trade wrapper and first Berry Blender function are Thumb functions.
 assert r1[R[0]:R[0]+2]==bytes.fromhex("00 b5")
 assert d[D[0]:D[0]+2]==bytes.fromhex("00 b5")
 assert r1[R[1]:R[1]+2]==bytes.fromhex("00 b5")
 assert d[D[1]:D[1]+2]==bytes.fromhex("00 b5")

 # Blender_ControlHitPitch contains the literal field offset behavior directly
 # after its entry; both builds should match for the first 16 bytes.
 assert r1[R[1]:R[1]+16]==d[D[1]:D[1]+16]

 print("German trade verification passed")
 print("Module size: 0x6600; stable Debug delta +0x41CC")
 print("Next: berry_blender / Blender_ControlHitPitch")

if __name__=="__main__": main()
