#!/usr/bin/env python3
import argparse
import hashlib
from pathlib import Path

REV0_SHA1="1c2a53332382e14dab8815e3a6dd81ad89534050"
REV1_SHA1="424740be1fc67a5ddb954794443646e6aeee2c1b"
DEBUG_SHA1="ca5e3d415c4b47353a73a616878ba833f3648b7a"

RETAIL_START=0xC7EC
RETAIL_END=0xD40C
DEBUG_START=0xCA08
DEBUG_END=0xD628
DELTA=0x21C

RETAIL_SHA256="5debedeab09cd8a8b401345cfd75d15eb97915582661a85624a204ac9eb38935"
DEBUG_SHA256="7d19ce0e6c41d743eaf46cef52af0a66ed0fd98d273c9aeaeafcd4d98b74ff9f"

STARTS=[51180,51216,51256,51320,51384,51416,51452,51484,51516,51548,51580,51612,51644,51676,51708,51780,51996,52284,52524,52568,52600,52660,52712,52772,52804,52860,52912,52996,53056,53088,53160,53264,53336,53408,53452,53508,53552,53596,53628,53660,53692,53724,53756,53788,53832,53876,53908,53940,53972,54044,54076,54108,54144,54188,54220,54252]

def sha1(data):
    return hashlib.sha1(data).hexdigest()

def sha256(data):
    return hashlib.sha256(data).hexdigest()

def main():
    p=argparse.ArgumentParser()
    p.add_argument("--rev0",type=Path,required=True)
    p.add_argument("--rev1",type=Path,required=True)
    p.add_argument("--debug",type=Path,required=True)
    a=p.parse_args()

    r0=a.rev0.read_bytes()
    r1=a.rev1.read_bytes()
    dbg=a.debug.read_bytes()

    assert sha1(r0)==REV0_SHA1
    assert sha1(r1)==REV1_SHA1
    assert sha1(dbg)==DEBUG_SHA1

    assert r0[RETAIL_START:RETAIL_END] == r1[RETAIL_START:RETAIL_END]
    assert sha256(r1[RETAIL_START:RETAIL_END]) == RETAIL_SHA256
    assert sha256(dbg[DEBUG_START:DEBUG_END]) == DEBUG_SHA256

    assert len(STARTS)==56

    for cmd,off in enumerate(STARTS):
        doff=off+DELTA
        # All emitters begin at the same relative byte pattern; literal pools
        # later in each function may differ because Debug globals are relocated.
        assert r1[off:off+2] == dbg[doff:doff+2], (cmd,hex(off),hex(doff))

    # First command writes command ID 0; second command writes 1.
    assert r1[0xC7F6:0xC7FA] == bytes.fromhex("00 23 0b 70")
    assert r1[0xC81C:0xC820] == bytes.fromhex("01 23 0b 70")

    # Transfer buffer literals.
    assert r1[0xC80C:0xC810] == (0x03004050).to_bytes(4,"little")
    assert dbg[0xCA28:0xCA2C] == (0x030040D0).to_bytes(4,"little")

    # End of command 55 / start of next module.
    assert r1[0xD3EC:0xD3EE] == bytes.fromhex("00 b5")
    assert dbg[0xD608:0xD60A] == bytes.fromhex("00 b5")
    assert r1[0xD40C:0xD40E] != bytes.fromhex("00 00")
    assert dbg[0xD628:0xD62A] != bytes.fromhex("00 00")

    print("German battle-controller emitter protocol verification passed")
    print("Commands: 56 (0..55)")
    print("Retail emitter bytes:", RETAIL_END-RETAIL_START)
    print("Debug delta: +0x21C")

if __name__=="__main__":
    main()
