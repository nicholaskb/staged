#!/usr/bin/env python3
"""
Generate TTL instances from the CMC Stage Gate spreadsheet.

Input:  /Users/nicholasbaro/Python/staged/data/Protein and CGT_SGD Template Final_ENDORSED JAN 2023.xlsx
Output: /Users/nicholasbaro/Python/staged/cmc_stagegate_instances.ttl

Approach (phase 1 - minimal):
- Read the extracted SGD sheet CSV as canonical source.
- Map columns: Value Stream, Stage Gate, Stage Gate Description, Functional Area/Subteam, Deliverable
- Create resources:
  - ex:Stage for each numeric Stage Gate with label and stream
  - ex:StageGate activity per stage (e.g., ex:Gate-<stream>-<stage>)
  - ex:StagePlan for each stage
  - ex:Specification per stage; CQAs linked to that Specification via ex:hasCQA
- Write TTL with safe IRIs.

External vocabularies are defined in cmc_stagegate_base.ttl.
"""

from __future__ import annotations

import csv
import re
from pathlib import Path
from typing import Dict, Iterable, Tuple, List, Set, Mapping

BASE_DIR = Path("/Users/nicholasbaro/Python/staged")
DATA_DIR = BASE_DIR / "data"
# New folder structure: current extraction in 'current' folder
EXTRACTED_DIR = DATA_DIR / "current"
INPUT_DIR = DATA_DIR / "current_input"
# Look for any Excel file in current_input folder
EXCEL_FILES = list(INPUT_DIR.glob("*.xlsx")) if INPUT_DIR.exists() else []
EXCEL_FILE = EXCEL_FILES[0] if EXCEL_FILES else INPUT_DIR / "input.xlsx"
# Look for SGD.csv file in current folder (name may vary)
# More specific pattern: files ending with __SGD.csv
SGD_FILES = list(EXTRACTED_DIR.glob("*__SGD.csv")) if EXTRACTED_DIR.exists() else []
SGD_FILE = SGD_FILES[0] if SGD_FILES else EXTRACTED_DIR / "SGD.csv"
# Output goes to output/current/ directory
OUTPUT_DIR = BASE_DIR / "output" / "current"
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
OUTPUT_TTL = OUTPUT_DIR / "cmc_stagegate_instances.ttl"

PREFIXES = (
    "@prefix ex:    <https://w3id.org/cmc-stagegate#> .\n"
    "@prefix xsd:   <http://www.w3.org/2001/XMLSchema#> .\n"
    "@prefix rdfs:  <http://www.w3.org/2000/01/rdf-schema#> .\n"
    "@prefix prov:  <http://www.w3.org/ns/prov#> .\n"
)


OFFICIAL_COLS = {
    "Value Stream": ["Value Stream", "Drop Down"],
    "Stage Gate": ["Stage Gate", "Drop Down.1"],
    "Stage Gate Description": ["Stage Gate Description", "Drop Down.2"],
    "Functional Area/Subteam": ["Functional Area/Subteam", "Drop Down.3"],
    "Category": ["Category", "Unnamed: 4"],
    "Deliverable": ["Deliverable", "Unnamed: 5"],
    # Include newline variant from sheet
    "Explanation/Translation": ["Explanation/Translation", "Explanation/\nTranslation", "Unnamed: 6"],
    "Owner": ["Owner", "Unnamed: 7"],
    "Status": ["Status", "Drop Down.4"],
    "To be presented at": ["To be presented at", "Drop Down.5"],
    # New columns added 251031
    "Plan date": ["Plan date", "Plan \ndate", "251031 - added column from Synthetics"],
    "Actual date": ["Actual date", "Actual\ndate", "251031 - added column from Synthetics .1"],
    "Comments/Document reference": ["Comments/Document reference", "Comments/\nDocument reference", "251031 - added column from Synthetics .2"],
}


def safe_id(text: str) -> str:
    text = text.strip().lower()
    text = re.sub(r"[^a-z0-9]+", "-", text)
    text = text.strip("-")
    return text or "unnamed"


def escape_turtle_literal(value: str) -> str:
    # Escape backslash, quotes, and control characters not allowed raw in TTL literals
    value = value.replace('\\', '\\\\').replace('"', '\\"')
    value = value.replace('\r', '\\n').replace('\n', '\\n').replace('\t', '\\t')
    return value


def read_csv_second_row_headers(path: Path) -> Tuple[List[str], Iterable[Dict[str, str]]]:
    with path.open("r", encoding="utf-8") as f:
        reader = csv.reader(f)
        rows = list(reader)
    if len(rows) < 2:
        return [], []
    headers = [h.strip() for h in rows[1]]
    normalized_rows: List[Dict[str, str]] = []
    for r in rows[2:]:
        row_vals = (r + [""] * len(headers))[: len(headers)]
        normalized_rows.append({h: (v or "").strip() for h, v in zip(headers, row_vals)})
    return headers, normalized_rows


def get_value(row: Dict[str, str], logical_name: str) -> str:
    for name in OFFICIAL_COLS.get(logical_name, []):
        if name in row:
            return row.get(name, "")
    return ""


def build_stage_info(rows: Iterable[Dict[str, str]]) -> Mapping[Tuple[str, str], str]:
    info: Dict[Tuple[str, str], str] = {}
    for row in rows:
        stream = get_value(row, "Value Stream")
        stage = get_value(row, "Stage Gate")
        desc = get_value(row, "Stage Gate Description")
        if not stream or not stage:
            continue
        key = (safe_id(stream), safe_id(stage))
        if key not in info and desc:
            info[key] = desc
    return info


def emit_stage_blocks(rows: Iterable[Dict[str, str]]) -> Tuple[str, int]:
    ttl_lines = []
    seen_stages: Dict[Tuple[str, str], bool] = {}
    count = 0

    for row in rows:
        value_stream = get_value(row, "Value Stream")
        stage_num = get_value(row, "Stage Gate")
        stage_desc = get_value(row, "Stage Gate Description")
        if value_stream == "Value Stream" and stage_num == "Stage Gate":
            continue
        if not stage_num:
            continue
        key = (value_stream, stage_num)
        if key in seen_stages:
            continue
        seen_stages[key] = True
        count += 1

        stream_id = safe_id(value_stream or "generic")
        stage_id = safe_id(stage_num)

        stage_iri = f"ex:Stage-{stream_id}-{stage_id}"
        plan_iri = f"ex:Plan-{stream_id}-{stage_id}"
        gate_iri = f"ex:Gate-{stream_id}-{stage_id}"
        spec_iri = f"ex:Spec-{stream_id}-{stage_id}"

        label = stage_desc or f"Stage {stage_num}"

        ttl_lines.append(f"{stage_iri} a ex:Stage ; rdfs:label \"{escape_turtle_literal(label)}\" ; ex:hasPlan {plan_iri} ; ex:hasGate {gate_iri} .\n")
        ttl_lines.append(f"{stage_iri} ex:hasSpecification {spec_iri} .\n")
        ttl_lines.append(f"{plan_iri} a ex:StagePlan ; rdfs:label \"Plan for {escape_turtle_literal(label)}\" .\n")
        ttl_lines.append(f"{gate_iri} a ex:StageGate ; rdfs:label \"Gate for {escape_turtle_literal(label)}\" .\n")

    return ("".join(ttl_lines), count)


def emit_specs_and_deliverables(rows: Iterable[Dict[str, str]], stage_info: Mapping[Tuple[str, str], str]) -> Tuple[str, int]:
    ttl_lines = []
    count = 0
    declared_agents: Set[str] = set()
    declared_specs: Set[str] = set()

    for row in rows:
        value_stream = get_value(row, "Value Stream")
        stage_num = get_value(row, "Stage Gate")
        deliverable = get_value(row, "Deliverable")
        if not stage_num or not value_stream:
            continue
        # Declare per-stage Specification once
        stream_id = safe_id(value_stream or "generic")
        stage_id = safe_id(stage_num)
        spec_iri = f"ex:Spec-{stream_id}-{stage_id}"
        spec_key = (stream_id, stage_id)
        if spec_iri not in declared_specs:
            declared_specs.add(spec_iri)
            stage_label = stage_info.get(spec_key, f"Stage {stage_num}")
            ttl_lines.append(f"{spec_iri} a ex:Specification ; rdfs:label \"Specification for {escape_turtle_literal(stage_label)}\" .\n")
            count += 1

        if not deliverable:
            continue

        explanation = get_value(row, "Explanation/Translation")
        owner_raw = get_value(row, "Owner")
        category = get_value(row, "Category")
        plan_date = get_value(row, "Plan date")
        actual_date = get_value(row, "Actual date")
        comments = get_value(row, "Comments/Document reference")

        deliv_id = safe_id(deliverable)[:64]
        qa_iri = f"ex:CQA-{stream_id}-{stage_id}-{deliv_id}"

        # Build one QA triple with optional comment and list of agents
        triple_parts: List[str] = [f"{qa_iri} a ex:QualityAttribute", f"rdfs:label \"{escape_turtle_literal(deliverable)}\""]
        if explanation:
            triple_parts.append(f"rdfs:comment \"{escape_turtle_literal(explanation)}\"")
        
        # Add category if present
        if category:
            triple_parts.append(f"ex:hasCategory \"{escape_turtle_literal(category)}\"")
        
        # Add new date and comment properties
        if plan_date:
            triple_parts.append(f"ex:plannedDate \"{escape_turtle_literal(plan_date)}\"")
        if actual_date:
            triple_parts.append(f"ex:actualDate \"{escape_turtle_literal(actual_date)}\"")
        if comments:
            triple_parts.append(f"ex:reference \"{escape_turtle_literal(comments)}\"")

        owner_parts: List[str] = []
        agent_iris: List[str] = []
        if owner_raw:
            owner_parts = [p.strip() for p in owner_raw.split(",") if p.strip()]
            for part in owner_parts:
                agent_id = safe_id(part)
                agent_iri = f"ex:Agent-{agent_id}"
                agent_iris.append(agent_iri)
        if agent_iris:
            triple_parts.append("prov:wasAttributedTo " + ", ".join(agent_iris))

        ttl_lines.append(" ; ".join(triple_parts) + " .\n")
        count += 1

        # Declare any new agents after the QA triple
        for part in owner_parts:
            agent_id = safe_id(part)
            agent_iri = f"ex:Agent-{agent_id}"
            if agent_iri not in declared_agents:
                declared_agents.add(agent_iri)
                ttl_lines.append(f"{agent_iri} a prov:Agent ; rdfs:label \"{escape_turtle_literal(part)}\" .\n")
                count += 1

        # Link CQA to the stage Specification
        ttl_lines.append(f"{spec_iri} ex:hasCQA {qa_iri} .\n")
        count += 1

    return ("".join(ttl_lines), count)


def main() -> int:
    # Show which files we're using
    print(f"Input Excel: {EXCEL_FILE.name if EXCEL_FILE.exists() else 'Not found'}")
    print(f"SGD CSV: {SGD_FILE.name if SGD_FILE.exists() else 'Not found'}")
    print(f"Output: {OUTPUT_TTL}")
    print()
    
    # Optional: show Excel headers if possible
    if EXCEL_FILE.exists():
        try:
            from pandas import read_excel  # type: ignore
            sheets = read_excel(EXCEL_FILE, sheet_name=None, dtype=str, engine="openpyxl")
            print("Excel header preview:")
            for name, df in sheets.items():
                cols = [str(c).strip() for c in df.columns]
                print(f"- Sheet: {name}")
                print("  Columns:")
                for c in cols:
                    print(f"    - {c}")
        except Exception:
            pass

    if not SGD_FILE.exists():
        print(f"Missing source CSV: {SGD_FILE}")
        return 2

    headers, rows = read_csv_second_row_headers(SGD_FILE)
    print(f"Using headers: {headers}")

    # Build stage label info for Specification labels
    rows_list = list(rows)
    stage_info = build_stage_info(rows_list)

    stage_ttl, num_stages = emit_stage_blocks(iter(rows_list))
    specs_qas_ttl, num_specs_qas = emit_specs_and_deliverables(iter(rows_list), stage_info)

    OUTPUT_TTL.write_text(PREFIXES + "\n" + stage_ttl + "\n" + specs_qas_ttl, encoding="utf-8")
    print(f"Wrote TTL: {OUTPUT_TTL} (stages={num_stages}, spec_and_qas_triples={num_specs_qas})")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
