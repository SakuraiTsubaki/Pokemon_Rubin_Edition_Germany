#!/usr/bin/env python3
import argparse
import hashlib
from pathlib import Path

RETAIL=(0x84DCC,0x85ABC)
DEBUG=(0x92138,0x92E88)
RETAIL_SHA256="957aab21eeb0e9a3f6fe29b2b0a8884ab46f3d1ca239c48f02ad38a548357413"
DEBUG_SHA256="b9022adf9e727020045e3f601fa1073865d2cf5f4f510eae98c8e79708da6cdc"
ENTRY=bytes.fromhex("01 49 08 70 70 47 00 00")
DEBUG_FEEBAS=(0x92344,0x9236C)
DEBUG_DICE=(0x9283C,0x92874)
DEBUG_FEEBAS_SHA256="4e4b5a83b8afa73f3f3b25eb73c5bf3491531398dbd0805fe22e2608dd957b42"
DEBUG_DICE_SHA256="3c06b8bdc88b76b1777c7337fe0fc9144061ef10bf1505ebe5feb7d703f4e7a0"
TAIL_RETAIL=(0x85A94,0x85ABC)
TAIL_DEBUG=(0x92E60,0x92E88)
TAIL_RETAIL_SHA256="dbb891d095b12726f53ac3658337ec1168a99ab0f35a94dd1eda1b70c189a1c6"
TAIL_DEBUG_SHA256="53f5e67a03e31cde8943aa20a7044fd19816594da491d2fe9b41a023480169b2"
NEXT=bytes.fromhex("30 b5 82 b0 04 1c 24 06 24 0e 20 1c")

def sha256(data): return hashlib.sha256(data).hexdigest()

def main():
    p=argparse.ArgumentParser(description="Verify German Pokemon Ruby wild_encounter module")
    p.add_argument("--rev0",type=Path,required=True)
    p.add_argument("--rev1",type=Path,required=True)
    p.add_argument("--debug",type=Path,required=True)
    a=p.parse_args()
    r0=a.rev0.read_bytes(); r1=a.rev1.read_bytes(); dbg=a.debug.read_bytes()
    x0=r0[RETAIL[0]:RETAIL[1]]; x1=r1[RETAIL[0]:RETAIL[1]]; xd=dbg[DEBUG[0]:DEBUG[1]]
    assert len(x0)==len(x1)==0xCF0
    assert len(xd)==0xD50
    assert x0==x1
    assert sha256(x0)==RETAIL_SHA256 and sha256(x1)==RETAIL_SHA256
    assert sha256(xd)==DEBUG_SHA256
    assert DEBUG[0]-RETAIL[0]==0xD36C
    assert DEBUG[1]-RETAIL[1]==0xD3CC
    assert len(xd)-len(x0)==0x60
    assert x0[:8]==ENTRY and xd[:8]==ENTRY
    assert int.from_bytes(r0[RETAIL[0]+8:RETAIL[0]+12],"little")==0x0202FF7C
    assert int.from_bytes(dbg[DEBUG[0]+8:DEBUG[0]+12],"little")==0x02030228
    assert sha256(dbg[DEBUG_FEEBAS[0]:DEBUG_FEEBAS[1]])==DEBUG_FEEBAS_SHA256
    assert sha256(dbg[DEBUG_DICE[0]:DEBUG_DICE[1]])==DEBUG_DICE_SHA256
    assert sha256(r0[TAIL_RETAIL[0]:TAIL_RETAIL[1]])==TAIL_RETAIL_SHA256
    assert sha256(dbg[TAIL_DEBUG[0]:TAIL_DEBUG[1]])==TAIL_DEBUG_SHA256
    assert r0[RETAIL[1]:RETAIL[1]+len(NEXT)]==NEXT
    assert r1[RETAIL[1]:RETAIL[1]+len(NEXT)]==NEXT
    assert dbg[DEBUG[1]:DEBUG[1]+len(NEXT)]==NEXT
    print("German wild_encounter verification passed")
    print("Retail Rev0/Rev1: 0x08084DCC..0x08085ABC, 0xCF0 bytes")
    print("Debug:            0x08092138..0x08092E88, 0xD50 bytes")
    print("Debug growth: 0x60 = Feebas debug 0x28 + dice-roll sampler 0x38")
    print("Accumulated Retail->Debug delta changes +0xD36C -> +0xD3CC")
    print("Next: field_effect / FieldEffectStart")

if __name__=="__main__":
    main()
