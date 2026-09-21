#!/usr/bin/env python3
import argparse
import hashlib
import struct
from pathlib import Path

REV0_SHA1="1c2a53332382e14dab8815e3a6dd81ad89534050"
REV1_SHA1="424740be1fc67a5ddb954794443646e6aeee2c1b"
DEBUG_SHA1="ca5e3d415c4b47353a73a616878ba833f3648b7a"

R=(0x1F8EC,0x21164)
D=(0x22E90,0x24708)
DELTA=0x35A4
R_SHA="f5f2a488df39c10cbba61705aec1c94623d31a6a5d16b9cb65e4fc8cb8bbff73"
D_SHA="bddba2d8ebb93f3266d79c3eaeab0a4d3a75c7852e1cb46d171d52c39f48c1ad"
STARTS=[129260,129276,129408,130312,130372,130472,130592,130712,130952,131072,131320,131452,131544,134024,134512,134536,134560,134632,134664,134824,134992,135172,135308,135440,135480]

TR=0x20770C
TD=0x2208A4

def sha1(x): return hashlib.sha1(x).hexdigest()
def sha256(x): return hashlib.sha256(x).hexdigest()
def u32(x,o): return struct.unpack_from("<I",x,o)[0]

def main():
 p=argparse.ArgumentParser()
 p.add_argument("--rev0",type=Path,required=True); p.add_argument("--rev1",type=Path,required=True); p.add_argument("--debug",type=Path,required=True)
 a=p.parse_args(); r0=a.rev0.read_bytes(); r1=a.rev1.read_bytes(); d=a.debug.read_bytes()
 assert sha1(r0)==REV0_SHA1 and sha1(r1)==REV1_SHA1 and sha1(d)==DEBUG_SHA1
 assert r0[R[0]:R[1]]==r1[R[0]:R[1]]
 assert sha256(r1[R[0]:R[1]])==R_SHA and sha256(d[D[0]:D[1]])==D_SHA
 assert R[1]-R[0]==D[1]-D[0]==6264

 for opcode,off in zip(range(0x17,0x30),STARTS):
  assert (u32(r1,TR+4*opcode)&~1)==0x08000000+off
  assert (u32(d,TD+4*opcode)&~1)==0x08000000+off+DELTA

 assert 0x08020D24 + DELTA == 0x080242C8
 assert any(r1[0x20D24:0x20D70]) and any(d[0x242C8:0x24314])

 print("German faint/EXP/generic VM core verification passed")
 print("Opcodes: 0x17..0x2F")
 print("Stable Debug delta: +0x35A4")
 print("Next: 0x30 atk30_subbyte")

if __name__=="__main__": main()
