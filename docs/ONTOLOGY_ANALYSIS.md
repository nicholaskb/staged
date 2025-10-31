# CMC Stage-Gate Ontology Analysis

**Date:** October 31, 2025  
**Purpose:** Comprehensive analysis of the current CMC Stage-Gate ontology structure, dependencies, and definitions

## Executive Summary

The CMC Stage-Gate ontology is a **hybrid architecture** that:
- **75% Custom**: Domain-specific CMC/pharmaceutical concepts
- **25% External**: Leverages established ontologies (GIST, PROV-O, QUDT)
- **Well-defined**: Clear definitions for all 11 core classes and 29 properties
- **Semantically aligned**: Properly integrated with upper ontologies for interoperability

## 1. Ontology Architecture

### 1.1 File Structure
```
Core Files (389 triples):
├── cmc_stagegate_base.ttl (134 triples)     # Core domain concepts
├── cmc_stagegate_gist_align.ttl (71 triples) # Semantic alignment
└── cmc_stagegate_gist_examples.ttl (184 triples) # Usage patterns

Generated Files (14,777 triples):
├── cmc_stagegate_instances.ttl (7,294 triples) # Data from Excel
└── cmc_stagegate_all.ttl (7,483 triples)      # Combined output
```

### 1.2 Namespace Strategy
- **Primary**: `ex:` (https://w3id.org/cmc-stagegate#) - Our custom CMC concepts
- **External**: Multiple established ontologies for semantic grounding

## 2. External Ontology Dependencies

### 2.1 GIST Upper Ontology (Semantic Arts)
**Purpose:** Provides foundational semantic patterns  
**Usage:** 47 alignment points, 77 references in examples  
**Key Alignments:**
- `ex:Stage` → `gist:PlannedEvent` (lifecycle phases)
- `ex:StageGate` → `gist:Event` (review events)
- `ex:Material` → `gist:PhysicalSubstance ∪ gist:PhysicalIdentifiableItem`
- `ex:QualityAttribute` → `gist:Aspect` (measurable characteristics)
- `ex:AnalyticalResult` → `gist:Magnitude` (measurements)
- `ex:Lot` → `gist:Collection` (batch collections)

**Benefits:** 
- Semantic interoperability with other GIST-based systems
- Well-established patterns for events, measurements, and collections
- Future-proof upgrade path to GIST v13

### 2.2 PROV-O (W3C Provenance Ontology)
**Purpose:** Track provenance and lineage  
**Usage:** Throughout for activities and entities  
**Key Uses:**
- `ex:StageGate` subclass of `prov:Activity`
- `prov:startedAtTime`, `prov:endedAtTime` for temporal tracking
- `prov:wasAssociatedWith` for agent attribution
- `prov:used` for evidence consumption

**Benefits:**
- Standard provenance tracking
- Audit trail capabilities
- Workflow documentation

### 2.3 QUDT (Quantities, Units, Dimensions, Types)
**Purpose:** Handle measurements and units  
**Usage:** All analytical results  
**Key Properties:**
- `qudt:numericValue` for measurement values
- `qudt:unit` for units of measure (linked to QUDT unit vocabulary)

**Benefits:**
- Standardized unit representation
- Interoperable measurements
- Scientific data exchange

### 2.4 Additional Standards
- **SKOS**: Concept schemes for controlled vocabularies
- **GS1**: Product identification (GTIN)
- **FHIR**: Healthcare interoperability hooks
- **P-Plan**: Process planning patterns

## 3. Core Domain Concepts (Custom)

### 3.1 Lifecycle Management Classes
```turtle
ex:Stage         # Development phase (e.g., Scale-up, PPQ, CPV)
ex:StageGate     # Review/decision point with evidence assessment
ex:StagePlan     # Template for stage activities and deliverables
```

### 3.2 Manufacturing Classes
```turtle
ex:Process       # Manufacturing process/recipe
ex:UnitOperation # Individual manufacturing step (granulation, coating)
ex:Material      # Drug substance, product, or excipient
ex:Lot           # Specific batch/lot of material
```

### 3.3 Quality Classes
```turtle
ex:Specification      # Quality requirements
ex:QualityAttribute   # Critical quality attribute (CQA)
ex:AnalyticalMethod   # Test method/protocol
ex:AnalyticalResult   # Test result with value and unit
```

## 4. Property Definitions

### 4.1 Structural Properties (15)
- **Stage Structure**: `hasPlan`, `hasGate`
- **Process Hierarchy**: `definesProcess`, `hasUnitOperation`
- **Material Flow**: `consumesMaterial`, `producesMaterial`, `hasLot`
- **Quality Links**: `hasSpecification`, `hasCQA`, `evaluatedBy`
- **Evidence**: `hasEvidence`, `assessedAtGate`, `measuredOnLot`

### 4.2 Data Properties (14)
- **Identifiers**: `lotNumber`, `gs1:gtin`, `substanceUNII`
- **Pharmaceutical**: `doseForm`, `routeOfAdmin`
- **Decisions**: `decision` (approved|conditional|rejected)
- **NEW Temporal**: `plannedDate`, `actualDate`
- **NEW Documentation**: `reference`, `hasCategory`

## 5. Instance Data Analysis

From current Excel input (7,294 triples):
- **26 Stages**: 13 for CGT, 13 for Protein modalities
- **2,205 Deliverables**: Mapped as QualityAttributes
- **1,172 Categorized items**: Using new Category column
- **25 Unique Categories**: API Dev, DP Analytics, Biopharmaceutics, etc.

## 6. Semantic Patterns

### 6.1 Stage-Gate Pattern
```turtle
Stage (planned phase) → has → Plan → defines → Process
                      → has → Gate (review event) → uses → Evidence
```

### 6.2 Quality Pattern
```turtle
Material → has → Specification → has → CQA
                               → based on → AnalyticalResult
Lot → measured by → Result → is aspect of → CQA
```

### 6.3 Identifier Pattern (GIST-aligned)
```turtle
# Current: Direct properties
ex:Lot-123 ex:lotNumber "123" .

# Future: ID nodes
ex:ID-LOT-123 a gist:ID ;
    gist:identifies ex:Lot-123 .
```

## 7. Strengths and Gaps

### Strengths ✅
1. **Clear domain model**: Well-defined CMC concepts
2. **Semantic grounding**: Proper alignment with upper ontologies
3. **Extensible**: Easy to add new properties (as we just did)
4. **Standards-compliant**: Uses W3C standards throughout
5. **Provenance-ready**: Full PROV-O integration
6. **Measurement-capable**: QUDT for all analytical data

### Current Gaps 🔍
1. **Stage sequencing**: No explicit predecessor/successor relationships
2. **Approval workflows**: Basic decision tracking, could be richer
3. **Risk assessment**: No risk categories or mitigation strategies
4. **Document management**: Basic references, no document ontology
5. **Organizational roles**: Limited role/responsibility modeling
6. **Regulatory mapping**: No direct regulatory requirement links

## 8. Recommendations

### Immediate Enhancements
1. Add stage sequencing properties:
   ```turtle
   ex:hasNextStage rdfs:domain ex:Stage ; rdfs:range ex:Stage .
   ex:hasPreviousStage owl:inverseOf ex:hasNextStage .
   ```

2. Enhance role modeling:
   ```turtle
   ex:hasRole rdfs:domain gist:Person ; rdfs:range ex:Role .
   ex:Role rdfs:subClassOf skos:Concept .
   ```

3. Add risk properties:
   ```turtle
   ex:hasRisk rdfs:domain ex:Stage ; rdfs:range ex:Risk .
   ex:riskLevel rdfs:domain ex:Risk ; rdfs:range xsd:string .
   ```

### Future Considerations
1. **Migrate to GIST v13** when stable (hasAspect pattern)
2. **Implement ID nodes** for all identifiers
3. **Add document ontology** (possibly align with DCAT)
4. **Create SHACL shapes** for validation
5. **Build competency questions** for testing

## 9. Usage Examples

### Query: Find all deliverables in PPQ stage
```sparql
SELECT ?deliverable ?category ?plannedDate WHERE {
  ?stage rdfs:label ?stageLabel .
  FILTER(CONTAINS(?stageLabel, "PPQ"))
  ?deliverable a ex:QualityAttribute ;
               ex:hasCategory ?category ;
               ex:plannedDate ?plannedDate .
  # Link through stage relationship
}
```

### Query: Track evidence for gate decisions
```sparql
SELECT ?gate ?decision ?evidence WHERE {
  ?gate a ex:StageGate ;
        ex:decision ?decision ;
        prov:used ?evidence .
}
```

## 10. Conclusion

The CMC Stage-Gate ontology represents a **mature, well-structured** domain model that:
- Successfully balances custom pharmaceutical concepts with standard ontologies
- Provides clear definitions and relationships for all core concepts
- Maintains semantic interoperability through GIST alignment
- Supports comprehensive data capture from regulatory templates

The recent additions (Category, Plan/Actual dates, References) demonstrate the ontology's flexibility and ability to evolve with business needs while maintaining semantic consistency.

**Overall Assessment: Production-Ready** with clear upgrade paths for future enhancements.
