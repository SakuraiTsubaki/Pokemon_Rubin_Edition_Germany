#!/usr/bin/env python3
import argparse, hashlib
from pathlib import Path
R=(0xA2654,0xA2C68); D=(0xAFEE4,0xB05C4)
RS="6be9fdd17acaf4a027dfaa86910ed014dc98c1652e88518454fe51e0a004c548"; DS="337c6fba9a54af29502dc2e62fcfa5e99ed0a24655c343e93ede974a0a94746d"
DBG=(0xAFEE4,0xAFFB0); DBGS="daa2efebe8574e6b559ae418eb20884950d8d3a7519ae8c88617636fac1a906d"
TR=(0xA2C50,0xA2C68); TD=(0xB05AC,0xB05C4)
TRS="7efe7b605c208fa906fb0fab38e7dcfdbbbc761e07271e0ee6fc3c0ebd8f92e2"; TDS="357678a73b9bbe53f16963c07c5047f266afe9da96d3e5ef85033ee6f342beb7"
NR=bytes.fromhex("30 b5 00 24 07 4d e0 00 00 19 80 00 40 19 00 f0 0b f8")
ND=bytes.fromhex("00 b5 00 f0 03 f8 00 20 02 bc 08 47")
def h(x): return hashlib.sha256(x).hexdigest()
def main():
 p=argparse.ArgumentParser(); p.add_argument("--rev0",type=Path,required=True); p.add_argument("--rev1",type=Path,required=True); p.add_argument("--debug",type=Path,required=True); a=p.parse_args()
 r0=a.rev0.read_bytes(); r1=a.rev1.read_bytes(); d=a.debug.read_bytes()
 x0=r0[R[0]:R[1]]; x1=r1[R[0]:R[1]]; xd=d[D[0]:D[1]]
 assert len(x0)==0x614 and len(x1)==0x614 and len(xd)==0x6E0 and x0==x1
 assert h(x0)==RS and h(x1)==RS and h(xd)==DS
 assert D[0]-R[0]==0xD890 and D[1]-R[1]==0xD95C and len(xd)-len(x0)==0xCC
 assert h(d[DBG[0]:DBG[1]])==DBGS and len(d[DBG[0]:DBG[1]])==0xCC
 assert h(r0[TR[0]:TR[1]])==TRS and h(d[TD[0]:TD[1]])==TDS
 assert r0[R[1]:R[1]+len(NR)]==NR and r1[R[1]:R[1]+len(NR)]==NR
 assert d[D[1]:D[1]+len(ND)]==ND
 print("German fldeff_cut verification passed")
 print("Retail Rev0/Rev1: 0x080A2654..0x080A2C68, 0x614 bytes")
 print("Debug:            0x080AFEE4..0x080B05C4, 0x6E0 bytes")
 print("Debug growth: 0xCC in Debug_SetUpFieldMove_Cut")
 print("Accumulated Retail->Debug delta changes +0xD890 -> +0xD95C")
 print("Next Retail: mail_data / ClearMailData")
 print("Next Debug: kagaya_debug_menu / InitKagayaDebugMenu_A")
if __name__=="__main__": main()
