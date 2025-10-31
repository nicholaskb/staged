# Stage-Gate Ontology SPARQL Queries

## Overview
This collection demonstrates the structure and relationships within the CMC Stage-Gate Ontology, showcasing stages, gates, deliverables, SME assignments, and organizational structure.

## Query Catalog

### 🏗️ Structure & Organization

#### 01. Stage Structure (`01_stage_structure.sparql`)
- **Purpose**: Complete stage-gate framework overview
- **Shows**: All stages, gates, plans, specifications, deliverable counts
- **Key Insight**: How stages are organized by value stream (Protein vs CGT)

#### 11. Stage Progression Paths (`11_stage_progression_paths.sparql`)
- **Purpose**: Maps the flow between stages
- **Shows**: Stage transitions, gate requirements, critical paths
- **Key Insight**: Dependencies and prerequisites between stages

### 📋 Deliverables & Requirements

#### 02. Deliverable Catalog (`02_deliverable_catalog.sparql`)
- **Purpose**: Complete inventory of all deliverables
- **Shows**: 2,205 Quality Attributes organized by stage
- **Key Fields**: Functional area, category, owner, status, explanation

#### 05. Gate Requirements (`05_gate_requirements.sparql`)
- **Purpose**: What's required to pass each gate
- **Shows**: Critical deliverables for gate passage
- **Key Insight**: Must-have vs nice-to-have deliverables

#### 06. Deliverable Categories (`06_deliverable_categories.sparql`)
- **Purpose**: Analysis by deliverable category
- **Shows**: Distribution across categories (API Dev, Analytics, etc.)
- **Key Metrics**: Total deliverables, stages involved, SME count

#### 08. Date Tracking (`08_date_tracking_deliverables.sparql`)
- **Purpose**: Deliverables with planned/actual dates
- **Shows**: Timeline compliance, variances, document references
- **Key Feature**: New columns from updated Excel (Plan date, Actual date, References)

### 👥 People & Organization

#### 03. SME Assignments (`03_sme_assignments.sparql`)
- **Purpose**: Subject Matter Expert mapping
- **Shows**: 41 SMEs across 40 functional areas
- **Key Features**: Primary vs backup, expertise areas, modality

#### 07. Functional Area Workload (`07_functional_area_workload.sparql`)
- **Purpose**: Workload distribution analysis
- **Shows**: Deliverables per functional area
- **Key Metrics**: Stage involvement, SME coverage, complexity

### 📊 Analytics & Comparison

#### 04. Value Stream Comparison (`04_value_stream_comparison.sparql`)
- **Purpose**: Compare Protein vs CGT pathways
- **Shows**: Deliverable counts, SME allocation differences
- **Key Insight**: Modality-specific requirements

#### 09. GIST Alignment (`09_gist_alignment.sparql`)
- **Purpose**: Semantic interoperability analysis
- **Shows**: How CMC classes map to GIST upper ontology
- **Key Classes**: Event, Person, Organization, Product, Material

#### 10. Ontology Statistics (`10_ontology_statistics.sparql`)
- **Purpose**: Overall metrics and graph size
- **Shows**: Total counts for all major elements
- **Key Stats**: 26 stages, 2,205 deliverables, 41 SMEs, 13,043 triples

## Key Ontology Components

### Core Classes
```turtle
ex:Stage                # Development stages (0-13)
ex:StageGate           # Decision points between stages
ex:QualityAttribute    # Deliverables (2,205 instances)
ex:Specification       # Stage requirements
ex:SubjectMatterExpert # SMEs (41 people)
ex:FunctionalArea      # Organizational units (40 areas)
```

### Key Properties
```turtle
ex:hasGate            # Stage → Gate
ex:hasCQA             # Specification → Deliverable
ex:hasSME             # FunctionalArea → SME
ex:hasCategory        # Deliverable → Category
ex:functionalArea     # Deliverable → Functional Area
ex:owner              # Deliverable → Owner
ex:plannedDate        # Deliverable → Date
ex:actualDate         # Deliverable → Date
ex:reference          # Deliverable → Document
```

## Value Streams

### Protein Pathway
- **Stages**: 13 (Stage-protein-0 through Stage-protein-13)
- **Focus**: Traditional biologics, antibodies
- **Deliverables**: ~1,100
- **SMEs**: 21 primary experts

### CGT Pathway  
- **Stages**: 13 (Stage-cgt-0 through Stage-cgt-13)
- **Focus**: Cell & Gene Therapies
- **Deliverables**: ~1,105
- **SMEs**: 19 primary experts
- **Special**: Multiple SMEs per area (Cell, Gene, Lentivirus expertise)

## Example Stage-Gate Flow

```
Stage 0: Entry in ED
  ├── Deliverables: 45-52
  ├── Gate 0 Requirements
  └── SMEs: 8-12
         ↓
Stage 1: NME Selection  
  ├── Deliverables: 58-62
  ├── Gate 1 Requirements
  └── SMEs: 10-14
         ↓
Stage 2: LI/LO Candidate
  ├── Deliverables: 73-78
  ├── Gate 2 Requirements
  └── SMEs: 12-16
         ↓
     [continues...]
```

## Query Execution Examples

### Find all deliverables for a specific stage
```sparql
SELECT ?deliverable ?name ?category ?owner WHERE {
    ex:Stage-protein-5 ex:hasSpecification ?spec .
    ?spec ex:hasCQA ?deliverable .
    ?deliverable rdfs:label ?name ;
                 ex:hasCategory ?category ;
                 ex:owner ?owner .
}
```

### Get SME assignments by modality
```sparql
SELECT ?area ?sme ?modality WHERE {
    ?area a ex:FunctionalArea ;
          ex:modality ?modality ;
          ex:hasSME ?sme .
    FILTER(?modality = "CGT")
}
```

### Track deliverable completion
```sparql
SELECT ?stage ?deliverable ?plannedDate ?actualDate WHERE {
    ?deliverable ex:plannedDate ?plannedDate .
    OPTIONAL { ?deliverable ex:actualDate ?actualDate }
    ?spec ex:hasCQA ?deliverable .
    ?stage ex:hasSpecification ?spec .
}
ORDER BY ?plannedDate
```

## Business Applications

### 1. Portfolio Planning
- Understand deliverable requirements per stage
- Identify resource needs
- Plan SME allocation

### 2. Process Optimization
- Analyze deliverable distribution
- Find bottlenecks in categories
- Balance workload across functions

### 3. Compliance Management
- Track required deliverables
- Monitor date compliance
- Ensure SME coverage

### 4. Knowledge Management
- Document organizational structure
- Capture expertise areas
- Maintain delivery standards

## Integration Points

### With Drug Products
- Deliverables link to specific drugs via `ex:appliesTo`
- SMEs assigned to drug-specific work
- Gate reviews for drug progression

### With Temporal Tracking
- Stage occupancy periods
- Deliverable completion timelines
- Historical progression analysis

### With IDMP
- Regulatory deliverable requirements
- Submission readiness tracking
- Global identifier management

## Files in This Directory

1. **Structure Queries** (01, 11): Framework and flow
2. **Deliverable Queries** (02, 05, 06, 08): Requirements and tracking
3. **People Queries** (03, 07): SME and functional areas
4. **Analysis Queries** (04, 09, 10): Comparisons and metrics
5. **README.md**: This documentation

## Related Resources
- [Stage-Gate Base Ontology](../../cmc_stagegate_base.ttl)
- [Generated Instances](../../output/current/cmc_stagegate_instances.ttl)
- [SME Instances](../../output/current/cmc_stagegate_sme_instances.ttl)
- [Product Instance Queries](../product_instance/)
