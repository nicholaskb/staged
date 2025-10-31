# Implementation Guide: Adding Drug Products to Your Knowledge Graph

## Quick Start

### Step 1: Add Drug Product Ontology
```bash
# Combine with existing ontology
cat cmc_stagegate_drug_products.ttl >> cmc_stagegate_base.ttl
```

### Step 2: Create Your Drug Instances
```turtle
# Template for new drug
ex:Drug-YOUR-DRUG-ID a ex:DrugProduct ;
    rdfs:label "Drug Name Dosage Form Strength" ;
    ex:targetIndication "Disease/Condition" ;
    ex:currentStage ex:Stage-[modality]-[number] ;
    ex:hasActiveSubstance ex:Substance-YOUR-API ;
    
    # IDMP identifiers (get from regulatory)
    idmp:mpid "UUID-here" ;
    ex:substanceUNII "UNII-code" ;
    
    # Regulatory tracking
    ex:hasIND "IND-number" ;
    
    # Timeline
    ex:developmentStartDate "YYYY-MM-DD"^^xsd:date ;
    ex:projectedLaunch "YYYY-QQ" .
```

### Step 3: Link to Existing Data

#### Connect to Deliverables
```turtle
# Your existing deliverable now points to specific drug
ex:CQA-protein-5-stability-data 
    ex:appliesTo ex:Drug-YOUR-DRUG-ID ;
    ex:status ex:Complete ;
    ex:assignedTo ex:SME-john-doe .  # Links to SME!
```

#### Track Gate Reviews
```turtle
ex:GateReview-YOUR-DRUG-Gate5 a ex:GateReviewEvent ;
    ex:reviewedDrug ex:Drug-YOUR-DRUG-ID ;
    ex:atGate ex:Gate-protein-5 ;
    ex:reviewDate "2024-10-31"^^xsd:date ;
    ex:decision ex:Approved .
```

## Integration with Your Current System

### Your Current Data Model
```
Stages (26) → Deliverables (2,205) → SMEs (41)
```

### Enhanced with Drug Products
```
DRUGS → Stages (26) → Deliverables (2,205) → SMEs (41)
  ↓
Clinical Trials
  ↓
IDMP/Regulatory
```

## Sample Queries

### 1. Portfolio Dashboard
```sparql
# Show all drugs and their stages
SELECT ?drug ?label ?stage ?indication WHERE {
    ?drug a ex:DrugProduct ;
          rdfs:label ?label ;
          ex:currentStage ?stage ;
          ex:targetIndication ?indication .
}
ORDER BY ?stage
```

### 2. Resource Planning
```sparql
# Which SMEs are needed for upcoming work?
SELECT ?drug ?deliverable ?sme ?targetDate WHERE {
    ?deliverable ex:appliesTo ?drug ;
                 ex:status ex:InProgress ;
                 ex:assignedTo ?sme ;
                 ex:targetDate ?targetDate .
    FILTER(?targetDate > NOW())
}
ORDER BY ?targetDate
```

### 3. Risk Assessment
```sparql
# Find blocked deliverables by drug
SELECT ?drug ?deliverable ?issue WHERE {
    ?drug a ex:DrugProduct .
    ?deliverable ex:appliesTo ?drug ;
                 ex:status ex:Blocked ;
                 ex:reference ?issue .
}
```

### 4. IDMP Readiness
```sparql
# Check IDMP identifier completeness
SELECT ?drug ?label 
       (BOUND(?mpid) AS ?has_mpid)
       (BOUND(?unii) AS ?has_unii) WHERE {
    ?drug a ex:DrugProduct ;
          rdfs:label ?label .
    OPTIONAL { ?drug idmp:mpid ?mpid }
    OPTIONAL { ?drug ex:substanceUNII ?unii }
}
```

## IDMP Integration Points

### Required IDMP Elements
1. **Substance (ISO 11238)**
   - UNII code
   - CAS number
   - Molecular formula

2. **Product (ISO 11615/11616)**
   - MPID (Medicinal Product ID)
   - PHPID (Pharmaceutical Product ID)
   
3. **Dose Form (ISO 11239)**
   - EDQM Standard Terms
   - Example: `edqm:10219000` = Tablet

4. **Route of Admin (ISO 11239)**
   - EDQM codes
   - Example: `edqm:20053000` = Oral use

### Mapping Your Data

| Your Field | IDMP Property | Example |
|------------|---------------|---------|
| Product Name | rdfs:label | "ABC-123 Tablet 50mg" |
| API | ex:hasActiveSubstance | Link to substance |
| Strength | ex:hasStrength | "50 mg" |
| Form | idmp:hasDoseForm | edqm:10219000 |
| Route | idmp:hasRouteOfAdministration | edqm:20053000 |
| IND# | ex:hasIND | "IND-123456" |
| NCT# | ex:nctNumber | "NCT04567890" |

## Next Steps

### Immediate Actions
1. ✅ Review drug product ontology extensions
2. ✅ Test with example drugs (PTX2024, CART789, SMX456)
3. ⬜ Create instances for your actual drugs
4. ⬜ Link existing deliverables to drugs
5. ⬜ Add gate review history

### Future Enhancements
1. **Clinical Integration**
   - Import ClinicalTrials.gov data
   - Link protocol amendments
   - Track enrollment status

2. **Manufacturing**
   - Link to batch records
   - Track scale-up activities
   - Connect to ERP/MES

3. **Regulatory**
   - eCTD section mapping
   - Submission tracking
   - Agency interactions

4. **Quality**
   - Deviation tracking
   - CAPA linkage
   - Stability trends

## Benefits

### For Program Management
- Real-time portfolio visibility
- Risk identification
- Resource optimization

### For Regulatory
- IDMP-ready from day 1
- Audit trail complete
- Submission preparation

### For Quality
- End-to-end traceability
- Impact assessments
- Trend analysis

## Technical Notes

### File Locations
```
cmc_stagegate_drug_products.ttl  # Drug ontology extensions
data/example_drug_instances.ttl  # Example drugs
docs/DRUG_PRODUCT_STAGE_GATE_INTEGRATION.md  # Full documentation
docs/DRUG_FLOW_EXAMPLE.md  # Visual examples
```

### To Combine Everything
```bash
# Create complete ontology with drugs
python3 scripts/etl/combine_ttls.py \
    --files cmc_stagegate_base.ttl \
            cmc_stagegate_drug_products.ttl \
            output/current/cmc_stagegate_instances.ttl \
            output/current/cmc_stagegate_sme_instances.ttl \
            data/example_drug_instances.ttl \
    --out output/current/cmc_stagegate_all_with_drugs.ttl
```

### Validation
```bash
# Check syntax
rapper -i turtle -c cmc_stagegate_drug_products.ttl
rapper -i turtle -c data/example_drug_instances.ttl

# Count triples
rapper -i turtle -c output/current/cmc_stagegate_all_with_drugs.ttl | grep "triples"
```
