# TTL File Reorganization Summary

## ✅ What We're Doing

Moving all TTL files from scattered locations into one organized directory:
`data/required_ttl_files/`

## 📁 Files Being Moved

### From Root Directory (6 files):
1. `cmc_stagegate_base.ttl` - Core ontology
2. `cmc_stagegate_drug_products.ttl` - Drug/IDMP
3. `cmc_stagegate_modalities.ttl` - Modality types
4. `cmc_stagegate_temporal.ttl` - Time tracking
5. `cmc_stagegate_gist_align.ttl` - GIST alignment
6. `cmc_stagegate_gist_examples.ttl` - Examples

### From data/ Directory (3 files):
7. `example_drug_instances.ttl` - Mock drugs
8. `example_temporal_tracking.ttl` - Timeline examples
9. `example_triples.txt` - Additional examples

## 🚀 How to Execute

### Step 1: Update Script Paths First
```bash
chmod +x update_script_paths.sh
./update_script_paths.sh
```
This updates:
- `scripts/etl/combine_ttls.py` - New TTL paths
- `verify_critical_files.sh` - New verification paths

### Step 2: Move the Files
```bash
chmod +x reorganize_ttl_files.sh
./reorganize_ttl_files.sh
```
This moves all 9 files to `data/required_ttl_files/`

### Step 3: Test Everything Works
```bash
# Test the pipeline still works
./run_pipeline.sh -e

# Verify critical files
./verify_critical_files.sh
```

## 📊 Benefits

### Before:
```
staged/
├── cmc_stagegate_base.ttl          # Scattered
├── cmc_stagegate_drug_products.ttl # in
├── cmc_stagegate_modalities.ttl    # root
├── cmc_stagegate_temporal.ttl      # directory
├── cmc_stagegate_gist_align.ttl    #
├── cmc_stagegate_gist_examples.ttl #
├── data/
│   ├── example_drug_instances.ttl  # Mixed
│   ├── example_temporal_tracking.ttl # with
│   └── example_triples.txt         # data
```

### After:
```
staged/
├── data/
│   └── required_ttl_files/         # All in one place!
│       ├── cmc_stagegate_base.ttl
│       ├── cmc_stagegate_drug_products.ttl
│       ├── cmc_stagegate_modalities.ttl
│       ├── cmc_stagegate_temporal.ttl
│       ├── cmc_stagegate_gist_align.ttl
│       ├── cmc_stagegate_gist_examples.ttl
│       ├── example_drug_instances.ttl
│       ├── example_temporal_tracking.ttl
│       └── example_triples.txt
```

## ✅ What Gets Updated

| File | Changes |
|------|---------|
| `scripts/etl/combine_ttls.py` | Paths updated to `data/required_ttl_files/` |
| `verify_critical_files.sh` | Checks new locations |
| `README.md` | Documents new structure |
| Root directory | Cleaner (6 fewer files) |
| `data/required_ttl_files/` | New organized location |

## ⚠️ Important Notes

1. **Run update_script_paths.sh FIRST** - This ensures scripts know where to find files
2. **Test after moving** - Always run pipeline test to ensure it works
3. **Commit when verified** - Only commit after confirming everything works
4. **No functionality lost** - Just better organization

## 🎯 Result

- **Cleaner root directory** - No more scattered TTL files
- **Logical grouping** - All required ontology files together
- **Easier maintenance** - Know exactly where TTL files live
- **Better documentation** - Clear separation of core vs generated files
