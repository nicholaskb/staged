# 📚 Lexicon CSV Analysis & Integration Proposal

## Overview
The Lexicon CSV contains **174 pharmaceutical/biotechnology abbreviations and their definitions** used throughout the CMC Stage-Gate process.

## 📊 Data Structure

| Column | Description | Example |
|--------|-------------|---------|
| **Abbreviation & Nomenclature** | Industry acronym/term | `CQA`, `PPQ`, `GMP` |
| **Definition** | Full meaning/explanation | `Critical Quality Attributes`, `Process Performance Qualification` |

## 📈 Content Analysis

### Categories of Terms

#### 1. **Stage-Gate Core Terms** (Directly Referenced)
- `CQA` - Critical Quality Attributes (used in deliverables)
- `CPP` - Critical Process Parameters
- `PPQ` - Process Performance Qualification (stage name)
- `FIH` - First in Human
- `BLA` - Biologic License Application
- `IND` - Investigational New Drug

#### 2. **Organizational/Teams** (15 terms)
- `CDT` - Compound Development Team
- `BTDS` - BioTherapeutics Development & Supply
- `DAS` - Disease Area Stronghold
- `VCT` - Value Chain Team

#### 3. **Regulatory/Compliance** (20+ terms)
- `GMP` - Good Manufacturing Practice
- `CTD` - Common Technical Document
- `EMA` - European Medicines Agency (implied)
- `FDA` - Food and Drug Administration (implied)

#### 4. **Process/Manufacturing** (30+ terms)
- `DSP` - Down Stream Process
- `USP` - Up Stream Process
- `DOE` - Design of Experiments
- `PAR` - Proven Acceptable Range

#### 5. **Cell/Gene Therapy Specific** (10+ terms)
- `MCB` - Master Cell Bank
- `WCB` - Working Cell Bank
- `EOPCB` - End of Production Cell Bank
- `CGTV` - Cell & Gene Therapy and Vaccines

## 🎯 Integration into CMC Ontology

### Proposed Ontology Extensions

```turtle
# New Classes
ex:Abbreviation rdfs:subClassOf gist:Category ;
    rdfs:label "Industry Abbreviation" ;
    rdfs:comment "Standard pharmaceutical/biotech abbreviation" .

ex:DefinedTerm rdfs:subClassOf skos:Concept ;
    rdfs:label "Defined Term" ;
    rdfs:comment "Term with formal industry definition" .

# New Properties
ex:hasAbbreviation a owl:DatatypeProperty ;
    rdfs:domain ex:DefinedTerm ;
    rdfs:range xsd:string ;
    rdfs:label "has abbreviation" .

ex:hasDefinition a owl:DatatypeProperty ;
    rdfs:domain ex:DefinedTerm ;
    rdfs:range xsd:string ;
    rdfs:label "has definition" .

ex:usedInStage a owl:ObjectProperty ;
    rdfs:domain ex:DefinedTerm ;
    rdfs:range ex:Stage ;
    rdfs:label "used in stage" .

ex:relatedToDeliverable a owl:ObjectProperty ;
    rdfs:domain ex:DefinedTerm ;
    rdfs:range ex:QualityAttribute ;
    rdfs:label "related to deliverable" .
```

## 💡 Use Cases

### 1. **Enhanced Deliverable Understanding**
Link abbreviations to deliverables for clarity:
```sparql
# Find all abbreviations used in Stage 5 deliverables
SELECT ?abbr ?definition WHERE {
    ?deliverable ex:inStage ex:Stage-protein-5 ;
                 ex:deliverableText ?text .
    ?term ex:hasAbbreviation ?abbr ;
          ex:hasDefinition ?definition ;
          ex:relatedToDeliverable ?deliverable .
}
```

### 2. **Regulatory Compliance Tracking**
Track regulatory terms across stages:
```sparql
# Find all regulatory abbreviations (GMP, GLP, etc.)
SELECT ?stage ?abbr WHERE {
    ?term ex:hasAbbreviation ?abbr ;
          ex:category "Regulatory" ;
          ex:usedInStage ?stage .
    FILTER(REGEX(?abbr, "^G[ML]P"))
}
```

### 3. **Team/Organization Mapping**
Link teams to their deliverables:
```sparql
# Find which teams are responsible for what
SELECT ?team ?definition ?deliverable WHERE {
    ?term ex:hasAbbreviation ?team ;
          ex:hasDefinition ?definition ;
          ex:category "Organization" .
    ?deliverable ex:responsibleTeam ?term .
}
```

## 📝 Implementation Script

```python
# generate_lexicon_ttl.py
import csv
from pathlib import Path

def generate_lexicon_ontology():
    """Generate RDF from Lexicon CSV"""
    
    csv_path = Path("data/current/..._Lexicon.csv")
    output_path = Path("output/current/cmc_stagegate_lexicon_instances.ttl")
    
    with open(csv_path, 'r') as f:
        reader = csv.DictReader(f)
        
        ttl_lines = [
            "@prefix ex: <https://w3id.org/cmc-stagegate#> .",
            "@prefix skos: <http://www.w3.org/2004/02/skos/core#> .",
            "@prefix rdfs: <http://www.w3.org/2000/01/rdf-schema#> .",
            "",
            "# Lexicon Terms",
        ]
        
        for row in reader:
            abbr = row['Abbreviation & Nomenclature']
            defn = row['Definition']
            
            # Generate GUPRI
            term_id = f"ex:Term_{abbr.replace(' ', '_')}"
            
            ttl_lines.extend([
                f"{term_id} a ex:DefinedTerm ;",
                f"    ex:hasAbbreviation \"{abbr}\" ;",
                f"    ex:hasDefinition \"{escape(defn)}\" ;",
                f"    skos:prefLabel \"{abbr}\" ;",
                f"    skos:definition \"{escape(defn)}\" .",
                ""
            ])
```

## 🔗 Linkage Opportunities

### Connect to Existing Data
1. **CQA** → Link to all `ex:QualityAttribute` instances
2. **PPQ** → Link to `ex:Stage-protein-11` (PPQ stage)
3. **MCB/WCB** → Link to Cell Therapy stages
4. **FIH** → Link to `ex:Stage-protein-3` (First in Human)

### Create Cross-References
- Link SMEs to their abbreviations (e.g., `QA` → Quality Assurance SME)
- Link modalities to relevant terms (e.g., `CAR` → Cell Therapy modality)
- Link stages to required regulatory terms

## 📊 Statistics

| Metric | Count |
|--------|-------|
| Total Terms | 174 |
| Regulatory Terms | ~25 |
| Process Terms | ~40 |
| Organization Terms | ~15 |
| Cell/Gene Terms | ~12 |
| Quality Terms | ~20 |

## 🎯 Value Proposition

### Why Integrate the Lexicon?

1. **Disambiguation**: Clear definitions for all abbreviations
2. **Searchability**: Query by abbreviation or full term
3. **Context**: Link terms to where they're used
4. **Compliance**: Track regulatory terminology usage
5. **Onboarding**: Help new team members understand terminology

## 💼 Business Benefits

- **Reduced Confusion**: Everyone knows what abbreviations mean
- **Better Search**: Find deliverables by abbreviation
- **Regulatory Alignment**: Track compliance terminology
- **Knowledge Management**: Central glossary of terms
- **Training Tool**: New employee onboarding

## 🚀 Next Steps

1. **Create Lexicon Ontology Extension** (`cmc_stagegate_lexicon.ttl`)
2. **Generate Instance Data** from CSV
3. **Link to Existing Entities** (stages, deliverables, SMEs)
4. **Add to Pipeline** (include in `combine_ttls.py`)
5. **Create SPARQL Queries** for term lookup

Would you like me to implement the Lexicon integration into your ontology?
