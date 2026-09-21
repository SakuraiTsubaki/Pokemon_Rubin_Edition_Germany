#!/usr/bin/env python3
import argparse, hashlib, struct
from pathlib import Path
REV0_SHA1="1c2a53332382e14dab8815e3a6dd81ad89534050"
REV1_SHA1="424740be1fc67a5ddb954794443646e6aeee2c1b"
DEBUG_SHA1="ca5e3d415c4b47353a73a616878ba833f3648b7a"
R=(0x29850,0x2AE54); D=(0x2CEB4,0x2E4B8); DELTA=0x3664
R_SHA="174eb2f5c256fe591be923bbd873e24d3121ff76af5306bafadcf47b9b9b7540"
D_SHA="54a42142ac9ed17d164c5186698419eebb41dc38219c608dbecc19631a92a736"
STARTS=[170064,170328,170624,170740,171036,171564,171696,171840,171904,171992,172148,172224,172324,172440,172572,172660,172752,172868,173036,173700,173820,174032,174120,174224,174336,174444,174544,174696,174952,175040,175192,175568]
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
 for opcode,off in zip(range(0xC0,0xE0),STARTS):
  rp=u32(r1,TR+4*opcode)&~1; dp=u32(d,TD+4*opcode)&~1
  assert rp==0x08000000+off and dp-rp==DELTA
 print("German late-Gen3 mechanics script core verification passed")
 print("Opcodes: 0xC0..0xDF; stable Debug delta +0x3664")

if __name__=="__main__": main()
