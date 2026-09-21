#!/usr/bin/env python3
import argparse, hashlib, struct
from pathlib import Path

REV0_SHA1="1c2a53332382e14dab8815e3a6dd81ad89534050"
REV1_SHA1="424740be1fc67a5ddb954794443646e6aeee2c1b"
DEBUG_SHA1="ca5e3d415c4b47353a73a616878ba833f3648b7a"

TAIL_R=(0x1A200,0x1C1DC); TAIL_D=(0x1D754,0x1F754)
MODULE_R=(0x15324,0x1C1DC); MODULE_D=(0x183AC,0x1F754)
TAIL_R_SHA="89bba501313e49c894400ca736698e3c5b15ea142f28b0eddeeeea327b32429c"
TAIL_D_SHA="6a3350e10866d249f54ad7baa9939aa14766198460b93eb02171a4b3b0d8cce1"
MODULE_R_SHA="d6faa3fa2b22fcfe2cfdb8ddabb9161558683a5d1bf64bc4781efefa427fe9c4"
MODULE_D_SHA="11f5c8a6cbece220bc932537185f4c892d61fbc71009dabafb322325c60b3807"
FUNCS=[(0x1A200,0x1D754),(0x1B5E0,0x1EB34),(0x1B768,0x1ECBC),(0x1B794,0x1ECE8),(0x1BAFC,0x1F050)]

def sha1(x): return hashlib.sha1(x).hexdigest()
def sha256(x): return hashlib.sha256(x).hexdigest()
def u32(x,o): return struct.unpack_from("<I",x,o)[0]

def main():
 p=argparse.ArgumentParser()
 p.add_argument("--rev0",type=Path,required=True); p.add_argument("--rev1",type=Path,required=True); p.add_argument("--debug",type=Path,required=True)
 a=p.parse_args(); r0=a.rev0.read_bytes(); r1=a.rev1.read_bytes(); d=a.debug.read_bytes()
 assert sha1(r0)==REV0_SHA1 and sha1(r1)==REV1_SHA1 and sha1(d)==DEBUG_SHA1
 assert r0[TAIL_R[0]:TAIL_R[1]]==r1[TAIL_R[0]:TAIL_R[1]]
 assert sha256(r1[TAIL_R[0]:TAIL_R[1]])==TAIL_R_SHA and sha256(d[TAIL_D[0]:TAIL_D[1]])==TAIL_D_SHA
 assert r0[MODULE_R[0]:MODULE_R[1]]==r1[MODULE_R[0]:MODULE_R[1]]
 assert sha256(r1[MODULE_R[0]:MODULE_R[1]])==MODULE_R_SHA and sha256(d[MODULE_D[0]:MODULE_D[1]])==MODULE_D_SHA
 assert (MODULE_D[1]-MODULE_D[0])-(MODULE_R[1]-MODULE_R[0])==0x4F0
 for ro,do in FUNCS: assert r1[ro:ro+2]==d[do:do+2], (hex(ro),hex(do))
 assert u32(r1,0x207610+40)==0x0801B769 and u32(d,0x2207A8+40)==0x0801ECBD
 assert (0x1F754-0x1F050)-(0x1C1DC-0x1BAFC)==0x24
 assert 0x1F754-0x1C1DC==0x3578
 assert r1[0x1C1DC:0x1C1EC]==d[0x1F754:0x1F764]
 print("German battle_util tail/module verification passed")
 print("Action 10 resolved; next module battle_script_commands; delta +0x3578")

if __name__=="__main__": main()
