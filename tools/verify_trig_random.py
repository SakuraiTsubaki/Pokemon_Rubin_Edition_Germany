#!/usr/bin/env python3
import argparse, hashlib, struct
from pathlib import Path
TR=(0x41110,0x411A8); TD=(0x4528C,0x45324)
RR=(0x411A8,0x411D8); RD=(0x45324,0x45354)
def h(x): return hashlib.sha256(x).hexdigest()
def u32(x,o): return struct.unpack_from("<I",x,o)[0]
def main():
 p=argparse.ArgumentParser(); p.add_argument("--rev0",type=Path,required=True); p.add_argument("--rev1",type=Path,required=True); p.add_argument("--debug",type=Path,required=True)
 a=p.parse_args(); r0=a.rev0.read_bytes(); r1=a.rev1.read_bytes(); d=a.debug.read_bytes()
 assert r0[TR[0]:RR[1]]==r1[TR[0]:RR[1]]
 assert h(r1[TR[0]:TR[1]])=="4ca4702ed06a970f5502bb52b7354e995528a32dae91ade3d9ddbf48f1e276aa"
 assert h(d[TD[0]:TD[1]])=="0542d9f677d3195b88fbe91590a9167b8fb741f5635c6aa39420e576d050bc6e"
 assert h(r1[RR[0]:RR[1]])=="0124eac0db619a26f2570eac3dc66b5963878fb31e450a0b0aa8f6f223cd55a4"
 assert h(d[RD[0]:RD[1]])=="519530735ef7cefd06e9c01b6abd00cc661c01fea7d2aa829be89b51cb4e65cf"
 sine_r=u32(r1,0x41128)-0x08000000; sine_d=u32(d,0x452A4)-0x08000000
 deg_r=u32(r1,0x41180)-0x08000000; deg_d=u32(d,0x452FC)-0x08000000
 assert h(r1[sine_r:sine_r+640])==h(d[sine_d:sine_d+640])=="dbdf49974fb8a6f319acc84a54ad90b3167aa588b2a3eafc62a6289c4d926205"
 assert h(r1[deg_r:deg_r+360])==h(d[deg_d:deg_d+360])=="353f23c8d42a29b25f44f9ef952af11f4745681ab8c479887b23f984631c72a0"
 assert u32(r1,0x411BC)==0x03004828 and u32(d,0x45338)==0x030048F8
 assert r1[0x411D8:0x411DC]==d[0x45354:0x45358]
 print("German trig/random verification passed")
 print("Next: util at +0x417C")
if __name__=="__main__": main()
