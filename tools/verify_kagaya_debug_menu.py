#!/usr/bin/env python3
import argparse, hashlib
from pathlib import Path
K=(0xB05C4,0xB082C)
KS="4c12dd142520ba4092d845b622771c5b5ab31988d606746c06b8af8fb9a34526"
LAST=(0xB0800,0xB082C); LASTS="60a1c0b773316494820caa986f65f8ee90c0b6c609bde4275e496e8aa32dcc28"
ENTRY=bytes.fromhex("00 b5 00 f0 03 f8 00 20 02 bc 08 47")
MAIL=bytes.fromhex("30 b5 00 24 07 4d e0 00 00 19 80 00 40 19 00 f0 0b f8")
def h(x): return hashlib.sha256(x).hexdigest()
def main():
 p=argparse.ArgumentParser(); p.add_argument("--rev0",type=Path,required=True); p.add_argument("--rev1",type=Path,required=True); p.add_argument("--debug",type=Path,required=True); a=p.parse_args()
 r0=a.rev0.read_bytes(); r1=a.rev1.read_bytes(); d=a.debug.read_bytes()
 assert len(d[K[0]:K[1]])==0x268 and h(d[K[0]:K[1]])==KS
 assert d[K[0]:K[0]+len(ENTRY)]==ENTRY
 assert h(d[LAST[0]:LAST[1]])==LASTS
 assert d[K[1]:K[1]+len(MAIL)]==MAIL
 assert r0[0xA2C68:0xA2C68+len(MAIL)]==MAIL and r1[0xA2C68:0xA2C68+len(MAIL)]==MAIL
 assert 0xB082C-0xA2C68==0xDBC4
 print("German kagaya_debug_menu verification passed")
 print("Debug: 0x080B05C4..0x080B082C, 0x268 bytes")
 print("mail_data rejoin delta: +0xDBC4")
if __name__=="__main__": main()
