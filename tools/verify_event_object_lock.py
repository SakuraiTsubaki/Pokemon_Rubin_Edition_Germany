#!/usr/bin/env python3
import argparse
import hashlib
from pathlib import Path

RETAIL = (0x65000, 0x65234)
DEBUG = (0x69600, 0x69834)
RETAIL_SHA256 = "b82387f905398a3c212afd964dab927367abaaacf016cafc8d5b0a8d5fe00a2d"
DEBUG_SHA256 = "f43b11ba73cfa31e0990719d4f824bd5220881e86bb9dbec3c4c1cb55f96dfc0"

ENTRY_PREFIX = bytes.fromhex("00 b5 03 48 c0 78 01 28 04 d0 01 20 03 e0")
ENTRY_SUFFIX = bytes.fromhex("00 20 02 bc 08 47")
NEXT_PREFIX = bytes.fromhex("00 04 00 0c 02 49 08 80 09 30 00 04 00 0c 70 47")
NEXT_BASE_TILE_ADDR = (0x030005AC).to_bytes(4, "little")

RETAIL_GLOBALS = {
    "player": 0x0202E858,
    "objects": 0x030048B0,
    "selected": 0x03004AF0,
    "facing": 0x0202E8E0,
}
DEBUG_GLOBALS = {
    "player": 0x0202EAFC,
    "objects": 0x03004980,
    "selected": 0x03004BC4,
    "facing": 0x0202EB84,
}

def sha256(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()

def verify_entry(data: bytes, start: int, globals_: dict) -> None:
    func = data[start:start + 0x1C]
    assert func[:14] == ENTRY_PREFIX
    assert func[16:20] == globals_["player"].to_bytes(4, "little")
    assert func[20:26] == ENTRY_SUFFIX

def verify_global_refs(chunk: bytes, globals_: dict) -> None:
    assert chunk.count(globals_["objects"].to_bytes(4, "little")) == 6
    assert chunk.count(globals_["selected"].to_bytes(4, "little")) == 5
    assert chunk.count(globals_["facing"].to_bytes(4, "little")) == 1

def main() -> None:
    p = argparse.ArgumentParser(description="Verify German Pokemon Ruby event_object_lock module")
    p.add_argument("--rev0", type=Path, required=True)
    p.add_argument("--rev1", type=Path, required=True)
    p.add_argument("--debug", type=Path, required=True)
    a = p.parse_args()

    rev0 = a.rev0.read_bytes()
    rev1 = a.rev1.read_bytes()
    debug = a.debug.read_bytes()

    r0 = rev0[RETAIL[0]:RETAIL[1]]
    r1 = rev1[RETAIL[0]:RETAIL[1]]
    dbg = debug[DEBUG[0]:DEBUG[1]]

    assert len(r0) == len(r1) == len(dbg) == 0x234
    assert r0 == r1
    assert sha256(r0) == RETAIL_SHA256
    assert sha256(r1) == RETAIL_SHA256
    assert sha256(dbg) == DEBUG_SHA256

    assert DEBUG[0] - RETAIL[0] == 0x4600
    assert DEBUG[1] - RETAIL[1] == 0x4600

    verify_entry(rev0, RETAIL[0], RETAIL_GLOBALS)
    verify_entry(rev1, RETAIL[0], RETAIL_GLOBALS)
    verify_entry(debug, DEBUG[0], DEBUG_GLOBALS)

    verify_global_refs(r0, RETAIL_GLOBALS)
    verify_global_refs(dbg, DEBUG_GLOBALS)

    assert rev0[RETAIL[1]:RETAIL[1] + 16] == NEXT_PREFIX
    assert rev1[RETAIL[1]:RETAIL[1] + 16] == NEXT_PREFIX
    assert debug[DEBUG[1]:DEBUG[1] + 16] == NEXT_PREFIX
    assert rev0[RETAIL[1] + 16:RETAIL[1] + 20] == NEXT_BASE_TILE_ADDR
    assert debug[DEBUG[1] + 16:DEBUG[1] + 20] == NEXT_BASE_TILE_ADDR

    print("German event_object_lock verification passed")
    print("Retail Rev0/Rev1: 0x08065000..0x08065234, 0x234 bytes")
    print("Debug:            0x08069600..0x08069834, 0x234 bytes")
    print("Accumulated Retail->Debug delta remains +0x4600")
    print("Next: text_window / TextWindow_SetBaseTileNum")

if __name__ == "__main__":
    main()
