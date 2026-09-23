#!/usr/bin/env python3
import argparse
import hashlib
from pathlib import Path

TOMO=(0x8B85C,0x8F3C4)
NOHARA=(0x8F3C4,0x90454)
MORI_R=(0x84144,0x84410)
MORI_D=(0x90454,0x90720)
TAYA=(0x90720,0x9177C)
DEBUG_BLOCK=(0x8B85C,0x9177C)

SHA={
    "tomo":"8382ed4234377c500d28fa69ad170d7dd9c6eeef46b045b4286a7ddd70b22b91",
    "nohara":"1858b8fb291d3f7c9a1e1e114fbaaa159221ef499d3a42aef0195bc176fc2a98",
    "mori_r":"f060b11a1bf4848bacf58419c38441f6c25d44850c8cbc10129c5a2c417b5663",
    "mori_d":"ed44baed947a6c5cb01c4a7c7ac5305c33070cf572cf536fc5ebb95df2670b52",
    "taya":"87df792ed184eb1dc86755a576a045247dc87e3a9f88097dad80a0f827c5d48d",
    "block":"0d8a1167d6047c0f2bef58ff748db967bc45955bda4fa299f46eb874008deb14",
}
TRAINER_PREFIX=bytes.fromhex("30 b5 00 24 0a 4d e0 00 00 19 80 00 41 19 08 78 c0 07 00 28 0e d0 c8 79 01 28 01 d0 03 28 09 d1")

def h(data):
    return hashlib.sha256(data).hexdigest()

def main():
    p=argparse.ArgumentParser(description="Verify German Pokemon Ruby Debug-menu module block")
    p.add_argument("--rev0",type=Path,required=True)
    p.add_argument("--rev1",type=Path,required=True)
    p.add_argument("--debug",type=Path,required=True)
    a=p.parse_args()
    r0=a.rev0.read_bytes()
    r1=a.rev1.read_bytes()
    d=a.debug.read_bytes()

    assert h(d[TOMO[0]:TOMO[1]])==SHA["tomo"]
    assert h(d[NOHARA[0]:NOHARA[1]])==SHA["nohara"]
    assert h(r0[MORI_R[0]:MORI_R[1]])==SHA["mori_r"]
    assert h(r1[MORI_R[0]:MORI_R[1]])==SHA["mori_r"]
    assert r0[MORI_R[0]:MORI_R[1]]==r1[MORI_R[0]:MORI_R[1]]
    assert h(d[MORI_D[0]:MORI_D[1]])==SHA["mori_d"]
    assert h(d[TAYA[0]:TAYA[1]])==SHA["taya"]
    assert h(d[DEBUG_BLOCK[0]:DEBUG_BLOCK[1]])==SHA["block"]

    assert TOMO[1]-TOMO[0]==0x3B68
    assert NOHARA[1]-NOHARA[0]==0x1090
    assert MORI_R[1]-MORI_R[0]==MORI_D[1]-MORI_D[0]==0x2CC
    assert TAYA[1]-TAYA[0]==0x105C
    assert (TOMO[1]-TOMO[0])+(NOHARA[1]-NOHARA[0])+(TAYA[1]-TAYA[0])==0x5C54
    assert MORI_D[0]-MORI_R[0]==0xC310
    assert 0x9177C-0x84410==0xD36C

    assert r0[0x84410:0x84410+len(TRAINER_PREFIX)]==TRAINER_PREFIX
    assert r1[0x84410:0x84410+len(TRAINER_PREFIX)]==TRAINER_PREFIX
    assert d[0x9177C:0x9177C+len(TRAINER_PREFIX)]==TRAINER_PREFIX

    print("German debug menu block verification passed")
    print("Retail: Mori 0x08084144..0x08084410")
    print("Debug: Tomomichi 0x0808B85C..0x0808F3C4")
    print("       Nohara     0x0808F3C4..0x08090454")
    print("       Mori       0x08090454..0x08090720")
    print("       Taya       0x08090720..0x0809177C")
    print("Trainer-see convergence delta: +0xD36C")

if __name__=="__main__":
    main()
