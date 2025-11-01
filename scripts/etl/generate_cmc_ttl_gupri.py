#!/usr/bin/env python3
"""
Generate CMC stage gate RDF triples from CSV - GUPRI Compliant Version.
Uses Globally Unique, Persistent, Resolvable Identifiers (GUPRIs).
"""

from __future__ import annotations

import csv
import json
import re
import sys
import uuid
from pathlib import Path
from glob import glob
from typing import Dict, Iterable, List, Mapping, Set, Tuple

# Skip pandas import to avoid segfault
pd = None

# CMC Stage-Gate namespace UUID (consistent across all runs)
# Generated once using uuid.uuid4() and hardcoded for persistence
CMC_NAMESPACE_UUID = uuid.UUID('a7c6f3e0-8b5d-4e2a-9f1c-3d7e5a9b2c4e')

# Find files
xlsx_files = glob("/Users/nicholasbaro/Python/staged/data/current_input/*.xlsx")
EXCEL_FILE = Path(xlsx_files[0]) if xlsx_files else Path("/Users/nicholasbaro/Python/staged/data/current_input/input.xlsx")

sgd_files = glob("/Users/nicholasbaro/Python/staged/data/current/*__SGD.csv")
SGD_FILE = Path(sgd_files[0]) if sgd_files else Path("/Users/nicholasbaro/Python/staged/data/current/SGD.csv")

OUTPUT_DIR = Path("/Users/nicholasbaro/Python/staged/output/current")
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
OUTPUT_TTL = OUTPUT_DIR / "cmc_stagegate_instances.ttl"

# ID mapping persistence
ID_MAPPING_FILE = OUTPUT_DIR / "gupri_mappings.json"
ID_MAPPINGS = {}

PREFIXES = (
    "@prefix ex:    <https://w3id.org/cmc-stagegate#> .\n"
    "@prefix xsd:   <http://www.w3.org/2001/XMLSchema#> .\n"
    "@prefix rdfs:  <http://www.w3.org/2000/01/rdf-schema#> .\n"
    "@prefix prov:  <http://www.w3.org/ns/prov#> .\n"
    "@prefix owl:   <http://www.w3.org/2002/07/owl#> .\n"
)

OFFICIAL_COLS = {
    "Value Stream": ["Value Stream", "Drop Down"],
    "Stage Gate": ["Stage Gate", "Drop Down.1"],
    "Stage Gate Description": ["Stage Gate Description", "Drop Down.2"],
    "Functional Area/Subteam": ["Functional Area/Subteam", "Drop Down.3"],
    "Category": ["Category", "Unnamed: 4"],
    "Deliverable": ["Deliverable", "Unnamed: 5"],
    "Explanation/Translation": ["Explanation/Translation", "Explanation/\nTranslation", "Unnamed: 6"],
    "Owner": ["Owner", "Unnamed: 7"],
    "Status": ["Status", "Drop Down.4"],
    "To be presented at": ["To be presented at", "Drop Down.5"],
    "Plan date": ["Plan date", "Plan \ndate", "251031 - added column from Synthetics"],
    "Actual date": ["Actual date", "Actual\ndate", "251031 - added column from Synthetics .1"],
    "Comments/Document reference": ["Comments/Document reference", "Comments/\nDocument reference", "251031 - added column from Synthetics .2"],
}


def load_id_mappings():
    """Load existing ID mappings for persistence across runs."""
    global ID_MAPPINGS
    if ID_MAPPING_FILE.exists():
        try:
            with open(ID_MAPPING_FILE) as f:
                ID_MAPPINGS = json.load(f)
        except json.JSONDecodeError:
            print(f"Warning: Could not load {ID_MAPPING_FILE}, starting fresh")
            ID_MAPPINGS = {}


def save_id_mappings():
    """Save ID mappings for persistence."""
    with open(ID_MAPPING_FILE, 'w') as f:
        json.dump(ID_MAPPINGS, f, indent=2, sort_keys=True)


def create_gupri(entity_type: str, *key_components, readable_hint: str = None) -> str:
    """
    Create a GUPRI (Globally Unique, Persistent, Resolvable Identifier).
    
    Args:
        entity_type: Type of entity (Stage, QualityAttribute, SME, etc.)
        key_components: Components that uniquely identify this entity
        readable_hint: Optional human-readable hint to include
    
    Returns:
        GUPRI in format ex:EntityType_[readable]_UUID
    """
    # Create deterministic key from components
    cache_key = f"{entity_type}:{':'.join(str(k) for k in key_components if k)}"
    
    # Return existing mapping if available
    if cache_key in ID_MAPPINGS:
        return ID_MAPPINGS[cache_key]
    
    # Generate deterministic UUID from namespace + seed
    entity_uuid = uuid.uuid5(CMC_NAMESPACE_UUID, cache_key)
    
    # Create GUPRI with optional readable component
    if readable_hint:
        # Clean readable hint (limit length, safe chars)
        clean_hint = re.sub(r'[^a-zA-Z0-9]+', '_', readable_hint)[:20].strip('_')
        gupri = f"ex:{entity_type}_{clean_hint}_{str(entity_uuid)[:8]}"
    else:
        gupri = f"ex:{entity_type}_{str(entity_uuid)[:8]}"
    
    # Cache for consistency
    ID_MAPPINGS[cache_key] = gupri
    
    return gupri


def create_legacy_alias(entity_type: str, legacy_id: str) -> str:
    """Create a legacy-style ID for backwards compatibility."""
    return f"ex:{entity_type}-{legacy_id}"


def safe_id(text: str) -> str:
    """Create safe ID component (for legacy compatibility)."""
    text = text.strip().lower()
    text = re.sub(r"[^a-z0-9]+", "-", text)
    text = text.strip("-")
    return text or "unnamed"


def escape_turtle_literal(value: str) -> str:
    """Escape special characters for Turtle format."""
    # Handle None
    if value is None:
        return '""'
    
    # Convert to string and handle multiline
    value = str(value)
    
    # Use triple quotes for multiline strings
    if '\n' in value or '\r' in value:
        # For triple-quoted strings, only escape backslash and triple quotes
        value = value.replace('\\', '\\\\')
        value = value.replace('"""', '\\"\\"\\"')
        return f'"""{value}"""'
    else:
        # For single-line strings, escape backslash, quotes, and control chars
        value = value.replace('\\', '\\\\')
        value = value.replace('"', '\\"')
        value = value.replace('\t', '\\t')
        value = value.replace('\r', '\\r')
        return f'"{value}"'


def get_value(row: dict, col_name: str) -> str:
    """Get value from row using official column mappings."""
    if col_name in OFFICIAL_COLS:
        for possible_name in OFFICIAL_COLS[col_name]:
            if possible_name in row:
                val = row[possible_name]
                if val and val != "":
                    return str(val).strip()
    return ""


def emit_stage_blocks_gupri(rows: Iterable[Dict[str, str]]) -> Tuple[str, int]:
    """Emit stage blocks with GUPRIs."""
    ttl_lines = []
    seen_stages: Dict[str, bool] = {}
    count = 0

    for row in rows:
        value_stream = get_value(row, "Value Stream")
        stage_num = get_value(row, "Stage Gate")
        stage_desc = get_value(row, "Stage Gate Description")
        
        if value_stream == "Value Stream" and stage_num == "Stage Gate":
            continue
        if not stage_num:
            continue
            
        # Create unique key for this stage
        stage_key = f"{value_stream}:{stage_num}"
        if stage_key in seen_stages:
            continue
        seen_stages[stage_key] = True
        count += 1

        # Generate GUPRIs for all related entities
        readable_hint = f"{safe_id(value_stream)}_{safe_id(stage_num)}"
        stage_gupri = create_gupri("Stage", value_stream, stage_num, readable_hint=readable_hint)
        plan_gupri = create_gupri("StagePlan", value_stream, stage_num)
        gate_gupri = create_gupri("StageGate", value_stream, stage_num)
        spec_gupri = create_gupri("Specification", value_stream, stage_num)
        
        # Create legacy IDs for backwards compatibility
        stream_id = safe_id(value_stream or "generic")
        stage_id = safe_id(stage_num)
        legacy_stage = create_legacy_alias("Stage", f"{stream_id}-{stage_id}")

        label = stage_desc or f"Stage {stage_num}"

        # Emit triples with GUPRI as primary ID
        # Clean label for comment (single line)
        comment_label = label.replace('\n', ' / ').replace('\r', ' ')
        ttl_lines.append(f"\n# Stage: {comment_label}\n")
        ttl_lines.append(f"{stage_gupri} a ex:Stage ;\n")
        ttl_lines.append(f"    rdfs:label {escape_turtle_literal(label)} ;\n")
        ttl_lines.append(f"    ex:hasPlan {plan_gupri} ;\n")
        ttl_lines.append(f"    ex:hasGate {gate_gupri} ;\n")
        ttl_lines.append(f"    ex:hasSpecification {spec_gupri} ;\n")
        ttl_lines.append(f"    owl:sameAs {legacy_stage} .\n")
        
        # Add legacy ID triple for compatibility
        ttl_lines.append(f"{legacy_stage} owl:sameAs {stage_gupri} .\n")
        
        # Plan
        ttl_lines.append(f"{plan_gupri} a ex:StagePlan ;\n")
        ttl_lines.append(f"    rdfs:label {escape_turtle_literal(f'Plan for {label}')} .\n")
        
        # Gate
        ttl_lines.append(f"{gate_gupri} a ex:StageGate ;\n")
        ttl_lines.append(f"    rdfs:label {escape_turtle_literal(f'Gate for {label}')} .\n")

    return ("".join(ttl_lines), count)


def emit_deliverable_blocks_gupri(rows: Iterable[Dict[str, str]]) -> Tuple[str, int]:
    """Emit deliverable blocks with GUPRIs."""
    ttl_lines = []
    count = 0
    declared_specs: Set[str] = set()

    for row in rows:
        value_stream = get_value(row, "Value Stream")
        stage_num = get_value(row, "Stage Gate")
        deliverable = get_value(row, "Deliverable")
        
        if not stage_num or not value_stream:
            continue
            
        # Emit specification once per stage
        spec_gupri = create_gupri("Specification", value_stream, stage_num)
        spec_key = f"{value_stream}:{stage_num}"
        
        if spec_key not in declared_specs:
            declared_specs.add(spec_key)
            stage_desc = get_value(row, "Stage Gate Description") or f"Stage {stage_num}"
            ttl_lines.append(f"{spec_gupri} a ex:Specification ;\n")
            ttl_lines.append(f"    rdfs:label {escape_turtle_literal(f'Specification for {stage_desc}')} .\n")
            count += 1

        if not deliverable:
            continue

        # Get additional fields
        explanation = get_value(row, "Explanation/Translation")
        owner_raw = get_value(row, "Owner")
        category = get_value(row, "Category")
        plan_date = get_value(row, "Plan date")
        actual_date = get_value(row, "Actual date")
        comments = get_value(row, "Comments/Document reference")

        # Generate GUPRI for deliverable
        readable_hint = safe_id(deliverable)[:30]
        qa_gupri = create_gupri("QualityAttribute", value_stream, stage_num, deliverable, 
                               readable_hint=readable_hint)
        
        # Legacy ID for compatibility
        stream_id = safe_id(value_stream or "generic")
        stage_id = safe_id(stage_num)
        deliv_id = safe_id(deliverable)[:64]
        legacy_qa = create_legacy_alias("CQA", f"{stream_id}-{stage_id}-{deliv_id}")

        # Build triple
        # Clean deliverable for comment (single line)
        comment_deliv = deliverable.replace('\n', ' / ').replace('\r', ' ')
        ttl_lines.append(f"\n# Deliverable: {comment_deliv[:50]}{'...' if len(comment_deliv) > 50 else ''}\n")
        ttl_lines.append(f"{qa_gupri} a ex:QualityAttribute ;\n")
        ttl_lines.append(f"    rdfs:label {escape_turtle_literal(deliverable)} ;\n")
        
        if explanation:
            ttl_lines.append(f"    rdfs:comment {escape_turtle_literal(explanation)} ;\n")
        if category:
            ttl_lines.append(f"    ex:hasCategory {escape_turtle_literal(category)} ;\n")
        if plan_date:
            ttl_lines.append(f"    ex:plannedDate {escape_turtle_literal(plan_date)} ;\n")
        if actual_date:
            ttl_lines.append(f"    ex:actualDate {escape_turtle_literal(actual_date)} ;\n")
        if comments:
            ttl_lines.append(f"    ex:reference {escape_turtle_literal(comments)} ;\n")
        
        # Add legacy alias
        ttl_lines.append(f"    owl:sameAs {legacy_qa} .\n")
        ttl_lines.append(f"{legacy_qa} owl:sameAs {qa_gupri} .\n")
        
        count += 1

    return ("".join(ttl_lines), count)


def main():
    """Main entry point."""
    print(f"GUPRI-Compliant CMC Stage Gate TTL Generator")
    print(f"=" * 50)
    
    # Load existing ID mappings
    load_id_mappings()
    print(f"Loaded {len(ID_MAPPINGS)} existing ID mappings")
    
    print(f"Input CSV: {SGD_FILE.name if SGD_FILE.exists() else 'Not found'}")
    print(f"Output: {OUTPUT_TTL}")
    print()
    
    # Read CSV
    if not SGD_FILE.exists():
        print(f"Error: {SGD_FILE} not found")
        return 1
        
    with open(SGD_FILE, encoding="utf-8") as f:
        rows = list(csv.DictReader(f))
    
    # Map columns
    print(f"Using headers: {list(OFFICIAL_COLS.keys())}")
    
    # Generate stage blocks
    stage_ttl, stage_count = emit_stage_blocks_gupri(rows)
    
    # Generate deliverables
    deliv_ttl, qa_count = emit_deliverable_blocks_gupri(rows)
    
    # Combine and write
    final_ttl = PREFIXES + "\n" + stage_ttl + "\n" + deliv_ttl
    
    with open(OUTPUT_TTL, "w", encoding="utf-8") as f:
        f.write(final_ttl)
    
    # Save ID mappings
    save_id_mappings()
    print(f"Saved {len(ID_MAPPINGS)} ID mappings to {ID_MAPPING_FILE.name}")
    
    print(f"Wrote TTL: {OUTPUT_TTL} (stages={stage_count}, deliverables={qa_count})")
    print(f"Total GUPRIs created: {len(ID_MAPPINGS)}")
    
    return 0


if __name__ == "__main__":
    sys.exit(main())
