#!/usr/bin/env python3
import argparse, hashlib, struct
from pathlib import Path
REV0_SHA1="1c2a53332382e14dab8815e3a6dd81ad89534050"
REV1_SHA1="424740be1fc67a5ddb954794443646e6aeee2c1b"
DEBUG_SHA1="ca5e3d415c4b47353a73a616878ba833f3648b7a"
R=(0x25A70,0x27B64); D=(0x29014,0x2B1C8)
R_SHA="4ff38ee3cd2d99b00c61ac34cd1ce77e206fdfc8c240cf20bf1216b8fa4ab805"
D_SHA="64e2ac7d35bed453b2c3ee3b6d6531e04ad38ace1a7dd9d4829f8643cc5726ff"
STARTS=[154224,154352,154560,154632,154804,154928,155052,155348,155584,156824,156908,156992,157104,157168,157244,157540,158304,158724,158868,159052,159788,159848,159936,160312,160780,161052,161200,161292,161708,161968,162444,162612]
TR=0x20770C; TD=0x2208A4
HELPERS=[(0x25C18,0x291BC),(0x25FF4,0x29598),(0x26694,0x29C38),(0x27868,0x2AE0C)]

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
 assert R[1]-R[0]==8436 and D[1]-D[0]==8628
 for opcode,off in zip(range(0x80,0xA0),STARTS):
  rp=u32(r1,TR+4*opcode)&~1; dp=u32(d,TD+4*opcode)&~1
  assert rp==0x08000000+off
  expected=0x35A4 if opcode<=0x9E else 0x3664
  assert dp-rp==expected,(hex(opcode),hex(dp-rp))
 for ro,do in HELPERS:
  assert r1[ro:ro+4]==d[do:do+4],(hex(ro),hex(do))
 assert ((u32(d,TD+4*0x9F)&~1)-(u32(d,TD+4*0x9E)&~1))-((u32(r1,TR+4*0x9F)&~1)-(u32(r1,TR+4*0x9E)&~1))==0xC0
 print("German advanced-effects/Metronome core verification passed")
 print("Opcodes: 0x80..0x9F")
 print("Metronome Debug growth: 0xC0; next delta +0x3664")

if __name__=="__main__": main()
