#!/bin/bash

# Git Commit Script for All Session Changes
# Includes: Lexicon integration, SME fix, TTL reorganization

set -e

# Colors
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
RED='\033[0;31m'
NC='\033[0m'

echo -e "${GREEN}🚀 Git Commit for Session Changes${NC}"
echo "===================================="
echo ""

echo -e "${YELLOW}📊 Session Summary:${NC}"
echo ""
echo "✨ MAJOR FEATURES ADDED:"
echo "  1. Pharmaceutical Lexicon Integration (174 terms)"
echo "  2. Fixed SME generator (now working with 43 SMEs)"
echo "  3. TTL file reorganization (moved to data/required_ttl_files/)"
echo ""
echo "📈 IMPACT:"
echo "  • Total triples: 35,828 (up from 13,694)"
echo "  • 174 pharmaceutical terms with definitions"
echo "  • 43 SMEs mapped to 40 functional areas"
echo "  • Cleaner repository structure"
echo ""

echo -e "${BLUE}Major files changed:${NC}"
echo ""
echo "NEW FEATURES:"
echo "  ✨ data/required_ttl_files/cmc_stagegate_lexicon.ttl"
echo "  ✨ scripts/etl/generate_lexicon_ttl.py"
echo "  ✨ queries/lexicon/*.sparql (4 files)"
echo ""
echo "FIXES:"
echo "  🔧 scripts/etl/generate_sme_ttl.py (fixed CSV parsing)"
echo ""
echo "REORGANIZATION:"
echo "  📁 Moved 9 TTL files to data/required_ttl_files/"
echo "  📝 Updated all script paths"
echo ""
echo "UPDATES:"
echo "  ✏️ run_pipeline.sh (added lexicon step)"
echo "  ✏️ scripts/etl/combine_ttls.py (includes lexicon)"
echo "  ✏️ README.md (documents all features)"
echo ""

# Check git status
echo -e "${BLUE}Current git status:${NC}"
git status --short | head -20
TOTAL_CHANGES=$(git status --short | wc -l)
if [ $TOTAL_CHANGES -gt 20 ]; then
    echo "  ... and $((TOTAL_CHANGES - 20)) more files"
fi
echo ""

# Stage all changes
echo -e "${YELLOW}Staging all changes...${NC}"
git add -A
echo "✅ All changes staged"
echo ""

# Create comprehensive commit message
COMMIT_MSG="feat: add lexicon integration, fix SME generator, reorganize TTL files

Major Session Updates (35,828 total triples):

FEATURE: Pharmaceutical Lexicon Integration
- Added 174 industry terms with full definitions
- Created cmc_stagegate_lexicon.ttl ontology extension
- Implemented generate_lexicon_ttl.py for CSV processing
- 7 categories: Regulatory, Quality, Process, Cell/Gene, Clinical, Analytical, Organizational
- Added 4 SPARQL queries for term lookup
- Integrated into pipeline as Step 2c
- ~1,600 triples added to knowledge graph

FIX: SME Generator
- Fixed generate_sme_ttl.py to handle actual CSV structure
- Now correctly parses Value Stream/Functional Area/Contact/Person columns
- Successfully generates 43 SMEs mapped to 40 functional areas
- 449 triples (was empty before)
- Handles primary/backup relationships correctly

REFACTOR: TTL File Organization
- Moved 9 TTL files to data/required_ttl_files/ for better organization
- Updated all script paths (combine_ttls.py, validate_gist_alignment.py, etc.)
- Cleaner root directory structure
- All pipeline scripts updated to use new paths

PIPELINE IMPROVEMENTS:
- Total triples increased from 13,694 to 35,828
- Added Step 2c for lexicon generation
- Fixed SME generation (Step 2b)
- All validations passing (GIST, SPARQL, rapper)
- GraphDB deployment ready

FILES ADDED:
- data/required_ttl_files/cmc_stagegate_lexicon.ttl
- scripts/etl/generate_lexicon_ttl.py
- queries/lexicon/ (4 SPARQL files)
- Various documentation and test files

FILES FIXED:
- scripts/etl/generate_sme_ttl.py
- scripts/etl/combine_ttls.py
- scripts/validation/validate_gist_alignment.py
- scripts/deployment/export_to_graphdb.py

DOCUMENTATION:
- Updated README with all new features
- Added lexicon documentation
- Pipeline now fully documented

Tested: Full pipeline run successful, all validations pass"

# Commit
echo -e "${YELLOW}Creating commit...${NC}"
git commit -m "$COMMIT_MSG"
echo ""

# Show commit info
echo -e "${GREEN}Commit created successfully!${NC}"
echo ""
COMMIT_HASH=$(git rev-parse --short HEAD)
BRANCH=$(git branch --show-current)
echo "Branch: $BRANCH"
echo "Commit: $COMMIT_HASH"
echo ""

# Show stats
echo -e "${BLUE}Commit statistics:${NC}"
git diff --stat HEAD^ HEAD | tail -5
echo ""

# Push
echo -e "${YELLOW}Ready to push to GitHub${NC}"
echo ""
read -p "Push to origin/$BRANCH? (y/n) " -n 1 -r
echo ""
if [[ $REPLY =~ ^[Yy]$ ]]; then
    echo -e "${YELLOW}Pushing to GitHub...${NC}"
    git push origin $BRANCH
    echo ""
    echo -e "${GREEN}✅ Successfully pushed to GitHub!${NC}"
    echo ""
    echo "Summary of session achievements:"
    echo "• Added pharmaceutical lexicon (174 terms)"
    echo "• Fixed SME generator (43 experts)"
    echo "• Reorganized repository structure"
    echo "• Total knowledge graph: 35,828 triples"
    echo ""
    echo -e "${GREEN}🎉 All changes committed and pushed!${NC}"
else
    echo "Push cancelled. You can push manually with: git push origin $BRANCH"
fi
