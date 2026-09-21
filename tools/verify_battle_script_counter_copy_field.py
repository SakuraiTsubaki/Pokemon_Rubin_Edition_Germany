#!/usr/bin/env python3
import argparse, hashlib, struct
from pathlib import Path
REV0_SHA1="1c2a53332382e14dab8815e3a6dd81ad89534050"
REV1_SHA1="424740be1fc67a5ddb954794443646e6aeee2c1b"
DEBUG_SHA1="ca5e3d415c4b47353a73a616878ba833f3648b7a"
R=(0x27B64,0x29850); D=(0x2B1C8,0x2CEB4); DELTA=0x3664
R_SHA="6644ec154e3cd15bf0be45a27a6a3375dbb6b35228fb9c1d05ce3f15d1705065"
D_SHA="0befa4b0c047905478c820e4da840fef77e821d441db7e2755cfabfaeadc67cc"
STARTS=[162660,162744,162992,163240,163564,163872,164120,164624,164712,165364,165676,165820,165844,165948,166444,167080,167236,167376,167424,167608,167988,168092,168272,168404,168592,168736,169028,169404,169492,169620,169692,170016]
TR=0x20770C; TD=0x2208A4
HELPERS=[(0x28524,0x2BB88),(0x28560,0x2BBC4),(0x28588,0x2BBEC),(0x2875C,0x2BDC0)]

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
 assert R[1]-R[0]==D[1]-D[0]==7404
 for opcode,off in zip(range(0xA0,0xC0),STARTS):
  rp=u32(r1,TR+4*opcode)&~1; dp=u32(d,TD+4*opcode)&~1
  assert rp==0x08000000+off and dp-rp==DELTA
 for ro,do in HELPERS: assert r1[ro:ro+4]==d[do:do+4]
 print("German counter/copy/field-rule script core verification passed")
 print("Opcodes: 0xA0..0xBF; stable Debug delta +0x3664")

if __name__=="__main__": main()
