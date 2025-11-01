#!/bin/bash

# Safe Repository Cleanup Script
# This script ONLY removes safe items and preserves ALL functionality

set -e  # Exit on error

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

echo -e "${GREEN}🧹 Safe Repository Cleanup Script${NC}"
echo "=================================="
echo ""
echo -e "${YELLOW}This script will ONLY remove:${NC}"
echo "  • Python __pycache__ directories"
echo "  • .DS_Store files (Mac system files)"
echo "  • Nothing else (unless you explicitly approve)"
echo ""
echo -e "${GREEN}This script PRESERVES:${NC}"
echo "  ✅ All .ttl ontology files"
echo "  ✅ All scripts and code"
echo "  ✅ All documentation"
echo "  ✅ All current data"
echo "  ✅ GUPRI mappings (critical!)"
echo ""

# Check if backup exists
echo -e "${YELLOW}⚠️  IMPORTANT: Have you created a backup?${NC}"
echo "   Recommended: tar -czf ~/staged_backup_$(date +%Y%m%d).tar.gz ."
echo ""
read -p "Have you created a backup? (y/n) " -n 1 -r
echo ""
if [[ ! $REPLY =~ ^[Yy]$ ]]; then
    echo -e "${RED}❌ Please create a backup first!${NC}"
    echo "   Run: tar -czf ~/staged_backup_$(date +%Y%m%d).tar.gz ."
    exit 1
fi

echo ""
echo -e "${GREEN}Starting safe cleanup...${NC}"
echo ""

# 1. Remove Python cache (always safe)
echo "1. Cleaning Python cache directories..."
PYCACHE_COUNT=$(find . -type d -name "__pycache__" -not -path "./.venv/*" 2>/dev/null | wc -l)
if [ $PYCACHE_COUNT -gt 0 ]; then
    find . -type d -name "__pycache__" -not -path "./.venv/*" -exec rm -rf {} + 2>/dev/null || true
    echo -e "   ${GREEN}✅ Removed $PYCACHE_COUNT __pycache__ directories${NC}"
else
    echo "   ℹ️  No __pycache__ directories found"
fi

# 2. Remove .DS_Store files (Mac system files, always safe)
echo "2. Removing .DS_Store files..."
DSSTORE_COUNT=$(find . -name ".DS_Store" 2>/dev/null | wc -l)
if [ $DSSTORE_COUNT -gt 0 ]; then
    find . -name ".DS_Store" -delete 2>/dev/null || true
    echo -e "   ${GREEN}✅ Removed $DSSTORE_COUNT .DS_Store files${NC}"
else
    echo "   ℹ️  No .DS_Store files found"
fi

# 3. Check for old archived folders (but don't auto-delete)
echo ""
echo -e "${YELLOW}3. Old archived folders found:${NC}"
OLD_FOLDERS=""
if [ -d "data/extracted_250910" ]; then
    SIZE=$(du -sh data/extracted_250910 | cut -f1)
    echo "   • data/extracted_250910/ ($SIZE)"
    OLD_FOLDERS="yes"
fi
if [ -d "data/previous_input_250910" ]; then
    SIZE=$(du -sh data/previous_input_250910 | cut -f1)
    echo "   • data/previous_input_250910/ ($SIZE)"
    OLD_FOLDERS="yes"
fi
if [ -d "output/ttl_241031_original" ]; then
    SIZE=$(du -sh output/ttl_241031_original | cut -f1)
    echo "   • output/ttl_241031_original/ ($SIZE)"
    OLD_FOLDERS="yes"
fi

if [ "$OLD_FOLDERS" == "yes" ]; then
    echo ""
    echo -e "${YELLOW}These are archived versions from previous runs.${NC}"
    echo "If you have external backups, they can be safely removed."
    echo ""
    read -p "Remove old archived folders? (y/n) " -n 1 -r
    echo ""
    if [[ $REPLY =~ ^[Yy]$ ]]; then
        [ -d "data/extracted_250910" ] && rm -rf data/extracted_250910/ && echo -e "   ${GREEN}✅ Removed data/extracted_250910/${NC}"
        [ -d "data/previous_input_250910" ] && rm -rf data/previous_input_250910/ && echo -e "   ${GREEN}✅ Removed data/previous_input_250910/${NC}"
        [ -d "output/ttl_241031_original" ] && rm -rf output/ttl_241031_original/ && echo -e "   ${GREEN}✅ Removed output/ttl_241031_original/${NC}"
    else
        echo "   ℹ️  Keeping old archived folders"
    fi
else
    echo "   ℹ️  No old archived folders found"
fi

# 4. Summary
echo ""
echo -e "${GREEN}═══════════════════════════════════${NC}"
echo -e "${GREEN}✅ Safe cleanup complete!${NC}"
echo -e "${GREEN}═══════════════════════════════════${NC}"
echo ""
echo "Preserved (verified):"

# Verify critical files still exist
if [ -f "output/current/gupri_mappings.json" ]; then
    echo -e "  ${GREEN}✅${NC} GUPRI mappings ($(cat output/current/gupri_mappings.json | grep -c '":') IDs)"
fi

TTL_COUNT=$(ls -1 *.ttl 2>/dev/null | wc -l)
if [ $TTL_COUNT -gt 0 ]; then
    echo -e "  ${GREEN}✅${NC} Ontology files ($TTL_COUNT .ttl files)"
fi

SCRIPT_COUNT=$(find scripts -name "*.py" 2>/dev/null | wc -l)
if [ $SCRIPT_COUNT -gt 0 ]; then
    echo -e "  ${GREEN}✅${NC} Python scripts ($SCRIPT_COUNT scripts)"
fi

DOC_COUNT=$(find docs -name "*.md" 2>/dev/null | wc -l)
if [ $DOC_COUNT -gt 0 ]; then
    echo -e "  ${GREEN}✅${NC} Documentation ($DOC_COUNT files)"
fi

if [ -d "output/current" ]; then
    OUTPUT_COUNT=$(ls -1 output/current/*.ttl 2>/dev/null | wc -l)
    echo -e "  ${GREEN}✅${NC} Current outputs ($OUTPUT_COUNT TTL files)"
fi

echo ""
echo -e "${GREEN}Repository is clean and safe!${NC}"
echo ""
echo "Next step: Test the pipeline"
echo "  ./run_pipeline.sh -e"
