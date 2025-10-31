#!/usr/bin/env python3
"""
Stage Gate Flow Visualization
Shows the relationship between stages and gates, with focus on Gate 0
"""

import csv
from pathlib import Path
from collections import defaultdict


def analyze_stage_gate_progression():
    """Analyze the progression of stages and gates from the source data."""
    
    csv_path = Path("/Users/nicholasbaro/Python/staged/data/extracted/"
                    "Protein_and_CGT_SGD_Template_Final_ENDORSED_JAN_2023__SGD.csv")
    
    # Collect unique gates and their descriptions
    gates = {}
    gate_deliverables = defaultdict(int)
    
    with open(csv_path, 'r', encoding='utf-8') as f:
        reader = csv.reader(f)
        next(reader)  # Skip first row
        headers = next(reader)  # Get headers
        
        for row in reader:
            if len(row) < 6:
                continue
                
            value_stream = row[0]
            gate_num = row[1]
            gate_desc = row[2]
            deliverable = row[5] if len(row) > 5 else ""
            
            if value_stream == "CGT" and gate_num.isdigit():
                gate_key = int(gate_num)
                if gate_key not in gates:
                    gates[gate_key] = gate_desc
                if deliverable.strip():
                    gate_deliverables[gate_key] += 1
    
    return gates, gate_deliverables


def create_stage_gate_flow_diagram():
    """Create a comprehensive flow diagram showing stages and gates."""
    
    gates, deliverable_counts = analyze_stage_gate_progression()
    
    # Define the stages between gates based on pharmaceutical development
    stage_flow = """
    ================================================================================
                        CGT STAGE GATE PROCESS FLOW
    ================================================================================
    
    STAGES AND GATES RELATIONSHIP:
    ━━━━━━━━━━━━━━━━━━━━━━━━━━━━
    
    A "Stage" is a development phase where work happens
    A "Gate" is a checkpoint/review between stages
    
    ┌─────────────────────────────────────────────────────────────────────┐
    │                     THE COMPLETE STAGE FLOW                         │
    └─────────────────────────────────────────────────────────────────────┘
    
    DISCOVERY STAGE
    ═══════════════
    • Basic research
    • Target identification
    • Lead optimization
    • Proof of concept
           │
           │
           ▼
    ╔═══════════════╗
    ║    GATE 0     ║  Entry in Early Development (C&GT)
    ╚═══════════════╝  17 deliverables required
           │           Review: Ready for development?
           │
           ▼
    EARLY DEVELOPMENT STAGE
    ═══════════════════════
    • Process development
    • Analytical method development  
    • Early safety studies
    • Formulation development
           │
           │
           ▼
    ╔═══════════════╗
    ║    GATE 1     ║  NME Selection
    ╚═══════════════╝  71 deliverables required
           │           Review: Candidate selected?
           │
           ▼
    PHASE 1/2 PREPARATION STAGE
    ═══════════════════════════
    • Manufacturing readiness
    • Clinical protocol development
    • Regulatory documentation
    • Safety assessments
           │
           │
           ▼
    ╔═══════════════╗
    ║    GATE 2     ║  Ph1/2 Manufacturing Readiness
    ╚═══════════════╝  88 deliverables required
           │           Review: Ready for clinical trials?
           │
           ▼
    CLINICAL PHASE 1/2 STAGE
    ════════════════════════
    • First-in-human studies
    • Safety evaluation
    • Dose finding
    • Early efficacy signals
           │
           │
           ▼
    ╔═══════════════╗
    ║    GATE 3     ║  FIH (First in Human) Readiness
    ╚═══════════════╝  65 deliverables required
           │           Review: Continue development?
           │
           ▼
    PHASE 2B/3 PREPARATION STAGE
    ════════════════════════════
    • Scale-up development
    • Process optimization
    • Commercial readiness planning
           │
           │
           ▼
    ╔═══════════════╗
    ║    GATE 4     ║  Entry into Full Development
    ╚═══════════════╝  72 deliverables required
           │           Review: Commit to Phase 3?
           │
           ▼
    [Continues through Gates 5-12...]
    
    ────────────────────────────────────────────────────────────────────
    
    FOCUS: GATE 0 IN CONTEXT
    ═════════════════════════
    
    Where Gate 0 Fits:
    ┌────────────────┐
    │  DISCOVERY     │  ← Pre-clinical research
    │    STAGE       │    Target validation
    └────────┬───────┘    Lead optimization
             │
             ▼
    ┌────────────────┐
    │    GATE 0      │  ← DECISION POINT
    │  Entry in ED   │    Must complete 17 deliverables
    │    Review      │    Cross-functional assessment
    └────────┬───────┘    Go/No-Go decision
             │
             ▼
    ┌────────────────┐
    │     EARLY      │  ← Development begins
    │  DEVELOPMENT   │    Process development
    │     STAGE      │    Method development
    └────────────────┘    Preparation for Gate 1
    
    ────────────────────────────────────────────────────────────────────
    """
    
    # Add gate details
    gate_details = "\n    GATE DETAILS (CGT Stream):\n"
    gate_details += "    " + "─" * 60 + "\n"
    
    for gate_num in sorted(gates.keys()):
        if gate_num <= 5:  # Show first 6 gates
            desc = gates[gate_num]
            count = deliverable_counts.get(gate_num, 0)
            gate_details += f"    Gate {gate_num}: {desc}\n"
            gate_details += f"            Deliverables: {count}\n\n"
    
    return stage_flow + gate_details


def create_gate_0_context():
    """Create detailed context for Gate 0."""
    
    context = """
    ================================================================================
                            GATE 0: DETAILED CONTEXT
    ================================================================================
    
    WHAT HAPPENS BEFORE GATE 0 (Discovery Stage):
    ──────────────────────────────────────────────
    
    Discovery Stage Activities:
    • Target identification and validation
    • Lead compound optimization
    • Proof of concept studies
    • Initial safety assessment
    • Intellectual property evaluation
    • Technology transfer preparation
    
    Key Outputs from Discovery:
    • Validated therapeutic target
    • Lead candidate molecule
    • Preliminary safety data
    • IP documentation
    • Technology transfer package
    
    
    GATE 0 REVIEW (Entry in Early Development):
    ────────────────────────────────────────────
    
    Purpose: Transition from Discovery to Development
    
    17 Deliverables Required Across:
    • Analytical Development (4)
      - Method alignment
      - Data review
      - Reagent identification
      - De novo method needs
      
    • API Cell & Gene (3)
      - Plasmid construct review
      - Sequencing completion
      - Sourcing committee approval
      
    • CMC Leadership (7)
      - EHS requirements
      - Risk assessment
      - Team assignments
      - Target molecule profile
      - Critical questions
      - Material sourcing strategy
      - Donor material alignment
      
    • Discovery (2)
      - Knowledge transfer
      - IPSC meetings
      
    • Material Sciences (1)
      - Material/supplier selection
    
    
    WHAT HAPPENS AFTER GATE 0 (Early Development Stage):
    ─────────────────────────────────────────────────────
    
    Early Development Stage Activities:
    • Process development and optimization
    • Analytical method development
    • Formulation development
    • Manufacturing process design
    • Scale-up planning
    • Stability studies initiation
    • Regulatory strategy development
    • Preparation for NME selection (Gate 1)
    
    Key Outputs for Gate 1:
    • Defined manufacturing process
    • Validated analytical methods
    • Preliminary formulation
    • Regulatory strategy
    • Development timeline
    • Resource requirements
    
    ================================================================================
    
    CRITICAL SUCCESS FACTORS FOR GATE 0:
    ────────────────────────────────────
    
    1. Knowledge Transfer
       ✓ Complete handoff from Discovery to Development
       ✓ All technical documentation transferred
       ✓ Key personnel briefed and aligned
    
    2. Resource Readiness
       ✓ Team assignments confirmed
       ✓ Budget allocated
       ✓ Facilities identified
    
    3. Technical Foundation
       ✓ Methods aligned between teams
       ✓ Critical reagents identified
       ✓ Plasmid/vector sequences verified
    
    4. Regulatory & Compliance
       ✓ EHS requirements defined
       ✓ IP freedom to operate confirmed
       ✓ Donor material strategy aligned
    
    5. Risk Management
       ✓ Risk register initiated
       ✓ Critical questions documented
       ✓ Mitigation plans in place
    
    ================================================================================
    """
    
    return context


def main():
    """Generate stage and gate flow visualizations."""
    
    print(create_stage_gate_flow_diagram())
    print(create_gate_0_context())
    
    # Summary
    print("=" * 80)
    print("SUMMARY: Gate 0 bridges Discovery and Early Development stages")
    print("=" * 80)
    print()
    print("• BEFORE Gate 0: Discovery Stage (research & target validation)")
    print("• AT Gate 0:     Review checkpoint (17 deliverables)")
    print("• AFTER Gate 0:  Early Development Stage (process & method development)")
    print()
    print("Gate 0 ensures readiness to transition from research to development.")
    print("=" * 80)


if __name__ == "__main__":
    main()


