#!/usr/bin/env python3
import argparse, hashlib
from pathlib import Path

R=(0x8C430,0x93260)
D=(0x99864,0xA0694)
R_SHA="6e9cb760626238d323e52e2e7e273e108d3231c4a7aa03a1d93da7721bbf94f9"
D_SHA="adfc0aa3861ad4c0f5269d0ed3193cdaae58a7cf026c704bc381d826683fec62"
ENTRY36=bytes.fromhex("70 b5 16 48 00 21 01 80 15 4a 40 20 10 70 15 48 01 70 15 4c 00 20 61 76 21 76 a1 76 e1 76 e0 61 20 62 60 62")
LOOP=bytes.fromhex("48 1c 00 04 01 0c 33 29 f2 d9")
TAIL_R=(0x931DC,0x93260)
TAIL_D=(0xA0610,0xA0694)
TAIL_R_SHA="f92c2f9f66b399e72a99f1ebe646d4348cbde9d87b0cd6881750c479f14f1dc3"
TAIL_D_SHA="ac30dd4644022b708eaef9615e3057a11637b3941c5ff66f84535b0c44795e0a"
NEXT_R=bytes.fromhex("00 b5 00 f0 cb f8 04 48 6d f7 4a f9 03 48 9c 30 05 21 01 70 01 bc 00 47")
NEXT_D=bytes.fromhex("00 b5 07 4a 00 21 11 70 00 f0 20 f9")

def h(x): return hashlib.sha256(x).hexdigest()

def main():
 p=argparse.ArgumentParser()
 p.add_argument("--rev0",type=Path,required=True)
 p.add_argument("--rev1",type=Path,required=True)
 p.add_argument("--debug",type=Path,required=True)
 a=p.parse_args()
 r0=a.rev0.read_bytes(); r1=a.rev1.read_bytes(); d=a.debug.read_bytes()
 x0=r0[R[0]:R[1]]; x1=r1[R[0]:R[1]]; xd=d[D[0]:D[1]]
 assert len(x0)==len(x1)==len(xd)==0x6E30
 assert x0==x1
 assert h(x0)==R_SHA and h(x1)==R_SHA and h(xd)==D_SHA
 assert D[0]-R[0]==D[1]-R[1]==0xD434
 assert x0[:len(ENTRY36)]==ENTRY36 and xd[:len(ENTRY36)]==ENTRY36
 assert r0[R[0]+0x4A:R[0]+0x54]==LOOP
 assert d[D[0]+0x4A:D[0]+0x54]==LOOP
 assert h(r0[TAIL_R[0]:TAIL_R[1]])==TAIL_R_SHA
 assert h(d[TAIL_D[0]:TAIL_D[1]])==TAIL_D_SHA
 assert r0[R[1]:R[1]+len(NEXT_R)]==NEXT_R
 assert r1[R[1]:R[1]+len(NEXT_R)]==NEXT_R
 assert d[D[1]:D[1]+len(NEXT_D)]==NEXT_D
 print("German pokedex verification passed")
 print("Retail Rev0/Rev1: 0x0808C430..0x08093260, 0x6E30 bytes")
 print("Debug:            0x08099864..0x080A0694, 0x6E30 bytes")
 print("Accumulated Retail->Debug delta remains +0xD434")
 print("Next: trainer_card / TrainerCard_ShowPlayerCard")

if __name__=="__main__": main()
