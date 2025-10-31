# Adaptation Plan for New Input File Structure

**Date**: October 31, 2025  
**Purpose**: Modify existing pipeline to handle new input file with:
- Additional modality (beyond CGT and Protein)
- Different column sequencing

## 📊 Current System Analysis

### Current Input Expectations
- **File**: `Protein and CGT_SGD Template Final_ENDORSED JAN 2023.xlsx`
- **Modalities**: CGT, Protein (2 value streams)
- **Column Order** (Row 2 as headers):
  1. Value Stream
  2. Stage Gate
  3. Stage Gate Description
  4. Functional Area/Subteam
  5. Category
  6. Deliverable
  7. Explanation/Translation
  8. Owner
  9. Status
  10. To be presented at
  11. VPAD-specific?

### Hardcoded Dependencies Found
- File paths with specific names
- Column name mappings
- Row 2 as header assumption
- Value stream limited to CGT/Protein

## 🔧 Scripts Requiring Modification

### 1. **CRITICAL - Data Processing Scripts**

#### `scripts/etl/generate_cmc_ttl.py` (HIGH PRIORITY)
**Current Issues**:
- Hardcoded file path: `Protein and CGT_SGD Template Final_ENDORSED JAN 2023.xlsx`
- Hardcoded column mappings in `OFFICIAL_COLS` dictionary
- Assumes specific column names and their variations
- Row 2 hardcoded as header row

**Changes Needed**:
```python
# Make configurable:
- Input file path (via command line argument)
- Column mappings (via configuration file)
- Header row position (configurable)
- Support for new modality values
```

#### `scripts/etl/analyze_columns.py` (MEDIUM PRIORITY)
**Current Issues**:
- Hardcoded SGD_PATH to specific filename
- Fixed MAPPING_GUIDE dictionary
- Comments mention only CGT/Protein/SM/Vaccines

**Changes Needed**:
```python
# Make configurable:
- Input file path
- Dynamic column mapping discovery
- Support for any modality value
```

#### `scripts/etl/extract_xlsx.py` (LOW PRIORITY)
**Current Issues**:
- None - already generic and flexible!
- Can handle any Excel file structure

**Changes Needed**:
- No changes required ✅

#### `scripts/etl/combine_ttls.py` (NO CHANGES)
**Current Issues**:
- None - works with any TTL files

**Changes Needed**:
- No changes required ✅

### 2. **Validation Scripts**

#### `scripts/validation/verify_ttl_files.py` (LOW PRIORITY)
**Current Issues**:
- Hardcoded path: `/Users/nicholasbaro/Python/staged`
- Expects specific file names for GIST alignment checks

**Changes Needed**:
- Make base path configurable
- Keep GIST alignment checks generic

#### `scripts/validation/validate_gist_alignment.py` (NO CHANGES)
**Current Issues**:
- None - works with generated TTL structure

**Changes Needed**:
- No changes required ✅

#### `scripts/validation/test_gist_alignment.sh` (NO CHANGES)
**Current Issues**:
- None - SPARQL queries are generic

**Changes Needed**:
- No changes required ✅

### 3. **Analysis Scripts**

#### `scripts/analysis/stage_gate_flow.py` (LOW PRIORITY)
**Current Issues**:
- May have assumptions about specific stage gates
- Visualization might assume CGT/Protein only

**Changes Needed**:
- Make modality list dynamic
- Adjust visualizations for new modality

#### Other analysis scripts (NO CHANGES)
- `comprehensive_stage_gate_ontology.py`
- `stage_gate_recommendation.py`
- `visualize_stage_gate.py`

These work with generated data and should adapt automatically.

### 4. **Pipeline Script**

#### `run_pipeline.sh` (MEDIUM PRIORITY)
**Current Issues**:
- Comments reference specific Excel filename
- No parameter for input file selection

**Changes Needed**:
- Add parameter for input file path
- Update help text and examples

## 📝 Proposed Solution: Configuration-Based Approach

### Step 1: Create Configuration File
Create `config/column_mappings.json`:
```json
{
  "input_file": "path/to/new_excel.xlsx",
  "header_row": 2,
  "column_mappings": {
    "value_stream": ["Value Stream", "Modality", "Product Type"],
    "stage_gate": ["Stage Gate", "Gate Number", "Stage"],
    "description": ["Stage Gate Description", "Description", "Gate Description"],
    "functional_area": ["Functional Area/Subteam", "Team", "Function"],
    "deliverable": ["Deliverable", "Requirement", "Task"],
    "owner": ["Owner", "Responsible", "Assignee"],
    "status": ["Status", "State"],
    "category": ["Category", "Type"],
    "presented_at": ["To be presented at", "Presentation"],
    "vpad_specific": ["VPAD-specific?", "VPAD"]
  },
  "valid_modalities": ["CGT", "Protein", "SmallMolecule", "Vaccine", "Device"],
  "output_paths": {
    "instances_ttl": "cmc_stagegate_instances.ttl",
    "combined_ttl": "cmc_stagegate_all.ttl"
  }
}
```

### Step 2: Modify Key Scripts

#### Modified `generate_cmc_ttl.py` Structure:
```python
import json
from pathlib import Path
import argparse

def load_config(config_path):
    """Load column mappings from configuration file"""
    with open(config_path) as f:
        return json.load(f)

def get_column_value(row, column_key, config):
    """Get value from row using configured column mappings"""
    possible_names = config['column_mappings'].get(column_key, [])
    for name in possible_names:
        if name in row:
            return row[name]
    return ""

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--config', default='config/column_mappings.json')
    parser.add_argument('--input', help='Override input file from config')
    args = parser.parse_args()
    
    config = load_config(args.config)
    input_file = args.input or config['input_file']
    
    # Process with flexible column mappings
    value_stream = get_column_value(row, 'value_stream', config)
    # ... etc
```

### Step 3: Update Pipeline Script
Add configuration support to `run_pipeline.sh`:
```bash
# Add new parameter
-c, --config         Configuration file for column mappings
-i, --input-file     Input Excel file (overrides config)

# Usage example
./run_pipeline.sh --config config/new_file_mappings.json
```

## 🚀 Implementation Plan

### Phase 1: Preparation (Day 1)
1. Back up current working version
2. Create configuration file structure
3. Document current column mappings

### Phase 2: Core Modifications (Day 2-3)
1. **Modify `generate_cmc_ttl.py`**:
   - Add configuration loading
   - Replace hardcoded paths
   - Make column access flexible
   - Test with current file

2. **Update `analyze_columns.py`**:
   - Add configuration support
   - Make path configurable
   - Test column analysis

3. **Update `run_pipeline.sh`**:
   - Add configuration parameters
   - Update documentation

### Phase 3: Testing (Day 4)
1. Test with current Excel file (regression test)
2. Create test file with new structure
3. Test with new modality
4. Validate TTL generation

### Phase 4: Documentation (Day 5)
1. Update README with configuration instructions
2. Create migration guide
3. Document new modality support

## 🎯 Benefits of This Approach

1. **Backward Compatible**: Works with existing files
2. **Flexible**: Handles column reordering
3. **Extensible**: Easy to add new modalities
4. **Maintainable**: Configuration separate from code
5. **Reusable**: Same code for different file structures

## ⚠️ Risk Mitigation

1. **Testing Strategy**:
   - Keep original files for regression testing
   - Create unit tests for column mapping
   - Validate output TTL structure

2. **Rollback Plan**:
   - Git branch for changes
   - Keep original scripts as `.backup`
   - Document all changes

3. **Validation Checks**:
   - Verify triple counts remain consistent
   - Check GIST alignment still works
   - Validate SPARQL queries still function

## 📋 Implementation Checklist

- [ ] Create configuration file structure
- [ ] Modify `generate_cmc_ttl.py` for flexibility
- [ ] Update `analyze_columns.py` 
- [ ] Enhance `run_pipeline.sh`
- [ ] Test with original file
- [ ] Test with new file structure
- [ ] Test with new modality
- [ ] Update documentation
- [ ] Create migration guide
- [ ] Commit to new branch

## 💡 Alternative Approaches

### Option A: Multiple Generator Scripts
- Keep original for old format
- Create new generator for new format
- Select via pipeline parameter

### Option B: Auto-Detection
- Detect file structure automatically
- Map columns by content analysis
- More complex but user-friendly

### Option C: Excel Template Converter
- Convert new format to old format
- Use existing scripts unchanged
- Simple but less flexible

## 📝 Next Steps

1. **Review this plan** with stakeholders
2. **Choose approach** (recommended: Configuration-based)
3. **Create test file** with new structure
4. **Begin implementation** in feature branch
5. **Test thoroughly** before merging

---

**Recommendation**: The configuration-based approach provides the best balance of flexibility, maintainability, and backward compatibility. It allows the system to handle any future file structure changes with minimal code modifications.
