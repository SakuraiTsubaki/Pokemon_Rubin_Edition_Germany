#!/usr/bin/env python3
import argparse, hashlib, struct
from pathlib import Path
UR=(0x411D8,0x41534); UD=(0x45354,0x456B0)
BR=(0x41534,0x415D4); BD=(0x456B0,0x45750)
U_SHA="23eb87e96a7473038854c0f9edc982689d01efc389454663a1cd2d5a32419b96"
UD_SHA="7d86e6c9bd856b123c5b322d05da50efaeefd70d8b657bb36da5bbbe435ab35e"
B_SHA="13150341e5969b2327aed9ed6452aa2d6da482e3527ee5fedaac3a123d5da778"
BD_SHA="f98222f2d23d62a0b4c281964709531e1725a0bc394a8406ae481dc860cb070b"
STARTS=[0x411D8,0x41210,0x4121C,0x4122C,0x41258,0x412A4,0x41470,0x41498,0x414F0]
def h(x): return hashlib.sha256(x).hexdigest()
def u32(x,o): return struct.unpack_from("<I",x,o)[0]
def main():
 p=argparse.ArgumentParser(); p.add_argument("--rev0",type=Path,required=True); p.add_argument("--rev1",type=Path,required=True); p.add_argument("--debug",type=Path,required=True)
 a=p.parse_args(); r0=a.rev0.read_bytes(); r1=a.rev1.read_bytes(); d=a.debug.read_bytes()
 assert r0[UR[0]:BR[1]]==r1[UR[0]:BR[1]]
 assert h(r1[UR[0]:UR[1]])==U_SHA and h(d[UD[0]:UD[1]])==UD_SHA
 assert h(r1[BR[0]:BR[1]])==B_SHA and h(d[BD[0]:BD[1]])==BD_SHA
 for ro in STARTS+[0x41534]:
  assert r1[ro:ro+2]==d[ro+0x417C:ro+0x417E]
 assert u32(r1,0x414C8)==0x1121 and u32(r1,0x414CC)==0x8408
 crc_r=u32(r1,0x41530)-0x08000000; crc_d=u32(d,0x456AC)-0x08000000
 assert h(r1[crc_r:crc_r+512])==h(d[crc_d:crc_d+512])=="638dbc5f735cced09b3d0d767a72a8800baeb1b3bb399a514af61b3ea7be8a01"
 assert r1[0x415D4:0x415DC]==d[0x45750:0x45758]
 print("German util/blend_palette verification passed")
 print("util 0x35C; blend_palette 0xA0; stable Debug delta +0x417C")
 print("Next: daycare")
if __name__=="__main__": main()
