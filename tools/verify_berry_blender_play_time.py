#!/usr/bin/env python3
import argparse, hashlib
from pathlib import Path

BR=(0x4E5FC,0x52F68); BD=(0x527C8,0x57158)
PR=(0x52F68,0x53040); PD=(0x57158,0x57230)

def h(x): return hashlib.sha256(x).hexdigest()

def main():
 p=argparse.ArgumentParser()
 p.add_argument("--rev0",type=Path,required=True)
 p.add_argument("--rev1",type=Path,required=True)
 p.add_argument("--debug",type=Path,required=True)
 a=p.parse_args(); r0=a.rev0.read_bytes(); r1=a.rev1.read_bytes(); d=a.debug.read_bytes()

 assert r0[BR[0]:PR[1]]==r1[BR[0]:PR[1]]

 assert h(r1[BR[0]:BR[1]])=="62fbfcba5debf22f2b64ad53dd3c5eda741cf850c9c150d8795c7fa3b2090966"
 assert h(d[BD[0]:BD[1]])=="7d7d9ca8ce896788f29041665b0b537b8c4ae462f7dc1cabecbfd46a2ac913e3"
 assert BR[1]-BR[0]==0x496C
 assert BD[1]-BD[0]==0x4990
 assert (BD[1]-BD[0])-(BR[1]-BR[0])==0x24
 assert BD[0]-BR[0]==0x41CC
 assert BD[1]-BR[1]==0x41F0

 assert h(r1[PR[0]:PR[1]])=="cbe0ba61dc55c205fab73d819b5c367d5f6660e0e60a7506f29a3af9d1e23ee7"
 assert h(d[PD[0]:PD[1]])=="942d56b27ff8b4f95fdd33623153482f69d052ce76ffcf0808e1706368da4281"
 assert PR[1]-PR[0]==PD[1]-PD[0]==0xD8
 assert PD[0]-PR[0]==PD[1]-PR[1]==0x41F0

 # PlayTimeCounter_Reset and new_game write_word_to_mem fingerprints.
 assert r1[0x52F68:0x52F7E]==d[0x57158:0x5716E]
 assert r1[0x53040:0x53050]==d[0x57230:0x57240]

 print("German berry_blender/play_time verification passed")
 print("Berry Debug growth: 0x24; accumulated delta now +0x41F0")
 print("Next: new_game")

if __name__=="__main__": main()
