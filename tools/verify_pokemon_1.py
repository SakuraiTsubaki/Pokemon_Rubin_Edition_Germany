#!/usr/bin/env python3
import argparse, hashlib, struct
from pathlib import Path

REV0_SHA1="1c2a53332382e14dab8815e3a6dd81ad89534050"
REV1_SHA1="424740be1fc67a5ddb954794443646e6aeee2c1b"
DEBUG_SHA1="ca5e3d415c4b47353a73a616878ba833f3648b7a"

R=(0x3A894,0x3BC00)
D=(0x3E768,0x3FD7C)
R_SHA="b1dcf9b7bf3072ad0ab17e2d85a1cbcea07df28f5a509be3ac41e502cb7ada2e"
D_SHA="8da5f12cbf393f7623b27b2c855447dde85c1fec05219e5e047aaf1c4f875027"
STARTS=[239764,239788,239916,239948,239980,240092,240816,240920,241176,241280,241344,241460,241596,241996,242424,242572,243336,243416,243524,243632,243652,243764,243832,243896,243944,243956,244124,244392,244564]

def sha1(x): return hashlib.sha1(x).hexdigest()
def sha256(x): return hashlib.sha256(x).hexdigest()
def u16(x,o): return struct.unpack_from("<H",x,o)[0]

def bl_target(data, off):
    h1=u16(data,off); h2=u16(data,off+2)
    assert h1 & 0xF800 == 0xF000 and h2 & 0xF800 == 0xF800
    value=((h1 & 0x7FF)<<12)|((h2 & 0x7FF)<<1)
    if value & (1<<22): value -= 1<<23
    return 0x08000000 + off + 4 + value

def main():
 p=argparse.ArgumentParser()
 p.add_argument("--rev0",type=Path,required=True)
 p.add_argument("--rev1",type=Path,required=True)
 p.add_argument("--debug",type=Path,required=True)
 a=p.parse_args()
 r0=a.rev0.read_bytes(); r1=a.rev1.read_bytes(); d=a.debug.read_bytes()
 assert sha1(r0)==REV0_SHA1 and sha1(r1)==REV1_SHA1 and sha1(d)==DEBUG_SHA1
 assert r0[R[0]:R[1]]==r1[R[0]:R[1]]
 assert sha256(r1[R[0]:R[1]])==R_SHA and sha256(d[D[0]:D[1]])==D_SHA
 assert (D[1]-D[0])-(R[1]-R[0])==0x2A8

 for i,ro in enumerate(STARTS):
  delta=0x3ED4 if i<=15 else 0x417C
  do=ro+delta
  assert r1[ro:ro+2]==d[do:do+2],(i,hex(ro),hex(do))

 # CalculateMonStats keeps its Retail size, then Debug inserts 0x2A8 bytes.
 assert 0x3F55C-(0x3B38C+0x3ED4)==0x2FC
 assert 0x3F804-0x3F55C==0x2A8
 assert 0x3F804-(0x3B688)==0x417C

 # atk05_damagecalc directly proves the next CalculateBaseDamage entry.
 assert bl_target(r1,0x1CC12)==0x0803BC00
 assert bl_target(d,0x2018A)==0x0803FD7C

 print("German pokemon_1 verification passed")
 print("Retail functions: 29; Debug extra function: 680 bytes")
 print("BoxPokemon 0x50 / Pokemon 0x64 / four move slots")
 print("Next: CalculateBaseDamage at +0x417C")

if __name__=="__main__": main()
