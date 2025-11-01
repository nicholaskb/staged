#!/usr/bin/env python3
"""
Generate RDF triples from SME CSV data.
Handles the actual CSV structure with columns:
- Value Stream (Protein/CGT)
- Functional Area of Responsibility
- Contact (Primary/Secondary)
- Person (SME name)
- Specialty
"""

import csv
import re
from pathlib import Path
from typing import Dict, List, Set

# Configuration
BASE_DIR = Path("/Users/nicholasbaro/Python/staged")
DATA_DIR = BASE_DIR / "data" / "current"

# Find SME CSV file
SME_FILES = list(DATA_DIR.glob("*SME.csv")) if DATA_DIR.exists() else []
# Filter out SME_old.csv
SME_FILES = [f for f in SME_FILES if 'SME_old' not in f.name]
SME_FILE = SME_FILES[0] if SME_FILES else DATA_DIR / "SME.csv"

# Output configuration
OUTPUT_DIR = BASE_DIR / "output" / "current"
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
OUTPUT_TTL = OUTPUT_DIR / "cmc_stagegate_sme_instances.ttl"


def safe_id(text: str) -> str:
    """Convert text to safe ID for RDF IRI."""
    text = text.strip()
    # Remove parenthetical content for ID
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


def extract_primary_backup(name_text: str):
    """Extract primary name and backup name from text like 'Name (Backup Other)'."""
    backup_match = re.search(r'\(Backup ([^)]+)\)', name_text)
    if backup_match:
        primary = re.sub(r'\(Backup [^)]+\)', '', name_text).strip()
        backup = backup_match.group(1).strip()
        return primary, backup
    return name_text.strip(), None


def generate_sme_ttl():
    """Generate RDF triples from SME CSV data."""
    
    print(f"Reading SME data from: {SME_FILE}")
    
    if not SME_FILE.exists():
        print(f"Error: SME file not found at {SME_FILE}")
        return
    
    # Read CSV data
    with open(SME_FILE, 'r', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        rows = list(reader)
    
    # Data structures
    functional_areas = {}  # {modality: {area_name: set of SMEs}}
    all_smes = {}  # {sme_name: {modalities, areas, is_primary, is_backup_for}}
    
    for row in rows:
        value_stream = row.get('Value Stream', '').strip()
        functional_area = row.get('Functional Area of Responsibility', '').strip()
        contact_type = row.get('Contact', '').strip()
        person = row.get('Person', '').strip()
        specialty = row.get('Specialty', '').strip()
        
        if not value_stream or not person:
            continue
        
        # Initialize modality if needed
        if value_stream not in functional_areas:
            functional_areas[value_stream] = {}
        
        # Initialize functional area if needed
        if functional_area and functional_area not in functional_areas[value_stream]:
            functional_areas[value_stream][functional_area] = {
                'primary': [],
                'secondary': []
            }
        
        # Extract primary and backup from person field
        primary_name, backup_name = extract_primary_backup(person)
        
        # Process primary person
        if primary_name:
            if primary_name not in all_smes:
                all_smes[primary_name] = {
                    'modalities': set(),
                    'areas': set(),
                    'is_primary': set(),
                    'is_backup': set(),
                    'specialty': specialty if specialty else ""
                }
            
            all_smes[primary_name]['modalities'].add(value_stream)
            if functional_area:
                all_smes[primary_name]['areas'].add(f"{functional_area} ({value_stream})")
                
                if contact_type.lower() == 'primary':
                    functional_areas[value_stream][functional_area]['primary'].append(primary_name)
                    all_smes[primary_name]['is_primary'].add(f"{functional_area} ({value_stream})")
                elif contact_type.lower() == 'secondary':
                    functional_areas[value_stream][functional_area]['secondary'].append(primary_name)
                    all_smes[primary_name]['is_backup'].add(f"{functional_area} ({value_stream})")
        
        # Process backup person if present
        if backup_name:
            if backup_name not in all_smes:
                all_smes[backup_name] = {
                    'modalities': set(),
                    'areas': set(),
                    'is_primary': set(),
                    'is_backup': set(),
                    'specialty': ""
                }
            
            all_smes[backup_name]['modalities'].add(value_stream)
            if functional_area:
                all_smes[backup_name]['areas'].add(f"{functional_area} ({value_stream})")
                all_smes[backup_name]['is_backup'].add(f"{functional_area} ({value_stream})")
                functional_areas[value_stream][functional_area]['secondary'].append(backup_name)
    
    # Generate TTL output
    ttl_lines = []
    ttl_lines.append("@prefix ex: <https://w3id.org/cmc-stagegate#> .")
    ttl_lines.append("@prefix gist: <https://ontologies.semanticarts.com/gist/> .")
    ttl_lines.append("@prefix rdfs: <http://www.w3.org/2000/01/rdf-schema#> .")
    ttl_lines.append("@prefix xsd: <http://www.w3.org/2001/XMLSchema#> .")
    ttl_lines.append("@prefix prov: <http://www.w3.org/ns/prov#> .")
    ttl_lines.append("")
    ttl_lines.append("# SME (Subject Matter Expert) Instances")
    ttl_lines.append(f"# Generated from: {SME_FILE.name}")
    ttl_lines.append("")
    
    # Generate Functional Area instances
    for modality in sorted(functional_areas.keys()):
        ttl_lines.append(f"\n# Functional Areas - {modality}")
        for area_name in sorted(functional_areas[modality].keys()):
            area_id = safe_id(area_name)
            ttl_lines.append(f"\nex:FA-{modality}-{area_id} a ex:FunctionalArea ;")
            ttl_lines.append(f'    rdfs:label "{escape_turtle_literal(area_name)} ({modality})" ;')
            ttl_lines.append(f'    ex:modality "{modality}" ;')
            
            # Add primary SMEs
            primary_smes = functional_areas[modality][area_name]['primary']
            for sme_name in primary_smes:
                sme_id = safe_id(sme_name)
                ttl_lines.append(f"    ex:hasSME ex:SME-{sme_id} ;")
            
            # Add secondary/backup SMEs
            secondary_smes = functional_areas[modality][area_name]['secondary']
            for sme_name in secondary_smes:
                sme_id = safe_id(sme_name)
                ttl_lines.append(f"    ex:hasBackupSME ex:SME-{sme_id} ;")
            
            # Remove trailing semicolon and add period
            ttl_lines[-1] = ttl_lines[-1].replace(' ;', ' .')
    
    # Generate SME instances
    ttl_lines.append("\n\n# Subject Matter Experts")
    for sme_name in sorted(all_smes.keys()):
        sme_data = all_smes[sme_name]
        sme_id = safe_id(sme_name)
        
        ttl_lines.append(f"\nex:SME-{sme_id} a ex:SubjectMatterExpert ;")
        ttl_lines.append(f'    rdfs:label "{escape_turtle_literal(sme_name)}" ;')
        ttl_lines.append(f'    gist:name "{escape_turtle_literal(sme_name)}" ;')
        
        # Add modalities
        for modality in sorted(sme_data['modalities']):
            ttl_lines.append(f'    ex:hasExpertiseInModality "{modality}" ;')
        
        # Add functional areas
        for area in sorted(sme_data['areas']):
            ttl_lines.append(f'    ex:responsibleForArea "{escape_turtle_literal(area)}" ;')
        
        # Add specialty if present
        if sme_data['specialty']:
            ttl_lines.append(f'    ex:hasSpecialty "{escape_turtle_literal(sme_data["specialty"])}" ;')
        
        # Add primary/backup status
        if sme_data['is_primary']:
            ttl_lines.append(f'    ex:isPrimaryFor "{", ".join(sorted(sme_data["is_primary"]))}" ;')
        
        if sme_data['is_backup']:
            ttl_lines.append(f'    ex:isBackupFor "{", ".join(sorted(sme_data["is_backup"]))}" ;')
        
        # Remove trailing semicolon and add period
        ttl_lines[-1] = ttl_lines[-1].replace(' ;', ' .')
    
    # Write output
    output_content = '\n'.join(ttl_lines)
    with open(OUTPUT_TTL, 'w', encoding='utf-8') as f:
        f.write(output_content)
    
    # Print statistics
    total_areas = sum(len(areas) for areas in functional_areas.values())
    total_smes = len(all_smes)
    
    print(f"\nGenerated SME TTL:")
    print(f"  Functional Areas: {total_areas}")
    for modality in functional_areas:
        print(f"    - {modality}: {len(functional_areas[modality])}")
    print(f"  Subject Matter Experts: {total_smes}")
    print(f"  Output: {OUTPUT_TTL}")
    
    # Show sample data
    print("\nSample Functional Areas:")
    for modality in functional_areas:
        for area in list(functional_areas[modality].keys())[:2]:
            print(f"  - {area} ({modality})")
    
    print("\nSample SMEs:")
    for sme_name in list(all_smes.keys())[:5]:
        print(f"  - {sme_name}")


if __name__ == "__main__":
    generate_sme_ttl()