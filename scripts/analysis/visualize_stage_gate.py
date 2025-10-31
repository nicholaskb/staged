#!/usr/bin/env python3
"""
Visual representation of the Stage Gate 0 workflow.
Creates ASCII art diagrams and visual summaries.
"""

import json
from pathlib import Path
from datetime import datetime, timedelta
from typing import Dict, List


def print_header(title: str, char: str = "=", width: int = 80):
    """Print a formatted header."""
    print(f"\n{char * width}")
    print(f"{title.center(width)}")
    print(f"{char * width}\n")


def create_stage_gate_diagram():
    """Create ASCII art diagram of the stage gate process."""
    
    diagram = """
    STAGE GATE 0: Entry in Early Development (C&GT)
    ================================================
    
    Discovery Phase                    Early Development Phase
    ───────────────                    ─────────────────────────
         │                                      │
         │                                      │
         ▼                                      ▼
    ┌─────────┐      Gate 0 Review      ┌──────────────┐
    │Discovery│ ──────────────────────> │Early Dev (ED)│
    └─────────┘          │              └──────────────┘
                         │                      │
                    ┌────▼────┐                 │
                    │ GATE 0  │                 ▼
                    │ 17 Deliv│           [To Gate 1]
                    └─────────┘
                         │
                ┌────────┴────────┐
                │                 │
        ┌───────▼──────┐ ┌───────▼──────┐
        │ Pass Gate    │ │ Remediation  │
        │ → Proceed    │ │ → Fix Issues │
        └──────────────┘ └──────────────┘
    
    Functional Areas at Gate 0:
    ─────────────────────────────
    • Analytical Development (AD) ────── 4 deliverables
    • API (Cell & Gene) ──────────────── 3 deliverables  
    • CMC Leadership (CMC-L) ─────────── 7 deliverables
    • Discovery ──────────────────────── 2 deliverables
    • Material Sciences (MS) ─────────── 1 deliverable
                                        ───
                                 Total: 17 deliverables
    """
    return diagram


def create_workflow_timeline():
    """Create a timeline visualization of the workflow."""
    
    timeline = """
    WORKFLOW TIMELINE
    ═════════════════
    
    Week 1: Assignment Phase
    ├─ Day 1-2: Team kickoff & orientation
    ├─ Day 3-4: Deliverable assignment
    └─ Day 5:   Initial planning complete
    
    Week 2-3: Execution Phase  
    ├─ Week 2:  70% deliverables started
    ├─ Mid-point review & risk assessment
    └─ Week 3:  Continued execution
    
    Week 4-6: Completion Phase
    ├─ Week 4:  First deliverables completed
    ├─ Week 5:  Accelerated completion
    └─ Week 6:  Final reviews & gate prep
    
    Gate Review Day
    ├─ Morning:   Final deliverable check
    ├─ Afternoon: Gate review meeting
    └─ Decision:  Pass/Fail determination
    
    Progress Bar:
    [██████████████████████████████] 100% Complete
    """
    return timeline


def create_deliverable_matrix(json_path: Path):
    """Create a matrix view of deliverables by area and status."""
    
    if not json_path.exists():
        return "JSON file not found"
    
    with open(json_path, 'r') as f:
        data = json.load(f)
    
    matrix = []
    matrix.append("DELIVERABLE STATUS MATRIX")
    matrix.append("=" * 60)
    matrix.append("")
    matrix.append("Legend: ✓ Complete  ⚡ In Progress  ○ Pending")
    matrix.append("")
    
    # Header
    matrix.append(f"{'Functional Area':<30} {'Deliverables':<10} {'Status':<20}")
    matrix.append("-" * 60)
    
    # Data rows
    for area_name, area_data in data['functional_areas'].items():
        area_short = area_name[:28] + ".." if len(area_name) > 30 else area_name
        count = area_data['deliverable_count']
        
        # Simulate status (in real implementation, would track actual status)
        status_bar = "✓" * count  # All complete in final state
        
        matrix.append(f"{area_short:<30} {count:<10} {status_bar}")
    
    matrix.append("-" * 60)
    total = data['stage_gate']['deliverable_count']
    matrix.append(f"{'TOTAL':<30} {total:<10} {'✓' * 17}")
    
    return "\n".join(matrix)


def create_risk_assessment():
    """Create a risk assessment visualization."""
    
    assessment = """
    RISK ASSESSMENT FOR GATE 0
    ══════════════════════════
    
    Risk Categories:
    
    1. TECHNICAL RISKS
       ├─ Plasmid sequencing delays      [LOW]    ●○○○○
       ├─ Method development gaps         [MEDIUM] ●●●○○
       └─ Material sourcing issues        [LOW]    ●○○○○
    
    2. REGULATORY RISKS
       ├─ EHS classification incomplete   [LOW]    ●○○○○
       ├─ Donor material compliance       [MEDIUM] ●●●○○
       └─ GMO strategy alignment          [LOW]    ●○○○○
    
    3. RESOURCE RISKS
       ├─ Team availability               [LOW]    ●○○○○
       ├─ Budget constraints              [LOW]    ●○○○○
       └─ Timeline pressure               [MEDIUM] ●●●○○
    
    4. QUALITY RISKS
       ├─ Knowledge transfer gaps         [MEDIUM] ●●●○○
       ├─ Documentation incomplete        [LOW]    ●○○○○
       └─ Review process delays           [LOW]    ●○○○○
    
    Overall Risk Level: LOW-MEDIUM
    Mitigation: Standard processes with enhanced monitoring
    """
    return assessment


def create_decision_tree():
    """Create a decision tree for gate passage."""
    
    tree = """
    GATE 0 DECISION TREE
    ════════════════════
    
    Start: Are all 17 deliverables complete?
                    │
           ┌────────┴────────┐
           │                 │
         YES                NO
           │                 │
           ▼                 ▼
    Documentation      Identify gaps
       complete?            │
           │                ▼
    ┌──────┴──────┐   Create remediation
    │             │         plan
   YES           NO         │
    │             │         ▼
    ▼             └────> Schedule
   Quality               follow-up
   review                    │
   passed?                   ▼
    │                   [Return to
    ├─YES               execution]
    │  │
    │  ▼
    │ Risk assessment
    │ acceptable?
    │  │
    │  ├─YES → PASS GATE 0 → Proceed to Gate 1
    │  │
    │  └─NO → Mitigation required → Re-assess
    │
    └─NO → Remediation required → Re-review
    """
    return tree


def main():
    """Generate all visualizations."""
    
    print_header("STAGE GATE 0: VISUAL WORKFLOW REPRESENTATION")
    
    # 1. Stage Gate Diagram
    print(create_stage_gate_diagram())
    
    # 2. Workflow Timeline
    print("\n")
    print(create_workflow_timeline())
    
    # 3. Deliverable Matrix
    print("\n")
    json_path = Path("stage_gate_0_summary.json")
    if json_path.exists():
        print(create_deliverable_matrix(json_path))
    
    # 4. Risk Assessment
    print("\n")
    print(create_risk_assessment())
    
    # 5. Decision Tree
    print("\n")
    print(create_decision_tree())
    
    # Summary Statistics
    print_header("SUMMARY STATISTICS", char="─", width=60)
    
    if json_path.exists():
        with open(json_path, 'r') as f:
            data = json.load(f)
        
        print(f"Stage Gate:        {data['stage_gate']['id']}")
        print(f"Value Stream:      {data['stage_gate']['value_stream']}")
        print(f"Description:       {data['stage_gate']['description']}")
        print(f"Total Deliverables: {data['stage_gate']['deliverable_count']}")
        print(f"Functional Areas:   {len(data['functional_areas'])}")
        print(f"Generated:         {data['stage_gate']['generated_at']}")
    
    print("\n" + "─" * 60)
    print("Visualization complete. Ready for gate review.")
    print("─" * 60)


if __name__ == "__main__":
    main()


