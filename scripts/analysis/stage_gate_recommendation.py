#!/usr/bin/env python3
"""
Stage Gate Recommendation Analysis
Analyzes all stage gates and recommends the best 1-2 for initial ontology modeling
"""

import csv
from pathlib import Path
from collections import defaultdict
from typing import Dict, List, Tuple


def analyze_all_stage_gates():
    """Analyze complexity and characteristics of all stage gates."""
    
    csv_path = Path("/Users/nicholasbaro/Python/staged/data/extracted/"
                    "Protein_and_CGT_SGD_Template_Final_ENDORSED_JAN_2023__SGD.csv")
    
    gate_stats = defaultdict(lambda: {
        'description': '',
        'deliverables': 0,
        'functional_areas': set(),
        'has_owners': 0,
        'has_status': 0,
        'categories': set(),
        'complexity_factors': []
    })
    
    with open(csv_path, 'r', encoding='utf-8') as f:
        reader = csv.reader(f)
        next(reader)  # Skip first row
        headers = next(reader)  # Get headers
        
        for row in reader:
            if len(row) < 11:
                continue
                
            value_stream = row[0]
            gate_num = row[1]
            gate_desc = row[2]
            functional_area = row[3]
            category = row[4]
            deliverable = row[5]
            owner = row[7] if len(row) > 7 else ""
            status = row[8] if len(row) > 8 else ""
            
            if value_stream == "CGT" and gate_num.isdigit():
                gate_key = int(gate_num)
                
                if not gate_stats[gate_key]['description']:
                    gate_stats[gate_key]['description'] = gate_desc
                
                if deliverable.strip():
                    gate_stats[gate_key]['deliverables'] += 1
                    
                if functional_area.strip():
                    gate_stats[gate_key]['functional_areas'].add(functional_area.strip())
                    
                if category.strip():
                    gate_stats[gate_key]['categories'].add(category.strip())
                    
                if owner.strip():
                    gate_stats[gate_key]['has_owners'] += 1
                    
                if status.strip():
                    gate_stats[gate_key]['has_status'] += 1
    
    # Calculate complexity scores
    for gate_num, stats in gate_stats.items():
        complexity_score = 0
        factors = []
        
        # Deliverable count factor
        deliv_count = stats['deliverables']
        if deliv_count < 30:
            complexity_score += 1
            factors.append("Low deliverable count")
        elif deliv_count < 70:
            complexity_score += 2
            factors.append("Medium deliverable count")
        else:
            complexity_score += 3
            factors.append("High deliverable count")
        
        # Functional area diversity
        area_count = len(stats['functional_areas'])
        if area_count <= 5:
            complexity_score += 1
            factors.append("Few functional areas")
        elif area_count <= 8:
            complexity_score += 2
            factors.append("Moderate functional areas")
        else:
            complexity_score += 3
            factors.append("Many functional areas")
        
        # Data completeness
        if stats['has_owners'] > deliv_count * 0.5:
            complexity_score += 1
            factors.append("Good owner coverage")
        
        stats['complexity_score'] = complexity_score
        stats['complexity_factors'] = factors
    
    return gate_stats


def generate_recommendation_report():
    """Generate a recommendation report for stage gate selection."""
    
    gate_stats = analyze_all_stage_gates()
    
    print("=" * 80)
    print("STAGE GATE ANALYSIS & RECOMMENDATION REPORT")
    print("=" * 80)
    print()
    
    print("ALL CGT STAGE GATES OVERVIEW:")
    print("-" * 80)
    
    # Sort by gate number
    sorted_gates = sorted(gate_stats.items())
    
    for gate_num, stats in sorted_gates:
        if gate_num <= 5:  # Show first 6 gates for clarity
            print(f"\nGate {gate_num}: {stats['description']}")
            print(f"  • Deliverables: {stats['deliverables']}")
            print(f"  • Functional Areas: {len(stats['functional_areas'])}")
            print(f"  • Categories: {len(stats['categories'])}")
            print(f"  • Complexity Score: {stats['complexity_score']}/7")
            print(f"  • Factors: {', '.join(stats['complexity_factors'])}")
    
    print("\n" + "=" * 80)
    print("RECOMMENDATION FOR ONTOLOGY MODELING")
    print("=" * 80)
    print()
    
    print("RECOMMENDED STAGE GATES: Gate 0 and Gate 3")
    print("-" * 40)
    print()
    
    print("RATIONALE:")
    print()
    
    print("1. GATE 0 - Entry in Early Development (C&GT)")
    print("   WHY SELECTED:")
    print("   • Simplest structure (17 deliverables) - ideal for initial modeling")
    print("   • Clear transition point (Discovery → Development)")
    print("   • Complete functional area coverage (5 areas)")
    print("   • Foundation gate - all projects must pass through")
    print("   • Low complexity allows focus on ontology design")
    print()
    
    print("2. GATE 3 - First in Human (FIH) Readiness")
    print("   WHY SELECTED:")
    print("   • Medium complexity (65 deliverables) - good scaling test")
    print("   • Critical regulatory milestone - rich criteria/requirements")
    print("   • Safety-focused - extensive risk modeling opportunities")
    print("   • Multiple artifact types (protocols, reports, approvals)")
    print("   • Cross-functional dependencies clearly defined")
    print()
    
    print("BENEFITS OF THIS COMBINATION:")
    print("• Covers both simple and medium complexity")
    print("• Spans pre-clinical to clinical transition")
    print("• Includes regulatory, safety, and technical aspects")
    print("• Progressive complexity for iterative development")
    print("• Rich variety of deliverable types and criteria")
    
    print("\n" + "=" * 80)
    print("ONTOLOGY ELEMENTS TO MODEL:")
    print("-" * 80)
    print("""
    Core Elements:
    ─────────────
    • STAGE:       Development phase between gates
    • GATE:        Review checkpoint with go/no-go decision
    • DELIVERABLE: Specific output/artifact required
    • ARTIFACT:    Document, dataset, or other tangible output
    • CRITERION:   Testable condition for acceptance
    • ROLE:        Person/team responsible
    • RISK:        Identified project/technical/regulatory risk
    • MILESTONE:   Key date or achievement
    • REQUIREMENT: Mandatory condition or specification
    
    Additional Elements:
    ───────────────────
    • DEPENDENCY:   Links between deliverables
    • REVIEW:       Gate review meeting/decision
    • ACTION_ITEM:  Tasks to complete deliverables
    • APPROVAL:     Sign-off or authorization
    • METRIC:       Measurable success indicator
    """)
    
    return gate_stats


def main():
    """Generate recommendation report."""
    gate_stats = generate_recommendation_report()
    
    print("\n" + "=" * 80)
    print("NEXT STEPS:")
    print("1. Create comprehensive ontology for Gate 0 (simple case)")
    print("2. Generate complete mock data for Gate 0 lifecycle")
    print("3. Extend model to Gate 3 (medium complexity)")
    print("4. Validate scalability and completeness")
    print("5. Generate RDF/TTL for knowledge graph")
    print("=" * 80)


if __name__ == "__main__":
    main()


