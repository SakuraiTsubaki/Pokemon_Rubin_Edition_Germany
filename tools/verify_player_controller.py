#!/usr/bin/env python3
import argparse, hashlib, struct
from pathlib import Path
REV0_SHA1="1c2a53332382e14dab8815e3a6dd81ad89534050"
REV1_SHA1="424740be1fc67a5ddb954794443646e6aeee2c1b"
DEBUG_SHA1="ca5e3d415c4b47353a73a616878ba833f3648b7a"
MR=(0x2C144,0x314C4); MD=(0x2F7A8,0x3527C)
TR=0x207D68; TD=0x220F00; N=57
MR_SHA="7b2e93299fcb177e344049e3b6443099374d57a624ba2c86f80ef3bd2c1093fb"
MD_SHA="bc563162bc54b9e206540d86fcb8509c040cc12bf77f9eedb317c7e86ad18f68"
TR_SHA="96b74032006663bbeb41941c1331912b07f7cb5e31dc4cea4bb18c92c48e8d4f"
TD_SHA="4380e6eff2e2beabccb6ced1f9817bd951f8e406d02786585edb3fdabb2ba99e"

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
 assert (MD[1]-MD[0])-(MR[1]-MR[0])==0x754
 tr=r1[TR:TR+N*4]; td=d[TD:TD+N*4]
 assert r0[TR:TR+N*4]==tr
 assert sha256(tr)==TR_SHA and sha256(td)==TD_SHA
 for i in range(N):
  rp=u32(r1,TR+4*i)&~1; dp=u32(d,TD+4*i)&~1
  assert dp-rp==0x3DB8,(i,hex(rp),hex(dp))
 assert r1[0x314C0:0x314C4]==bytes.fromhex("70 47 00 00")
 assert d[0x35278:0x3527C]==bytes.fromhex("70 47 00 00")
 assert r1[0x314C4:0x314C6]==bytes.fromhex("f0 b5")
 assert d[0x3527C:0x3527E]==bytes.fromhex("f0 b5")
 print("German player battle controller verification passed")
 print("57 commands (0x00..0x38)")
 print("Debug growth before handlers: 0x754")
 print("Next: battle_gfx_sfx_util")

if __name__=="__main__": main()
