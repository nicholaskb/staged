# 🧹 Safe Repository Cleanup Plan

## ⚠️ IMPORTANT: Review Before Executing!

This cleanup plan identifies safe-to-remove files while preserving ALL critical functionality.

---

## 🛡️ WILL PRESERVE (Critical Files)

### Core Ontology Files ✅
- ✅ All 6 root `.ttl` files 
- ✅ `cmc_stagegate_base.ttl`
- ✅ `cmc_stagegate_drug_products.ttl`
- ✅ `cmc_stagegate_modalities.ttl`
- ✅ `cmc_stagegate_temporal.ttl`
- ✅ `cmc_stagegate_gist_align.ttl`
- ✅ `cmc_stagegate_gist_examples.ttl`

### Current Data ✅
- ✅ `data/current/` - Latest CSV extractions
- ✅ `data/current_input/` - Current Excel input
- ✅ `output/current/` - All current TTL outputs
- ✅ `output/current/gupri_mappings.json` - **CRITICAL ID mappings**

### All Scripts ✅
- ✅ All 19 Python scripts in `scripts/`
- ✅ `run_pipeline.sh`
- ✅ `run_without_extraction.sh`

### All Documentation ✅
- ✅ `README.md`
- ✅ All 27 files in `docs/`
- ✅ All `.gitignore` and Git files

### All Queries ✅
- ✅ All SPARQL files in `queries/`

---

## 🗑️ SAFE TO CLEAN (With Your Approval)

### 1. **Old Archived Data** (Can Remove After Confirming Backups)
```bash
# These are from previous iterations - already archived
data/extracted_250910/        # Old extracted CSVs from Sept
data/previous_input_250910/   # Old input from Sept
output/ttl_241031_original/   # Old output from yesterday
```
**Space Saved**: ~3-4 MB

### 2. **Python Cache** (Always Safe to Remove)
```bash
# Auto-generated Python bytecode
__pycache__/
```
**Space Saved**: Minimal

### 3. **Virtual Environment** (Recreatable)
```bash
.venv/                        # Python packages (can reinstall)
```
**Space Saved**: ~140 MB (but you'd need to reinstall packages)

### 4. **Temporary Files** (If Any Found)
```bash
*.tmp
*.bak
*~
.DS_Store                     # Mac system files
```
**Space Saved**: Minimal

---

## 📋 Recommended Cleanup Script

### Step 1: Create Full Backup First! 
```bash
# CRITICAL: Backup everything first!
cd /Users/nicholasbaro/Python
tar -czf staged_backup_$(date +%Y%m%d_%H%M%S).tar.gz staged/
```

### Step 2: Safe Cleanup (Preserves All Functionality)
```bash
#!/bin/bash
# save as: cleanup_safe.sh

echo "🧹 Safe Repository Cleanup"
echo "========================="
echo ""

# Confirm with user
read -p "Have you created a backup? (y/n) " -n 1 -r
echo ""
if [[ ! $REPLY =~ ^[Yy]$ ]]; then
    echo "❌ Please create backup first: tar -czf staged_backup.tar.gz staged/"
    exit 1
fi

echo "Cleaning Python cache..."
find . -type d -name "__pycache__" -exec rm -rf {} + 2>/dev/null

echo "Removing Mac system files..."
find . -name ".DS_Store" -delete 2>/dev/null

# Optional: Remove old archives (uncomment if sure)
# echo "Remove old data archives? (data/extracted_250910, data/previous_input_250910)"
# read -p "Continue? (y/n) " -n 1 -r
# echo ""
# if [[ $REPLY =~ ^[Yy]$ ]]; then
#     rm -rf data/extracted_250910/
#     rm -rf data/previous_input_250910/
#     rm -rf output/ttl_241031_original/
#     echo "✅ Old archives removed"
# fi

echo ""
echo "✅ Safe cleanup complete!"
echo ""
echo "Preserved:"
echo "  ✅ All ontology files (.ttl)"
echo "  ✅ All scripts"
echo "  ✅ All documentation"  
echo "  ✅ Current data & outputs"
echo "  ✅ GUPRI mappings"
```

---

## 🚫 NEVER DELETE These Files

**CRITICAL - Data Loss if Deleted:**
1. `output/current/gupri_mappings.json` - Loses ID persistence!
2. `data/current/` - Current working data
3. `output/current/*.ttl` - Current outputs

**CRITICAL - Functionality Loss:**
1. Any `.ttl` file in root directory
2. Any `.py` file in `scripts/`
3. `run_pipeline.sh`
4. `README.md`

---

## 💡 Space-Saving Recommendations

### If You Need More Space:
1. **Archive old data folders** to external storage (3-4 MB)
2. **Compress** `.venv` if not actively developing (saves 140 MB)
3. **Use Git** to track changes instead of keeping old folders

### Best Practice Going Forward:
```bash
# After each successful pipeline run:
1. Verify new output is correct
2. Archive previous data: tar -czf archive_$(date +%Y%m%d).tar.gz data/previous_* output/ttl_*
3. Move archives to external storage
4. Delete local archives
```

---

## ✅ Cleanup Checklist

- [ ] Created full backup
- [ ] Reviewed what will be deleted
- [ ] Confirmed current pipeline works
- [ ] Verified GUPRI mappings are safe
- [ ] Ran cleanup script
- [ ] Tested pipeline still works

---

**RECOMMENDATION**: Start with the safest cleanup (Python cache, .DS_Store) and only remove old archives after confirming you have backups elsewhere.

**Your data is safe as long as you follow this plan!** 🛡️
