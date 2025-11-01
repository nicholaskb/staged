#!/usr/bin/env python3
"""
Generate RDF/TTL from Lexicon CSV file.
Creates instance data for pharmaceutical/biotechnology terminology.
"""

import csv
import re
import uuid
from pathlib import Path
from typing import Dict, List, Tuple
from datetime import datetime

# Paths
BASE_DIR = Path("/Users/nicholasbaro/Python/staged")
DATA_DIR = BASE_DIR / "data" / "current"
OUTPUT_DIR = BASE_DIR / "output" / "current"

# GUPRI namespace for consistent IDs
LEXICON_NAMESPACE_UUID = uuid.UUID('b8d7e4a1-9c3f-4e2b-8a1d-6f5c3b9e7d2a')

# ID mappings for persistence
LEXICON_ID_MAPPINGS: Dict[str, str] = {}
MAPPINGS_FILE = OUTPUT_DIR / "lexicon_gupri_mappings.json"


def safe_id(text: str) -> str:
    """Create a safe ID from text."""
    # Remove special characters, keep alphanumeric and underscore
    text = re.sub(r'[^a-zA-Z0-9_]', '_', text)
    # Remove multiple underscores
    text = re.sub(r'_+', '_', text)
    # Remove leading/trailing underscores
    text = text.strip('_')
    return text


def generate_lexicon_gupri(abbr: str) -> str:
    """Generate a GUPRI for a lexicon term."""
    unique_key = f"Term:{abbr}"
    
    if unique_key in LEXICON_ID_MAPPINGS:
        return LEXICON_ID_MAPPINGS[unique_key]
    
    # Generate deterministic UUID
    term_uuid = uuid.uuid5(LEXICON_NAMESPACE_UUID, unique_key)
    safe_abbr = safe_id(abbr)
    gupri = f"ex:Term_{safe_abbr}_{str(term_uuid)[:8]}"
    
    LEXICON_ID_MAPPINGS[unique_key] = gupri
    return gupri


def escape_turtle_literal(value: str) -> str:
    """Escape special characters for Turtle format."""
    if value is None:
        return '""'
    
    value = str(value).strip()
    
    # Handle multi-line strings
    if '\n' in value or '\r' in value:
        value = value.replace('\\', '\\\\')
        value = value.replace('"""', '\\"\\"\\"')
        return f'"""{value}"""'
    else:
        value = value.replace('\\', '\\\\')
        value = value.replace('"', '\\"')
        value = value.replace('\t', '\\t')
        value = value.replace('\r', '\\r')
        value = value.replace('\n', '\\n')
        return f'"{value}"'


def categorize_term(abbr: str, definition: str) -> str:
    """Categorize a term based on its abbreviation and definition."""
    abbr_upper = abbr.upper()
    def_lower = definition.lower()
    
    # Regulatory terms
    if any(term in abbr_upper for term in ['GMP', 'GLP', 'FDA', 'EMA', 'IND', 'NDA', 'BLA', 'MAA', 'CTD', 'ICH']):
        return "ex:TermCategory-Regulatory"
    
    # Quality terms
    if any(term in abbr_upper for term in ['QA', 'QC', 'CQA', 'CPP', 'OOS', 'OOT', 'CoA', 'QBD']):
        return "ex:TermCategory-Quality"
    
    # Cell & Gene Therapy terms
    if any(term in abbr_upper for term in ['MCB', 'WCB', 'EOPCB', 'DCB', 'CAR', 'CGT', 'MVB']):
        return "ex:TermCategory-CellGene"
    
    # Process/Manufacturing terms
    if any(term in abbr_upper for term in ['DSP', 'USP', 'PPQ', 'PV', 'DOE', 'PAR', 'CPV', 'FMEA']):
        return "ex:TermCategory-Process"
    
    # Clinical terms
    if any(term in abbr_upper for term in ['FIH', 'PK', 'CTA', 'CSR', 'IDE']) or 'clinical' in def_lower:
        return "ex:TermCategory-Clinical"
    
    # Analytical terms
    if any(term in abbr_upper for term in ['AD', 'ATP', 'CMA', 'TOE']) or 'analytical' in def_lower:
        return "ex:TermCategory-Analytical"
    
    # Organization terms
    if any(term in def_lower for term in ['team', 'committee', 'council', 'department', 'organization']):
        return "ex:TermCategory-Organization"
    
    # Default to Process if unclear
    return "ex:TermCategory-Process"


def is_critical_term(abbr: str) -> bool:
    """Determine if this is a critical term."""
    critical_abbrs = {'CQA', 'CPP', 'CMA', 'FIH', 'PPQ', 'GMP', 'MCB', 'WCB'}
    return abbr.upper() in critical_abbrs


def is_regulatory_term(abbr: str) -> bool:
    """Determine if this is a regulatory term."""
    regulatory_abbrs = {'GMP', 'GLP', 'FDA', 'EMA', 'IND', 'NDA', 'BLA', 'MAA', 'CTD', 'ICH', 'CTA', 'IMPD'}
    return abbr.upper() in regulatory_abbrs


def find_related_stage(abbr: str, definition: str) -> List[str]:
    """Find stages that might use this term."""
    related_stages = []
    abbr_upper = abbr.upper()
    def_lower = definition.lower()
    
    # PPQ is specifically Stage 11
    if abbr_upper == 'PPQ':
        related_stages.append('ex:Stage-protein-11')
        related_stages.append('ex:Stage-cgt-11')
    
    # FIH relates to early clinical stages
    if abbr_upper == 'FIH' or 'first in human' in def_lower:
        related_stages.append('ex:Stage-protein-3')
        related_stages.append('ex:Stage-cgt-3')
    
    # Cell bank terms relate to CGT stages
    if abbr_upper in ['MCB', 'WCB', 'DCB', 'EOPCB']:
        related_stages.extend([f'ex:Stage-cgt-{i}' for i in range(0, 4)])
    
    # Late stage terms
    if abbr_upper in ['BLA', 'MAA', 'NDA']:
        related_stages.append('ex:Stage-protein-12')
        related_stages.append('ex:Stage-cgt-12')
    
    return related_stages


def generate_lexicon_ttl():
    """Generate TTL from Lexicon CSV."""
    
    # Find the Lexicon CSV file
    csv_files = list(DATA_DIR.glob("*Lexicon.csv"))
    if not csv_files:
        print("Error: No Lexicon CSV file found in data/current/")
        return
    
    csv_path = csv_files[0]
    print(f"Processing: {csv_path.name}")
    
    # Output file
    output_path = OUTPUT_DIR / "cmc_stagegate_lexicon_instances.ttl"
    
    # TTL header
    ttl_lines = [
        "@prefix ex: <https://w3id.org/cmc-stagegate#> .",
        "@prefix rdfs: <http://www.w3.org/2000/01/rdf-schema#> .",
        "@prefix skos: <http://www.w3.org/2004/02/skos/core#> .",
        "@prefix xsd: <http://www.w3.org/2001/XMLSchema#> .",
        "@prefix dcterms: <http://purl.org/dc/terms/> .",
        "@prefix owl: <http://www.w3.org/2002/07/owl#> .",
        "",
        "#################################################################",
        "#    Lexicon Instance Data",
        f"#    Generated from: {csv_path.name}",
        f"#    Generated on: {datetime.now().isoformat()}",
        "#    Total terms: Will be counted after processing",
        "#################################################################",
        "",
    ]
    
    term_count = 0
    triple_count = 0
    
    # Read and process CSV
    with open(csv_path, 'r', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        
        for row in reader:
            abbr = row.get('Abbreviation & Nomenclature', '').strip()
            definition = row.get('Definition', '').strip()
            
            if not abbr or not definition:
                continue
            
            term_count += 1
            
            # Generate GUPRI
            term_id = generate_lexicon_gupri(abbr)
            
            # Determine category
            category = categorize_term(abbr, definition)
            
            # Check if critical or regulatory
            is_critical = is_critical_term(abbr)
            is_regulatory = is_regulatory_term(abbr)
            
            # Find related stages
            related_stages = find_related_stage(abbr, definition)
            
            # Generate TTL
            ttl_lines.append(f"### Term: {abbr}")
            ttl_lines.append(f"{term_id} a ex:DefinedTerm ;")
            ttl_lines.append(f"    ex:hasAbbreviation {escape_turtle_literal(abbr)} ;")
            ttl_lines.append(f"    ex:hasDefinition {escape_turtle_literal(definition)} ;")
            ttl_lines.append(f"    ex:hasTermCategory {category} ;")
            ttl_lines.append(f"    skos:prefLabel {escape_turtle_literal(abbr)} ;")
            ttl_lines.append(f"    skos:definition {escape_turtle_literal(definition)} ;")
            ttl_lines.append(f"    skos:notation {escape_turtle_literal(abbr)} ;")
            ttl_lines.append(f"    skos:inScheme ex:LexiconScheme ;")
            
            triple_count += 7
            
            if is_critical:
                ttl_lines.append(f"    ex:isCritical true ;")
                triple_count += 1
            
            if is_regulatory:
                ttl_lines.append(f"    ex:isRegulatory true ;")
                triple_count += 1
            
            # Add related stages
            if related_stages:
                for stage in related_stages:
                    ttl_lines.append(f"    ex:usedInStage {stage} ;")
                    triple_count += 1
            
            # Add label and close
            ttl_lines.append(f"    rdfs:label {escape_turtle_literal(f'{abbr} - {definition[:50]}...' if len(definition) > 50 else f'{abbr} - {definition}')} .")
            ttl_lines.append("")
            triple_count += 1
    
    # Add statistics comment at the top
    ttl_lines[11] = f"#    Total terms: {term_count}"
    ttl_lines.insert(12, f"#    Total triples: {triple_count}")
    
    # Write output file
    output_path.parent.mkdir(parents=True, exist_ok=True)
    with open(output_path, 'w', encoding='utf-8') as f:
        f.write('\n'.join(ttl_lines))
    
    print(f"✅ Generated {output_path.name}")
    print(f"   Terms: {term_count}")
    print(f"   Triples: {triple_count}")
    print(f"   Categories: {len(set(categorize_term(abbr, '') for abbr in ['GMP', 'CQA', 'MCB', 'CDT', 'FIH', 'AD']))}")
    
    # Save ID mappings
    if LEXICON_ID_MAPPINGS:
        import json
        with open(MAPPINGS_FILE, 'w') as f:
            json.dump(LEXICON_ID_MAPPINGS, f, indent=2, sort_keys=True)
        print(f"✅ Saved {len(LEXICON_ID_MAPPINGS)} ID mappings to {MAPPINGS_FILE.name}")


if __name__ == "__main__":
    generate_lexicon_ttl()
