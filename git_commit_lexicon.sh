#!/bin/bash

# Git Commit Script for Lexicon Integration
# Commits all changes from adding the pharmaceutical lexicon feature

set -e

# Colors
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m'

echo -e "${GREEN}🚀 Git Commit for Lexicon Integration${NC}"
echo "========================================"
echo ""

echo -e "${YELLOW}📚 Lexicon Feature Summary:${NC}"
echo ""
echo "✨ NEW FEATURE: Pharmaceutical Lexicon Integration"
echo "  • 174 industry terms with full definitions"
echo "  • 7 categories (Regulatory, Quality, Process, etc.)"
echo "  • Critical and regulatory term flagging"
echo "  • Stage-specific term usage tracking"
echo "  • SKOS-compatible for semantic web"
echo ""

echo -e "${BLUE}Files to commit:${NC}"
echo ""
echo "📁 New Ontology Extension:"
echo "  • data/required_ttl_files/cmc_stagegate_lexicon.ttl"
echo ""
echo "📝 New Scripts:"
echo "  • scripts/etl/generate_lexicon_ttl.py"
echo "  • test_lexicon.sh"
echo "  • verify_lexicon_pipeline.sh"
echo ""
echo "🔍 New Queries (4 files):"
echo "  • queries/lexicon/*.sparql"
echo ""
echo "📚 New Documentation:"
echo "  • docs/LEXICON_ANALYSIS.md"
echo "  • docs/LEXICON_INTEGRATION_COMPLETE.md"
echo "  • LEXICON_PIPELINE_STATUS.md"
echo ""
echo "✏️ Updated Files:"
echo "  • run_pipeline.sh - Added Step 2c"
echo "  • scripts/etl/combine_ttls.py - Includes lexicon"
echo "  • README.md - Documents lexicon feature"
echo ""

# Check git status
echo -e "${BLUE}Current git status:${NC}"
git status --short
echo ""

# Stage all changes
echo -e "${YELLOW}Staging all changes...${NC}"
git add -A
echo "✅ All changes staged"
echo ""

# Create detailed commit message
COMMIT_MSG="feat: add pharmaceutical lexicon integration (174 terms)

Major feature addition: Comprehensive pharmaceutical/biotechnology terminology database

New Ontology Extension:
- Created cmc_stagegate_lexicon.ttl with DefinedTerm class
- 7 term categories (Regulatory, Quality, Process, Cell/Gene, Clinical, Analytical, Organizational)
- Properties for abbreviations, definitions, criticality, and stage linkages
- SKOS integration for semantic web compatibility

New Functionality:
- generate_lexicon_ttl.py processes Lexicon CSV to RDF
- Auto-categorizes 174 pharmaceutical terms
- Flags critical terms (CQA, CPP, PPQ, etc.)
- Links terms to relevant stages
- GUPRI-compliant IDs for persistence

Pipeline Integration:
- Added Step 2c to run_pipeline.sh for lexicon generation
- Updated combine_ttls.py to include lexicon files
- Execution order: Main → SME → Lexicon → Combine
- Increases total triples from 13,694+ to 15,000+

SPARQL Queries:
- Lookup any abbreviation definition
- Find critical and regulatory terms
- Group terms by category
- Find stage-specific terminology

Documentation:
- Updated README with lexicon feature description
- Created comprehensive analysis and integration guides
- Added test and verification scripts

Business Value:
- Instant definition lookup for any abbreviation
- Regulatory compliance term tracking
- Enhanced onboarding with complete glossary
- Stage-specific term usage visibility
- Cross-referencing with deliverables and SMEs

Files Added:
- data/required_ttl_files/cmc_stagegate_lexicon.ttl
- scripts/etl/generate_lexicon_ttl.py
- queries/lexicon/ (4 SPARQL queries)
- docs/LEXICON_*.md (documentation)
- test_lexicon.sh, verify_lexicon_pipeline.sh

Tested: Lexicon generator working, pipeline integration verified"

# Commit
echo -e "${YELLOW}Creating commit...${NC}"
git commit -m "$COMMIT_MSG"
echo ""

# Show what will be pushed
echo -e "${BLUE}Ready to push to GitHub${NC}"
echo ""
BRANCH=$(git branch --show-current)
echo "Current branch: $BRANCH"
echo ""

# Get commit info
COMMIT_HASH=$(git rev-parse --short HEAD)
FILES_CHANGED=$(git diff --stat HEAD^ HEAD | tail -1)
echo "Commit: $COMMIT_HASH"
echo "Changes: $FILES_CHANGED"
echo ""

# Push
read -p "Push to origin/$BRANCH? (y/n) " -n 1 -r
echo ""
if [[ $REPLY =~ ^[Yy]$ ]]; then
    echo -e "${YELLOW}Pushing to GitHub...${NC}"
    git push origin $BRANCH
    echo ""
    echo -e "${GREEN}✅ Successfully pushed Lexicon integration to GitHub!${NC}"
    echo ""
    echo "Feature added:"
    echo "• 174 pharmaceutical terms"
    echo "• Full integration with pipeline"
    echo "• Ready for production use"
else
    echo "Push cancelled. You can push manually with: git push origin $BRANCH"
fi
