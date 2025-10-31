# Excel to Stage-Gate Conversion Guide

## Quick Reference

This guide explains how the system converts an Excel spreadsheet of pharmaceutical stage-gate deliverables into a semantic knowledge graph.

## Input: Excel Spreadsheet

**File**: `data/Protein and CGT_SGD Template Final_ENDORSED JAN 2023.xlsx`

### Key Columns in SGD Sheet:
- **Value Stream**: CGT or Protein (product type)
- **Stage Gate**: 0-12 (development checkpoint)
- **Stage Gate Description**: Name of the gate
- **Functional Area/Subteam**: Responsible team
- **Deliverable**: Specific requirement
- **Owner**: Person responsible (optional)

### Sample Input Row:
```
Value Stream: CGT
Stage Gate: 0
Stage Gate Description: Entry in Early Development
Functional Area: Analytical Development
Deliverable: Start collaboration with Cell Engineering
Owner: AD Lead
```

## Output: RDF/TTL Knowledge Graph

### Created Entities (per stage gate):

1. **ex:Stage-{stream}-{number}**
   - The development phase
   - Example: `ex:Stage-cgt-0`

2. **ex:Gate-{stream}-{number}**
   - The review checkpoint
   - Example: `ex:Gate-cgt-0`

3. **ex:Plan-{stream}-{number}**
   - The work plan
   - Example: `ex:Plan-cgt-0`

4. **ex:Spec-{stream}-{number}**
   - Requirements specification
   - Example: `ex:Spec-cgt-0`

5. **ex:CQA-{stream}-{number}-{deliverable}**
   - Individual deliverable as Quality Attribute
   - Example: `ex:CQA-cgt-0-start-collaboration`

### Sample Output (TTL/RDF):
```turtle
# Stage (development phase)
ex:Stage-cgt-0 a ex:Stage ;
    rdfs:label "Entry in Early Development" ;
    ex:hasPlan ex:Plan-cgt-0 ;
    ex:hasGate ex:Gate-cgt-0 ;
    ex:hasSpecification ex:Spec-cgt-0 .

# Gate (review checkpoint)
ex:Gate-cgt-0 a ex:StageGate ;
    rdfs:label "Gate for Entry in Early Development" .

# Specification (requirements)
ex:Spec-cgt-0 a ex:Specification ;
    rdfs:label "Specification for Entry in Early Development" ;
    ex:hasCQA ex:CQA-cgt-0-start-collaboration-with-cell .

# Quality Attribute (deliverable)
ex:CQA-cgt-0-start-collaboration-with-cell a ex:QualityAttribute ;
    rdfs:label "Start collaboration with Cell Engineering" ;
    prov:wasAttributedTo "AD Lead" .
```

## Conversion Process

### Step 1: Extract (Excel → CSV)
```bash
python3 scripts/etl/extract_xlsx.py --input-dir ./data
```
- Reads: Excel file with 5 sheets
- Creates: 5 CSV files in `data/extracted/`
- Main data: `*__SGD.csv` (~2,200 rows)

### Step 2: Generate (CSV → RDF)
```bash
python3 scripts/etl/generate_cmc_ttl.py
```
- Reads: SGD.csv
- Groups: Deliverables by stage gate
- Creates: RDF triples for each entity
- Output: `cmc_stagegate_instances.ttl` (~7,400 triples)

### Step 3: Combine (Merge Ontologies)
```bash
python3 scripts/etl/combine_ttls.py
```
- Merges:
  - Base ontology definitions
  - Generated instances
  - GIST alignment
  - Examples
- Output: `cmc_stagegate_all.ttl` (~15,466 triples)

### Step 4: Validate
```bash
python3 scripts/validation/verify_ttl_files.py
```
- Checks: TTL syntax
- Counts: Triples
- Verifies: GIST alignment

## Results

### By the Numbers:
- **Input**: 1 Excel file, 5 sheets, ~2,200 rows
- **Output**: 5 TTL files, 15,466 triples
- **Created**:
  - 26 Stage Gates (13 CGT + 13 Protein)
  - 26 Specifications
  - 2,113 Quality Attributes (deliverables)
  - 100% GIST aligned

### Stage Gate Distribution:
| Gate | CGT Deliverables | Protein Deliverables |
|------|-----------------|---------------------|
| 0 | 17 | 14 |
| 1 | 71 | 70 |
| 2 | 88 | 83 |
| 3 | 65 | 52 |
| 4 | 72 | 68 |
| 5 | 99 | 96 |
| 6 | 107 | 106 |
| 7 | 115 | 116 |
| 8 | 124 | 124 |
| 9 | 118 | 119 |
| 10 | 87 | 87 |
| 11 | 81 | 81 |
| 12 | 73 | 74 |

## One-Command Execution

Run the entire pipeline:
```bash
./run_pipeline.sh
```

Or with options:
```bash
./run_pipeline.sh --all              # Include GraphDB
./run_pipeline.sh -e                 # Skip extraction
./run_pipeline.sh --help             # See all options
```

## GIST Alignment

The system aligns all concepts to the GIST upper ontology:
- **ex:Stage** → **gist:PlannedEvent**
- **ex:StageGate** → **gist:Event**
- **ex:QualityAttribute** → **gist:Aspect**
- **ex:Specification** → **gist:Specification**

This enables interoperability with other enterprise systems using GIST.

## Use Cases

### Query Examples:

**Find all deliverables for Stage Gate 0:**
```sparql
SELECT ?deliverable ?label WHERE {
  ?stage rdfs:label ?stageLabel .
  FILTER(CONTAINS(?stageLabel, "Entry in Early Development"))
  ?stage ex:hasSpecification ?spec .
  ?spec ex:hasCQA ?deliverable .
  ?deliverable rdfs:label ?label .
}
```

**Count deliverables by functional area:**
```sparql
SELECT ?area (COUNT(?cqa) as ?count) WHERE {
  ?cqa a ex:QualityAttribute ;
       prov:wasAttributedTo ?area .
} GROUP BY ?area
```

## Files Generated

1. **CSVs** (in `data/extracted/`):
   - Protein_and_CGT_SGD_Template_Final_ENDORSED_JAN_2023__SGD.csv (main)
   - Plus 4 other sheets

2. **TTL Files** (in root):
   - `cmc_stagegate_base.ttl` - Ontology definitions
   - `cmc_stagegate_instances.ttl` - Generated data
   - `cmc_stagegate_gist_align.ttl` - GIST mappings
   - `cmc_stagegate_gist_examples.ttl` - Examples
   - `cmc_stagegate_all.ttl` - Complete graph

## Troubleshooting

| Problem | Solution |
|---------|----------|
| No CSVs created | Run extraction: `python3 scripts/etl/extract_xlsx.py --input-dir ./data` |
| TTL generation fails | Check pandas installed: `pip install pandas openpyxl` |
| Validation errors | Install rapper: `brew install raptor` or `apt-get install raptor2-utils` |
| Wrong counts | Verify Excel file has expected structure |

## Next Steps

1. **Deploy to GraphDB**: `./run_pipeline.sh --with-graphdb --no-dry-run`
2. **Run SPARQL queries**: Use GraphDB workbench or scripts
3. **Integrate with systems**: Use the RDF/TTL files or GraphDB API
4. **Extend ontology**: Add custom properties or alignments as needed

---

*For full documentation, see the main [README.md](../README.md)*
