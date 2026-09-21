#!/usr/bin/env python3
import argparse
import hashlib
import struct
from pathlib import Path

REV0_SHA1 = "1c2a53332382e14dab8815e3a6dd81ad89534050"
REV1_SHA1 = "424740be1fc67a5ddb954794443646e6aeee2c1b"

MONTHS = [31, 28, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31]

def sha1(data):
    return hashlib.sha1(data).hexdigest()

def u16(data, off):
    return struct.unpack_from("<H", data, off)[0]

def u32(data, off):
    return struct.unpack_from("<I", data, off)[0]

def main():
    p = argparse.ArgumentParser()
    p.add_argument("--rev0", required=True, type=Path)
    p.add_argument("--rev1", required=True, type=Path)
    args = p.parse_args()

    r0 = args.rev0.read_bytes()
    r1 = args.rev1.read_bytes()

    assert sha1(r0) == REV0_SHA1, "Rev 0 SHA-1 mismatch"
    assert sha1(r1) == REV1_SHA1, "Rev 1 SHA-1 mismatch"

    diffs = [i for i in range(0x92B0, 0x9610) if r0[i] != r1[i]]
    assert diffs == [0x9367, 0x938B], diffs

    assert u16(r0, 0x9366) == 0xDD11
    assert u16(r1, 0x9366) == 0xDB11
    assert u16(r0, 0x938A) == 0xDCED
    assert u16(r1, 0x938A) == 0xDAED

    assert u32(r1, 0x92D0) == 0x0300046E
    assert u32(r1, 0x92D4) == 0x04000208
    assert r1[0x1F458C:0x1F4596] == bytes([0,1,1,0,0,0,0,0,0,0])

    months = [u32(r1, 0x1F4598 + i * 4) for i in range(12)]
    assert months == MONTHS, months

    assert all(r0[i] == r1[i] for i in range(0x9608, 0x988A))
    assert u32(r1, 0x968C) == 0x03000460
    assert u32(r1, 0x97A0) == 0x03000460
    assert u32(r1, 0x97A4) == 0x03004048
    assert u32(r1, 0x97A8) == 0x02023C4F
    assert u32(r1, 0x97E4) == 0x03004048
    assert u32(r1, 0x97E8) == 0x03000460
    assert u32(r1, 0x97EC) == 0x02023C4F
    assert u32(r1, 0x988C) == 0x03000460

    print("RTC baseline verification passed")
    print("Rev 0:", REV0_SHA1)
    print("Rev 1:", REV1_SHA1)
    print("Retail RTC delta offsets:", ", ".join(hex(x) for x in diffs))

if __name__ == "__main__":
    main()
