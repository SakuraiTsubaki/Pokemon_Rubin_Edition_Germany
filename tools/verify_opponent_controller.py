#!/usr/bin/env python3
import argparse, hashlib, struct
from pathlib import Path
REV0_SHA1="1c2a53332382e14dab8815e3a6dd81ad89534050"
REV1_SHA1="424740be1fc67a5ddb954794443646e6aeee2c1b"
DEBUG_SHA1="ca5e3d415c4b47353a73a616878ba833f3648b7a"
MR=(0x32CB0,0x361C0); MD=(0x36A68,0x3A084)
TR=0x207F2C; TD=0x2210C4; N=57
MR_SHA="5aead473c0aa0e87861721324c5e59275a32c4b94272ce9c177675a0a1ad6bc8"
MD_SHA="2087279f73310a779b9615932200a34c5bd722e3475055ec516bf1d810fb48fc"
TR_SHA="94f93ad58b25d4be6b9354903bae1be753b4fa5dba2f8d7aa86f85d6e0d8b80f"
TD_SHA="19e1a40f578aa5973776361b3e4fa749e6552b469e47628d71a645431a6dad40"

def sha1(x): return hashlib.sha1(x).hexdigest()
def sha256(x): return hashlib.sha256(x).hexdigest()
def u32(x,o): return struct.unpack_from("<I",x,o)[0]

def main():
 p=argparse.ArgumentParser()
 p.add_argument("--rev0",type=Path,required=True); p.add_argument("--rev1",type=Path,required=True); p.add_argument("--debug",type=Path,required=True)
 a=p.parse_args(); r0=a.rev0.read_bytes(); r1=a.rev1.read_bytes(); d=a.debug.read_bytes()
 assert sha1(r0)==REV0_SHA1 and sha1(r1)==REV1_SHA1 and sha1(d)==DEBUG_SHA1
 assert r0[MR[0]:MR[1]]==r1[MR[0]:MR[1]]
 assert sha256(r1[MR[0]:MR[1]])==MR_SHA and sha256(d[MD[0]:MD[1]])==MD_SHA
 assert (MD[1]-MD[0])-(MR[1]-MR[0])==0x10C
 tr=r1[TR:TR+N*4]; td=d[TD:TD+N*4]
 assert r0[TR:TR+N*4]==tr
 assert sha256(tr)==TR_SHA and sha256(td)==TD_SHA
 for i in range(N):
  rp=u32(r1,TR+4*i)&~1; dp=u32(d,TD+4*i)&~1
  expected=0x3DB8 if i<=7 else (0x3DDC if i<=20 else 0x3EC4)
  assert dp-rp==expected,(i,hex(dp-rp),hex(expected))
 assert r1[0x361BC:0x361C0]==bytes.fromhex("70 47 00 00")
 assert d[0x3A080:0x3A084]==bytes.fromhex("70 47 00 00")
 assert d[0x3A084:0x3A086]==r1[0x361C0:0x361C2]
 print("German opponent controller verification passed")
 print("57 commands; Debug growth 0x10C = 0x24 + 0xE8")
 print("Next: battle_ai_switch_items at +0x3EC4")

if __name__=="__main__": main()
