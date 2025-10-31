#!/usr/bin/env python3
from __future__ import annotations

import csv
from collections import Counter
from pathlib import Path
from typing import Dict, List, Tuple

BASE_DIR = Path("/Users/nicholasbaro/Python/staged")
# New folder structure: look for SGD file in current extraction
CURRENT_DIR = BASE_DIR / "data" / "current"
# Find any SGD CSV file in current folder
SGD_FILES = list(CURRENT_DIR.glob("*SGD*.csv")) if CURRENT_DIR.exists() else []
SGD_PATH = SGD_FILES[0] if SGD_FILES else CURRENT_DIR / "SGD.csv"

MAPPING_GUIDE: Dict[str, str] = {
    "Value Stream": "IRI component for ex:Stage/Plan/Gate; product domain (CGT/Protein/SM/Vaccines)",
    "Stage Gate": "Stage number; IRI component for ex:Stage-<stream>-<num>",
    "Stage Gate Description": "Label for ex:Stage; Plan/Gate labels derived; maps to lifecycle name",
    "Functional Area/Subteam": "prov:Agent or ex:FunctionalArea; link stages/deliverables to responsible groups",
    "Category": "skos:Concept or ex:category on deliverable/spec",
    "Deliverable": "ex:QualityAttribute (CQA-like item) label; later linked to ex:Specification",
    "Explanation/Translation": "rdfs:comment on ex:QualityAttribute or ex:Specification",
    "Owner": "prov:Agent; associate via prov:wasAssociatedWith to StageGate or Deliverable",
    "Status": "ex:status literal; or Gate ex:decision when applicable",
    "To be presented at": "ex:presentedAt literal on Deliverable or StageGate",
    "VPAD-specific?": "ex:isVPADSpecific xsd:boolean",
}


def summarize_column(values: List[str]) -> Dict[str, object]:
    total = len(values)
    non_empty_vals = [v for v in values if (v or "").strip() != ""]
    empty = total - len(non_empty_vals)
    unique = len(set(non_empty_vals))
    counts = Counter(non_empty_vals)
    top5 = counts.most_common(5)
    examples = [v for v, _ in top5]

    # comma-separated detection
    with_commas = [v for v in non_empty_vals if "," in v]
    with_commas_count = len(with_commas)
    multi_value_examples = []
    for v in with_commas[:5]:
        parts = [p.strip() for p in v.split(",") if p.strip()]
        if parts:
            multi_value_examples.append(parts[:5])

    return {
        "total_rows": total,
        "non_empty": len(non_empty_vals),
        "empty": empty,
        "unique": unique,
        "top5": top5,
        "examples": examples,
        "with_commas_count": with_commas_count,
        "multi_value_examples": multi_value_examples,
    }


def load_csv_columns_second_row_headers(path: Path) -> Tuple[List[str], Dict[str, List[str]]]:
    with path.open("r", encoding="utf-8") as f:
        reader = csv.reader(f)
        rows = list(reader)
    if not rows:
        return [], {}
    # The second row contains the real headers
    header_row = rows[1]
    headers = [h.strip() for h in header_row]
    data: Dict[str, List[str]] = {h: [] for h in headers}
    # Data starts from the third row
    for r in rows[2:]:
        # Pad/truncate row to header length
        row_vals = (r + [""] * len(headers))[: len(headers)]
        for h, v in zip(headers, row_vals):
            data[h].append((v or "").strip())
    return headers, data


def main() -> int:
    if not SGD_PATH.exists():
        print(f"Missing CSV: {SGD_PATH}")
        print(f"Looking in: {CURRENT_DIR}")
        print("Available CSV files:")
        if CURRENT_DIR.exists():
            for csv_file in CURRENT_DIR.glob("*.csv"):
                print(f"  - {csv_file.name}")
        return 2

    headers, data = load_csv_columns_second_row_headers(SGD_PATH)
    print(f"Analyzing: {SGD_PATH}")
    print(f"Columns ({len(headers)}): {', '.join(headers)}\n")

    for h in headers:
        stats = summarize_column(data[h])
        mapping = MAPPING_GUIDE.get(h, "(no mapping defined yet)")
        print(f"Column: {h}")
        print(f"  - total_rows: {stats['total_rows']}")
        print(f"  - non_empty:  {stats['non_empty']}")
        print(f"  - empty:      {stats['empty']}")
        print(f"  - unique:     {stats['unique']}")
        print(f"  - top5:       {stats['top5']}")
        print(f"  - examples:   {stats['examples']}")
        print(f"  - values_with_commas: {stats['with_commas_count']}")
        if stats['with_commas_count']:
            print(f"  - multi_value_examples: {stats['multi_value_examples']}")
        print(f"  - ontology:   {mapping}\n")

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
