#!/usr/bin/env python3
import argparse
import hashlib
import json
from pathlib import Path

TARGETS = {
    "retail": {
        "sha1": "424740be1fc67a5ddb954794443646e6aeee2c1b",
        "base": 0x08000000,
        "strings": [["welcome",136133791,134,"805d3360b9fc99182402fba64c98e653c2bea093026b89379ca05765713e3732"],["this_is_pokemon",136133925,30,"d046998cb15c3187068869ef8be123541d4614dc4c5250a3026be13566051673"],["world_inhabited_by_pokemon",136133955,472,"8507a17c7a10d993439c3edb635eb948ebb2324bbfffb469d6594fc38a667454"],["and_you_are",136134427,17,"de572bc601eab5bf2d6df9d059fcb9cf4fdad7031d461726cd343cc66d10b4bb"],["boy_or_girl",136134444,45,"808c1b2684bcee3ec6638c126a218d97d930699281a336f2a030d5cce54a74b6"],["whats_your_name",136134489,24,"b2892f13f043a5977a555dc71d203c170053f6c8d9fe5e16f0a1b5493eeec471"],["so_its_player",136134513,23,"6f0b0f8e6d52e4e8c85225ba2ce54d01a870516632cd7f358ceec93716299ffc"],["ah_okay_player",136134536,103,"a6ca7d95c122b2ffb7b168b01b9a244c6ced4b6d5dbf4eb4e61cbf9ede06d352"],["are_you_ready",136134639,221,"4d1eb62afbf05383e52fdeb2d09c0c30fc52cb81e60d83ec94b296e7a4fd4a18"]]
    },
    "debug": {
        "sha1": "ca5e3d415c4b47353a73a616878ba833f3648b7a",
        "base": 0x08000000,
        "strings": [["welcome",136235507,134,"805d3360b9fc99182402fba64c98e653c2bea093026b89379ca05765713e3732"],["this_is_pokemon",136235641,30,"d046998cb15c3187068869ef8be123541d4614dc4c5250a3026be13566051673"],["world_inhabited_by_pokemon",136235671,472,"8507a17c7a10d993439c3edb635eb948ebb2324bbfffb469d6594fc38a667454"],["and_you_are",136236143,17,"de572bc601eab5bf2d6df9d059fcb9cf4fdad7031d461726cd343cc66d10b4bb"],["boy_or_girl",136236160,45,"808c1b2684bcee3ec6638c126a218d97d930699281a336f2a030d5cce54a74b6"],["whats_your_name",136236205,24,"b2892f13f043a5977a555dc71d203c170053f6c8d9fe5e16f0a1b5493eeec471"],["so_its_player",136236229,23,"6f0b0f8e6d52e4e8c85225ba2ce54d01a870516632cd7f358ceec93716299ffc"],["ah_okay_player",136236252,103,"a6ca7d95c122b2ffb7b168b01b9a244c6ced4b6d5dbf4eb4e61cbf9ede06d352"],["are_you_ready",136236355,221,"4d1eb62afbf05383e52fdeb2d09c0c30fc52cb81e60d83ec94b296e7a4fd4a18"]]
    },
}

MAP = {
    0x00: " ", 0x15: "ß", 0x1B: "é",
    0x2D: "&", 0x2E: "+", 0x35: "=", 0x36: ";",
    0x5B: "%", 0x5C: "(", 0x5D: ")",
    0xAB: "!", 0xAC: "?", 0xAD: ".", 0xAE: "-", 0xB0: "…",
    0xB1: "“", 0xB2: "”", 0xB3: "‘", 0xB4: "'", 0xB8: ",", 0xBA: "/",
    0xF0: ":", 0xF1: "Ä", 0xF2: "Ö", 0xF3: "Ü", 0xF4: "ä", 0xF5: "ö", 0xF6: "ü",
}
for i, ch in enumerate("0123456789", 0xA1):
    MAP[i] = ch
for i, ch in enumerate("ABCDEFGHIJKLMNOPQRSTUVWXYZ", 0xBB):
    MAP[i] = ch
for i, ch in enumerate("abcdefghijklmnopqrstuvwxyz", 0xD5):
    MAP[i] = ch

def sha1(data):
    return hashlib.sha1(data).hexdigest()

def sha256(data):
    return hashlib.sha256(data).hexdigest()

def decode(raw):
    out = []
    i = 0
    while i < len(raw):
        b = raw[i]
        if b == 0xFF:
            break
        if b == 0xFE:
            out.append("\n")
        elif b == 0xFB:
            out.append("{PARA}")
        elif b == 0xFA:
            out.append("{PAUSE}")
        elif b == 0xFD and i + 1 < len(raw):
            out.append("{VAR:%02X}" % raw[i + 1])
            i += 1
        else:
            out.append(MAP.get(b, "<%02X>" % b))
        i += 1
    return "".join(out)

def main():
    p = argparse.ArgumentParser()
    p.add_argument("rom", type=Path)
    p.add_argument("--profile", choices=TARGETS, required=True)
    args = p.parse_args()

    data = args.rom.read_bytes()
    target = TARGETS[args.profile]
    if sha1(data) != target["sha1"]:
        raise SystemExit("ROM SHA-1 does not match selected profile")

    result = []
    for name, address, length, expected_hash in target["strings"]:
        offset = address - target["base"]
        raw = data[offset:offset + length]
        actual = sha256(raw)
        if actual != expected_hash:
            raise SystemExit(f"{name}: SHA-256 mismatch")
        result.append({
            "id": name,
            "address": f"0x{address:08X}",
            "encoded_length": length,
            "sha256": actual,
            "text": decode(raw),
        })

    print(json.dumps(result, ensure_ascii=False, indent=2))

if __name__ == "__main__":
    main()
