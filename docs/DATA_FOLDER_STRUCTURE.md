# Data Folder Structure

**Updated**: October 31, 2025

## 📁 New Folder Organization

The `data/` directory now uses a clear naming convention that separates current working files from historical versions:

```
data/
├── current_input/           # Current input Excel file(s)
│   └── *.xlsx              # The active Excel file being processed
│
├── current/                 # Current extracted CSV files
│   ├── *__SGD.csv          # Main stage-gate data
│   ├── *__Drop_Downs.csv   # Controlled vocabularies
│   ├── *__Lexicon.csv      # Term definitions
│   ├── *__SME.csv          # Subject matter experts
│   └── [other sheets].csv  # Any other sheets from Excel
│
├── previous_input_YYMMDD/  # Archived input files (timestamped)
│   └── *.xlsx              # Previous version of Excel file
│
└── extracted_YYMMDD/        # Archived extractions (timestamped)
    └── *.csv               # Previous extracted CSV files
```

## 🔄 Workflow with New Structure

### Current Files (Active Development)
- **Input**: Place your Excel file in `data/current_input/`
- **Extract**: CSVs are generated in `data/current/`
- **Process**: Scripts read from `data/current/`
- **Generate**: TTL files created in root directory

### Archiving Process
When updating to a new input file:
1. Move old input: `current_input/` → `previous_input_YYMMDD/`
2. Move old CSVs: `current/` → `extracted_YYMMDD/`
3. Place new Excel in `current_input/`
4. Extract to `current/`

## 📝 Script Updates

All ETL scripts have been updated to use this structure:

| Script | Reads From | Writes To |
|--------|------------|-----------|
| `extract_xlsx.py` | `data/current_input/` | `data/current/` |
| `generate_cmc_ttl.py` | `data/current/*SGD*.csv` | `cmc_stagegate_instances.ttl` |
| `analyze_columns.py` | `data/current/*SGD*.csv` | (console output) |
| `combine_ttls.py` | `*.ttl` files | `cmc_stagegate_all.ttl` |

## 🎯 Benefits

1. **Clear Separation**: Current vs historical data
2. **Date Tracking**: Timestamped archives
3. **Matched Pairs**: Input files match their extractions
4. **Easy Rollback**: Previous versions preserved
5. **Clean Working Directory**: Only current files active

## 📋 Example Timeline

```
October 31, 2025:
- previous_input_250910/     # September 2025 input
- extracted_250910/          # September 2025 CSVs
- current_input/             # October 2025 input (with MOD NB)
- current/                   # October 2025 CSVs

Future (e.g., December 2025):
- previous_input_250910/     # September version
- extracted_250910/          
- previous_input_251031/     # October version
- extracted_251031/
- current_input/             # December version
- current/                   # December CSVs
```

## 🔧 Usage Examples

### Extract Current Input
```bash
python3 scripts/etl/extract_xlsx.py
# Automatically uses: current_input/ → current/
```

### Extract with Explicit Paths
```bash
python3 scripts/etl/extract_xlsx.py \
  --input-dir ./data/current_input \
  --output-dir ./data/current
```

### Run Full Pipeline
```bash
./run_pipeline.sh
# Uses the new folder structure automatically
```

### Analyze Current Data
```bash
python3 scripts/etl/analyze_columns.py
# Automatically looks in data/current/
```

## 🔍 Finding Files

The scripts are smart about finding files:

1. **Input Excel**: Looks for any `*.xlsx` in `current_input/`
2. **SGD CSV**: Looks for `*SGD*.csv` in `current/`
3. **Fallback**: Uses first matching file if multiple exist

## ⚠️ Migration Notes

If you have existing data:
1. Old `data/extracted/` → `data/extracted_250910/` ✅
2. Old Excel files → `data/previous_input_250910/` ✅
3. New Excel → `data/current_input/` ✅
4. New extraction → `data/current/` (ready to populate)

---

*This structure supports multiple input file formats and makes version management clear and systematic.*
