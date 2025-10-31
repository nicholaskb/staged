# Drug Product Stage-Gate Integration & IDMP Alignment

## Executive Summary
This document describes how actual drug products flow through the CMC stage-gate process and integrate with IDMP (Identification of Medicinal Products) standards.

## Current Ontology Support

The CMC ontology already includes foundational elements for drug products:

### Existing Classes
- **`ex:Material`** - Base class for drug substances, drug products, intermediates
- **`ex:Lot`** - Specific batches/lots of materials
- **`ex:Specification`** - Quality specifications for materials
- **`ex:Process`** - Manufacturing processes
- **`ex:AnalyticalResult`** - Test results for lots

### Existing IDMP/Regulatory Links
- **`ex:medicinalProduct`** → `fhir:MedicinalProductDefinition` (IDMP alignment)
- **`ex:substanceUNII`** - GSRS/UNII substance identifiers
- **`ex:doseForm`** → EDQM Standard Terms
- **`ex:routeOfAdmin`** → EDQM Standard Terms
- **`gs1:gtin`** - Pack identification

## Proposed Drug Product Representation

### 1. Drug Product Instance Model

```turtle
# Example: A specific drug "ABC-123" going through development
ex:Drug-ABC123 a ex:DrugProduct ;
    rdfs:label "ABC-123 Tablet 50mg" ;
    ex:hasActiveSubstance ex:Substance-ABC123-API ;
    ex:hasDoseForm edqm:Tablet ;
    ex:hasStrength "50 mg" ;
    ex:hasRouteOfAdmin edqm:OralUse ;
    ex:currentStage ex:Stage-protein-5 ;  # Currently at Stage 5
    ex:targetIndication "Type 2 Diabetes Mellitus" ;
    ex:developmentProgram ex:Program-ABC123 .

# The API (Active Pharmaceutical Ingredient)
ex:Substance-ABC123-API a ex:DrugSubstance ;
    rdfs:label "ABC-123 API" ;
    ex:substanceUNII "XYZ789DEF" ;
    ex:chemicalName "..." ;
    ex:molecularFormula "C20H25N3O4" ;
    ex:hasSpecification ex:Spec-ABC123-API .

# Development Program linking stages
ex:Program-ABC123 a ex:DevelopmentProgram ;
    rdfs:label "ABC-123 Development Program" ;
    ex:hasModality ex:ValueStream-Protein ;
    ex:startedAt ex:Stage-protein-0 ;
    ex:currentlyAt ex:Stage-protein-5 ;
    ex:hasCompletedGates ex:Gate-protein-0, ex:Gate-protein-1, 
                         ex:Gate-protein-2, ex:Gate-protein-3, ex:Gate-protein-4 .
```

### 2. Stage Progression Tracking

```turtle
# Track when drug passes through gates
ex:GateReview-ABC123-Gate5 a ex:GateReviewEvent ;
    rdfs:label "ABC-123 Gate 5 Review" ;
    ex:reviewedDrug ex:Drug-ABC123 ;
    ex:atGate ex:Gate-protein-5 ;
    ex:reviewDate "2024-10-31"^^xsd:date ;
    ex:decision ex:Approved ;
    ex:hasEvidence ex:CQA-protein-5-stability-data ,
                   ex:CQA-protein-5-process-validation ,
                   ex:CQA-protein-5-analytical-methods .
```

### 3. Linking Deliverables to Products

```turtle
# Connect deliverables to specific drug products
ex:CQA-protein-5-stability-data
    ex:appliesTo ex:Drug-ABC123 ;
    ex:hasResult ex:StabilityResult-ABC123-24month ;
    ex:status ex:Complete ;
    ex:completedDate "2024-10-15"^^xsd:date .

ex:StabilityResult-ABC123-24month a ex:AnalyticalResult ;
    ex:measuredOnLot ex:Lot-ABC123-001 ;
    ex:stabilityPeriod "24 months" ;
    ex:storageCondition "25°C/60% RH" ;
    ex:conclusion "Meets specifications" .
```

## IDMP Integration Strategy

### 1. Core IDMP Identifiers

```turtle
# Extend Material class with IDMP identifiers
ex:Drug-ABC123
    # ISO 11615 - Medicinal Product
    idmp:mpid "12345678-90AB-CDEF-1234-567890ABCDEF" ;
    
    # ISO 11616 - Pharmaceutical Product  
    idmp:phpid "FEDCBA09-8765-4321-FEDC-BA0987654321" ;
    
    # Link to regulatory submissions
    ex:hasIND "IND-123456" ;
    ex:hasNDA "NDA-987654" ;
    ex:hasEMA "EMEA/H/C/005678" .

ex:Substance-ABC123-API
    # ISO 11238 - Substance
    idmp:substanceId "SUB-123-456-789" ;
    ex:substanceUNII "XYZ789DEF" ;
    ex:casNumber "123456-78-9" .
```

### 2. IDMP Vocabulary Integration

```turtle
@prefix idmp: <http://www.iso.org/idmp#> .
@prefix edqm: <https://standardterms.edqm.eu#> .
@prefix ucum: <http://unitsofmeasure.org/> .

# Use IDMP controlled vocabularies
ex:Drug-ABC123
    idmp:hasDoseForm edqm:10219000 ;  # Tablet
    idmp:hasUnitOfPresentation edqm:15054000 ; # Tablet
    idmp:hasRouteOfAdministration edqm:20053000 ; # Oral use
    idmp:hasPackageType edqm:30009000 ; # Bottle
    idmp:hasManufacturedDoseForm edqm:10221000 . # Film-coated tablet
```

### 3. Clinical Trial Integration

```turtle
# Link to clinical development
ex:Drug-ABC123
    ex:hasClinicalTrial ex:Trial-ABC123-Ph2-001 ,
                        ex:Trial-ABC123-Ph3-001 .

ex:Trial-ABC123-Ph3-001 a ex:ClinicalTrial ;
    rdfs:label "ABC-123 Phase 3 Pivotal Study" ;
    ex:trialPhase "Phase 3" ;
    ex:nctNumber "NCT05123456" ;
    ex:requiredAtGate ex:Gate-protein-8 ;
    ex:status "Completed" .
```

## Implementation Approach

### Phase 1: Basic Drug Product Tracking
1. Create `ex:DrugProduct` and `ex:DrugSubstance` subclasses
2. Add `ex:DevelopmentProgram` to track stage progression
3. Link deliverables to specific products

### Phase 2: IDMP Alignment
1. Add IDMP identifier properties
2. Import EDQM/UCUM vocabularies
3. Map existing dose forms to EDQM codes

### Phase 3: Regulatory Integration
1. Add IND/NDA/MAA tracking
2. Link to regulatory milestones
3. Connect to eCTD sections

## Example Queries

### 1. Find all drugs at a specific stage
```sparql
SELECT ?drug ?label WHERE {
    ?drug a ex:DrugProduct ;
          rdfs:label ?label ;
          ex:currentStage ex:Stage-protein-5 .
}
```

### 2. Track deliverables for a drug
```sparql
SELECT ?deliverable ?status ?date WHERE {
    ?deliverable ex:appliesTo ex:Drug-ABC123 ;
                 ex:status ?status ;
                 ex:completedDate ?date .
}
```

### 3. Find drugs by indication
```sparql
SELECT ?drug ?indication WHERE {
    ?drug a ex:DrugProduct ;
          ex:targetIndication ?indication .
    FILTER(CONTAINS(?indication, "Diabetes"))
}
```

## Benefits

1. **End-to-End Traceability**: Track drugs from discovery through approval
2. **Regulatory Compliance**: IDMP-ready identifiers for global submissions
3. **Portfolio Management**: Query across all drugs in development
4. **Risk Assessment**: Identify drugs blocked at specific gates
5. **Resource Planning**: See which drugs need specific deliverables

## Next Steps

1. **Extend Ontology**: Add DrugProduct and DevelopmentProgram classes
2. **Import IDMP Vocabularies**: Integrate EDQM, UCUM standards
3. **Create Examples**: Build sample drug instances
4. **Develop Dashboards**: Visualize drug progression through stages
5. **Link to External Systems**: Connect to LIMS, ERP, regulatory systems

## Technical Requirements

### New Classes Needed
```turtle
ex:DrugProduct rdfs:subClassOf ex:Material
ex:DrugSubstance rdfs:subClassOf ex:Material
ex:DevelopmentProgram rdfs:subClassOf prov:Activity
ex:GateReviewEvent rdfs:subClassOf prov:Activity
ex:ClinicalTrial rdfs:subClassOf prov:Activity
```

### New Properties Needed
```turtle
ex:hasActiveSubstance
ex:currentStage
ex:targetIndication
ex:developmentProgram
ex:hasCompletedGates
ex:appliesTo
ex:hasClinicalTrial
```

### External Ontologies to Import
- IDMP Core (ISO 11615, 11616, 11238)
- EDQM Standard Terms
- UCUM Units of Measure
- FHIR R5 MedicinalProductDefinition
