#!/usr/bin/env python3
import argparse, hashlib, struct
from pathlib import Path

REV0_SHA1="1c2a53332382e14dab8815e3a6dd81ad89534050"
REV1_SHA1="424740be1fc67a5ddb954794443646e6aeee2c1b"
DEBUG_SHA1="ca5e3d415c4b47353a73a616878ba833f3648b7a"
R=(0x224B0,0x2446C); D=(0x25A54,0x27A10); DELTA=0x35A4
R_SHA="fd0fbc4f5136c719654a6aa60db0c86df7d57f0ba9dac8492e0e99b5fd288b49"
D_SHA="ccbd097180e90153754f95259031b3551a4d33d0e22cdd7cca6e879342782303"
STARTS=[140464,141056,141136,141252,141656,141828,142444,144624,145144,145824,145888,145948,146008,146056,146112,146164,146636,147528,147800,147944,148328,148508]
TR=0x20770C; TD=0x2208A4

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
 assert R[1]-R[0]==D[1]-D[0]==8124
 for opcode,off in zip(range(0x4A,0x60),STARTS):
  assert (u32(r1,TR+4*opcode)&~1)==0x08000000+off
  assert (u32(d,TD+4*opcode)&~1)==0x08000000+off+DELTA
 assert (u32(r1,TR+4*0x60)&~1)==0x0802446C
 assert (u32(d,TD+4*0x60)&~1)==0x08027A10
 print("German switch/move-learning/reward core verification passed")
 print("Opcodes: 0x4A..0x5F")
 print("Stable Debug delta: +0x35A4")

if __name__=="__main__": main()
