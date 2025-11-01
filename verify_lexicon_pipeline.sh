#!/bin/bash

# Verify Lexicon is fully integrated in pipeline
# Quick check script

set -e

# Colors
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
NC='\033[0m'

echo -e "${GREEN}🔍 Verifying Lexicon Pipeline Integration${NC}"
echo "==========================================="
echo ""

ISSUES=0

# Check 1: Pipeline includes lexicon generation
echo -e "${YELLOW}1. Checking run_pipeline.sh includes lexicon:${NC}"
if grep -q "generate_lexicon_ttl.py" run_pipeline.sh; then
    echo -e "   ${GREEN}✅${NC} Lexicon generator is in pipeline"
    
    # Check it's in the right order (after SME, before combine)
    SME_LINE=$(grep -n "generate_sme_ttl.py" run_pipeline.sh | cut -d: -f1)
    LEX_LINE=$(grep -n "generate_lexicon_ttl.py" run_pipeline.sh | cut -d: -f1)
    COMBINE_LINE=$(grep -n "combine_ttls.py" run_pipeline.sh | cut -d: -f1)
    
    if [ $SME_LINE -lt $LEX_LINE ] && [ $LEX_LINE -lt $COMBINE_LINE ]; then
        echo -e "   ${GREEN}✅${NC} Execution order correct: SME → Lexicon → Combine"
    else
        echo -e "   ${RED}❌${NC} Execution order incorrect"
        ISSUES=$((ISSUES + 1))
    fi
else
    echo -e "   ${RED}❌${NC} Lexicon generator NOT in pipeline"
    ISSUES=$((ISSUES + 1))
fi

# Check 2: Combine script includes lexicon files
echo ""
echo -e "${YELLOW}2. Checking combine_ttls.py includes lexicon:${NC}"
if grep -q "cmc_stagegate_lexicon.ttl" scripts/etl/combine_ttls.py && \
   grep -q "cmc_stagegate_lexicon_instances.ttl" scripts/etl/combine_ttls.py; then
    echo -e "   ${GREEN}✅${NC} Both lexicon files in combine script"
else
    echo -e "   ${RED}❌${NC} Lexicon files missing from combine script"
    ISSUES=$((ISSUES + 1))
fi

# Check 3: README documents lexicon
echo ""
echo -e "${YELLOW}3. Checking README documentation:${NC}"
if grep -q "174 pharmaceutical terms" README.md; then
    echo -e "   ${GREEN}✅${NC} README mentions lexicon (174 terms)"
else
    echo -e "   ${RED}❌${NC} README doesn't mention lexicon terms"
    ISSUES=$((ISSUES + 1))
fi

if grep -q "generate_lexicon_ttl.py" README.md; then
    echo -e "   ${GREEN}✅${NC} README mentions lexicon generator script"
else
    echo -e "   ${RED}❌${NC} README doesn't mention generator script"
    ISSUES=$((ISSUES + 1))
fi

if grep -q "15,000+ triples" README.md; then
    echo -e "   ${GREEN}✅${NC} README shows updated triple count (15,000+)"
else
    echo -e "   ${RED}❌${NC} README has old triple count"
    ISSUES=$((ISSUES + 1))
fi

# Check 4: Files exist
echo ""
echo -e "${YELLOW}4. Checking required files exist:${NC}"
if [ -f "data/required_ttl_files/cmc_stagegate_lexicon.ttl" ]; then
    echo -e "   ${GREEN}✅${NC} Lexicon ontology file exists"
else
    echo -e "   ${RED}❌${NC} Lexicon ontology file missing"
    ISSUES=$((ISSUES + 1))
fi

if [ -f "scripts/etl/generate_lexicon_ttl.py" ]; then
    echo -e "   ${GREEN}✅${NC} Lexicon generator script exists"
else
    echo -e "   ${RED}❌${NC} Generator script missing"
    ISSUES=$((ISSUES + 1))
fi

# Summary
echo ""
echo "==========================================="
if [ $ISSUES -eq 0 ]; then
    echo -e "${GREEN}✅ Lexicon is fully integrated!${NC}"
    echo ""
    echo "Pipeline will execute:"
    echo "  1. Excel extraction"
    echo "  2a. Main TTL generation"
    echo "  2b. SME generation"
    echo "  2c. Lexicon generation ← NEW!"
    echo "  3. Combine all TTLs"
    echo "  4. Validation"
    echo ""
    echo "Ready to run: ./run_pipeline.sh"
else
    echo -e "${RED}❌ Found $ISSUES issues${NC}"
    echo ""
    echo "Please fix the issues above before running pipeline."
fi

exit $ISSUES
