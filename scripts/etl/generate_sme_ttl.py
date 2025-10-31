#!/usr/bin/env python3
"""
Generate SME (Subject Matter Expert) RDF triples from CSV data.
Reads the SME CSV file and creates functional area and SME instances.
"""

from __future__ import annotations

import csv
import re
from pathlib import Path
from typing import Dict, List, Tuple, Set

# Configuration
BASE_DIR = Path("/Users/nicholasbaro/Python/staged")
DATA_DIR = BASE_DIR / "data" / "current"

# Find SME CSV file
SME_FILES = list(DATA_DIR.glob("*SME*.csv")) if DATA_DIR.exists() else []
SME_FILE = SME_FILES[0] if SME_FILES else DATA_DIR / "SME.csv"

# Output configuration
OUTPUT_DIR = BASE_DIR / "output" / "current"
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
OUTPUT_TTL = OUTPUT_DIR / "cmc_stagegate_sme_instances.ttl"

# TTL prefixes
TTL_PREFIXES = """@prefix ex: <https://w3id.org/cmc-stagegate#> .
@prefix gist: <https://ontologies.semanticarts.com/gist/> .
@prefix rdfs: <http://www.w3.org/2000/01/rdf-schema#> .
@prefix xsd: <http://www.w3.org/2001/XMLSchema#> .
@prefix prov: <http://www.w3.org/ns/prov#> .

"""


def safe_id(text: str) -> str:
    """Convert text to safe ID for RDF IRI."""
    text = text.strip()
    # Remove parenthetical content for ID but preserve original
    text_for_id = re.sub(r'\([^)]*\)', '', text)
    text_for_id = text_for_id.strip().lower()
    text_for_id = re.sub(r'[^a-z0-9]+', '-', text_for_id)
    text_for_id = text_for_id.strip('-')
    return text_for_id or "unnamed"


def escape_turtle_literal(value: str) -> str:
    """Escape special characters for Turtle format."""
    value = value.replace('\\', '\\\\').replace('"', '\\"')
    value = value.replace('\r', '\\n').replace('\n', '\\n').replace('\t', '\\t')
    return value


def parse_sme_name(sme_text: str) -> List[Tuple[str, str, bool]]:
    """
    Parse SME text to extract names, expertise areas, and backup status.
    Returns list of (name, expertise, is_backup) tuples.
    """
    if not sme_text or sme_text.strip() == "":
        return []
    
    results = []
    
    # Check if this contains "Backup" notation
    is_backup_notation = "Backup" in sme_text
    
    # Split by newlines for multiple SMEs (common in CGT)
    lines = sme_text.replace('\n', '|').split('|')
    
    for line in lines:
        line = line.strip()
        if not line:
            continue
            
        # Check for backup notation like (Backup Name)
        backup_match = re.search(r'\(Backup ([^)]+)\)', line)
        if backup_match:
            # This line has a primary and backup
            primary_name = re.sub(r'\(Backup [^)]+\)', '', line).strip()
            backup_name = backup_match.group(1).strip()
            
            # Extract expertise from primary name if present
            primary_expertise = ""
            exp_match = re.search(r'\(([^)]+)\)$', primary_name)
            if exp_match:
                primary_expertise = exp_match.group(1)
                primary_name = re.sub(r'\([^)]+\)$', '', primary_name).strip()
            
            results.append((primary_name, primary_expertise, False))
            results.append((backup_name, "", True))
        else:
            # Single SME, check for expertise area in parentheses
            name = line
            expertise = ""
            
            # Extract expertise like (Cell)(Auto) or (Gene)
            exp_matches = re.findall(r'\(([^)]+)\)', line)
            if exp_matches:
                # Join multiple parenthetical notes
                expertise = ' '.join(exp_matches)
                # Remove all parenthetical content from name
                name = re.sub(r'\([^)]*\)', '', line).strip()
            
            if name:
                results.append((name, expertise, False))
    
    return results


def generate_sme_ttl():
    """Generate RDF triples from SME CSV data."""
    
    print(f"Reading SME data from: {SME_FILE}")
    
    if not SME_FILE.exists():
        print(f"Error: SME file not found at {SME_FILE}")
        return
    
    # Read CSV data
    with open(SME_FILE, 'r', encoding='utf-8') as f:
        reader = csv.reader(f)
        rows = list(reader)
    
    # Parse the structure - data starts at row 7 (index 6)
    functional_areas_protein = {}
    functional_areas_cgt = {}
    all_smes = {}  # Track unique SMEs
    
    for row_idx in range(6, len(rows)):
        if row_idx >= len(rows):
            break
            
        row = rows[row_idx]
        if len(row) < 6:
            continue
        
        # Extract data from columns
        # Col 1: Protein Functional Area
        # Col 2: Protein SMEs
        # Col 4: CGT Functional Area  
        # Col 5: CGT SMEs
        
        protein_area = row[1].strip() if len(row) > 1 else ""
        protein_smes = row[2].strip() if len(row) > 2 else ""
        cgt_area = row[4].strip() if len(row) > 4 else ""
        cgt_smes = row[5].strip() if len(row) > 5 else ""
        
        # Process Protein data
        if protein_area and protein_area not in ["", "Functional Area of Responsibility"]:
            sme_list = parse_sme_name(protein_smes)
            if sme_list:
                functional_areas_protein[protein_area] = sme_list
                for name, expertise, is_backup in sme_list:
                    if name not in all_smes:
                        all_smes[name] = {
                            'expertise': set(),
                            'areas_protein': set(),
                            'areas_cgt': set(),
                            'is_backup': set()
                        }
                    all_smes[name]['areas_protein'].add(protein_area)
                    if expertise:
                        all_smes[name]['expertise'].add(expertise)
                    if is_backup:
                        all_smes[name]['is_backup'].add(protein_area + " (Protein)")
        
        # Process CGT data
        if cgt_area and cgt_area not in ["", "Functional Area of Responsibility"]:
            sme_list = parse_sme_name(cgt_smes)
            if sme_list:
                functional_areas_cgt[cgt_area] = sme_list
                for name, expertise, is_backup in sme_list:
                    if name not in all_smes:
                        all_smes[name] = {
                            'expertise': set(),
                            'areas_protein': set(),
                            'areas_cgt': set(),
                            'is_backup': set()
                        }
                    all_smes[name]['areas_cgt'].add(cgt_area)
                    if expertise:
                        all_smes[name]['expertise'].add(expertise)
                    if is_backup:
                        all_smes[name]['is_backup'].add(cgt_area + " (CGT)")
    
    # Generate TTL output
    ttl_lines = [TTL_PREFIXES]
    ttl_lines.append("# SME (Subject Matter Expert) Instances\n")
    ttl_lines.append("# Generated from SME CSV data\n\n")
    
    # Generate Functional Area instances
    ttl_lines.append("# Functional Areas - Protein\n")
    for area_name in functional_areas_protein:
        area_id = safe_id(area_name)
        ttl_lines.append(f"ex:FA-Protein-{area_id} a ex:FunctionalArea ;")
        ttl_lines.append(f'    rdfs:label "{escape_turtle_literal(area_name)} (Protein)" ;')
        ttl_lines.append(f'    ex:modality "Protein" ;')
        
        # Add SMEs for this area
        smes = functional_areas_protein[area_name]
        primary_smes = [s for s in smes if not s[2]]  # is_backup = False
        backup_smes = [s for s in smes if s[2]]  # is_backup = True
        
        for sme_name, expertise, _ in primary_smes:
            sme_id = safe_id(sme_name)
            ttl_lines.append(f"    ex:hasSME ex:SME-{sme_id} ;")
        
        for sme_name, expertise, _ in backup_smes:
            sme_id = safe_id(sme_name)
            ttl_lines.append(f"    ex:hasBackupSME ex:SME-{sme_id} ;")
        
        # Remove trailing semicolon and add period
        ttl_lines[-1] = ttl_lines[-1].replace(' ;', ' .')
        ttl_lines.append("")
    
    ttl_lines.append("# Functional Areas - CGT\n")
    for area_name in functional_areas_cgt:
        area_id = safe_id(area_name)
        ttl_lines.append(f"ex:FA-CGT-{area_id} a ex:FunctionalArea ;")
        ttl_lines.append(f'    rdfs:label "{escape_turtle_literal(area_name)} (CGT)" ;')
        ttl_lines.append(f'    ex:modality "CGT" ;')
        
        # Add SMEs for this area
        smes = functional_areas_cgt[area_name]
        primary_smes = [s for s in smes if not s[2]]
        backup_smes = [s for s in smes if s[2]]
        
        for sme_name, expertise, _ in primary_smes:
            sme_id = safe_id(sme_name)
            ttl_lines.append(f"    ex:hasSME ex:SME-{sme_id} ;")
        
        for sme_name, expertise, _ in backup_smes:
            sme_id = safe_id(sme_name)
            ttl_lines.append(f"    ex:hasBackupSME ex:SME-{sme_id} ;")
        
        # Remove trailing semicolon and add period
        ttl_lines[-1] = ttl_lines[-1].replace(' ;', ' .')
        ttl_lines.append("")
    
    # Generate SME instances
    ttl_lines.append("# Subject Matter Experts\n")
    for sme_name, sme_data in sorted(all_smes.items()):
        sme_id = safe_id(sme_name)
        ttl_lines.append(f"ex:SME-{sme_id} a ex:SubjectMatterExpert ;")
        ttl_lines.append(f'    rdfs:label "{escape_turtle_literal(sme_name)}" ;')
        ttl_lines.append(f'    gist:name "{escape_turtle_literal(sme_name)}" ;')
        
        # Add expertise areas if present
        if sme_data['expertise']:
            for expertise in sorted(sme_data['expertise']):
                ttl_lines.append(f'    ex:expertiseArea "{escape_turtle_literal(expertise)}" ;')
        
        # Add functional areas
        for area in sorted(sme_data['areas_protein']):
            area_id = safe_id(area)
            ttl_lines.append(f"    ex:expertFor ex:FA-Protein-{area_id} ;")
        
        for area in sorted(sme_data['areas_cgt']):
            area_id = safe_id(area)
            ttl_lines.append(f"    ex:expertFor ex:FA-CGT-{area_id} ;")
        
        # Add modality
        modalities = []
        if sme_data['areas_protein']:
            modalities.append("Protein")
        if sme_data['areas_cgt']:
            modalities.append("CGT")
        
        if modalities:
            ttl_lines.append(f'    ex:modality "{", ".join(modalities)}" ;')
        
        # Mark if this person is a backup for any area
        if sme_data['is_backup']:
            ttl_lines.append(f'    ex:isPrimary false ;')
            ttl_lines.append(f'    rdfs:comment "Backup SME for: {", ".join(sorted(sme_data["is_backup"]))}" ;')
        else:
            ttl_lines.append(f'    ex:isPrimary true ;')
        
        # Remove trailing semicolon and add period
        ttl_lines[-1] = ttl_lines[-1].replace(' ;', ' .')
        ttl_lines.append("")
    
    # Write output
    output_content = '\n'.join(ttl_lines)
    with open(OUTPUT_TTL, 'w', encoding='utf-8') as f:
        f.write(output_content)
    
    # Print statistics
    total_areas = len(functional_areas_protein) + len(functional_areas_cgt)
    total_smes = len(all_smes)
    
    print(f"\nGenerated SME TTL:")
    print(f"  Functional Areas: {total_areas}")
    print(f"    - Protein: {len(functional_areas_protein)}")
    print(f"    - CGT: {len(functional_areas_cgt)}")
    print(f"  Subject Matter Experts: {total_smes}")
    print(f"  Output: {OUTPUT_TTL}")
    
    # Show sample areas and SMEs
    print("\nSample Functional Areas:")
    for area in list(functional_areas_protein.keys())[:3]:
        print(f"  - {area} (Protein)")
    for area in list(functional_areas_cgt.keys())[:3]:
        print(f"  - {area} (CGT)")
    
    print("\nSample SMEs:")
    for sme_name in list(all_smes.keys())[:5]:
        print(f"  - {sme_name}")


if __name__ == "__main__":
    generate_sme_ttl()
