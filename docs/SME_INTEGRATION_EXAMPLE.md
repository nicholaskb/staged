# SME Integration Example: How It All Connects

## Current State (Without SME Data)

```
Deliverable: "API specification"
    ↓
Category: "API Analytics Development"
    ↓
❓ Who is responsible?
```

## With SME Integration

```
Deliverable: "API specification"
    ↓
Category: "API Analytics Development"
    ↓
Functional Area: "API Development"
    ↓
SME (Protein): Mark Teeters
SME (CGT): Kathleen Vermeersch, Kathryn Henckels, Abbey Weith, Nafiseh Poornejad
```

## Real Example from Your Data

### Current Deliverable (from SGD sheet)
```turtle
ex:CQA-sm-3-api-specification 
    a ex:QualityAttribute ;
    rdfs:label "API specification" ;
    ex:hasCategory "API Analytics Development" ;
    ex:belongsToStage ex:Stage-sm-3 .
```

### Enhanced with SME Data
```turtle
ex:CQA-sm-3-api-specification 
    a ex:QualityAttribute ;
    rdfs:label "API specification" ;
    ex:hasCategory "API Analytics Development" ;
    ex:belongsToStage ex:Stage-sm-3 ;
    ex:hasResponsibleSME ex:SME-MarkTeeters .  # NEW!

ex:SME-MarkTeeters
    a ex:SubjectMatterExpert ;
    rdfs:label "Mark Teeters" ;
    ex:expertFor ex:FA-API-Development ;
    ex:email "mark.teeters@company.com" ;  # if available
    ex:modality "Protein" .
```

## Query Power

### Before SME Integration
**Question:** "Who should I contact about API specifications?"
**Answer:** ❓ Unknown - need to ask around

### After SME Integration
**Query:**
```sparql
SELECT ?deliverable ?sme ?smeEmail WHERE {
    ?deliverable rdfs:label ?label .
    FILTER(CONTAINS(?label, "API specification"))
    ?deliverable ex:hasCategory ?category .
    ?area rdfs:label ?category ;
          ex:hasSME ?sme .
    ?sme rdfs:label ?smeName ;
         ex:email ?smeEmail .
}
```
**Answer:** 
- Protein: Mark Teeters
- CGT: Kathleen Vermeersch (Cell Auto), Kathryn Henckels (Cell Allo), Abbey Weith (Gene), Nafiseh Poornejad (Lentivirus)

## Multiple SMEs Example (CGT API Development)

```
                    ex:FA-API-Development-CGT
                    "API Development (CGT)"
                           ↓
            ┌──────────────┼──────────────┬──────────────┐
            ↓              ↓              ↓              ↓
    Kathleen Vermeersch  Kathryn Henckels  Abbey Weith  Nafiseh Poornejad
    (Cell - Auto)        (Cell - Allo)      (Gene)       (Lentivirus)
```

Each SME has a specialty area within CGT API Development!

## Backup SME Example

```
ex:FA-AnalyticalDevelopment-Protein
    ├── ex:hasSME → Patrick Sheehy (Primary)
    └── ex:hasBackupSME → Gulnur Elove (Backup)
```

## Cross-Modality SMEs

Some SMEs work across both Protein and CGT:
```
Lei Xue → Product Quality Management (BOTH)
Mark Stansfield → Material Sciences (BOTH)
Tom Merkel → Program Management (BOTH)
```

## Benefits Visualization

### 1. Accountability Dashboard
```
Stage 3 Deliverables:
├── API Specification → Mark Teeters ✓
├── Formulation Report → Mark Bruner ✓
├── Analytical Method → Patrick Sheehy ✓
└── Regulatory Filing → Judith Shuster ✓
```

### 2. Workload Analysis
```
Mark Teeters: 45 deliverables
Lei Xue: 38 deliverables  
Patrick Sheehy: 31 deliverables
```

### 3. Coverage Gaps
```
Vaccines (CGT): No SME assigned ⚠️
API (CEAS) CGT: No SME assigned ⚠️
```

## Implementation Impact

**Before:** 2,205 deliverables with categories
**After:** 2,205 deliverables with categories AND responsible SMEs

This creates a complete responsibility matrix!
