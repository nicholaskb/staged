#!/usr/bin/env python3
"""
Simple Example: CGT Stage Gate 0 (Entry in Early Development)

This is a minimal v0 implementation demonstrating a complete stage gate process.
Stage Gate 0 is the simplest with only 17 deliverables across 4 functional areas.

Process Flow:
1. Extract stage gate data from CSV
2. Transform to RDF/TTL format
3. Generate validation queries
4. Create visualization-ready output
"""

import csv
import json
from pathlib import Path
from typing import Dict, List, NamedTuple, Optional
from datetime import datetime


# Data model for Stage Gate deliverables
class Deliverable(NamedTuple):
    """Represents a single deliverable in a stage gate."""
    functional_area: str
    deliverable_text: str
    category: Optional[str] = None
    owner: Optional[str] = None
    status: Optional[str] = None
    vpad_specific: Optional[bool] = None


class StageGate(NamedTuple):
    """Represents a complete stage gate with metadata and deliverables."""
    value_stream: str  # CGT or Protein
    gate_number: int
    description: str
    deliverables: List[Deliverable]


def extract_stage_gate_0() -> StageGate:
    """
    Extract CGT Stage Gate 0 data from the CSV file.
    Returns a structured StageGate object.
    """
    csv_path = Path("/Users/nicholasbaro/Python/staged/data/extracted/"
                    "Protein_and_CGT_SGD_Template_Final_ENDORSED_JAN_2023__SGD.csv")
    
    deliverables = []
    
    with open(csv_path, 'r', encoding='utf-8') as f:
        reader = csv.reader(f)
        # Skip first row (column headers from Excel)
        next(reader)
        # Get actual headers from second row
        headers = next(reader)
        
        for row in reader:
            # Create dict from row
            data = dict(zip(headers, row))
            
            # Filter for CGT Stage Gate 0
            if data.get('Value Stream') == 'CGT' and data.get('Stage Gate') == '0':
                deliverable = Deliverable(
                    functional_area=data.get('Functional Area/Subteam', '').strip(),
                    deliverable_text=data.get('Deliverable', '').strip(),
                    category=data.get('Category', '').strip() or None,
                    owner=data.get('Owner', '').strip() or None,
                    status=data.get('Status', '').strip() or None,
                    vpad_specific=data.get('VPAD-specific?', '').strip().lower() == 'yes'
                )
                if deliverable.deliverable_text:  # Only add if there's actual deliverable text
                    deliverables.append(deliverable)
    
    return StageGate(
        value_stream='CGT',
        gate_number=0,
        description='Entry in ED (C&GT)',
        deliverables=deliverables
    )


def generate_ttl(stage_gate: StageGate) -> str:
    """
    Generate RDF/TTL representation of the stage gate.
    Uses a simplified ontology structure for clarity.
    """
    # Prefixes
    ttl = """@prefix sg: <http://example.org/stagegate#> .
@prefix rdfs: <http://www.w3.org/2000/01/rdf-schema#> .
@prefix xsd: <http://www.w3.org/2001/XMLSchema#> .
@prefix prov: <http://www.w3.org/ns/prov#> .

# Stage Gate Definition
sg:CGT-Gate-0 a sg:StageGate ;
    rdfs:label "CGT Stage Gate 0: Entry in ED" ;
    sg:valueStream "CGT" ;
    sg:gateNumber 0 ;
    sg:description "Entry in Early Development (Cell & Gene Therapy)" ;
    sg:createdDate "2023-01-01"^^xsd:date .

"""
    
    # Group deliverables by functional area
    by_area: Dict[str, List[Deliverable]] = {}
    for d in stage_gate.deliverables:
        area = d.functional_area or "Unspecified"
        if area not in by_area:
            by_area[area] = []
        by_area[area].append(d)
    
    # Generate functional areas and their deliverables
    for i, (area, delivs) in enumerate(by_area.items(), 1):
        area_id = area.replace(' ', '_').replace('(', '').replace(')', '').replace('&', 'and')
        area_uri = f"sg:Area-{area_id}"
        
        ttl += f"\n# Functional Area: {area}\n"
        ttl += f"{area_uri} a sg:FunctionalArea ;\n"
        ttl += f'    rdfs:label "{area}" ;\n'
        ttl += f"    sg:belongsToGate sg:CGT-Gate-0 .\n\n"
        
        # Add deliverables for this area
        for j, deliv in enumerate(delivs, 1):
            deliv_id = f"CGT-0-{area_id}-{j}"
            deliv_uri = f"sg:Deliverable-{deliv_id}"
            
            # Escape quotes in text
            deliv_text = deliv.deliverable_text.replace('"', '\\"')
            
            ttl += f"{deliv_uri} a sg:Deliverable ;\n"
            ttl += f'    rdfs:label "{deliv_text}" ;\n'
            ttl += f"    sg:functionalArea {area_uri} ;\n"
            ttl += f"    sg:stageGate sg:CGT-Gate-0"
            
            if deliv.owner:
                owner_text = deliv.owner.replace('"', '\\"')
                ttl += f' ;\n    sg:owner "{owner_text}"'
            
            if deliv.status:
                ttl += f' ;\n    sg:status "{deliv.status}"'
            
            if deliv.vpad_specific is not None:
                ttl += f' ;\n    sg:vpadSpecific {str(deliv.vpad_specific).lower()}'
            
            ttl += " .\n\n"
    
    return ttl


def generate_sparql_queries() -> Dict[str, str]:
    """
    Generate example SPARQL queries to validate and explore the stage gate data.
    """
    queries = {
        "count_deliverables": """
# Count total deliverables for CGT Stage Gate 0
PREFIX sg: <http://example.org/stagegate#>
SELECT (COUNT(?deliverable) as ?count)
WHERE {
    ?deliverable a sg:Deliverable ;
                 sg:stageGate sg:CGT-Gate-0 .
}
""",
        
        "deliverables_by_area": """
# List deliverables grouped by functional area
PREFIX sg: <http://example.org/stagegate#>
PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
SELECT ?area ?areaLabel ?deliverable ?delivLabel
WHERE {
    ?area a sg:FunctionalArea ;
          rdfs:label ?areaLabel .
    ?deliverable a sg:Deliverable ;
                 sg:functionalArea ?area ;
                 rdfs:label ?delivLabel .
}
ORDER BY ?areaLabel ?delivLabel
""",
        
        "find_unassigned": """
# Find deliverables without owners
PREFIX sg: <http://example.org/stagegate#>
PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
SELECT ?deliverable ?label
WHERE {
    ?deliverable a sg:Deliverable ;
                 rdfs:label ?label .
    FILTER NOT EXISTS { ?deliverable sg:owner ?owner }
}
""",
        
        "gate_summary": """
# Get stage gate summary information
PREFIX sg: <http://example.org/stagegate#>
PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
SELECT ?gate ?label ?stream ?number ?description (COUNT(?deliverable) as ?deliverableCount)
WHERE {
    ?gate a sg:StageGate ;
          rdfs:label ?label ;
          sg:valueStream ?stream ;
          sg:gateNumber ?number ;
          sg:description ?description .
    OPTIONAL {
        ?deliverable sg:stageGate ?gate .
    }
}
GROUP BY ?gate ?label ?stream ?number ?description
"""
    }
    
    return queries


def create_json_summary(stage_gate: StageGate) -> str:
    """
    Create a JSON summary of the stage gate for easy consumption by other tools.
    """
    summary = {
        "stage_gate": {
            "id": f"{stage_gate.value_stream}-{stage_gate.gate_number}",
            "value_stream": stage_gate.value_stream,
            "gate_number": stage_gate.gate_number,
            "description": stage_gate.description,
            "deliverable_count": len(stage_gate.deliverables),
            "generated_at": datetime.now().isoformat()
        },
        "functional_areas": {},
        "deliverables": []
    }
    
    # Group by functional area
    for deliv in stage_gate.deliverables:
        area = deliv.functional_area or "Unspecified"
        if area not in summary["functional_areas"]:
            summary["functional_areas"][area] = {
                "name": area,
                "deliverable_count": 0,
                "deliverables": []
            }
        
        deliv_data = {
            "text": deliv.deliverable_text,
            "functional_area": area,
            "has_owner": deliv.owner is not None,
            "owner": deliv.owner,
            "status": deliv.status,
            "vpad_specific": deliv.vpad_specific
        }
        
        summary["functional_areas"][area]["deliverables"].append(deliv_data)
        summary["functional_areas"][area]["deliverable_count"] += 1
        summary["deliverables"].append(deliv_data)
    
    return json.dumps(summary, indent=2)


def main():
    """
    Main execution: Extract, transform, and output Stage Gate 0 data.
    """
    print("=" * 60)
    print("CGT Stage Gate 0: Simple Example Implementation")
    print("=" * 60)
    print()
    
    # Step 1: Extract data
    print("Step 1: Extracting Stage Gate 0 data...")
    stage_gate = extract_stage_gate_0()
    print(f"  ✓ Found {len(stage_gate.deliverables)} deliverables")
    
    # Count by functional area
    areas = {}
    for d in stage_gate.deliverables:
        area = d.functional_area or "Unspecified"
        areas[area] = areas.get(area, 0) + 1
    
    print(f"  ✓ Across {len(areas)} functional areas:")
    for area, count in sorted(areas.items()):
        print(f"    - {area}: {count} deliverables")
    print()
    
    # Step 2: Generate TTL
    print("Step 2: Generating RDF/TTL representation...")
    ttl_content = generate_ttl(stage_gate)
    ttl_path = Path("stage_gate_0_example.ttl")
    ttl_path.write_text(ttl_content)
    print(f"  ✓ Written to {ttl_path}")
    print(f"  ✓ Size: {len(ttl_content)} bytes")
    print()
    
    # Step 3: Generate SPARQL queries
    print("Step 3: Generating validation SPARQL queries...")
    queries = generate_sparql_queries()
    queries_path = Path("stage_gate_0_queries.sparql")
    
    with open(queries_path, 'w') as f:
        for name, query in queries.items():
            f.write(f"# Query: {name}\n")
            f.write(query)
            f.write("\n" + "-" * 40 + "\n\n")
    
    print(f"  ✓ {len(queries)} queries written to {queries_path}")
    print()
    
    # Step 4: Generate JSON summary
    print("Step 4: Generating JSON summary...")
    json_content = create_json_summary(stage_gate)
    json_path = Path("stage_gate_0_summary.json")
    json_path.write_text(json_content)
    print(f"  ✓ Written to {json_path}")
    print()
    
    # Print sample of the first deliverable details
    print("Sample Deliverable Details:")
    print("-" * 40)
    if stage_gate.deliverables:
        d = stage_gate.deliverables[0]
        print(f"  Functional Area: {d.functional_area}")
        print(f"  Deliverable: {d.deliverable_text[:80]}...")
        print(f"  Owner: {d.owner or 'Not specified'}")
        print(f"  Status: {d.status or 'Not specified'}")
    print()
    
    print("✅ Stage Gate 0 example generation complete!")
    print()
    print("Next steps:")
    print("  1. Load stage_gate_0_example.ttl into a triple store")
    print("  2. Run queries from stage_gate_0_queries.sparql")
    print("  3. Use stage_gate_0_summary.json for reporting/visualization")
    

if __name__ == "__main__":
    main()


