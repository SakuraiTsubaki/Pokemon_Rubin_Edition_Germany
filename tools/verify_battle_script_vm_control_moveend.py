#!/usr/bin/env python3
import argparse
import hashlib
import struct
from pathlib import Path

REV0_SHA1="1c2a53332382e14dab8815e3a6dd81ad89534050"
REV1_SHA1="424740be1fc67a5ddb954794443646e6aeee2c1b"
DEBUG_SHA1="ca5e3d415c4b47353a73a616878ba833f3648b7a"

R=(0x21164,0x224B0); D=(0x24708,0x25A54); DELTA=0x35A4
R_SHA="eafda36717d95918b2233c1b582886630954e30ed4a235c4102ceb0eee044ecf"
D_SHA="0a4a16537389dd12cf1f96241506ef8906b6ab8663297fa126972bd03157a7b6"
STARTS=[135524,135568,135652,135760,135804,135860,135928,135972,136028,136096,136160,136192,136280,136292,136324,136348,136396,136444,136536,136612,136644,136840,137044,137168,137676]
OPCODES=[48,49,50,51,52,53,54,55,56,57,58,59,60,61,62,63,65,66,67,68,69,70,71,72,73]
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
 assert R[1]-R[0]==D[1]-D[0]==4940
 for opcode,off in zip(OPCODES,STARTS):
  assert (u32(r1,TR+4*opcode)&~1)==0x08000000+off
  assert (u32(d,TD+4*opcode)&~1)==0x08000000+off+DELTA
 assert (u32(r1,TR+4*0x40)&~1)==0x0801C26C
 assert (u32(d,TD+4*0x40)&~1)==0x0801F7E4
 print("German VM-control/move-end core verification passed")
 print("Mapped physical opcodes: 0x30..0x3F and 0x41..0x49")
 print("Stable local Debug delta: +0x35A4")

if __name__=="__main__": main()
