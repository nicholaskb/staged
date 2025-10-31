#!/usr/bin/env python3
"""
Comprehensive Stage Gate Ontology Model with Mock Data
Includes all requested elements: stage, gate, deliverables, artifacts,
criteria, roles, risks, milestones, and requirements
"""

import json
from datetime import datetime, timedelta
from pathlib import Path
from typing import Dict, List, Optional
from dataclasses import dataclass, field, asdict
import random
import uuid


# ============================================================================
# ONTOLOGY DATA MODELS
# ============================================================================

@dataclass
class Criterion:
    """A testable condition for acceptance."""
    id: str
    name: str
    description: str
    test_method: str
    acceptance_threshold: str
    measurement_unit: Optional[str] = None
    is_quantitative: bool = False
    
@dataclass
class Artifact:
    """A document, dataset, or other tangible output."""
    id: str
    name: str
    artifact_type: str  # document, dataset, report, approval, protocol
    format: str  # pdf, xlsx, json, csv, etc.
    version: str
    location: str
    size_bytes: Optional[int] = None
    checksum: Optional[str] = None

@dataclass
class Requirement:
    """A mandatory condition or specification."""
    id: str
    requirement_type: str  # regulatory, technical, quality, safety
    description: str
    source: str  # FDA, EMA, ICH, internal
    priority: str  # critical, high, medium, low
    is_mandatory: bool = True

@dataclass 
class Risk:
    """An identified project/technical/regulatory risk."""
    id: str
    risk_type: str  # technical, regulatory, resource, quality, safety
    description: str
    probability: str  # low, medium, high
    impact: str  # low, medium, high
    mitigation_strategy: str
    owner_role_id: str
    status: str = "identified"  # identified, mitigated, accepted, closed

@dataclass
class Milestone:
    """A key date or achievement."""
    id: str
    name: str
    description: str
    target_date: str
    actual_date: Optional[str] = None
    status: str = "planned"  # planned, on_track, delayed, completed
    dependencies: List[str] = field(default_factory=list)

@dataclass
class Role:
    """A person or team responsible for deliverables."""
    id: str
    name: str
    role_type: str  # individual, team, department
    department: str
    responsibilities: List[str]
    email: Optional[str] = None
    phone: Optional[str] = None

@dataclass
class Deliverable:
    """A specific output required for gate passage."""
    id: str
    name: str
    description: str
    functional_area: str
    artifact_ids: List[str]  # References to Artifacts
    criterion_ids: List[str]  # References to Criteria
    requirement_ids: List[str]  # References to Requirements
    owner_role_id: str  # Reference to Role
    approver_role_ids: List[str]  # References to Roles
    dependencies: List[str] = field(default_factory=list)
    status: str = "pending"
    due_date: Optional[str] = None
    completion_date: Optional[str] = None

@dataclass
class Gate:
    """A review checkpoint with go/no-go decision."""
    id: str
    gate_number: int
    name: str
    description: str
    deliverable_ids: List[str]
    milestone_ids: List[str]
    risk_ids: List[str]
    review_date: Optional[str] = None
    decision: Optional[str] = None  # pass, conditional_pass, fail, deferred
    decision_rationale: Optional[str] = None

@dataclass
class Stage:
    """A development phase between gates."""
    id: str
    name: str
    description: str
    start_date: str
    end_date: str
    preceding_gate_id: Optional[str]
    following_gate_id: str
    milestone_ids: List[str]
    activities: List[str]
    resource_requirements: Dict[str, any] = field(default_factory=dict)


# ============================================================================
# MOCK DATA GENERATOR FOR GATE 0
# ============================================================================

class Gate0MockDataGenerator:
    """Generates comprehensive mock data for Gate 0."""
    
    def __init__(self):
        self.base_date = datetime.now()
        self.roles = {}
        self.artifacts = {}
        self.criteria = {}
        self.requirements = {}
        self.risks = {}
        self.milestones = {}
        self.deliverables = {}
        
    def generate_all_data(self):
        """Generate complete mock data for Gate 0."""
        # Generate in dependency order
        self.generate_roles()
        self.generate_requirements()
        self.generate_criteria()
        self.generate_artifacts()
        self.generate_risks()
        self.generate_milestones()
        self.generate_deliverables()
        
        # Create stage and gate
        discovery_stage = self.generate_discovery_stage()
        gate_0 = self.generate_gate_0()
        early_dev_stage = self.generate_early_dev_stage()
        
        return {
            "stages": {
                discovery_stage.id: asdict(discovery_stage),
                early_dev_stage.id: asdict(early_dev_stage)
            },
            "gates": {
                gate_0.id: asdict(gate_0)
            },
            "deliverables": {k: asdict(v) for k, v in self.deliverables.items()},
            "artifacts": {k: asdict(v) for k, v in self.artifacts.items()},
            "criteria": {k: asdict(v) for k, v in self.criteria.items()},
            "requirements": {k: asdict(v) for k, v in self.requirements.items()},
            "risks": {k: asdict(v) for k, v in self.risks.items()},
            "milestones": {k: asdict(v) for k, v in self.milestones.items()},
            "roles": {k: asdict(v) for k, v in self.roles.items()}
        }
    
    def generate_roles(self):
        """Generate roles for Gate 0."""
        roles_data = [
            ("ad_lead", "Analytical Development Lead", "individual", "Analytical Development",
             ["Method development", "Data review", "Reagent planning"]),
            ("api_manager", "API Manager", "individual", "API Cell & Gene",
             ["Plasmid review", "Sequencing oversight", "Sourcing coordination"]),
            ("cmc_director", "CMC Director", "individual", "CMC Leadership",
             ["Risk assessment", "Team coordination", "Strategic planning"]),
            ("discovery_liaison", "Discovery Liaison", "individual", "Discovery",
             ["Knowledge transfer", "IPSC coordination", "Documentation"]),
            ("ms_specialist", "Material Sciences Specialist", "individual", "Material Sciences",
             ["Material selection", "Supplier qualification", "Quality assessment"]),
            ("qa_team", "Quality Assurance Team", "team", "Quality",
             ["Document review", "Compliance verification", "Approval workflow"]),
            ("regulatory_team", "Regulatory Affairs Team", "team", "Regulatory",
             ["EHS requirements", "Regulatory strategy", "Submission planning"])
        ]
        
        for role_id, name, role_type, dept, responsibilities in roles_data:
            self.roles[role_id] = Role(
                id=role_id,
                name=name,
                role_type=role_type,
                department=dept,
                responsibilities=responsibilities,
                email=f"{role_id}@pharma.com"
            )
    
    def generate_requirements(self):
        """Generate requirements for Gate 0."""
        requirements_data = [
            ("req_ehs_001", "regulatory", "EHS classification must be determined per 21 CFR 312", "FDA", "critical"),
            ("req_ip_001", "regulatory", "Freedom to operate analysis required for all sequences", "Legal", "critical"),
            ("req_donor_001", "regulatory", "Donor material must meet US/EU testing requirements", "FDA/EMA", "critical"),
            ("req_gmp_001", "quality", "GMP-grade plasmids required for clinical material", "ICH Q7", "high"),
            ("req_tech_001", "technical", "Full plasmid sequencing with 99.9% accuracy", "Internal", "high"),
            ("req_doc_001", "quality", "All knowledge transfer documented in controlled system", "Internal", "medium"),
            ("req_safety_001", "safety", "Biosafety level determination required", "CDC", "critical")
        ]
        
        for req_id, req_type, desc, source, priority in requirements_data:
            self.requirements[req_id] = Requirement(
                id=req_id,
                requirement_type=req_type,
                description=desc,
                source=source,
                priority=priority
            )
    
    def generate_criteria(self):
        """Generate acceptance criteria for Gate 0."""
        criteria_data = [
            ("crit_seq_001", "Sequence Identity", "Plasmid sequence must match reference", 
             "NGS sequencing", "≥99.9% identity", "%", True),
            ("crit_purity_001", "Plasmid Purity", "Endotoxin levels in plasmid prep",
             "LAL assay", "<5 EU/mg", "EU/mg", True),
            ("crit_kt_001", "Knowledge Transfer Completion", "All TD documents received",
             "Document checklist", "100% complete", "%", True),
            ("crit_team_001", "Team Readiness", "Core team members assigned",
             "Resource assessment", "All positions filled", None, False),
            ("crit_risk_001", "Risk Register Status", "Critical risks identified and mitigated",
             "Risk review", "No unmitigated critical risks", None, False),
            ("crit_method_001", "Method Alignment", "Analytical methods harmonized",
             "Method comparison", "≥95% correlation", "%", True)
        ]
        
        for crit_id, name, desc, method, threshold, unit, is_quant in criteria_data:
            self.criteria[crit_id] = Criterion(
                id=crit_id,
                name=name,
                description=desc,
                test_method=method,
                acceptance_threshold=threshold,
                measurement_unit=unit,
                is_quantitative=is_quant
            )
    
    def generate_artifacts(self):
        """Generate artifacts for Gate 0."""
        artifacts_data = [
            # Analytical Development artifacts
            ("art_method_align", "Method Alignment Report", "document", "pdf", "1.0",
             "/docs/gate0/method_alignment_v1.pdf"),
            ("art_data_review", "TD Data Review Summary", "document", "pdf", "1.0",
             "/docs/gate0/td_data_review.pdf"),
            ("art_reagent_plan", "Critical Reagent Plan", "document", "xlsx", "1.0",
             "/docs/gate0/reagent_plan.xlsx"),
            
            # API artifacts
            ("art_plasmid_seq", "Plasmid Sequence Report", "dataset", "json", "1.0",
             "/data/gate0/plasmid_sequence.json"),
            ("art_plasmid_map", "Plasmid Maps and Annotations", "document", "pdf", "2.1",
             "/docs/gate0/plasmid_maps.pdf"),
            ("art_sourcing_approval", "Sourcing Committee Approval", "approval", "pdf", "1.0",
             "/approvals/gate0/sourcing_approval.pdf"),
            
            # CMC Leadership artifacts
            ("art_risk_register", "Risk Register", "document", "xlsx", "3.2",
             "/docs/gate0/risk_register.xlsx"),
            ("art_target_profile", "Target Molecule Profile", "document", "pdf", "1.0",
             "/docs/gate0/target_molecule_profile.pdf"),
            ("art_critical_questions", "Critical Questions Document", "document", "docx", "1.1",
             "/docs/gate0/critical_questions.docx"),
            
            # Regulatory artifacts
            ("art_ehs_class", "EHS Classification Report", "document", "pdf", "1.0",
             "/docs/gate0/ehs_classification.pdf"),
            ("art_donor_strategy", "Donor Material Strategy", "document", "pdf", "1.0",
             "/docs/gate0/donor_strategy.pdf"),
            
            # Knowledge Transfer artifacts
            ("art_kt_package", "Knowledge Transfer Package", "dataset", "zip", "1.0",
             "/data/gate0/kt_package.zip"),
            ("art_ipsc_minutes", "IPSC Meeting Minutes", "document", "pdf", "1.0",
             "/docs/gate0/ipsc_minutes.pdf")
        ]
        
        for art_id, name, art_type, format, version, location in artifacts_data:
            self.artifacts[art_id] = Artifact(
                id=art_id,
                name=name,
                artifact_type=art_type,
                format=format,
                version=version,
                location=location,
                size_bytes=random.randint(50000, 5000000),
                checksum=uuid.uuid4().hex[:16]
            )
    
    def generate_risks(self):
        """Generate risks for Gate 0."""
        risks_data = [
            ("risk_seq_delay", "technical", "Plasmid sequencing contractor delay",
             "medium", "high", "Identify backup sequencing vendor", "api_manager"),
            ("risk_kt_gap", "technical", "Incomplete knowledge transfer from Discovery",
             "medium", "medium", "Schedule additional TD meetings", "discovery_liaison"),
            ("risk_resource", "resource", "Key AD personnel unavailable",
             "low", "high", "Cross-train backup resources", "ad_lead"),
            ("risk_reg_change", "regulatory", "EHS requirements change mid-process",
             "low", "medium", "Monitor regulatory updates weekly", "regulatory_team"),
            ("risk_material", "technical", "Critical reagent sourcing issues",
             "medium", "high", "Qualify multiple suppliers", "ms_specialist"),
            ("risk_donor", "regulatory", "Donor material non-compliance",
             "low", "high", "Implement enhanced screening protocol", "cmc_director")
        ]
        
        for risk_id, risk_type, desc, prob, impact, mitigation, owner in risks_data:
            self.risks[risk_id] = Risk(
                id=risk_id,
                risk_type=risk_type,
                description=desc,
                probability=prob,
                impact=impact,
                mitigation_strategy=mitigation,
                owner_role_id=owner,
                status="identified" if prob == "high" else "mitigated"
            )
    
    def generate_milestones(self):
        """Generate milestones for Gate 0."""
        base = self.base_date
        
        milestones_data = [
            ("ms_kt_start", "Knowledge Transfer Kickoff", "Initial meeting with Discovery team",
             base - timedelta(days=42), "completed"),
            ("ms_plasmid_seq", "Plasmid Sequencing Complete", "Full sequence verification",
             base - timedelta(days=28), "completed"),
            ("ms_team_assign", "Team Assignments Complete", "All core team members identified",
             base - timedelta(days=35), "completed"),
            ("ms_risk_review", "Risk Assessment Complete", "Initial risk register populated",
             base - timedelta(days=21), "completed"),
            ("ms_method_align", "Method Alignment Achieved", "AD and TD methods harmonized",
             base - timedelta(days=14), "completed"),
            ("ms_gate_prep", "Gate Package Complete", "All deliverables ready for review",
             base - timedelta(days=3), "completed"),
            ("ms_gate_review", "Gate 0 Review Meeting", "Formal gate review and decision",
             base, "completed")
        ]
        
        for ms_id, name, desc, target, status in milestones_data:
            self.milestones[ms_id] = Milestone(
                id=ms_id,
                name=name,
                description=desc,
                target_date=target.isoformat(),
                actual_date=target.isoformat() if status == "completed" else None,
                status=status
            )
    
    def generate_deliverables(self):
        """Generate deliverables for Gate 0."""
        
        # Analytical Development deliverables
        self.deliverables["deliv_ad_001"] = Deliverable(
            id="deliv_ad_001",
            name="Method Alignment with TD",
            description="Start collaboration with Cell Engineering and TD for method alignment",
            functional_area="Analytical Development",
            artifact_ids=["art_method_align"],
            criterion_ids=["crit_method_001"],
            requirement_ids=["req_doc_001"],
            owner_role_id="ad_lead",
            approver_role_ids=["cmc_director", "qa_team"],
            due_date=(self.base_date - timedelta(days=14)).isoformat(),
            completion_date=(self.base_date - timedelta(days=16)).isoformat(),
            status="completed"
        )
        
        self.deliverables["deliv_ad_002"] = Deliverable(
            id="deliv_ad_002",
            name="TD Data Review",
            description="Review available data from Therapeutics Discovery on the program",
            functional_area="Analytical Development",
            artifact_ids=["art_data_review"],
            criterion_ids=["crit_kt_001"],
            requirement_ids=["req_doc_001"],
            owner_role_id="ad_lead",
            approver_role_ids=["qa_team"],
            dependencies=["deliv_ad_001"],
            due_date=(self.base_date - timedelta(days=7)).isoformat(),
            completion_date=(self.base_date - timedelta(days=8)).isoformat(),
            status="completed"
        )
        
        self.deliverables["deliv_ad_003"] = Deliverable(
            id="deliv_ad_003",
            name="Critical Reagent Planning",
            description="Identify needs for critical reagents and plan for manufacturing",
            functional_area="Analytical Development",
            artifact_ids=["art_reagent_plan"],
            criterion_ids=[],
            requirement_ids=["req_tech_001"],
            owner_role_id="ad_lead",
            approver_role_ids=["ms_specialist"],
            due_date=(self.base_date - timedelta(days=10)).isoformat(),
            completion_date=(self.base_date - timedelta(days=11)).isoformat(),
            status="completed"
        )
        
        # API deliverables
        self.deliverables["deliv_api_001"] = Deliverable(
            id="deliv_api_001",
            name="Plasmid Construct Review",
            description="Review plasmid construct details including sequence and maps",
            functional_area="API Cell & Gene",
            artifact_ids=["art_plasmid_seq", "art_plasmid_map"],
            criterion_ids=["crit_seq_001", "crit_purity_001"],
            requirement_ids=["req_tech_001", "req_gmp_001"],
            owner_role_id="api_manager",
            approver_role_ids=["cmc_director", "qa_team"],
            due_date=(self.base_date - timedelta(days=21)).isoformat(),
            completion_date=(self.base_date - timedelta(days=22)).isoformat(),
            status="completed"
        )
        
        self.deliverables["deliv_api_002"] = Deliverable(
            id="deliv_api_002",
            name="Plasmid Sequencing and FTO",
            description="Full plasmid sequencing and freedom to operate analysis",
            functional_area="API Cell & Gene",
            artifact_ids=["art_plasmid_seq"],
            criterion_ids=["crit_seq_001"],
            requirement_ids=["req_ip_001", "req_tech_001"],
            owner_role_id="api_manager",
            approver_role_ids=["regulatory_team"],
            dependencies=["deliv_api_001"],
            due_date=(self.base_date - timedelta(days=28)).isoformat(),
            completion_date=(self.base_date - timedelta(days=28)).isoformat(),
            status="completed"
        )
        
        # CMC Leadership deliverables
        self.deliverables["deliv_cmc_001"] = Deliverable(
            id="deliv_cmc_001",
            name="EHS Requirements Definition",
            description="Determine DG classification and packaging requirements",
            functional_area="CMC Leadership",
            artifact_ids=["art_ehs_class"],
            criterion_ids=[],
            requirement_ids=["req_ehs_001", "req_safety_001"],
            owner_role_id="cmc_director",
            approver_role_ids=["regulatory_team"],
            due_date=(self.base_date - timedelta(days=35)).isoformat(),
            completion_date=(self.base_date - timedelta(days=36)).isoformat(),
            status="completed"
        )
        
        self.deliverables["deliv_cmc_002"] = Deliverable(
            id="deliv_cmc_002",
            name="Risk Assessment",
            description="Initiate risk assessment using Risk Registers",
            functional_area="CMC Leadership",
            artifact_ids=["art_risk_register"],
            criterion_ids=["crit_risk_001"],
            requirement_ids=[],
            owner_role_id="cmc_director",
            approver_role_ids=["qa_team"],
            due_date=(self.base_date - timedelta(days=21)).isoformat(),
            completion_date=(self.base_date - timedelta(days=21)).isoformat(),
            status="completed"
        )
        
        self.deliverables["deliv_cmc_003"] = Deliverable(
            id="deliv_cmc_003",
            name="Target Molecule Profile",
            description="Develop target molecule profile for the program",
            functional_area="CMC Leadership",
            artifact_ids=["art_target_profile"],
            criterion_ids=[],
            requirement_ids=["req_doc_001"],
            owner_role_id="cmc_director",
            approver_role_ids=["qa_team"],
            due_date=(self.base_date - timedelta(days=14)).isoformat(),
            completion_date=(self.base_date - timedelta(days=15)).isoformat(),
            status="completed"
        )
        
        # Add more deliverables as needed...
    
    def generate_discovery_stage(self):
        """Generate the Discovery Stage that precedes Gate 0."""
        return Stage(
            id="stage_discovery",
            name="Discovery Stage",
            description="Basic research, target identification, and lead optimization",
            start_date=(self.base_date - timedelta(days=180)).isoformat(),
            end_date=(self.base_date - timedelta(days=43)).isoformat(),
            preceding_gate_id=None,
            following_gate_id="gate_0",
            milestone_ids=["ms_kt_start"],
            activities=[
                "Target identification and validation",
                "Lead compound optimization",
                "Proof of concept studies",
                "Initial safety assessment",
                "IP evaluation",
                "Technology transfer preparation"
            ],
            resource_requirements={
                "fte_count": 15,
                "budget_usd": 2500000,
                "lab_space_sqft": 3000
            }
        )
    
    def generate_gate_0(self):
        """Generate Gate 0."""
        return Gate(
            id="gate_0",
            gate_number=0,
            name="Entry in Early Development (C&GT)",
            description="Transition from Discovery to Early Development",
            deliverable_ids=list(self.deliverables.keys()),
            milestone_ids=list(self.milestones.keys()),
            risk_ids=list(self.risks.keys()),
            review_date=self.base_date.isoformat(),
            decision="pass",
            decision_rationale="All 17 deliverables completed successfully with no critical risks"
        )
    
    def generate_early_dev_stage(self):
        """Generate the Early Development Stage that follows Gate 0."""
        return Stage(
            id="stage_early_dev",
            name="Early Development Stage",
            description="Process development, method development, and preparation for clinical trials",
            start_date=self.base_date.isoformat(),
            end_date=(self.base_date + timedelta(days=180)).isoformat(),
            preceding_gate_id="gate_0",
            following_gate_id="gate_1",
            milestone_ids=[],
            activities=[
                "Process development and optimization",
                "Analytical method development",
                "Formulation development",
                "Manufacturing process design",
                "Scale-up planning",
                "Stability studies initiation"
            ],
            resource_requirements={
                "fte_count": 25,
                "budget_usd": 5000000,
                "lab_space_sqft": 5000
            }
        )


# ============================================================================
# MAIN EXECUTION
# ============================================================================

def main():
    """Generate and save comprehensive ontology mock data."""
    
    print("=" * 80)
    print("GENERATING COMPREHENSIVE STAGE GATE ONTOLOGY")
    print("=" * 80)
    print()
    
    # Generate Gate 0 mock data
    print("Generating Gate 0 mock data...")
    generator = Gate0MockDataGenerator()
    gate_0_data = generator.generate_all_data()
    
    # Save to JSON
    json_path = Path("gate_0_complete_ontology.json")
    with open(json_path, 'w') as f:
        json.dump(gate_0_data, f, indent=2, default=str)
    
    print(f"✓ Generated complete ontology data for Gate 0")
    print(f"  Saved to: {json_path}")
    print()
    
    # Print summary statistics
    print("ONTOLOGY STATISTICS:")
    print("-" * 40)
    print(f"Stages:       {len(gate_0_data['stages'])}")
    print(f"Gates:        {len(gate_0_data['gates'])}")
    print(f"Deliverables: {len(gate_0_data['deliverables'])}")
    print(f"Artifacts:    {len(gate_0_data['artifacts'])}")
    print(f"Criteria:     {len(gate_0_data['criteria'])}")
    print(f"Requirements: {len(gate_0_data['requirements'])}")
    print(f"Risks:        {len(gate_0_data['risks'])}")
    print(f"Milestones:   {len(gate_0_data['milestones'])}")
    print(f"Roles:        {len(gate_0_data['roles'])}")
    print()
    
    # Show sample deliverable with all relationships
    print("SAMPLE DELIVERABLE WITH FULL RELATIONSHIPS:")
    print("-" * 40)
    sample = gate_0_data['deliverables']['deliv_api_001']
    print(f"ID: {sample['id']}")
    print(f"Name: {sample['name']}")
    print(f"Functional Area: {sample['functional_area']}")
    print(f"Status: {sample['status']}")
    print()
    
    print("Linked Artifacts:")
    for art_id in sample['artifact_ids']:
        art = gate_0_data['artifacts'][art_id]
        print(f"  • {art['name']} ({art['artifact_type']})")
    
    print("Acceptance Criteria:")
    for crit_id in sample['criterion_ids']:
        crit = gate_0_data['criteria'][crit_id]
        print(f"  • {crit['name']}: {crit['acceptance_threshold']}")
    
    print("Requirements:")
    for req_id in sample['requirement_ids']:
        req = gate_0_data['requirements'][req_id]
        print(f"  • {req['description']} [{req['priority']}]")
    
    print("Owner:")
    owner = gate_0_data['roles'][sample['owner_role_id']]
    print(f"  • {owner['name']} ({owner['department']})")
    
    print()
    print("=" * 80)
    print("✅ COMPREHENSIVE ONTOLOGY GENERATION COMPLETE")
    print("=" * 80)
    print()
    print("Next: Generate RDF/TTL for knowledge graph integration")


if __name__ == "__main__":
    main()


