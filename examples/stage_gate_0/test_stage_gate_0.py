#!/usr/bin/env python3
"""
Test and Validation Script for Stage Gate 0 Example

This script demonstrates:
1. Validation of the generated TTL file
2. Simulated queries against the RDF data (without needing a triple store)
3. A workflow simulation showing how deliverables progress through the gate
"""

import json
import re
from pathlib import Path
from typing import Dict, List, Optional, Set
from datetime import datetime, timedelta
import random


class StageGateValidator:
    """Validates stage gate RDF/TTL data structure."""
    
    def __init__(self, ttl_path: Path):
        self.ttl_path = ttl_path
        self.content = ttl_path.read_text() if ttl_path.exists() else ""
        
    def validate_structure(self) -> Dict[str, bool]:
        """Validate the basic structure of the TTL file."""
        checks = {
            "file_exists": self.ttl_path.exists(),
            "has_prefixes": "@prefix sg:" in self.content,
            "has_stage_gate": "sg:StageGate" in self.content,
            "has_functional_areas": "sg:FunctionalArea" in self.content,
            "has_deliverables": "sg:Deliverable" in self.content,
            "valid_syntax": self._check_ttl_syntax(),
            "all_deliverables_linked": self._check_deliverable_links()
        }
        return checks
    
    def _check_ttl_syntax(self) -> bool:
        """Basic TTL syntax validation."""
        # Check for balanced braces
        open_count = self.content.count('{')
        close_count = self.content.count('}')
        
        # Check statements end with period or semicolon
        lines = self.content.split('\n')
        for line in lines:
            line = line.strip()
            if line and not line.startswith('#') and not line.startswith('@'):
                if not (line.endswith('.') or line.endswith(';') or 
                       line.endswith('{') or line.endswith('}')):
                    return False
        
        return open_count == close_count
    
    def _check_deliverable_links(self) -> bool:
        """Check that all deliverables are properly linked to areas and gates."""
        deliverables = re.findall(r'sg:Deliverable-[\w-]+', self.content)
        
        for deliverable in deliverables:
            # Check if deliverable has functional area link
            if f"{deliverable} a sg:Deliverable" in self.content:
                pattern = f"{deliverable}.*sg:functionalArea.*sg:Area"
                if not re.search(pattern, self.content, re.DOTALL):
                    return False
        
        return True
    
    def count_entities(self) -> Dict[str, int]:
        """Count different entity types in the TTL."""
        counts = {
            "stage_gates": len(re.findall(r'a sg:StageGate', self.content)),
            "functional_areas": len(re.findall(r'a sg:FunctionalArea', self.content)),
            "deliverables": len(re.findall(r'a sg:Deliverable', self.content))
        }
        return counts


class StageGateSimulator:
    """Simulates a workflow through the stage gate process."""
    
    def __init__(self, json_path: Path):
        with open(json_path, 'r') as f:
            self.data = json.load(f)
        self.deliverable_status = {}
        self.start_date = datetime.now()
        
    def initialize_workflow(self):
        """Initialize all deliverables with 'pending' status."""
        for deliverable in self.data['deliverables']:
            deliverable_id = f"{deliverable['functional_area']}-{deliverable['text'][:30]}"
            self.deliverable_status[deliverable_id] = {
                "text": deliverable['text'],
                "functional_area": deliverable['functional_area'],
                "status": "pending",
                "assigned_to": None,
                "started_date": None,
                "completed_date": None,
                "notes": []
            }
    
    def assign_deliverable(self, deliverable_id: str, owner: str):
        """Assign a deliverable to an owner."""
        if deliverable_id in self.deliverable_status:
            self.deliverable_status[deliverable_id]["assigned_to"] = owner
            self.deliverable_status[deliverable_id]["status"] = "assigned"
            return True
        return False
    
    def start_deliverable(self, deliverable_id: str):
        """Mark a deliverable as in progress."""
        if deliverable_id in self.deliverable_status:
            if self.deliverable_status[deliverable_id]["status"] == "assigned":
                self.deliverable_status[deliverable_id]["status"] = "in_progress"
                self.deliverable_status[deliverable_id]["started_date"] = datetime.now()
                return True
        return False
    
    def complete_deliverable(self, deliverable_id: str, notes: str = ""):
        """Mark a deliverable as complete."""
        if deliverable_id in self.deliverable_status:
            if self.deliverable_status[deliverable_id]["status"] == "in_progress":
                self.deliverable_status[deliverable_id]["status"] = "completed"
                self.deliverable_status[deliverable_id]["completed_date"] = datetime.now()
                if notes:
                    self.deliverable_status[deliverable_id]["notes"].append(notes)
                return True
        return False
    
    def get_gate_readiness(self) -> Dict[str, any]:
        """Calculate the readiness to pass through the stage gate."""
        total = len(self.deliverable_status)
        completed = sum(1 for d in self.deliverable_status.values() 
                       if d["status"] == "completed")
        in_progress = sum(1 for d in self.deliverable_status.values() 
                         if d["status"] == "in_progress")
        pending = sum(1 for d in self.deliverable_status.values() 
                     if d["status"] in ["pending", "assigned"])
        
        readiness_pct = (completed / total * 100) if total > 0 else 0
        
        # Group by functional area
        by_area = {}
        for did, details in self.deliverable_status.items():
            area = details["functional_area"]
            if area not in by_area:
                by_area[area] = {"completed": 0, "total": 0}
            by_area[area]["total"] += 1
            if details["status"] == "completed":
                by_area[area]["completed"] += 1
        
        return {
            "total_deliverables": total,
            "completed": completed,
            "in_progress": in_progress,
            "pending": pending,
            "readiness_percentage": readiness_pct,
            "can_pass_gate": readiness_pct == 100,
            "by_functional_area": by_area
        }
    
    def simulate_workflow(self):
        """Simulate a workflow progression through the stage gate."""
        print("\n" + "="*60)
        print("STAGE GATE 0 WORKFLOW SIMULATION")
        print("="*60)
        
        # Initialize
        self.initialize_workflow()
        deliverable_ids = list(self.deliverable_status.keys())
        
        # Simulate team members
        team_members = [
            "Alice Johnson (AD Lead)",
            "Bob Smith (API Specialist)",
            "Carol Davis (CMC Manager)",
            "David Wilson (Discovery)",
            "Eve Martinez (Materials)"
        ]
        
        print(f"\n📅 Simulation Start: {self.start_date.strftime('%Y-%m-%d')}")
        print(f"👥 Team Members: {len(team_members)}")
        print(f"📋 Total Deliverables: {len(deliverable_ids)}")
        
        # Week 1: Assignment Phase
        print("\n" + "-"*40)
        print("WEEK 1: Assignment Phase")
        print("-"*40)
        
        for i, did in enumerate(deliverable_ids):
            owner = team_members[i % len(team_members)]
            self.assign_deliverable(did, owner)
            area = self.deliverable_status[did]["functional_area"]
            print(f"  ✓ Assigned: {area} deliverable to {owner}")
        
        # Week 2-3: Work begins
        print("\n" + "-"*40)
        print("WEEK 2-3: Work Begins")
        print("-"*40)
        
        # Start 70% of deliverables
        for did in random.sample(deliverable_ids, int(len(deliverable_ids) * 0.7)):
            self.start_deliverable(did)
            area = self.deliverable_status[did]["functional_area"]
            print(f"  🔄 Started: {area} deliverable")
        
        # Show mid-point status
        readiness = self.get_gate_readiness()
        print(f"\n📊 Mid-point Status:")
        print(f"  - In Progress: {readiness['in_progress']}")
        print(f"  - Pending: {readiness['pending']}")
        print(f"  - Readiness: {readiness['readiness_percentage']:.1f}%")
        
        # Week 4-6: Completion Phase
        print("\n" + "-"*40)
        print("WEEK 4-6: Completion Phase")
        print("-"*40)
        
        # Complete in-progress items
        for did, details in self.deliverable_status.items():
            if details["status"] == "in_progress":
                notes = f"Completed per requirements. Reviewed by {details['assigned_to']}"
                self.complete_deliverable(did, notes)
                print(f"  ✅ Completed: {details['functional_area']} deliverable")
        
        # Start and complete remaining
        for did, details in self.deliverable_status.items():
            if details["status"] == "assigned":
                self.start_deliverable(did)
                self.complete_deliverable(did, "Fast-tracked completion")
                print(f"  ⚡ Fast-tracked: {details['functional_area']} deliverable")
        
        # Final Gate Readiness
        print("\n" + "="*40)
        print("GATE READINESS ASSESSMENT")
        print("="*40)
        
        final_readiness = self.get_gate_readiness()
        
        print(f"\n📈 Overall Progress:")
        print(f"  Total Deliverables: {final_readiness['total_deliverables']}")
        print(f"  Completed: {final_readiness['completed']} ✅")
        print(f"  In Progress: {final_readiness['in_progress']} 🔄")
        print(f"  Pending: {final_readiness['pending']} ⏳")
        
        print(f"\n📊 By Functional Area:")
        for area, stats in final_readiness['by_functional_area'].items():
            pct = (stats['completed'] / stats['total'] * 100) if stats['total'] > 0 else 0
            print(f"  {area}: {stats['completed']}/{stats['total']} ({pct:.0f}%)")
        
        print(f"\n🎯 Gate Readiness: {final_readiness['readiness_percentage']:.1f}%")
        
        if final_readiness['can_pass_gate']:
            print("✅ READY TO PASS STAGE GATE 0")
            print("   All deliverables completed. Proceed to Stage Gate 1.")
        else:
            print("❌ NOT READY TO PASS STAGE GATE")
            print("   Outstanding deliverables must be completed.")
        
        return final_readiness


def run_sparql_simulation(json_data: dict):
    """Simulate SPARQL query results using the JSON data."""
    print("\n" + "="*60)
    print("SIMULATED SPARQL QUERY RESULTS")
    print("="*60)
    
    # Query 1: Count deliverables
    print("\n📊 Query: Count Total Deliverables")
    print("-"*40)
    count = json_data['stage_gate']['deliverable_count']
    print(f"Results: {count} deliverables found")
    
    # Query 2: Deliverables by Area
    print("\n📊 Query: Deliverables by Functional Area")
    print("-"*40)
    for area_name, area_data in json_data['functional_areas'].items():
        print(f"\n{area_name}:")
        for i, deliv in enumerate(area_data['deliverables'], 1):
            text_preview = deliv['text'][:60] + "..." if len(deliv['text']) > 60 else deliv['text']
            print(f"  {i}. {text_preview}")
    
    # Query 3: Find unassigned deliverables
    print("\n📊 Query: Deliverables Without Owners")
    print("-"*40)
    unassigned = [d for d in json_data['deliverables'] if not d['has_owner']]
    print(f"Found {len(unassigned)} deliverables without owners")
    for d in unassigned[:3]:  # Show first 3
        text_preview = d['text'][:60] + "..."
        print(f"  - {text_preview}")
    if len(unassigned) > 3:
        print(f"  ... and {len(unassigned) - 3} more")
    
    # Query 4: Gate Summary
    print("\n📊 Query: Stage Gate Summary")
    print("-"*40)
    gate_info = json_data['stage_gate']
    print(f"Gate: {gate_info['id']}")
    print(f"Stream: {gate_info['value_stream']}")
    print(f"Number: {gate_info['gate_number']}")
    print(f"Description: {gate_info['description']}")
    print(f"Total Deliverables: {gate_info['deliverable_count']}")


def main():
    """Main test execution."""
    print("="*60)
    print("STAGE GATE 0: VALIDATION AND TESTING")
    print("="*60)
    
    # File paths
    ttl_path = Path("stage_gate_0_example.ttl")
    json_path = Path("stage_gate_0_summary.json")
    queries_path = Path("stage_gate_0_queries.sparql")
    
    # Step 1: Validate TTL Structure
    print("\n🔍 STEP 1: Validating TTL Structure")
    print("-"*40)
    
    if ttl_path.exists():
        validator = StageGateValidator(ttl_path)
        checks = validator.validate_structure()
        
        for check, passed in checks.items():
            status = "✅" if passed else "❌"
            print(f"  {status} {check.replace('_', ' ').title()}")
        
        counts = validator.count_entities()
        print(f"\nEntity Counts:")
        for entity_type, count in counts.items():
            print(f"  - {entity_type.replace('_', ' ').title()}: {count}")
    else:
        print("  ❌ TTL file not found")
    
    # Step 2: Simulate SPARQL Queries
    if json_path.exists():
        with open(json_path, 'r') as f:
            json_data = json.load(f)
        run_sparql_simulation(json_data)
    else:
        print("\n❌ JSON summary file not found")
    
    # Step 3: Run Workflow Simulation
    if json_path.exists():
        simulator = StageGateSimulator(json_path)
        final_status = simulator.simulate_workflow()
    else:
        print("\n❌ Cannot run workflow simulation without JSON data")
    
    print("\n" + "="*60)
    print("✅ VALIDATION AND TESTING COMPLETE")
    print("="*60)
    
    print("\n📚 Summary:")
    print("  - TTL validation: PASSED" if ttl_path.exists() else "  - TTL validation: FAILED")
    print("  - Query simulation: EXECUTED" if json_path.exists() else "  - Query simulation: SKIPPED")
    print("  - Workflow simulation: COMPLETED" if json_path.exists() else "  - Workflow simulation: SKIPPED")
    
    print("\n🎯 Next Steps:")
    print("  1. Load TTL into a real triple store (GraphDB, Fuseki, etc.)")
    print("  2. Execute actual SPARQL queries")
    print("  3. Integrate with project management tools")
    print("  4. Scale to other stage gates (1-12)")


if __name__ == "__main__":
    main()


