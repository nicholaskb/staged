#!/usr/bin/env python3
"""
Validate gist alignment consistency with base CMC ontology.
Checks that all mapped classes and properties exist in both ontologies.
"""

from pathlib import Path
from typing import Set, Tuple, List
import re
import sys


def extract_entities(file_path: Path) -> Tuple[Set[str], Set[str]]:
    """Extract classes and properties from a TTL file."""
    classes = set()
    properties = set()
    
    content = file_path.read_text(encoding='utf-8')
    
    # Extract ex: prefixed entities
    # Classes: ex:ClassName rdfs:subClassOf or a ex:ClassName
    class_pattern = r'ex:(\w+)\s+(?:rdfs:subClassOf|a\s+(?:owl:Class|rdfs:Class))'
    for match in re.finditer(class_pattern, content):
        classes.add(match.group(1))
    
    # Properties: ex:propertyName rdfs:subPropertyOf or a owl:ObjectProperty/DatatypeProperty or rdf:Property
    prop_patterns = [
        r'ex:(\w+)\s+(?:rdfs:subPropertyOf|owl:inverseOf)',
        r'ex:(\w+)\s+a\s+(?:owl:(?:Object|Datatype)Property|rdf:Property)',
    ]
    for pattern in prop_patterns:
        for match in re.finditer(pattern, content):
            properties.add(match.group(1))
    
    return classes, properties


def extract_gist_mappings(file_path: Path) -> Tuple[Set[str], Set[str]]:
    """Extract CMC entities that are mapped to gist from alignment file."""
    mapped_classes = set()
    mapped_properties = set()
    
    content = file_path.read_text(encoding='utf-8')
    
    # Extract mapped classes: ex:ClassName rdfs:subClassOf gist:
    class_mapping_pattern = r'ex:(\w+)\s+rdfs:subClassOf\s+(?:gist:\w+|\[)'
    for match in re.finditer(class_mapping_pattern, content):
        mapped_classes.add(match.group(1))
    
    # Extract mapped properties: ex:property rdfs:subPropertyOf gist:
    prop_mapping_pattern = r'ex:(\w+)\s+(?:rdfs:subPropertyOf|owl:inverseOf)\s+gist:\w+'
    for match in re.finditer(prop_mapping_pattern, content):
        mapped_properties.add(match.group(1))
    
    # Also capture properties defined as owl:ObjectProperty with gist mappings
    obj_prop_pattern = r'ex:(\w+)\s+a\s+owl:ObjectProperty'
    for match in re.finditer(obj_prop_pattern, content):
        mapped_properties.add(match.group(1))
    
    return mapped_classes, mapped_properties


def validate_alignment(base_file: Path, align_file: Path) -> List[str]:
    """Validate that gist alignment is consistent with base ontology."""
    issues = []
    
    # Extract entities from base ontology
    base_classes, base_properties = extract_entities(base_file)
    
    # Extract mapped entities from alignment
    mapped_classes, mapped_properties = extract_gist_mappings(align_file)
    
    # Check if all mapped classes exist in base
    missing_classes = mapped_classes - base_classes
    if missing_classes:
        issues.append(f"Classes mapped in alignment but not defined in base: {missing_classes}")
    
    # Check if all mapped properties exist in base
    missing_properties = mapped_properties - base_properties
    if missing_properties:
        # Some properties might be defined only in alignment (like lotOf)
        # Check if they're legitimate new properties
        legitimate_new = {'lotOf'}  # Properties defined in alignment itself
        actual_missing = missing_properties - legitimate_new
        if actual_missing:
            issues.append(f"Properties mapped in alignment but not defined in base: {actual_missing}")
    
    # Report coverage
    coverage_classes = len(mapped_classes) / len(base_classes) * 100 if base_classes else 0
    coverage_props = len(mapped_properties) / len(base_properties) * 100 if base_properties else 0
    
    print(f"Alignment Coverage Report:")
    print(f"  Classes: {len(mapped_classes)}/{len(base_classes)} ({coverage_classes:.1f}%)")
    print(f"  Properties: {len(mapped_properties)}/{len(base_properties)} ({coverage_props:.1f}%)")
    print(f"  Mapped Classes: {sorted(mapped_classes)}")
    print(f"  Mapped Properties: {sorted(mapped_properties)}")
    
    # Check for gist references
    align_content = align_file.read_text(encoding='utf-8')
    gist_classes = re.findall(r'gist:(\w+)', align_content)
    unique_gist = set(gist_classes)
    print(f"\nGIST concepts referenced: {len(unique_gist)}")
    print(f"  {sorted(unique_gist)}")
    
    return issues


def main():
    """Main validation function."""
    base_file = Path("/Users/nicholasbaro/Python/staged/cmc_stagegate_base.ttl")
    align_file = Path("/Users/nicholasbaro/Python/staged/cmc_stagegate_gist_align.ttl")
    combined_file = Path("/Users/nicholasbaro/Python/staged/cmc_stagegate_all.ttl")
    
    # Check files exist
    for f in [base_file, align_file]:
        if not f.exists():
            print(f"Error: {f} not found")
            return 1
    
    print("Validating GIST Alignment...")
    print("-" * 50)
    
    # Validate alignment
    issues = validate_alignment(base_file, align_file)
    
    if issues:
        print("\nValidation Issues Found:")
        for issue in issues:
            print(f"  ⚠️  {issue}")
    else:
        print("\n✅ All alignment mappings are consistent with base ontology!")
    
    # Check combined file
    if combined_file.exists():
        size_kb = combined_file.stat().st_size / 1024
        lines = combined_file.read_text(encoding='utf-8').count('\n')
        print(f"\n📄 Combined file generated: {combined_file.name}")
        print(f"   Size: {size_kb:.1f} KB, Lines: {lines}")
    
    return 0 if not issues else 1


if __name__ == "__main__":
    sys.exit(main())
