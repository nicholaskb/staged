#!/usr/bin/env python3
from __future__ import annotations

import argparse
from pathlib import Path
from typing import List, Set, Optional

# Source files in root, generated instances in output/current/
DEFAULT_FILES = [
    "/Users/nicholasbaro/Python/staged/cmc_stagegate_base.ttl",
    "/Users/nicholasbaro/Python/staged/output/current/cmc_stagegate_instances.ttl",
    "/Users/nicholasbaro/Python/staged/output/current/cmc_stagegate_sme_instances.ttl",
    "/Users/nicholasbaro/Python/staged/cmc_stagegate_gist_align.ttl",
]
# Combined output goes to output/current/
DEFAULT_OUTPUT = "/Users/nicholasbaro/Python/staged/output/current/cmc_stagegate_all.ttl"


def parse_args(argv: Optional[List[str]] = None) -> argparse.Namespace:
    p = argparse.ArgumentParser(description="Combine TTL files, de-duplicating @prefix lines.")
    p.add_argument("--files", nargs="+", default=DEFAULT_FILES, help="TTL files in order")
    p.add_argument("--out", default=DEFAULT_OUTPUT, help="Output TTL path")
    return p.parse_args(argv)


def is_prefix_line(line: str) -> bool:
    s = line.lstrip()
    return s.startswith("@prefix ")


def main(argv: Optional[List[str]] = None) -> int:
    args = parse_args(argv)

    seen_prefixes: Set[str] = set()
    out_lines: List[str] = []

    for fp in args.files:
        path = Path(fp)
        if not path.exists():
            print(f"Skip missing: {path}")
            continue
        with path.open("r", encoding="utf-8") as f:
            for line in f:
                if is_prefix_line(line):
                    key = line.strip()
                    if key in seen_prefixes:
                        continue
                    seen_prefixes.add(key)
                    out_lines.append(line)
                else:
                    out_lines.append(line)
        # ensure a newline separation between files
        if out_lines and out_lines[-1].strip() != "":
            out_lines.append("\n")

    out_path = Path(args.out)
    out_path.write_text("".join(out_lines), encoding="utf-8")
    print(f"Wrote combined TTL: {out_path} ({len(out_lines)} lines)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

