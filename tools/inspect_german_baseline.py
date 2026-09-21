#!/usr/bin/env python3
import argparse
import hashlib
import json
import struct
from pathlib import Path

SAVE_SIGNATURE = 0x08012025
SECTION_DATA_SIZES = [0xF2C, 0xF80, 0xF80, 0xF80, 0xF08] + [0xF80] * 8 + [0x7D0]


def hashes(data):
    return {
        "md5": hashlib.md5(data).hexdigest(),
        "sha1": hashlib.sha1(data).hexdigest(),
        "sha256": hashlib.sha256(data).hexdigest(),
    }


def gba_checksum(data):
    if len(data) < 0xBE:
        return None
    return (-sum(data[0xA0:0xBD]) - 0x19) & 0xFF


def inspect_rom(path, data):
    return {
        "path": str(path),
        "kind": "gba-rom",
        "size": len(data),
        **hashes(data),
        "header": {
            "title": data[0xA0:0xAC].rstrip(b"\0 ").decode("ascii", "replace"),
            "game_code": data[0xAC:0xB0].decode("ascii", "replace"),
            "maker_code": data[0xB0:0xB2].decode("ascii", "replace"),
            "software_version": data[0xBC],
            "header_checksum": data[0xBD],
            "calculated_header_checksum": gba_checksum(data),
            "header_checksum_valid": data[0xBD] == gba_checksum(data),
        },
    }


def save_checksum(data):
    total = 0
    for offset in range(0, len(data), 4):
        chunk = data[offset:offset + 4]
        if len(chunk) < 4:
            chunk += b"\0" * (4 - len(chunk))
        total = (total + int.from_bytes(chunk, "little")) & 0xFFFFFFFF
    return ((total >> 16) + (total & 0xFFFF)) & 0xFFFF


def inspect_save(path, data):
    sectors = []
    indices = {}
    for physical in range(len(data) // 0x1000):
        sector = data[physical * 0x1000:(physical + 1) * 0x1000]
        section_id = struct.unpack_from("<H", sector, 0xFF4)[0]
        stored_checksum = struct.unpack_from("<H", sector, 0xFF6)[0]
        signature = struct.unpack_from("<I", sector, 0xFF8)[0]
        save_index = struct.unpack_from("<I", sector, 0xFFC)[0]
        row = {
            "physical_sector": physical,
            "section_id": section_id,
            "save_index": save_index,
            "signature": f"0x{signature:08X}",
        }
        if signature == SAVE_SIGNATURE and section_id < len(SECTION_DATA_SIZES):
            calculated = save_checksum(sector[:SECTION_DATA_SIZES[section_id]])
            row.update({
                "stored_checksum": f"0x{stored_checksum:04X}",
                "calculated_checksum": f"0x{calculated:04X}",
                "checksum_valid": stored_checksum == calculated,
            })
            indices.setdefault(str(save_index), []).append(section_id)
        sectors.append(row)

    complete = sorted(int(k) for k, v in indices.items() if sorted(v) == list(range(14)))
    return {
        "path": str(path),
        "kind": "gba-save",
        "size": len(data),
        **hashes(data),
        "complete_main_save_indices": complete,
        "main_save_checksums_valid": all(
            s.get("checksum_valid", True) for s in sectors
            if s["signature"] == f"0x{SAVE_SIGNATURE:08X}" and s["section_id"] < 14
        ),
        "sectors": sectors,
    }


def diff_files(a_path, b_path):
    a = a_path.read_bytes()
    b = b_path.read_bytes()
    limit = min(len(a), len(b))
    differences = [
        {"offset": f"0x{i:X}", "a": a[i], "b": b[i]}
        for i in range(limit)
        if a[i] != b[i]
    ]
    return {
        "a": str(a_path),
        "b": str(b_path),
        "size_a": len(a),
        "size_b": len(b),
        "different_byte_count": len(differences) + abs(len(a) - len(b)),
        "differences": differences if len(differences) <= 1024 else differences[:1024],
        "differences_truncated": len(differences) > 1024,
    }


def main():
    parser = argparse.ArgumentParser(
        description="Inspect German Pokemon Ruby ROM/SAV baselines without storing ROM data."
    )
    parser.add_argument("files", nargs="*", type=Path)
    parser.add_argument("--diff", nargs=2, type=Path, metavar=("A", "B"))
    args = parser.parse_args()

    output = {}
    if args.files:
        inspected = []
        for path in args.files:
            data = path.read_bytes()
            if path.suffix.lower() == ".gba":
                inspected.append(inspect_rom(path, data))
            else:
                inspected.append(inspect_save(path, data))
        output["files"] = inspected

    if args.diff:
        output["diff"] = diff_files(*args.diff)

    print(json.dumps(output, indent=2, ensure_ascii=False))


if __name__ == "__main__":
    main()
