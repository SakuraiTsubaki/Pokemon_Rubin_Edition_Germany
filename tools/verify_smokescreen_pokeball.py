#!/usr/bin/env python3
import argparse, hashlib
from pathlib import Path
BI_R=(0x43A60,0x46558); BI_D=(0x47BDC,0x4A724)
SM_R=(0x46558,0x46724); SM_D=(0x4A724,0x4A8F0)
PB_R=(0x46724,0x47CF0); PB_D=(0x4A8F0,0x4BEBC)
def h(x): return hashlib.sha256(x).hexdigest()
def main():
 p=argparse.ArgumentParser(); p.add_argument("--rev0",type=Path,required=True); p.add_argument("--rev1",type=Path,required=True); p.add_argument("--debug",type=Path,required=True)
 a=p.parse_args(); r0=a.rev0.read_bytes(); r1=a.rev1.read_bytes(); d=a.debug.read_bytes()
 assert r0[BI_R[0]:PB_R[1]]==r1[BI_R[0]:PB_R[1]]
 assert h(r1[BI_R[0]:BI_R[1]])=="3d9b4de9cf84eb5e822465da4d6da33b16f863c2171db1e45bc67a11c34c748b"
 assert h(d[BI_D[0]:BI_D[1]])=="c4ab84b3d9f3b3130081fe21e08026c878b28bdfb58fc1bdc5106a0e3c7f523a"
 assert h(r1[SM_R[0]:SM_R[1]])=="9d3da42856cd6652a3631b80949bc24d715b76379255c937072272f904847534"
 assert h(d[SM_D[0]:SM_D[1]])=="a68ab77999306175e97fbfccb0b864511952e7a087099004f40a31d02e4879ab"
 assert h(r1[PB_R[0]:PB_R[1]])=="118403c067324952cec68297957f769cc66c87579a83561c4213ea250dcb6b66"
 assert h(d[PB_D[0]:PB_D[1]])=="01145d9d2698d8fc33e6b6145a8fa77794ee41c2ddafb9c4fd99c742bf5bd11b"
 assert SM_R[1]-SM_R[0]==SM_D[1]-SM_D[0]==0x1CC
 assert PB_R[1]-PB_R[0]==PB_D[1]-PB_D[0]==0x15CC
 assert r1[0x46558:0x46568]==d[0x4A724:0x4A734]
 assert r1[0x46724:0x46734]==d[0x4A8F0:0x4A900]
 # load_save starts with CheckForFlashMemory; first instruction is push {lr}
 assert r1[0x47CF0:0x47CF2]==bytes.fromhex("00 b5")
 assert d[0x4BEBC:0x4BEBE]==bytes.fromhex("00 b5")
 print("Corrected battle_interface + smokescreen + pokeball verification passed")
 print("Next: load_save at +0x41CC")
if __name__=="__main__": main()
