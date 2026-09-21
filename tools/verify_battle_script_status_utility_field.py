#!/usr/bin/env python3
import argparse, hashlib, struct
from pathlib import Path
REV0_SHA1="1c2a53332382e14dab8815e3a6dd81ad89534050"
REV1_SHA1="424740be1fc67a5ddb954794443646e6aeee2c1b"
DEBUG_SHA1="ca5e3d415c4b47353a73a616878ba833f3648b7a"
R=(0x2446C,0x25A70); D=(0x27A10,0x29014); DELTA=0x35A4
R_SHA="387c50cd9ce66f37d2317559fbeb3b67a874d229b51fcdeb292431c9d01723e0"
D_SHA="86932d3b4f5a519048f6c4eaead2593027189a246bf598f2aa709bd12203eb8a"
STARTS=[148588,148636,148836,148884,148984,149128,149296,149444,149620,149676,150056,150164,150224,151072,151096,151128,151180,151272,151296,151364,151552,151740,151828,152324,152640,152924,153020,153184,153308,153764,153848,154032]
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
 assert R[1]-R[0]==D[1]-D[0]==5636
 for opcode,off in zip(range(0x60,0x80),STARTS):
  assert (u32(r1,TR+4*opcode)&~1)==0x08000000+off
  assert (u32(d,TD+4*opcode)&~1)==0x08000000+off+DELTA
 assert (u32(r1,TR+4*0x80)&~1)==0x08025A70
 assert (u32(d,TD+4*0x80)&~1)==0x08029014
 print("German status/utility/field script core verification passed")
 print("Opcodes: 0x60..0x7F")
 print("Stable Debug delta: +0x35A4")

if __name__=="__main__": main()
