# CMC Stage-Gate Ontology with GIST Alignment

A comprehensive ontology framework for stage-gated CMC (Chemistry, Manufacturing, and Controls) program management, featuring full alignment with the GIST upper ontology for semantic interoperability.

## 📁 Data Organization

### Where to Put Your Files
- **Input Excel**: Place in `data/current_input/` 📥
- **Extracted CSVs**: Auto-generated in `data/current/` 📤
- **Generated TTLs**: Created in `output/current/` 📦
- **Previous Data**: Archived in `data/previous_input_YYMMDD/` and `data/extracted_YYMMDD/`
- **Previous TTLs**: Archived in `output/ttl_YYMMDD_*/`

### Quick Setup for New Files
```bash
# 1. Place your Excel file in the input folder
cp "Your Excel File.xlsx" data/current_input/

# 2. Run the pipeline (extracts, converts, validates)
./run_pipeline.sh
```

## 🚀 Quick Start

### One-Command Pipeline
```bash
# Convert Excel → Stage Gates → RDF/TTL → Knowledge Graph
./run_pipeline.sh
```

### What This Does
1. **Extracts** Excel data from `data/current_input/` folder
2. **Converts** 2,200+ rows into stage gates with 2,200+ deliverables
3. **Generates** 15,466 RDF triples in TTL format
4. **Validates** all ontology files and GIST alignment
5. **Ready** for GraphDB deployment (add `--with-graphdb` to deploy)

### Manual Steps (if needed)
```bash
# Step 1: Extract Excel to CSV
# (reads from data/current_input/, writes to data/current/)
python3 scripts/etl/extract_xlsx.py

# Step 2: Generate RDF from CSV
# (reads from data/current/, creates output/current/cmc_stagegate_instances.ttl)
python3 scripts/etl/generate_cmc_ttl.py

# Step 3: Combine with ontology
# (creates output/current/cmc_stagegate_all.ttl)
python3 scripts/etl/combine_ttls.py

# Step 4: Validate
python3 scripts/validation/verify_ttl_files.py

# Step 5: Deploy (optional)
python3 scripts/deployment/export_to_graphdb.py --no-dry-run
```

**Result**: ✅ 15,466 triples validated, ready for use!

## 📋 Table of Contents
- [Overview](#overview)
- [Project Structure](#project-structure)
- [File Descriptions](#file-descriptions)
- [Installation & Setup](#installation--setup)
- [Usage Guide](#usage-guide)
- [GIST Alignment](#gist-alignment)
- [SPARQL Query Examples](#sparql-query-examples)
- [GraphDB Integration](#graphdb-integration)
- [Design Philosophy](#design-philosophy)
- [Technical Architecture](#technical-architecture)
- [Business Applications](#business-applications)
- [Roadmap & Next Steps](#roadmap--next-steps)

## Overview

This project provides a semantic framework for managing pharmaceutical CMC stage-gate processes, combining:
- A minimal, reuse-first ontology leveraging established vocabularies (PROV-O, P-Plan, QUDT, GS1)
- Full alignment with GIST v11+ upper ontology for enterprise interoperability
- Automated ETL pipeline from Excel to RDF/TTL
- GraphDB integration for knowledge graph deployment
- Comprehensive validation and query tools

### ✅ Key Achievements
- **15,466 triples** validated across 5 TTL files
- **100% GIST alignment** with 12 classes and 11 properties mapped
- **2,200+ Quality Attributes** successfully modeled as gist:Aspect
- **Stage-Gate processes** aligned to gist:PlannedEvent
- **7,385 triples** deployed to GraphDB
- **All SPARQL queries** validated and working

## Project Structure

```
staged/
├── Ontology Files (TTL)
│   └── SOURCE FILES (in root - manually created):
│       ├── cmc_stagegate_base.ttl          # Core CMC ontology definitions
│       ├── cmc_stagegate_gist_align.ttl    # GIST alignment mappings
│       └── cmc_stagegate_gist_examples.ttl # GIST pattern examples (optional)
│
├── output/                                  # Generated TTL files
│   ├── current/                            # Latest generated files
│   │   ├── cmc_stagegate_instances.ttl    # Generated from CSV (7,294 triples)
│   │   └── cmc_stagegate_all.ttl          # Combined output (7,483 triples)
│   └── ttl_YYMMDD_*/                      # Timestamped archives of previous versions
│
├── Python Scripts
│   ├── scripts/
│   │   ├── etl/                        # ETL pipeline scripts
│   │   │   ├── extract_xlsx.py         # Excel sheet extractor
│   │   │   ├── analyze_columns.py      # Data profiling & mapping tool
│   │   │   ├── generate_cmc_ttl.py     # TTL instance generator
│   │   │   └── combine_ttls.py         # TTL file merger
│   │   ├── validation/                 # Validation & testing scripts
│   │   │   ├── validate_gist_alignment.py  # GIST alignment validator
│   │   │   ├── verify_ttl_files.py     # Comprehensive TTL validator
│   │   │   ├── test_gist_queries.py    # GIST alignment test queries
│   │   │   ├── test_gist_alignment.sh  # SPARQL validation tests
│   │   │   └── gist_practical_examples.sh  # Practical GIST demonstrations
│   │   ├── deployment/                 # Deployment scripts
│   │   │   └── export_to_graphdb.py    # GraphDB uploader
│   │   └── analysis/                   # Analysis & visualization
│   │       ├── stage_gate_flow.py      # Stage gate flow analysis
│   │       ├── visualize_stage_gate.py # Visualization tools
│   │       ├── stage_gate_recommendation.py  # Recommendation system
│   │       └── comprehensive_stage_gate_ontology.py  # Ontology analysis
│
├── Query & Documentation
│   ├── queries/
│   │   └── gist_example_queries.sparql    # GIST-aligned SPARQL examples
│   ├── docs/
│   │   ├── TTL_GENERATION_REPORT.md       # Detailed generation statistics
│   │   ├── CONVERSION_GUIDE.md            # Excel to RDF conversion guide
│   │   └── CLEANUP_SUMMARY.md             # Repository organization
│   └── README.md                           # This documentation
│
└── Data Files
    ├── data/
    │   ├── current_input/              # 📥 PLACE NEW INPUT FILES HERE
    │   │   └── *.xlsx                  # Current Excel file being processed
    │   ├── current/                    # 📤 Auto-generated CSV extractions
    │   │   ├── *__SGD.csv             # Main stage-gate data
    │   │   ├── *__Drop_Downs.csv      # Vocabulary/picklists
    │   │   ├── *__Lexicon.csv         # Term definitions
    │   │   ├── *__SME.csv             # Subject matter experts
    │   │   └── *__[SheetName].csv     # Other sheets from Excel
    │   ├── previous_input_YYMMDD/     # Archived input files (timestamped)
    │   │   └── *.xlsx                  # Previous versions
    │   └── extracted_YYMMDD/          # Archived CSV extractions (timestamped)
    │       └── *.csv                   # Previous extractions
```

## File Descriptions

### 🔷 Ontology Files (TTL)

#### `cmc_stagegate_base.ttl`
**Purpose**: Core ontology defining the CMC stage-gate conceptual model  
**Size**: ~100 lines  
**Key Features**:
- Defines 11 core classes: Stage, StageGate, StagePlan, Process, UnitOperation, Material, Lot, Specification, QualityAttribute, AnalyticalMethod, AnalyticalResult
- Establishes relationships: hasPlan, hasGate, hasSpecification, hasCQA, evaluatedBy, hasEvidence
- Integrates external vocabularies: PROV-O (provenance), P-Plan (plans), QUDT (units), GS1 (identifiers)
- Provides extension points for EDQM, UNII/GSRS, FHIR

#### `cmc_stagegate_instances.ttl`
**Purpose**: Auto-generated instances from Excel data  
**Size**: ~4,000+ lines  
**Generated Content**:
- Stage instances for each value stream (CGT, Protein)
- StageGate reviews with associated specifications
- QualityAttribute (CQA) instances with owner attributions
- Provisional prov:Agent nodes for stakeholders

#### `cmc_stagegate_gist_align.ttl`
**Purpose**: Maps CMC concepts to GIST upper ontology for interoperability  
**Size**: ~250 lines  
**Mappings**:
- 11 class alignments (100% coverage)
- 13 property alignments  
- References 26 GIST concepts
- Includes GIST v13 migration notes
- Optional material subclasses (BulkMaterial, PackagedUnit)
- Lot-Material relationships (hasLot/lotOf)

#### `cmc_stagegate_gist_examples.ttl`
**Purpose**: Demonstrates all GIST alignment patterns with concrete examples  
**Size**: ~600 lines  
**Contents**:
- Stage vs Gate pattern with PPQ example
- Material union/split with bulk and packaged units
- Complete identifier node patterns (GTIN, NDC, Lot numbers)
- GIST v13 migration examples
- Full process chain with material flow
- Multiple CQAs with analytical results

#### `cmc_stagegate_all.ttl`
**Purpose**: Combined ontology (base + instances + GIST alignment)  
**Size**: ~706 KB, 4,891 lines  
**Usage**: Single file for GraphDB import containing complete knowledge graph

### 🔧 Python Scripts

#### `extract_xlsx.py`
**Purpose**: Extract all sheets from Excel workbooks to CSV files  
**Features**:
- Processes all .xlsx files in specified directory
- Preserves sheet names in output filenames
- Optional CSV combination for multi-sheet workbooks
- Handles special characters and encoding issues

**Usage**:
```bash
python3 scripts/etl/extract_xlsx.py --input-dir ./data --output-dir ./data/extracted --combine
```

#### `analyze_columns.py`
**Purpose**: Profile spreadsheet data and suggest ontology mappings  
**Analysis**:
- Column uniqueness detection
- Value distribution analysis
- Comma-separated value identification
- Data type inference
- Ontology mapping recommendations

**Output**: Detailed report with statistics and mapping suggestions for each column

#### `generate_cmc_ttl.py`
**Purpose**: Parse CSV data and generate RDF instances  
**Key Logic**:
- Treats row 2 as header in SGD sheet (skips metadata row 1)
- Creates Stage/StageGate/Specification hierarchies
- Links CQAs to specifications via ex:hasCQA
- Handles multi-owner attribution (comma-separated)
- Escapes special characters for GraphDB compatibility

**Configuration**: Hardcoded paths (modify DEFAULT_* constants as needed)

#### `combine_ttls.py`
**Purpose**: Merge multiple TTL files with prefix deduplication  
**Features**:
- Preserves first occurrence of each @prefix declaration
- Maintains file separation with newlines
- Default files: base, instances, gist_align → all

**Usage**:
```bash
python3 scripts/etl/combine_ttls.py --files base.ttl instances.ttl align.ttl --out combined.ttl
```

#### `validate_gist_alignment.py`
**Purpose**: Validate consistency between base ontology and GIST alignment  
**Validation Checks**:
- All mapped classes exist in base ontology
- All mapped properties are defined
- Coverage metrics (% of concepts aligned)
- Lists all GIST terms referenced

**Output**: Validation report with coverage statistics and any issues found

#### `verify_ttl_files.py`
**Purpose**: Comprehensive TTL/OWL file validation with rapper  
**Features**:
- Validates all TTL files for syntax errors
- Counts triples using rapper RDF parser
- Analyzes content (prefixes, classes, properties)
- Checks GIST alignment mappings
- Provides detailed statistics

**Output**: Full validation report with triple counts and statistics

#### `test_gist_queries.py`
**Purpose**: Test SPARQL queries demonstrating GIST alignment  
**Requirements**: `requests` library  
**Tests**: 12+ comprehensive queries validating all alignments

### 🐚 Shell Scripts

#### `scripts/validation/test_gist_alignment.sh`
**Purpose**: Validate GIST alignment with SPARQL queries  
**Tests**:
- Class alignments (12 mappings verified)
- Property alignments (11 mappings verified)
- Instance counts by GIST class
- QUDT-GIST bridge validation
- Integration patterns

**Results**: All alignments validated with 2,113 CQAs, 26 stages

#### `scripts/validation/gist_practical_examples.sh`
**Purpose**: Demonstrate practical GIST benefits  
**Examples**:
- Timeline of planned events
- Task decomposition hierarchies
- Measurable quality aspects
- Process participation patterns
- Universal specification queries
- Evidence traceability

#### `export_to_graphdb.py`
**Purpose**: Upload TTL data to GraphDB repository  
**Features**:
- RDF4J REST API integration
- Basic authentication support
- Named graph (context) specification
- Retry logic with exponential backoff
- Dry-run mode for testing

**Configuration via Environment Variables**:
- `GRAPHDB_URL`: Server URL (e.g., http://localhost:7200)
- `GRAPHDB_REPOSITORY`: Repository ID
- `GRAPHDB_CONTEXT`: Named graph IRI
- `GRAPHDB_USER`, `GRAPHDB_PASSWORD`: Optional auth

### 📊 Query & Documentation

#### `gist_example_queries.sparql`
**Purpose**: Demonstrate GIST-aligned query patterns  
**Contents**: 12+ SPARQL queries showing:
- Finding analytical results via gist:hasMagnitude
- Checking specification conformance
- Tracing material flow through processes
- Navigating task hierarchies
- Gate review assessments
- Quality attribute analysis
- GIST v13 migration examples

#### `README.md`
**Purpose**: Comprehensive project documentation (this file)

### 📁 Data Files

#### Source Data
- **Excel Workbook**: `Protein and CGT_SGD Template Final_ENDORSED JAN 2023.xlsx`
  - Multi-sheet workbook with CMC stage-gate definitions
  - Contains deliverables, owners, timelines, and metadata

#### Extracted CSVs
- **SGD.csv**: Main stage-gate deliverables (800+ rows)
- **Drop_Downs.csv**: Controlled vocabularies/picklists
- **Lexicon.csv**: Term definitions and explanations
- **SME.csv**: Subject matter expert assignments
- **Ped_CMC_Strat_Review_Protein.csv**: Pediatric strategy review data

## Installation & Setup

### Prerequisites
- Python 3.10 or higher
- Required: pandas, openpyxl (for Excel processing)
- Optional: GraphDB 10.x (for knowledge graph deployment)
- Optional: rapper (for TTL validation with verify_ttl_files.py)

### Installation Steps

1. **Clone/Download Repository**
```bash
git clone [repository-url]
cd staged
```

2. **Install Dependencies**
```bash
pip install pandas openpyxl requests
```

3. **Verify Installation**
```bash
python3 --version  # Should be 3.10+
ls -la *.ttl      # Check ontology files
```

4. **Clean Up (Optional)**
```bash
# The deprecated/ folder contains obsolete files and can be safely removed
rm -rf deprecated/
```

## Usage Guide

### 📊 Understanding the Input Data

#### Source Excel File Location
The system processes pharmaceutical CMC stage-gate template Excel files from:
- **Location**: `data/current_input/` folder
- **File Format**: `*.xlsx` Excel workbook
- **Purpose**: Contains stage-gate deliverables for pharmaceutical development
- **Sheets**: SGD (main data), Drop_Downs, Lexicon, SME, and others

#### 🔄 Updating the Input File
When you have a new Excel file to process:

1. **Place New File**: Put your Excel file in `data/current_input/`
   ```bash
   cp "Your New File.xlsx" data/current_input/
   ```

2. **Archive Previous Version** (Optional - for versioning):
   ```bash
   # Move old input to timestamped folder
   mv data/current_input/*.xlsx data/previous_input_$(date +%y%m%d)/
   
   # Move old CSVs to timestamped folder
   mv data/current/* data/extracted_$(date +%y%m%d)/
   ```

3. **Extract and Process**:
   ```bash
   # Run the pipeline - automatically uses current_input/
   ./run_pipeline.sh
   
   # Or extract manually
   python3 scripts/etl/extract_xlsx.py
   ```

The scripts automatically:
- Read Excel from `data/current_input/`
- Extract CSVs to `data/current/`
- Process from `data/current/`

#### Key Data Elements in Excel
The SGD sheet contains ~2,200 rows with these critical columns:
1. **Value Stream**: Product type (CGT or Protein)
2. **Stage Gate**: Gate number (0-12)
3. **Stage Gate Description**: What the gate represents (e.g., "Entry in Early Development")
4. **Functional Area/Subteam**: Responsible team (e.g., "Analytical Development")
5. **Deliverable**: Specific requirement that must be met
6. **Owner**: Person/role responsible (optional)
7. **Status**: Current state (optional)

### 🔄 Conversion Process: Excel to Stage-Gate Ontology

#### Visual Flow
```
Excel File (XLSX)
    │
    ├──[Extract]──> CSV Files (5 sheets)
    │                   │
    │                   └──> SGD.csv (main data ~2,200 rows)
    │                           │
    │                           ├── Value Stream (CGT/Protein)
    │                           ├── Stage Gate (0-12)
    │                           ├── Description
    │                           ├── Functional Area
    │                           ├── Deliverable
    │                           └── Owner
    │
    ├──[Generate]──> RDF/TTL Instances
    │                   │
    │                   ├──> ex:Stage (78 development phases)
    │                   ├──> ex:StageGate (78 review points)
    │                   ├──> ex:Specification (78 requirement sets)
    │                   └──> ex:QualityAttribute (2,205 deliverables)
    │
    ├──[Combine]──> Complete Ontology
    │                   │
    │                   ├── Base definitions
    │                   ├── Generated instances
    │                   ├── GIST alignment
    │                   └── Examples
    │
    └──[Deploy]──> GraphDB Knowledge Graph
                        │
                        └── 15,466 triples ready for SPARQL queries
```

#### What Gets Created
For each unique stage gate in the Excel data, the system creates:

1. **ex:Stage** - The development phase
   - Example: `ex:Stage-cgt-0` for "CGT Stage Gate 0"
   - Has label: "Entry in Early Development"

2. **ex:StageGate** - The review checkpoint
   - Example: `ex:Gate-cgt-0`
   - Represents the decision point between stages

3. **ex:StagePlan** - The plan for that stage
   - Example: `ex:Plan-cgt-0`
   - Contains the work to be done

4. **ex:Specification** - Requirements for the stage
   - Example: `ex:Spec-cgt-0`
   - Groups all deliverables for that gate

5. **ex:QualityAttribute** (CQA) - Individual deliverables
   - Example: `ex:CQA-cgt-0-start-collaboration-with-cell`
   - Each deliverable becomes a quality attribute
   - Linked to specification via `ex:hasCQA`

#### Data Transformation Example
**Input (Excel Row)**:
```
Value Stream: CGT
Stage Gate: 0
Stage Gate Description: Entry in Early Development
Functional Area: Analytical Development
Deliverable: Start collaboration with Cell Engineering
Owner: AD Lead
```

**Output (RDF/TTL)**:
```turtle
ex:Stage-cgt-0 a ex:Stage ;
    rdfs:label "Entry in Early Development" ;
    ex:hasPlan ex:Plan-cgt-0 ;
    ex:hasGate ex:Gate-cgt-0 ;
    ex:hasSpecification ex:Spec-cgt-0 .

ex:Gate-cgt-0 a ex:StageGate ;
    rdfs:label "Gate for Entry in Early Development" .

ex:Spec-cgt-0 a ex:Specification ;
    rdfs:label "Specification for Entry in Early Development" ;
    ex:hasCQA ex:CQA-cgt-0-start-collaboration-with-cell .

ex:CQA-cgt-0-start-collaboration-with-cell a ex:QualityAttribute ;
    rdfs:label "Start collaboration with Cell Engineering" ;
    prov:wasAttributedTo "AD Lead" .
```

### 🛠️ Complete Workflow - Step by Step

#### Option 1: Automated Pipeline (Recommended)
```bash
# Run everything with one command
./run_pipeline.sh

# Or with specific options:
./run_pipeline.sh --all              # Include GraphDB deployment
./run_pipeline.sh -e                 # Skip extraction if CSVs exist
./run_pipeline.sh --help             # See all options
```

#### Option 2: Manual Step-by-Step

##### Step 1: Extract Excel Data to CSV
```bash
python3 scripts/etl/extract_xlsx.py --input-dir ./data --combine
```
**What it does**: 
- Reads the Excel file
- Extracts each sheet to a separate CSV file
- Creates 5 CSV files in `data/extracted/`
- Main data is in `*__SGD.csv`

##### Step 2: Analyze Data Structure (Optional)
```bash
python3 scripts/etl/analyze_columns.py
```
**What it does**:
- Profiles each column in the CSV
- Shows data statistics (unique values, empty cells)
- Suggests ontology mappings
- Helps understand the data before conversion

##### Step 3: Generate RDF/TTL Instances
```bash
python3 scripts/etl/generate_cmc_ttl.py
```
**What it does**:
- Reads `data/extracted/*__SGD.csv`
- Creates RDF triples for each stage gate
- Generates ~7,400 triples
- Outputs to `cmc_stagegate_instances.ttl`

**Conversion Logic**:
1. Groups deliverables by Stage Gate number
2. Creates Stage, Gate, Plan, and Specification for each unique gate
3. Converts each deliverable to a QualityAttribute (CQA)
4. Links CQAs to their parent Specification
5. Preserves owner information as prov:wasAttributedTo

##### Step 4: Combine with Base Ontology
```bash
python3 scripts/etl/combine_ttls.py
```
**What it does**:
- Merges 4 TTL files:
  - `cmc_stagegate_base.ttl` (ontology definitions)
  - `cmc_stagegate_instances.ttl` (generated data)
  - `cmc_stagegate_gist_align.ttl` (GIST mappings)
  - `cmc_stagegate_gist_examples.ttl` (examples)
- Creates `cmc_stagegate_all.ttl` (complete knowledge graph)

##### Step 5: Validate Everything
```bash
python3 scripts/validation/verify_ttl_files.py
```
**Expected Output**:
- ✅ All 5 TTL files valid
- 📊 Total: 15,466 triples
- Shows breakdown by file

##### Step 6: Validate GIST Alignment
```bash
python3 scripts/validation/validate_gist_alignment.py
```
**Expected Output**:
- ✅ 100% class coverage
- ✅ 14 properties mapped
- Shows all GIST concepts used

##### Step 7: Deploy to GraphDB (Optional)
```bash
python3 scripts/deployment/export_to_graphdb.py \
  --graphdb-url http://localhost:7200 \
  --repository cmc-stagegate \
  --files cmc_stagegate_all.ttl \
  --no-dry-run
```
**What it does**:
- Uploads the complete ontology to GraphDB
- Creates knowledge graph for querying
- Result: ~7,385 triples loaded

##### Step 8: Test with SPARQL Queries
```bash
./scripts/validation/test_gist_alignment.sh
```
**What it does**:
- Runs validation queries against GraphDB
- Verifies all alignments work correctly

### 📈 Understanding Stage Gates in Pharmaceutical Development

#### What Are Stage Gates?
Stage gates are checkpoints in pharmaceutical development where teams review progress and decide whether to advance, modify, or stop a project. Each gate requires specific deliverables to be completed.

#### The 13 Stage Gates (0-12)
| Gate | Name | Purpose | Typical Deliverables |
|------|------|---------|---------------------|
| **0** | Entry in Early Development | Initiate development | ~17 deliverables |
| **1** | NME Selection | Select drug candidate | ~71 deliverables |
| **2** | Ph1/2 Manufacturing Readiness | Prepare for clinical trials | ~88 deliverables |
| **3** | FIH (First in Human) Readiness | Ready for human trials | ~65 deliverables |
| **4** | Entry into Full Development | Commit to Phase 3 | ~72 deliverables |
| **5** | Ph 3 Manufacturing Readiness | Scale-up for Phase 3 | ~195 deliverables |
| **6** | Process Lock & Validation | Finalize manufacturing | ~213 deliverables |
| **7** | Entry into Phase 3 | Start pivotal trials | ~231 deliverables |
| **8** | API & DP Validation Readiness | Validate processes | ~248 deliverables |
| **9** | Validation Review | Complete validation | ~237 deliverables |
| **10** | NDA/BLA Submission | Submit to FDA | ~174 deliverables |
| **11** | Approval & Launch | Commercial launch | ~162 deliverables |
| **12** | Post-Launch | Ongoing monitoring | ~147 deliverables |

#### Two Value Streams
- **CGT (Cell & Gene Therapy)**: Advanced therapies using cells or genes
- **Protein**: Traditional protein-based therapeutics

Each value stream has its own set of stage gates with specific requirements tailored to that modality.

### 📦 Understanding the TTL Files

#### Which Files are Required vs Generated?

**Source Files (Required)** - Must exist in repository:
1. **cmc_stagegate_base.ttl** (118 triples) - Core ontology definitions
2. **cmc_stagegate_gist_align.ttl** (71 triples) - GIST alignment mappings  
3. **cmc_stagegate_gist_examples.ttl** (184 triples) - Usage examples (optional but recommended)

**Generated Files** - Created automatically from your data:
1. **cmc_stagegate_instances.ttl** (7,294 triples) - Generated from Excel/CSV data
   - 26 stages (13 CGT + 13 Protein)
   - 2,205 deliverables as Quality Attributes
2. **cmc_stagegate_all.ttl** (7,483 triples) - Combined file containing all above

#### How to Regenerate the TTL Files

If you need to recreate the generated files from scratch:

```bash
# Option 1: Use the pipeline script
./run_pipeline.sh

# Option 2: Manual regeneration
# Step 1: Generate instances from CSV (creates cmc_stagegate_instances.ttl)
python3 scripts/etl/generate_cmc_ttl.py

# Step 2: Combine all TTL files (creates cmc_stagegate_all.ttl)
python3 scripts/etl/combine_ttls.py

# Step 3: Validate all files
python3 scripts/validation/verify_ttl_files.py
```

Expected output after regeneration:
- **cmc_stagegate_instances.ttl**: ~698 KB, 7,294 triples
- **cmc_stagegate_all.ttl**: ~711 KB, 7,483 triples
- All files validated with rapper (RDF syntax checker)

### 🔧 Troubleshooting

#### Common Issues and Solutions

| Issue | Solution |
|-------|----------|
| **Excel file not found** | Ensure your Excel file is in `data/current_input/` folder |
| **CSVs not generated** | Run `python3 scripts/etl/extract_xlsx.py` (auto-extracts to `data/current/`) |
| **Wrong file being processed** | Check `data/current_input/` has only one Excel file |
| **TTL validation fails** | Check that rapper is installed: `brew install raptor` (macOS) or `apt-get install raptor2-utils` (Linux) |
| **GraphDB connection fails** | Ensure GraphDB is running at http://localhost:7200 |
| **Missing Python dependencies** | Install required packages: `pip install pandas openpyxl requests` |
| **Permission denied** | Make scripts executable: `chmod +x run_pipeline.sh scripts/validation/*.sh` |

#### Verifying the Output
After running the pipeline, you should have:
- **5 CSV files** in `data/extracted/`
- **5 TTL files** in the root directory
- **15,466 total triples** across all TTL files
- **Multiple stage gates** across CGT and Protein streams
- **~2,200 deliverables** converted to Quality Attributes

#### Quick Validation
```bash
# Check if all files exist
ls -la *.ttl | wc -l  # Should show 5

# Validate TTL syntax
python3 scripts/validation/verify_ttl_files.py

# Count stages created
grep "a ex:Stage" cmc_stagegate_instances.ttl | wc -l  # Should be 78

# Count deliverables
grep "a ex:QualityAttribute" cmc_stagegate_instances.ttl | wc -l  # Should be ~2205
```

## GIST Alignment

### Overview
The project includes comprehensive alignment to [GIST v11+](https://ontologies.semanticarts.com/gist/), a minimalist upper ontology designed for enterprise data integration.

### Key Concept Mappings

| CMC Class | GIST Concept | Rationale |
|-----------|--------------|-----------|
| ex:Stage | gist:PlannedEvent | Planned phase in development |
| ex:StageGate | gist:Event + prov:Activity | Review event with provenance |
| ex:StagePlan | gist:TaskTemplate | Reusable plan template |
| ex:Process | gist:Task | Executable procedure |
| ex:UnitOperation | gist:PhysicalEvent | Concrete manufacturing step |
| ex:Lot | gist:Collection | Batch as collection |
| ex:Material | gist:PhysicalSubstance ∪ gist:PhysicalIdentifiableItem | Bulk or discrete |
| ex:Specification | gist:Specification | Quality specifications |
| ex:QualityAttribute | gist:Aspect | Measurable characteristic |
| ex:AnalyticalMethod | gist:TaskTemplate | Reusable method |
| ex:AnalyticalResult | gist:Magnitude | Numeric measurement |

### Property Mappings

| CMC Property | GIST Property | Usage |
|--------------|---------------|-------|
| ex:hasPlan | gist:hasPart | Compositional structure |
| ex:definesProcess | gist:hasSubTask | Task hierarchy |
| ex:consumesMaterial | gist:hasParticipant | Process participation |
| ex:producesMaterial | gist:produces | Output production |
| ex:hasSpecification | gist:hasPart | Design-time link |
| ex:hasEvidence | gist:isBasedOn | Evidence grounding |
| ex:evaluatedBy | gist:governs | Method governance |

### Advanced Features

#### Material Subclasses (Optional Stricter Typing)
```turtle
# Split materials into bulk vs discrete for better typing
ex:BulkMaterial rdfs:subClassOf ex:Material, gist:PhysicalSubstance .
ex:PackagedUnit rdfs:subClassOf ex:Material, gist:PhysicalIdentifiableItem .
```

#### Identifier Nodes (GIST ID Pattern)
```turtle
# Use ID nodes instead of datatype properties
ex:ID-GTIN-00312345678901 a gist:ID ;
    gist:identifies ex:DP-Pack-0001 .

ex:ID-LOT-000123 a gist:ID ;
    gist:identifies ex:DP-Lot-000123 .
```

### Usage Patterns

#### Pattern A: Analytical Results on Lots
```turtle
# Attach result to lot, link to CQA via aspect
ex:DP-Lot-000123 gist:hasMagnitude ex:Result-DP-000123-Dissolution .
ex:Result-DP-000123-Dissolution
  a ex:AnalyticalResult ;
  gist:isAspectOf ex:CQA-Dissolution-30min ;
  qudt:numericValue "82"^^xsd:decimal ;
  qudt:unit unit:PERCENT .
```

#### Pattern B: Specification Conformance
```turtle
# Spec based on evidence, lot conforms to spec
ex:Spec-Dissolution-30min gist:isBasedOn ex:Result-DP-000123-Dissolution .
ex:DP-Lot-000123 gist:conformsTo ex:Spec-Dissolution-30min .
```

#### Pattern C: Process Material Flow
```turtle
# Materials participate in and are produced by processes
ex:Process-001 gist:hasParticipant ex:Raw-Material-A .
ex:Process-001 gist:produces ex:Intermediate-Product-B .
```

### Migration to GIST v13
When upgrading to GIST v13:
1. Replace `gist:isAspectOf` with `gist:hasAspect` (direction reverses)
2. Update queries to use new direction
3. No other changes required

### Validation
Run validation to ensure alignment consistency:
```bash
python3 scripts/validation/validate_gist_alignment.py
# Output: Coverage report and any issues
```

## SPARQL Query Examples

### Basic Queries

#### Count CQAs per Stage
```sparql
PREFIX ex: <https://w3id.org/cmc-stagegate#>
SELECT ?stage ?stageLabel (COUNT(?cqa) AS ?cqaCount)
WHERE {
  ?stage a ex:Stage ; 
         rdfs:label ?stageLabel ; 
         ex:hasSpecification/ex:hasCQA ?cqa .
}
GROUP BY ?stage ?stageLabel
ORDER BY ?stageLabel
```

#### Find Orphan CQAs (No Owner)
```sparql
PREFIX ex:   <https://w3id.org/cmc-stagegate#>
PREFIX prov: <http://www.w3.org/ns/prov#>
SELECT ?stage ?cqa ?cqaLabel
WHERE {
  ?stage a ex:Stage ;
         ex:hasSpecification/ex:hasCQA ?cqa .
  ?cqa rdfs:label ?cqaLabel .
  FILTER NOT EXISTS { ?cqa prov:wasAttributedTo ?owner }
}
```

### GIST-Aligned Queries

#### Find All Measurements for a Lot
```sparql
PREFIX gist: <https://ontologies.semanticarts.com/gist/>
SELECT ?lot ?result ?cqa ?value ?unit
WHERE {
  ?lot a ex:Lot ;
       gist:hasMagnitude ?result .
  ?result gist:isAspectOf ?cqa ;
          qudt:numericValue ?value ;
          qudt:unit ?unit .
}
```

#### Trace Material Flow
```sparql
SELECT ?process ?input ?output
WHERE {
  ?process a ex:Process .
  OPTIONAL { ?process gist:hasParticipant ?input }
  OPTIONAL { ?process gist:produces ?output }
}
```

See `gist_example_queries.sparql` for more examples.

## GraphDB Integration

### ✅ Successfully Deployed

The CMC Stage-Gate ontology is now live in GraphDB:
- **Repository**: `cmc-stagegate`
- **Endpoint**: `http://localhost:7200/repositories/cmc-stagegate`
- **Triples Loaded**: 7,385
- **Named Graph**: `https://w3id.org/cmc-stagegate`

### Setup GraphDB Repository

1. **Create Repository**
   - Open GraphDB Workbench
   - Create new repository (type: GraphDB Free or use provided config)
   - Repository ID: `cmc-stagegate`

2. **Configure Environment**
```bash
export GRAPHDB_URL=http://localhost:7200
export GRAPHDB_REPOSITORY=cmc-stagegate
export GRAPHDB_CONTEXT=https://w3id.org/cmc-stagegate
```

3. **Upload Data**
```bash
# Dry run first
python3 scripts/deployment/export_to_graphdb.py --dry-run

# Actual upload
python3 scripts/deployment/export_to_graphdb.py --no-dry-run
# Result: Success (HTTP 204), 7,385 triples loaded
```

### Verified Queries

Test queries confirmed working:
```sparql
# Count stages
SELECT (COUNT(*) as ?count) WHERE { ?s a ex:Stage }
# Result: 26 stages

# GIST alignments
SELECT ?class ?gistClass WHERE { 
  ?class rdfs:subClassOf ?gistClass . 
  FILTER(STRSTARTS(STR(?gistClass), "http://ontologies.semanticarts.com/gist/"))
}
# Result: 12 class mappings verified
```

### Troubleshooting GraphDB

#### Check Repository Status
```bash
curl -s http://localhost:7200/repositories
```

#### Count Triples
```bash
curl -s http://localhost:7200/repositories/cmc-stagegate/size
# Result: 7385
```

#### Query via REST API
```bash
curl -X POST http://localhost:7200/repositories/cmc-stagegate \
  -H "Content-Type: application/sparql-query" \
  -d "SELECT (COUNT(*) as ?count) WHERE { ?s ?p ?o }"
```

## Design Philosophy

### Principles
1. **Reuse First**: Leverage established vocabularies (PROV-O, QUDT, GS1)
2. **Minimal Core**: Define only CMC-specific concepts
3. **Semantic Interoperability**: Full GIST alignment for enterprise integration
4. **Modular Architecture**: Separate concerns (base, instances, alignment)
5. **Readable IRIs**: Human-friendly identifiers from source data
6. **Progressive Enhancement**: Start simple, add complexity as needed

### Trade-offs
- **Simplicity vs Expressiveness**: Favored clarity over complex axioms
- **Performance vs Flexibility**: Chose flexible RDF over rigid schemas
- **Automation vs Control**: Automated generation with manual override points

## Technical Architecture

### Data Flow
```
Excel Workbook → CSV Extraction → Column Analysis → 
TTL Generation → Validation → Combination → GraphDB Upload
```

### Component Responsibilities
- **Extractors**: Handle messy Excel data
- **Generators**: Create clean RDF
- **Validators**: Ensure consistency
- **Combiners**: Manage modularity
- **Uploaders**: Deploy to graph stores

### Extension Points
- Custom vocabularies via @prefix declarations
- Additional mappings in generate_cmc_ttl.py
- New GIST alignments in separate adapter files
- Query templates in SPARQL files

## Business Applications

### Current Use Cases
- Stage-gate progress tracking
- CQA ownership analysis
- Deliverable dependency mapping
- Resource allocation planning

### Potential Applications
- Risk assessment dashboards
- Bottleneck identification
- Cross-functional coordination
- Regulatory compliance tracking
- Portfolio-level analytics

### Integration Opportunities
- ERP systems (SAP, Oracle)
- Project management (Jira, Smartsheet)
- Quality systems (LIMS, QMS)
- Regulatory platforms (Veeva, MasterControl)

## Roadmap & Next Steps

### Immediate Priorities
1. ✅ GIST alignment implementation
2. ⏳ Functional area/subteam modeling
3. ⏳ Status tracking integration
4. ⏳ Due date/timeline modeling

### Medium Term
- SHACL validation shapes
- GraphQL API layer
- Real-time data synchronization
- Advanced analytics queries
- Dashboard visualization

### Long Term
- ML-based risk prediction
- Automated compliance checking
- Cross-portfolio optimization
- Industry benchmark integration

### Community Contributions
Contributions welcome for:
- Additional vocabulary alignments
- Industry-specific extensions
- Query library expansion
- Visualization tools
- Documentation improvements

## Support & Contact

### Documentation
- GIST Ontology: https://ontologies.semanticarts.com/gist/
- PROV-O: https://www.w3.org/TR/prov-o/
- QUDT: http://qudt.org/
- GraphDB: https://graphdb.ontotext.com/documentation/

### Additional Project Documentation
- [Data Folder Structure](docs/DATA_FOLDER_STRUCTURE.md) - Input data organization guide
- [Output Folder Structure](docs/OUTPUT_FOLDER_STRUCTURE.md) - Generated TTL file organization
- [TTL Generation Report](docs/TTL_GENERATION_REPORT.md) - Detailed statistics and validation results
- [Conversion Guide](docs/CONVERSION_GUIDE.md) - Quick reference for Excel to RDF conversion
- [Cleanup Summary](docs/CLEANUP_SUMMARY.md) - Repository organization details
- [New File Adaptation Plan](docs/NEW_FILE_ADAPTATION_PLAN.md) - Guide for handling different file formats

### Issues & Questions
- Create GitHub issue for bugs/features
- Check existing documentation first
- Include error messages and context
- Provide minimal reproducible examples

## Complete GIST Alignment Summary

### ✅ All Required Alignments Implemented

The project now includes comprehensive GIST alignment with:

1. **Core Class Mappings** (11 classes, 100% coverage)
   - Lifecycle: Stage → PlannedEvent, StageGate → Event
   - Process: Process → Task, UnitOperation → PhysicalEvent  
   - Materials: Lot → Collection, Material → PhysicalSubstance ∪ PhysicalIdentifiableItem
   - Quality: QualityAttribute → Aspect, AnalyticalResult → Magnitude

2. **Property Alignments** (14 properties mapped)
   - Structure: hasPlan, hasGate → hasPart
   - Hierarchy: definesProcess, hasUnitOperation → hasSubTask
   - Flow: consumesMaterial → hasParticipant, producesMaterial → produces
   - Quality: hasEvidence → isBasedOn, evaluatedBy → governs

3. **Advanced Patterns**
   - **#stage_vs_gate**: Distinguishing planned phases from actual review events
   - **#materials_union_and_split**: Optional BulkMaterial and PackagedUnit subclasses
   - **#identifier_nodes**: GIST ID pattern for GTINs, lot numbers, NDCs
   - **#gist_v13_upgrade**: Ready for hasAspect migration

4. **QUDT Bridge**
   - qudt:numericValue ↔ gist:numericValue
   - qudt:unit → gist:hasUnitOfMeasure

### 📁 Key Files for GIST Integration

- **cmc_stagegate_gist_align.ttl**: Core alignment definitions
- **cmc_stagegate_gist_examples.ttl**: Complete working examples
- **gist_example_queries.sparql**: 12+ SPARQL query patterns
- **validate_gist_alignment.py**: Consistency checker

### 🎯 Validation Results

#### TTL File Validation (verify_ttl_files.py)
```
✅ All 5 TTL files valid
📊 Total: 15,466 triples
   - cmc_stagegate_all.ttl: 7,641 triples
   - cmc_stagegate_instances.ttl: 7,452 triples  
   - cmc_stagegate_gist_examples.ttl: 184 triples
   - cmc_stagegate_base.ttl: 118 triples
   - cmc_stagegate_gist_align.ttl: 71 triples
```

#### GIST Alignment Coverage
```
✓ Classes: 12/12 mapped (100%)
✓ Properties: 11 mapped
✓ GIST concepts: 26 referenced
✓ Instance data: 2,113 CQAs, 26 Stages, 26 Specifications
```

#### GraphDB Deployment
```
✅ Repository: cmc-stagegate
✅ Triples loaded: 7,385 (in named graph)
✅ Context: https://w3id.org/cmc-stagegate
✅ SPARQL endpoint: http://localhost:7200/repositories/cmc-stagegate
```

#### SPARQL Query Validation
```
✅ 12 class alignments verified
✅ 11 property alignments verified
✅ QUDT-GIST bridge functional
✅ All instance data queryable through GIST patterns
```

## License

Internal use only. Add appropriate license before external distribution.

---

*Last Updated: September 18, 2024*  
*Version: 1.1.0-gist*  
*Status: ✅ Production Ready*  
*GIST Version: v11+ (v13-ready)*  
*Validation: All files validated, 15,466 triples, GraphDB deployed*