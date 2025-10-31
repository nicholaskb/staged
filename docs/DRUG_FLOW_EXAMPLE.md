# Drug Flow Through Stage Gates - Visual Example

## Example: "ONCO-2024" Cancer Drug Development

### 🧬 The Drug Product
```
ONCO-2024 (Tablet 100mg)
├── Active Substance: Oncozumab-API
├── Indication: Non-Small Cell Lung Cancer
├── Route: Oral
└── Current Stage: Stage 5 (Phase 2 Clinical)
```

### 📊 Stage Progression

```
Stage 0: Entry in ED          ✅ Completed (Jan 2023)
  └── Deliverables Done:
      • Target identification
      • Initial synthesis
      
Stage 1: NME Selection        ✅ Completed (Mar 2023)  
  └── Deliverables Done:
      • Lead optimization
      • Preliminary tox
      
Stage 2: LI/LO Candidate      ✅ Completed (Jun 2023)
  └── Deliverables Done:
      • Scale-up feasibility
      • Formulation screening
      
Stage 3: FIH Readiness        ✅ Completed (Sep 2023)
  └── Deliverables Done:
      • GMP manufacturing
      • IND preparation
      
Stage 4: POC Readiness        ✅ Completed (Mar 2024)
  └── Deliverables Done:
      • Phase 1 completion
      • Dose selection
      
Stage 5: Ph2 Clinical         🔄 IN PROGRESS (Current)
  └── Deliverables Status:
      ✅ Clinical protocol
      ✅ Stability studies (12mo)
      ⏳ Process validation (70%)
      ⏳ Analytical methods (80%)
      ❌ Impurity qualification
      
Stage 6: Ph3 Readiness        🔮 Upcoming (Est. Q2 2025)
  └── Required Deliverables:
      • Commercial process
      • 24-month stability
      • Ph2 results
```

### 🔗 Knowledge Graph Representation

```turtle
# The Drug Product Instance
ex:Drug-ONCO2024 a ex:DrugProduct ;
    rdfs:label "ONCO-2024 Tablet 100mg" ;
    ex:hasActiveSubstance ex:Substance-Oncozumab ;
    ex:currentStage ex:Stage-cgt-5 ;
    ex:targetIndication "Non-Small Cell Lung Cancer" ;
    
    # IDMP Identifiers
    idmp:mpid "550e8400-e29b-41d4-a716-446655440000" ;
    ex:substanceUNII "ABC123XYZ" ;
    
    # Regulatory
    ex:hasIND "IND-147852" ;
    ex:nctNumber "NCT04567890" ;
    
    # Current Status
    ex:developmentStartDate "2023-01-15"^^xsd:date ;
    ex:projectedLaunch "2027-Q3" .

# Gate 5 Review (Most Recent)
ex:GateReview-ONCO2024-Gate5 a ex:GateReviewEvent ;
    ex:reviewDate "2024-03-15"^^xsd:date ;
    ex:decision ex:ConditionalApproval ;
    ex:condition "Complete impurity qualification by Q1 2025" ;
    ex:nextReview "2025-02-01"^^xsd:date .

# Link to Deliverables
ex:CQA-cgt-5-stability-12mo 
    ex:appliesTo ex:Drug-ONCO2024 ;
    ex:status ex:Complete ;
    ex:completedDate "2024-09-30"^^xsd:date ;
    ex:hasEvidence ex:StabilityReport-ONCO2024-12mo .

ex:CQA-cgt-5-process-validation
    ex:appliesTo ex:Drug-ONCO2024 ;
    ex:status ex:InProgress ;
    ex:percentComplete 70 ;
    ex:targetDate "2024-12-15"^^xsd:date ;
    ex:assignedTo ex:SME-mark-teeters .  # Links to SME!
```

### 🎯 How IDMP Integration Works

```
Your Drug                    IDMP Standards
-----------                  ---------------
ONCO-2024         →         ISO 11615 (Medicinal Product ID)
                            └── MPID: 550e8400-e29b-41d4...
                            
Oncozumab-API     →         ISO 11238 (Substance ID)
                            └── UNII: ABC123XYZ
                            └── CAS: 123456-78-9
                            
Tablet            →         EDQM Standard Terms
                            └── Code: 10219000
                            └── Term: "Tablet"
                            
100mg             →         UCUM (Units)
                            └── Code: "mg"
                            └── System: UCUM
```

### 📈 Business Value

1. **Real-time Status**: Know exactly where each drug is in development
2. **Risk Management**: See which deliverables are blocking progress
3. **Resource Planning**: Identify which SMEs are needed for upcoming work
4. **Regulatory Ready**: IDMP identifiers ready for submissions
5. **Portfolio View**: Compare progress across all drugs

### 🔍 Sample Queries

**"Show me all drugs stuck at Gate 5"**
```sparql
SELECT ?drug ?indication ?issue WHERE {
    ?drug ex:currentStage ex:Stage-cgt-5 ;
          ex:targetIndication ?indication .
    ?review ex:reviewedDrug ?drug ;
            ex:decision ex:ConditionalApproval ;
            ex:condition ?issue .
}
```

**"Which SMEs are working on ONCO-2024?"**
```sparql
SELECT ?sme ?deliverable ?area WHERE {
    ?deliverable ex:appliesTo ex:Drug-ONCO2024 ;
                 ex:assignedTo ?sme .
    ?sme ex:expertFor ?area .
}
```

**"What's blocking ONCO-2024 from advancing?"**
```sparql
SELECT ?deliverable ?status WHERE {
    ?deliverable ex:appliesTo ex:Drug-ONCO2024 ;
                 ex:requiredForGate ex:Gate-cgt-6 ;
                 ex:status ?status .
    FILTER(?status != ex:Complete)
}
```

### 🔄 Integration Points

```
CMC Ontology  ←→  External Systems
---------------------------------
Drug Products  ←→  LIMS (Lab data)
Stage Gates    ←→  Project Management
Deliverables   ←→  Document Management
SMEs           ←→  HR Systems
Specifications ←→  Quality Systems
Clinical Trials←→  ClinicalTrials.gov
Regulatory     ←→  eCTD/Gateway
```
