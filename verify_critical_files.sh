#!/bin/bash

# Verify Critical Files Script
# Ensures all critical files are present and repository is functional

set -e

# Colors
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m'

echo -e "${GREEN}🔍 Verifying Critical Files${NC}"
echo "============================"
echo ""

MISSING=0
WARNINGS=0

# Function to check file exists
check_file() {
    if [ -f "$1" ]; then
        echo -e "  ${GREEN}✅${NC} $1"
        return 0
    else
        echo -e "  ${RED}❌ MISSING:${NC} $1"
        MISSING=$((MISSING + 1))
        return 1
    fi
}

# Function to check directory exists
check_dir() {
    if [ -d "$1" ]; then
        COUNT=$(ls -1 "$1" 2>/dev/null | wc -l)
        echo -e "  ${GREEN}✅${NC} $1 ($COUNT items)"
        return 0
    else
        echo -e "  ${RED}❌ MISSING:${NC} $1"
        MISSING=$((MISSING + 1))
        return 1
    fi
}

# 1. Critical Ontology Files
echo -e "${YELLOW}1. Core Ontology Files:${NC}"
check_file "data/required_ttl_files/cmc_stagegate_base.ttl"
check_file "data/required_ttl_files/cmc_stagegate_drug_products.ttl"
check_file "data/required_ttl_files/cmc_stagegate_modalities.ttl"
check_file "data/required_ttl_files/cmc_stagegate_temporal.ttl"
check_file "data/required_ttl_files/cmc_stagegate_gist_align.ttl"
check_file "data/required_ttl_files/cmc_stagegate_gist_examples.ttl"
echo ""

# 2. Critical Scripts
echo -e "${YELLOW}2. Essential Scripts:${NC}"
check_file "run_pipeline.sh"
check_file "scripts/etl/generate_cmc_ttl_gupri.py"
check_file "scripts/etl/generate_sme_ttl.py"
check_file "scripts/etl/combine_ttls.py"
check_file "scripts/etl/extract_xlsx.py"
check_file "scripts/validation/verify_ttl_files.py"
echo ""

# 3. Critical Data/Output
echo -e "${YELLOW}3. Data Directories:${NC}"
check_dir "data/current"
check_dir "data/current_input"
check_dir "output/current"
echo ""

# 4. GUPRI Mappings (SUPER CRITICAL)
echo -e "${YELLOW}4. GUPRI Persistence:${NC}"
if check_file "output/current/gupri_mappings.json"; then
    ID_COUNT=$(cat output/current/gupri_mappings.json | grep -c '":' 2>/dev/null || echo "0")
    echo -e "     → Contains $ID_COUNT ID mappings"
fi
echo ""

# 5. Documentation
echo -e "${YELLOW}5. Documentation:${NC}"
check_file "README.md"
check_dir "docs"
echo ""

# 6. Current Generated Files
echo -e "${YELLOW}6. Current Generated Output:${NC}"
if [ -f "output/current/cmc_stagegate_instances.ttl" ]; then
    echo -e "  ${GREEN}✅${NC} output/current/cmc_stagegate_instances.ttl"
else
    echo -e "  ${YELLOW}⚠️${NC}  output/current/cmc_stagegate_instances.ttl (will be regenerated)"
    WARNINGS=$((WARNINGS + 1))
fi

if [ -f "output/current/cmc_stagegate_all.ttl" ]; then
    echo -e "  ${GREEN}✅${NC} output/current/cmc_stagegate_all.ttl"
else
    echo -e "  ${YELLOW}⚠️${NC}  output/current/cmc_stagegate_all.ttl (will be regenerated)"
    WARNINGS=$((WARNINGS + 1))
fi
echo ""

# 7. Test Pipeline Functionality
echo -e "${YELLOW}7. Testing Pipeline:${NC}"
if [ -x "run_pipeline.sh" ]; then
    echo -e "  ${GREEN}✅${NC} run_pipeline.sh is executable"
else
    echo -e "  ${RED}❌${NC} run_pipeline.sh is not executable"
    echo "     Fix with: chmod +x run_pipeline.sh"
    MISSING=$((MISSING + 1))
fi

# Check Python
if command -v python3 &> /dev/null; then
    echo -e "  ${GREEN}✅${NC} Python3 is available"
else
    echo -e "  ${RED}❌${NC} Python3 not found"
    MISSING=$((MISSING + 1))
fi

# Check rapper (optional but good)
if command -v rapper &> /dev/null; then
    echo -e "  ${GREEN}✅${NC} Rapper validator is available"
else
    echo -e "  ${YELLOW}⚠️${NC}  Rapper not found (optional, install with: brew install raptor)"
    WARNINGS=$((WARNINGS + 1))
fi
echo ""

# Summary
echo "══════════════════════════════"
if [ $MISSING -eq 0 ]; then
    if [ $WARNINGS -eq 0 ]; then
        echo -e "${GREEN}✅ ALL CRITICAL FILES PRESENT!${NC}"
        echo -e "${GREEN}Repository is ready to use!${NC}"
    else
        echo -e "${GREEN}✅ All critical files present${NC}"
        echo -e "${YELLOW}⚠️  $WARNINGS warnings (non-critical)${NC}"
        echo ""
        echo "Repository is functional."
        echo "Run './run_pipeline.sh -e' to regenerate any missing outputs."
    fi
else
    echo -e "${RED}❌ CRITICAL FILES MISSING: $MISSING${NC}"
    echo ""
    echo "DO NOT proceed with cleanup!"
    echo "Restore from backup or check what happened."
fi
echo "══════════════════════════════"
echo ""

# Suggest next steps
if [ $MISSING -eq 0 ]; then
    echo "Next steps:"
    echo "1. Run the pipeline to test: ./run_pipeline.sh -e"
    echo "2. Check output: ls -la output/current/"
    echo "3. Validate: python3 scripts/validation/verify_ttl_files.py"
fi

exit $MISSING
