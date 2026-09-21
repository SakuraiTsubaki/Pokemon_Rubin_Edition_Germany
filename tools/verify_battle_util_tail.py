#!/usr/bin/env python3
import argparse, hashlib, struct
from pathlib import Path

REV0_SHA1="1c2a53332382e14dab8815e3a6dd81ad89534050"
REV1_SHA1="424740be1fc67a5ddb954794443646e6aeee2c1b"
DEBUG_SHA1="ca5e3d415c4b47353a73a616878ba833f3648b7a"

TAIL_R=(0x1A200,0x1BE24); TAIL_D=(0x1D754,0x1F39C)
MODULE_R=(0x15324,0x1BE24); MODULE_D=(0x183AC,0x1F39C)
TAIL_R_SHA="44621a33d30d6284f4542e3fda5affeee98ebe74b833dcb3c5c7b7640cb52fd3"
TAIL_D_SHA="34cc518702cc203987d6959d06982c3cc5acbba314bd7457f62417fcddbf66fe"
MODULE_R_SHA="109bd414e182e4e3c73a3d9e4745cb2e834463752a8366aa00fd020c12f9cf17"
MODULE_D_SHA="2f46b142f1a06e1b5dfe8a0e94a42a35d85b8390496966fed1a0f2b8dd22bd1"
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
 assert (0x1F39C-0x1F050)-(0x1BE24-0x1BAFC)==0x24
 assert 0x1F39C-0x1BE24==0x3578
 assert r1[0x1BE24:0x1BE2C]==d[0x1F39C:0x1F3A4]
 print("German battle_util tail/module verification passed")
 print("Action 10 resolved; next module battle_script_commands at atk00; delta +0x3578")

if __name__=="__main__": main()
