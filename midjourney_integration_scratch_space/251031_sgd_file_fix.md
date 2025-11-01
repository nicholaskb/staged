# SGD File Selection Fix
**Date:** October 31, 2025, 16:20 PST  
**Objective:** Fix incorrect CSV file selection in generate_cmc_ttl.py  
**Status:** Fixed

## Issue Identified
Script was selecting wrong CSV file:
- **Selected:** `*__SME.csv` (2.4KB - only headers)
- **Should select:** `*__SGD.csv` (697KB - actual data)

## Root Cause
The glob pattern `*SGD*` matched ALL 5 extracted CSV files because they all contain "SGD" in the filename from "SGD Template":
- Drop_Downs.csv
- Lexicon.csv  
- Ped_CMC_Strat_Review_Protein.csv
- SGD.csv ✅ (correct one)
- SME.csv ❌ (was being selected)

## Fix Applied
Changed line 37-38 in `scripts/etl/generate_cmc_ttl.py`:
```python
# Before: 
SGD_FILES = list(EXTRACTED_DIR.glob("*SGD*.csv"))

# After:
SGD_FILES = list(EXTRACTED_DIR.glob("*__SGD.csv"))
```

## Verification
New pattern only matches the correct file:
- ✅ Matches: `Protein_and_CGT_SGD_Template_Final_ENDORSED_JAN_2023_MOD_NB__SGD.csv`
- ❌ Excludes: All other CSV files

## Endpoints Affected
- `generate_cmc_ttl.py` - Now correctly selects SGD data file

## Implemented vs Proposed
**Implemented:** Fixed file selection pattern
**Next:** Re-run script to generate TTL with actual data
