#!/usr/bin/env python3
import argparse, hashlib
from pathlib import Path
R=(0xA2C68,0xA3094); D=(0xB082C,0xB0C58)
RS="d1f7c56133c3f2cfaf49ca8e2563296e1d0d23c109e832aa5a8ed6fa520e25f7"; DS="4cae863753115f6685058df5d06f329b1c58d1d70dc3a047500794c19b066855"
ENTRY=bytes.fromhex("30 b5 00 24 07 4d e0 00 00 19 80 00 40 19 00 f0 0b f8")
TR=(0xA307C,0xA3094); TD=(0xB0C40,0xB0C58); TS="c95417e6a9324955274a945c1465d4e64bc47b5fa59d79522d36d3f260fffa1f"
NEXT_R=bytes.fromhex("00 b5 ce f7 51 ff 00 f0 03 f8 01 20 02 bc 08 47")
def h(x): return hashlib.sha256(x).hexdigest()
def main():
 p=argparse.ArgumentParser(); p.add_argument("--rev0",type=Path,required=True); p.add_argument("--rev1",type=Path,required=True); p.add_argument("--debug",type=Path,required=True); a=p.parse_args()
 r0=a.rev0.read_bytes(); r1=a.rev1.read_bytes(); d=a.debug.read_bytes()
 x0=r0[R[0]:R[1]]; x1=r1[R[0]:R[1]]; xd=d[D[0]:D[1]]
 assert len(x0)==len(x1)==len(xd)==0x42C and x0==x1
 assert h(x0)==RS and h(x1)==RS and h(xd)==DS
 assert D[0]-R[0]==D[1]-R[1]==0xDBC4
 assert x0[:len(ENTRY)]==ENTRY and xd[:len(ENTRY)]==ENTRY
 tr=r0[TR[0]:TR[1]]; td=d[TD[0]:TD[1]]; assert tr==td and h(tr)==TS
 assert r0[R[1]:R[1]+len(NEXT_R)]==NEXT_R and r1[R[1]:R[1]+len(NEXT_R)]==NEXT_R
 print("German mail_data verification passed")
 print("Retail Rev0/Rev1: 0x080A2C68..0x080A3094, 0x42C bytes")
 print("Debug:            0x080B082C..0x080B0C58, 0x42C bytes")
 print("Accumulated Retail->Debug delta remains +0xDBC4")
 print("Next: map_name_popup / unref_sub_80A2F44")
if __name__=="__main__": main()
