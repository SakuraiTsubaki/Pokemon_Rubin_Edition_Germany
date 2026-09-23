#!/usr/bin/env python3
import argparse
import hashlib
from pathlib import Path

RETAIL=(0x77E7C,0x7ADE8)
DEBUG=(0x7F0E8,0x82054)
RETAIL_SHA256="45ac9b3545cb3dfc58e3e2b02c2cd0b193e72cb998e2f0c85dc21d3ad8d337fa"
DEBUG_SHA256="b077bfd1b8f84650c1fe96a10724f3d215b876d880c62c0319234564d87867b7"
ENTRY=bytes.fromhex("30 b5 00 06 05 0e 09 06 0c 0e ff f7 8b f8 00 06 00 28 04 d0 03 2c 02 d1 03 2d 00 d1 01 24 04 2c")
TAIL_RETAIL=(0x7AD7C,0x7ADE8)
TAIL_DEBUG=(0x81FE8,0x82054)
TAIL_RETAIL_SHA256="bf5c11aa0f0330b73deb89f6afb0c3eee4f0240f6168c48418cbc5dbaa2c1bfd"
TAIL_DEBUG_SHA256="035e1847ab0e415478379d66fecd1ea36f25379df79968e279de1371150ac722"
RESET_PREFIX=bytes.fromhex("f0 b5 00 24 13 4e 37 1c 08 37 a0 00 00 19 c0 00 82 19 00 21 11 71 10 49 11 60 54 71 01 34 94 71 01 21 49 42 0d 1c ff 21 d1 71 c0 19 00 21 20 22")
RESET_COMMON_AFTER_BL=bytes.fromhex("24 06 24 0e 0f 2c e6 d9 05 48 fe 21 41 71 06 49 40 18 01 78 29 43 01 70 f0 bc 01 bc 00 47 00 00")

def sha256(data):
    return hashlib.sha256(data).hexdigest()

def check_reset(data,start,g_tasks,task_dummy):
    fn=data[start:start+0x60]
    assert len(fn)==0x60
    assert fn[:0x30]==RESET_PREFIX
    assert fn[0x34:0x54]==RESET_COMMON_AFTER_BL
    assert fn[0x54:0x58]==g_tasks.to_bytes(4,"little")
    assert fn[0x58:0x5c]==task_dummy.to_bytes(4,"little")
    assert fn[0x5c:0x60]==(0x25E).to_bytes(4,"little")

def main():
    p=argparse.ArgumentParser(description="Verify German Pokemon Ruby rom_8077ABC module")
    p.add_argument("--rev0",type=Path,required=True)
    p.add_argument("--rev1",type=Path,required=True)
    p.add_argument("--debug",type=Path,required=True)
    a=p.parse_args()
    r0=a.rev0.read_bytes(); r1=a.rev1.read_bytes(); dbg=a.debug.read_bytes()
    x0=r0[RETAIL[0]:RETAIL[1]]; x1=r1[RETAIL[0]:RETAIL[1]]; xd=dbg[DEBUG[0]:DEBUG[1]]
    assert len(x0)==len(x1)==len(xd)==0x2F6C
    assert x0==x1
    assert sha256(x0)==RETAIL_SHA256 and sha256(x1)==RETAIL_SHA256
    assert sha256(xd)==DEBUG_SHA256
    assert DEBUG[0]-RETAIL[0]==0x726C and DEBUG[1]-RETAIL[1]==0x726C
    assert x0[:32]==ENTRY and xd[:32]==ENTRY
    assert sha256(r0[TAIL_RETAIL[0]:TAIL_RETAIL[1]])==TAIL_RETAIL_SHA256
    assert sha256(dbg[TAIL_DEBUG[0]:TAIL_DEBUG[1]])==TAIL_DEBUG_SHA256
    check_reset(r0,RETAIL[1],0x03004B30,0x0807B011)
    check_reset(r1,RETAIL[1],0x03004B30,0x0807B011)
    check_reset(dbg,DEBUG[1],0x03004C10,0x08082285)
    print("German rom_8077ABC verification passed")
    print("Retail Rev0/Rev1: 0x08077E7C..0x0807ADE8, 0x2F6C bytes")
    print("Debug:            0x0807F0E8..0x08082054, 0x2F6C bytes")
    print("Accumulated Retail->Debug delta remains +0x726C")
    print("Next: task / ResetTasks")

if __name__=="__main__":
    main()
