#!/bin/bash

# Git Commit and Push Script for TTL Reorganization
# Commits all the changes from reorganizing TTL files and cleaning up

set -e

# Colors
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m'

echo -e "${GREEN}🚀 Git Commit & Push for Repository Reorganization${NC}"
echo "===================================================="
echo ""

echo -e "${YELLOW}Changes to commit:${NC}"
echo ""
echo "📁 TTL File Reorganization:"
echo "  • Moved 6 ontology TTL files from root → data/required_ttl_files/"
echo "  • Moved 3 example TTL files from data/ → data/required_ttl_files/"
echo ""
echo "📝 Script Updates:"
echo "  • Updated scripts/etl/combine_ttls.py - new TTL paths"
echo "  • Updated scripts/validation/validate_gist_alignment.py - new paths"
echo "  • Updated scripts/deployment/export_to_graphdb.py - new paths"
echo "  • Updated verify_critical_files.sh - check new locations"
echo ""
echo "🧹 Root Cleanup:"
echo "  • Removed 8 one-time scripts and documentation"
echo "  • Root directory now contains only 5 essential files"
echo ""

# Check current status
echo -e "${BLUE}Checking Git status...${NC}"
git status --short
echo ""

# Stage all changes
echo -e "${YELLOW}Staging changes...${NC}"
git add -A
echo "✅ All changes staged"
echo ""

# Create commit message
COMMIT_MSG="refactor: reorganize TTL files and clean up root directory

Major repository restructuring for better organization:

TTL File Reorganization:
- Created data/required_ttl_files/ directory
- Moved 6 core ontology files from root to new directory
- Moved 3 example files from data/ to new directory
- All 9 TTL files now centralized in one location

Script Updates:
- Updated combine_ttls.py with new file paths
- Updated validate_gist_alignment.py with new paths
- Updated export_to_graphdb.py with new paths  
- Updated verify_critical_files.sh to check new locations

Root Directory Cleanup:
- Removed one-time reorganization scripts (3 files)
- Removed temporary documentation (5 files)
- Root now contains only essential scripts (5 files)
- 62% reduction in root directory clutter

Benefits:
- Cleaner repository structure
- All required TTL files in one place
- Easier to locate and manage files
- Pipeline continues to work with new structure"

# Commit
echo -e "${YELLOW}Creating commit...${NC}"
git commit -m "$COMMIT_MSG"
echo ""

# Show what will be pushed
echo -e "${BLUE}Ready to push to origin/main${NC}"
echo ""
BRANCH=$(git branch --show-current)
echo "Current branch: $BRANCH"
echo ""

# Push
read -p "Push to origin/$BRANCH? (y/n) " -n 1 -r
echo ""
if [[ $REPLY =~ ^[Yy]$ ]]; then
    echo -e "${YELLOW}Pushing to GitHub...${NC}"
    git push origin $BRANCH
    echo ""
    echo -e "${GREEN}✅ Successfully pushed to GitHub!${NC}"
    echo ""
    echo "Changes pushed:"
    echo "• TTL files reorganized"
    echo "• Scripts updated"
    echo "• Repository cleaned up"
else
    echo "Push cancelled. You can push manually with: git push origin $BRANCH"
fi
