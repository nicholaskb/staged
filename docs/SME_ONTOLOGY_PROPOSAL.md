# SME (Subject Matter Expert) Ontology Integration Proposal

## Overview
The SME CSV file contains mappings between Functional Areas and their Subject Matter Experts for both Protein and CGT modalities. This organizational knowledge is crucial for understanding responsibility and expertise ownership.

## Current SME Data Structure

### Data Summary
- **25 Functional Areas** identified
- **~40 unique SMEs** across both modalities
- **2 modalities**: Protein and CGT
- **Backup SMEs** specified for some areas
- **Multiple SMEs** per area in some cases (especially CGT)

### Sample Data
```
Functional Area: API Development
- Protein SME: Mark Teeters
- CGT SMEs: 
  - Kathleen Vermeersch (Cell)(Auto)
  - Kathryn Henckels (Cell)(Allo)
  - Abbey Weith (Gene)
  - Nafiseh Poornejad (Lentivirus)
```

## Proposed Ontology Extension

### 1. New Classes to Add

```turtle
# Expert and organizational classes
ex:SubjectMatterExpert  a rdfs:Class ;
    rdfs:label "Subject Matter Expert" ;
    rdfs:comment "A person with specialized knowledge in a functional area" ;
    rdfs:subClassOf gist:Person .

ex:FunctionalArea  a rdfs:Class ;
    rdfs:label "Functional Area" ;
    rdfs:comment "An organizational unit or area of responsibility" ;
    rdfs:subClassOf gist:Organization .

ex:ExpertAssignment  a rdfs:Class ;
    rdfs:label "Expert Assignment" ;
    rdfs:comment "The assignment of an SME to a functional area for a modality" ;
    rdfs:subClassOf gist:Event .
```

### 2. New Properties to Add

```turtle
# Object properties for SME relationships
ex:hasSME  a rdf:Property ;
    rdfs:domain ex:FunctionalArea ;
    rdfs:range ex:SubjectMatterExpert ;
    rdfs:comment "Functional area has designated SME" .

ex:hasBackupSME  a rdf:Property ;
    rdfs:domain ex:FunctionalArea ;
    rdfs:range ex:SubjectMatterExpert ;
    rdfs:comment "Functional area has backup/alternate SME" .

ex:expertFor  a rdf:Property ;
    rdfs:domain ex:SubjectMatterExpert ;
    rdfs:range ex:FunctionalArea ;
    owl:inverseOf ex:hasSME ;
    rdfs:comment "SME is expert for functional area" .

ex:appliesTo  a rdf:Property ;
    rdfs:domain ex:ExpertAssignment ;
    rdfs:range ex:ValueStream ;
    rdfs:comment "Expert assignment applies to specific modality" .

# Data properties
ex:expertiseArea  a rdf:Property ;
    rdfs:domain ex:SubjectMatterExpert ;
    rdfs:range xsd:string ;
    rdfs:comment "Specific area of expertise (e.g., Cell, Gene, Lentivirus)" .

ex:isPrimary  a rdf:Property ;
    rdfs:domain ex:SubjectMatterExpert ;
    rdfs:range xsd:boolean ;
    rdfs:comment "Whether this is the primary SME (vs backup)" .
```

## How SME Data Links to Existing Ontology

### Connection Points

1. **FunctionalArea → Category**
   - The functional areas in SME data map to the Category values in deliverables
   - Example: "API Development" appears in both
   
2. **FunctionalArea → Stage/Deliverable**
   - SMEs are responsible for deliverables in their functional area
   - Can query: "Who is the SME for this deliverable's category?"

3. **ValueStream → Modality**
   - Protein vs CGT alignment already exists
   - SME assignments are modality-specific

## Example RDF Instances

```turtle
# Functional Area
ex:FA-API-Development a ex:FunctionalArea ;
    rdfs:label "API Development" ;
    ex:hasSME ex:SME-MarkTeeters ;
    ex:appliesTo ex:Stream-Protein .

# Subject Matter Expert
ex:SME-MarkTeeters a ex:SubjectMatterExpert ;
    rdfs:label "Mark Teeters" ;
    ex:expertFor ex:FA-API-Development ;
    ex:appliesTo ex:Stream-Protein ;
    prov:wasAssociatedWith ex:Stage-Protein-0 ;
    gist:name "Mark Teeters" .

# CGT with multiple SMEs
ex:FA-API-Development-CGT a ex:FunctionalArea ;
    rdfs:label "API Development (CGT)" ;
    ex:hasSME ex:SME-KathleenVermeersch ;
    ex:hasSME ex:SME-KathrynHenckels ;
    ex:hasSME ex:SME-AbbeyWeith ;
    ex:hasSME ex:SME-NafisehPoornejad ;
    ex:appliesTo ex:Stream-CGT .

ex:SME-KathleenVermeersch a ex:SubjectMatterExpert ;
    rdfs:label "Kathleen Vermeersch" ;
    ex:expertiseArea "Cell (Auto)" ;
    ex:expertFor ex:FA-API-Development-CGT .

# Backup SME example
ex:FA-AnalyticalDevelopment-Protein a ex:FunctionalArea ;
    rdfs:label "Analytical Development (Protein)" ;
    ex:hasSME ex:SME-PatrickSheehy ;
    ex:hasBackupSME ex:SME-GulnurElove ;
    ex:appliesTo ex:Stream-Protein .
```

## Implementation Approach

### Step 1: Update Base Ontology
Add the new classes and properties to `cmc_stagegate_base.ttl`

### Step 2: Create SME Processing Script
Create `scripts/etl/generate_sme_ttl.py` to:
1. Read the SME CSV file
2. Parse the functional areas and SME names
3. Handle multiple SMEs per area
4. Extract backup SMEs from parenthetical notes
5. Generate RDF triples

### Step 3: Link to Existing Data
Update `generate_cmc_ttl.py` to:
- Link deliverables to their functional area SMEs via category
- Add SME associations to stages based on functional area

## Benefits of SME Integration

1. **Accountability**: Know who owns each functional area
2. **Expertise Mapping**: Identify subject matter experts for questions
3. **Cross-functional Analysis**: See which SMEs work across modalities
4. **Succession Planning**: Track backup SMEs
5. **Workload Analysis**: Count deliverables per SME

## Sample SPARQL Queries

### Find SME for a deliverable
```sparql
SELECT ?deliverable ?category ?sme WHERE {
    ?deliverable ex:hasCategory ?category .
    ?functionalArea rdfs:label ?category ;
                    ex:hasSME ?sme .
    ?sme rdfs:label ?smeName .
}
```

### Find all deliverables for an SME
```sparql
SELECT ?sme ?deliverable WHERE {
    ?sme ex:expertFor ?area .
    ?area rdfs:label ?areaName .
    ?deliverable ex:hasCategory ?areaName .
}
```

### List SMEs with backups
```sparql
SELECT ?area ?primarySME ?backupSME WHERE {
    ?area ex:hasSME ?primarySME ;
          ex:hasBackupSME ?backupSME .
}
```

## Next Steps

1. **Review and approve** this ontology extension
2. **Update base ontology** with new classes/properties
3. **Create processing script** for SME data
4. **Test integration** with existing data
5. **Update documentation** with SME relationships

## Alternative Approaches

### Option A: Simple Properties (Current Proposal)
- Direct properties linking areas to SMEs
- Clean and straightforward
- Easy to query

### Option B: Reified Assignments
- Create assignment objects with dates, roles
- More complex but more flexible
- Better for tracking changes over time

### Option C: Use Existing Agent Framework
- Reuse prov:wasAssociatedWith pattern
- Minimal ontology changes
- Less semantic precision

**Recommendation: Start with Option A for simplicity, migrate to B if needed**
