#!/bin/bash

# TTL File Reorganization Script
# Moves all required TTL files to data/required_ttl_files/

set -e

# Colors
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
NC='\033[0m'

echo -e "${GREEN}📁 TTL File Reorganization Script${NC}"
echo "===================================="
echo ""

# Step 1: Create new directory
echo -e "${YELLOW}Step 1: Creating new directory structure${NC}"
mkdir -p data/required_ttl_files
echo -e "  ${GREEN}✅${NC} Created data/required_ttl_files/"

# Step 2: Move root TTL files (6 files)
echo ""
echo -e "${YELLOW}Step 2: Moving root TTL files${NC}"

ROOT_TTL_FILES=(
    "cmc_stagegate_base.ttl"
    "cmc_stagegate_drug_products.ttl"
    "cmc_stagegate_modalities.ttl"
    "cmc_stagegate_temporal.ttl"
    "cmc_stagegate_gist_align.ttl"
    "cmc_stagegate_gist_examples.ttl"
)

for file in "${ROOT_TTL_FILES[@]}"; do
    if [ -f "$file" ]; then
        mv "$file" "data/required_ttl_files/"
        echo -e "  ${GREEN}✅${NC} Moved $file"
    else
        echo -e "  ${YELLOW}⚠️${NC}  $file not found in root"
    fi
done

# Step 3: Move example TTL files (3 files)
echo ""
echo -e "${YELLOW}Step 3: Moving example TTL files${NC}"

EXAMPLE_FILES=(
    "data/example_drug_instances.ttl"
    "data/example_temporal_tracking.ttl"
    "data/example_triples.txt"  # Note: This is .txt not .ttl
)

for file in "${EXAMPLE_FILES[@]}"; do
    if [ -f "$file" ]; then
        filename=$(basename "$file")
        mv "$file" "data/required_ttl_files/$filename"
        echo -e "  ${GREEN}✅${NC} Moved $filename"
    else
        echo -e "  ${YELLOW}⚠️${NC}  $file not found"
    fi
done

# Step 4: List new structure
echo ""
echo -e "${YELLOW}Step 4: New file structure${NC}"
echo "data/required_ttl_files/"
ls -la data/required_ttl_files/ | grep -E "\.ttl|\.txt" | awk '{print "  • " $9}'

echo ""
echo -e "${GREEN}✅ Reorganization complete!${NC}"
echo ""
echo -e "${RED}IMPORTANT: Now run update_script_paths.sh to update all references${NC}"
