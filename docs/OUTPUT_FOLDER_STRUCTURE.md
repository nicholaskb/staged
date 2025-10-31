# Output Folder Structure

**Updated**: October 31, 2025

## 📁 Output Directory Organization

The `output/` directory uses a clear structure that separates current generated files from timestamped historical versions:

```
output/
├── current/                    # 📤 Latest generated TTL files
│   ├── cmc_stagegate_instances.ttl    # Generated from current CSV data
│   └── cmc_stagegate_all.ttl          # Combined ontology (all TTLs merged)
│
└── ttl_YYMMDD_[description]/   # 📦 Archived versions (timestamped)
    ├── cmc_stagegate_instances.ttl    # Previous instances
    └── cmc_stagegate_all.ttl          # Previous combined file
```

## 🔍 File Locations

### Source Files (Remain in Root)
These manually-created ontology files stay in the project root:
- `cmc_stagegate_base.ttl` - Core ontology definitions
- `cmc_stagegate_gist_align.ttl` - GIST alignment mappings
- `cmc_stagegate_gist_examples.ttl` - Usage examples

### Generated Files (In output/)
These automatically-generated files go to `output/current/`:
- `cmc_stagegate_instances.ttl` - Created from CSV data
- `cmc_stagegate_all.ttl` - Combined file (base + instances + alignments)

## 🔄 Complete Data Flow

```
INPUT                     EXTRACTION              GENERATION              OUTPUT
─────                     ──────────              ──────────              ──────

data/current_input/       data/current/           scripts/etl/            output/current/
└── *.xlsx          →     ├── *__SGD.csv     →    generate_cmc_ttl.py →   ├── instances.ttl
                          ├── *__SME.csv                                   └── all.ttl
                          └── [others].csv          combine_ttls.py ↗
```

## 📋 Workflow for Updates

### When Processing New Data:

1. **Place Input**: Put Excel in `data/current_input/`
2. **Extract**: CSVs generated in `data/current/`
3. **Generate**: TTLs created in `output/current/`
4. **Archive** (when needed): Move old outputs to timestamped folder

### Archiving Previous Output:
```bash
# Before generating new output, archive the current
DATE=$(date +%y%m%d)
mkdir -p output/ttl_${DATE}_previous
cp output/current/*.ttl output/ttl_${DATE}_previous/

# Or with description
mkdir -p output/ttl_${DATE}_beforeModNB
cp output/current/*.ttl output/ttl_${DATE}_beforeModNB/
```

## 📊 Current Structure Example

As of October 31, 2025:
```
output/
├── current/                         # Latest (from MOD NB file)
│   ├── cmc_stagegate_instances.ttl  # ~715 KB
│   └── cmc_stagegate_all.ttl        # ~728 KB
│
└── ttl_241031_original/             # Previous version
    ├── cmc_stagegate_instances.ttl  # Original instances
    └── cmc_stagegate_all.ttl        # Original combined
```

## 🎯 Benefits

1. **Clear Separation**: Current vs historical outputs
2. **Version Tracking**: Timestamped archives of all generations
3. **Clean Root**: Source files separate from generated files
4. **Easy Comparison**: Can diff current vs previous versions
5. **Rollback Capability**: Previous versions preserved

## 🔧 Script Configuration

### Scripts That Write to output/current/:
- `generate_cmc_ttl.py` → Creates `output/current/cmc_stagegate_instances.ttl`
- `combine_ttls.py` → Creates `output/current/cmc_stagegate_all.ttl`

### Scripts That Read From Multiple Locations:
- `verify_ttl_files.py` → Validates files in both root and `output/current/`
- `export_to_graphdb.py` → Uploads `output/current/cmc_stagegate_all.ttl`

## 📝 Usage Examples

### Generate New Output
```bash
# Generates to output/current/
python3 scripts/etl/generate_cmc_ttl.py
python3 scripts/etl/combine_ttls.py
```

### Validate All Files
```bash
# Validates both source (root) and generated (output/current/)
python3 scripts/validation/verify_ttl_files.py
```

### Deploy to GraphDB
```bash
# Deploys from output/current/
python3 scripts/deployment/export_to_graphdb.py \
  --files output/current/cmc_stagegate_all.ttl \
  --no-dry-run
```

### Compare Versions
```bash
# Compare current vs archived
diff output/current/cmc_stagegate_instances.ttl \
     output/ttl_241031_original/cmc_stagegate_instances.ttl
```

## 🔍 Finding Files

| File Type | Location | Created By |
|-----------|----------|------------|
| Source TTLs | Project root | Manual (version controlled) |
| Generated instances | `output/current/` | `generate_cmc_ttl.py` |
| Combined TTL | `output/current/` | `combine_ttls.py` |
| Archived versions | `output/ttl_YYMMDD_*/` | Manual archiving |

## ⚠️ Important Notes

1. **Don't Edit Generated Files**: Files in `output/` are regenerated from data
2. **Archive Before Regenerating**: Save current output before processing new data
3. **Source Files Stay in Root**: Never move base, gist_align, or gist_examples TTLs
4. **Version Control**: Consider `.gitignore` for `output/` if files are large

---

*This structure keeps generated output organized and separate from source ontology files.*
