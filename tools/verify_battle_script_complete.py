#!/usr/bin/env python3
import argparse, hashlib, struct
from pathlib import Path
REV0_SHA1="1c2a53332382e14dab8815e3a6dd81ad89534050"
REV1_SHA1="424740be1fc67a5ddb954794443646e6aeee2c1b"
DEBUG_SHA1="ca5e3d415c4b47353a73a616878ba833f3648b7a"
SLICE_R=(0x2AE54,0x2C144); SLICE_D=(0x2E4B8,0x2F7A8)
MOD_R=(0x1BE24,0x2C144); MOD_D=(0x1F39C,0x2F7A8)
SR_SHA="5f0c2a052fc9513f290c5cd3988c9468509211815bd88cd29d0ddaf3e884ead5"
SD_SHA="80a072aa0e859189edb0bf58407561412377dd7b941581a8621ddd1037581d0a"
MR_SHA="7cda4dc84fef6029645fb5fe6a6eceb05b02e582cf888663c2def8a4d42a6864"
MD_SHA="5938e9fa8bcfd0bf0ec3836249dc89afb2d2943188595188e98122da2ce763fe"
STARTS=[175700,175824,176044,176176,176260,176444,176680,176788,176860,177044,177248,177412,177588,177800,177904,178060,178996,179124,179300,179812,180420,180468,180508,180520]
TR=0x20770C; TD=0x2208A4; DELTA=0x3664
HELPERS=[(0x2BDA8,0x2F40C),(0x2BE40,0x2F4A4),(0x2BE60,0x2F4C4)]

def sha1(x): return hashlib.sha1(x).hexdigest()
def sha256(x): return hashlib.sha256(x).hexdigest()
def u32(x,o): return struct.unpack_from("<I",x,o)[0]

def main():
 p=argparse.ArgumentParser()
 p.add_argument("--rev0",type=Path,required=True); p.add_argument("--rev1",type=Path,required=True); p.add_argument("--debug",type=Path,required=True)
 a=p.parse_args(); r0=a.rev0.read_bytes(); r1=a.rev1.read_bytes(); d=a.debug.read_bytes()
 assert sha1(r0)==REV0_SHA1 and sha1(r1)==REV1_SHA1 and sha1(d)==DEBUG_SHA1
 assert r0[SLICE_R[0]:SLICE_R[1]]==r1[SLICE_R[0]:SLICE_R[1]]
 assert sha256(r1[SLICE_R[0]:SLICE_R[1]])==SR_SHA and sha256(d[SLICE_D[0]:SLICE_D[1]])==SD_SHA
 assert r0[MOD_R[0]:MOD_R[1]]==r1[MOD_R[0]:MOD_R[1]]
 assert sha256(r1[MOD_R[0]:MOD_R[1]])==MR_SHA and sha256(d[MOD_D[0]:MOD_D[1]])==MD_SHA
 assert (MOD_D[1]-MOD_D[0])-(MOD_R[1]-MOD_R[0])==0xEC
 for opcode,off in zip(range(0xE0,0xF8),STARTS):
  rp=u32(r1,TR+4*opcode)&~1; dp=u32(d,TD+4*opcode)&~1
  assert rp==0x08000000+off and dp-rp==DELTA
 for ro,do in HELPERS: assert r1[ro:ro+4]==d[do:do+4]
 assert r1[0x2C144:0x2C146]==bytes.fromhex("70 47")
 assert d[0x2F7A8:0x2F7AA]==bytes.fromhex("70 47")
 print("German battle_script_commands complete verification passed")
 print("248 opcodes mapped; retail bytes:",MOD_R[1]-MOD_R[0])
 print("Debug extra: 0xEC = 0x2C + 0xC0")
 print("Next: battle_controller_player")

if __name__=="__main__": main()
