#!/bin/bash

# Test TTL Reorganization Script
# Verifies all files are in the new location and scripts are updated

set -e

# Colors
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
NC='\033[0m'

echo -e "${GREEN}🧪 Testing TTL Reorganization${NC}"
echo "==============================="
echo ""

ERRORS=0

# Test 1: Check all files exist in new location
echo -e "${YELLOW}Test 1: Checking files in new location${NC}"
FILES=(
    "data/required_ttl_files/cmc_stagegate_base.ttl"
    "data/required_ttl_files/cmc_stagegate_drug_products.ttl"
    "data/required_ttl_files/cmc_stagegate_modalities.ttl"
    "data/required_ttl_files/cmc_stagegate_temporal.ttl"
    "data/required_ttl_files/cmc_stagegate_gist_align.ttl"
    "data/required_ttl_files/cmc_stagegate_gist_examples.ttl"
    "data/required_ttl_files/example_drug_instances.ttl"
    "data/required_ttl_files/example_temporal_tracking.ttl"
)

for file in "${FILES[@]}"; do
    if [ -f "$file" ]; then
        echo -e "  ${GREEN}✅${NC} $file"
    else
        echo -e "  ${RED}❌${NC} Missing: $file"
        ERRORS=$((ERRORS + 1))
    fi
done

# Test 2: Check no TTL files remain in root
echo ""
echo -e "${YELLOW}Test 2: Checking root directory is clean${NC}"
ROOT_TTL_COUNT=$(ls -1 *.ttl 2>/dev/null | wc -l)
if [ $ROOT_TTL_COUNT -eq 0 ]; then
    echo -e "  ${GREEN}✅${NC} No TTL files in root (clean!)"
else
    echo -e "  ${RED}❌${NC} Found $ROOT_TTL_COUNT TTL files still in root"
    ERRORS=$((ERRORS + 1))
fi

# Test 3: Test combine_ttls.py can find files
echo ""
echo -e "${YELLOW}Test 3: Testing combine_ttls.py${NC}"
if python3 -c "
import sys
from pathlib import Path
sys.path.insert(0, 'scripts/etl')
from combine_ttls import DEFAULT_FILES
missing = [f for f in DEFAULT_FILES if not Path(f).exists()]
if missing:
    print(f'Missing files: {missing}')
    sys.exit(1)
else:
    print('All files found')
" 2>/dev/null; then
    echo -e "  ${GREEN}✅${NC} combine_ttls.py can find all files"
else
    echo -e "  ${RED}❌${NC} combine_ttls.py has missing files"
    ERRORS=$((ERRORS + 1))
fi

# Test 4: Run the actual pipeline (skip extraction)
echo ""
echo -e "${YELLOW}Test 4: Running pipeline test${NC}"
echo "Running: ./run_pipeline.sh -e"
if ./run_pipeline.sh -e > /tmp/pipeline_test.log 2>&1; then
    echo -e "  ${GREEN}✅${NC} Pipeline completed successfully"
    
    # Check output was created
    if [ -f "output/current/cmc_stagegate_all.ttl" ]; then
        TRIPLE_COUNT=$(grep -c "^[^#@]" output/current/cmc_stagegate_all.ttl 2>/dev/null || echo "0")
        echo -e "  ${GREEN}✅${NC} Generated cmc_stagegate_all.ttl ($TRIPLE_COUNT lines)"
    else
        echo -e "  ${RED}❌${NC} Output file not created"
        ERRORS=$((ERRORS + 1))
    fi
else
    echo -e "  ${RED}❌${NC} Pipeline failed (check /tmp/pipeline_test.log)"
    ERRORS=$((ERRORS + 1))
fi

# Summary
echo ""
echo "==============================="
if [ $ERRORS -eq 0 ]; then
    echo -e "${GREEN}✅ All tests passed!${NC}"
    echo ""
    echo "TTL reorganization successful:"
    echo "• All files moved to data/required_ttl_files/"
    echo "• Scripts updated with new paths"
    echo "• Pipeline works correctly"
else
    echo -e "${RED}❌ $ERRORS tests failed${NC}"
    echo ""
    echo "Please fix the issues above."
fi

exit $ERRORS
