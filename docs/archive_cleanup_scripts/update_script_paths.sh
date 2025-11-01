#!/bin/bash

# Update Script Paths After TTL Reorganization
# Updates all references to TTL files in scripts

set -e

# Colors
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m'

echo -e "${GREEN}📝 Updating Script Paths for TTL Files${NC}"
echo "========================================"
echo ""

# Step 1: Update combine_ttls.py
echo -e "${YELLOW}Step 1: Updating combine_ttls.py${NC}"

cat > scripts/etl/combine_ttls.py << 'EOF'
#!/usr/bin/env python3
"""
Combine multiple TTL files into a single comprehensive file.
Consolidates base ontology, extensions, instances, and alignments.
"""

from pathlib import Path

# Default files to combine - now in organized location
DEFAULT_FILES = [
    "/Users/nicholasbaro/Python/staged/data/required_ttl_files/cmc_stagegate_base.ttl",
    "/Users/nicholasbaro/Python/staged/data/required_ttl_files/cmc_stagegate_drug_products.ttl",
    "/Users/nicholasbaro/Python/staged/data/required_ttl_files/cmc_stagegate_modalities.ttl",
    "/Users/nicholasbaro/Python/staged/data/required_ttl_files/cmc_stagegate_temporal.ttl",
    "/Users/nicholasbaro/Python/staged/output/current/cmc_stagegate_instances.ttl",
    "/Users/nicholasbaro/Python/staged/output/current/cmc_stagegate_sme_instances.ttl",
    "/Users/nicholasbaro/Python/staged/data/required_ttl_files/example_drug_instances.ttl",
    "/Users/nicholasbaro/Python/staged/data/required_ttl_files/example_temporal_tracking.ttl",
    "/Users/nicholasbaro/Python/staged/data/required_ttl_files/cmc_stagegate_gist_align.ttl",
]
# Combined output goes to output/current/
DEFAULT_OUTPUT = "/Users/nicholasbaro/Python/staged/output/current/cmc_stagegate_all.ttl"

def combine_ttl_files(input_files=DEFAULT_FILES, output_file=DEFAULT_OUTPUT):
    """
    Combine multiple TTL files into one.
    
    Args:
        input_files: List of TTL file paths to combine
        output_file: Output file path for combined TTL
    """
    output_path = Path(output_file)
    output_path.parent.mkdir(parents=True, exist_ok=True)
    
    # Track prefixes and triples
    all_prefixes = {}
    all_triples = []
    
    for file_path in input_files:
        file_path = Path(file_path)
        if not file_path.exists():
            print(f"Warning: {file_path} not found, skipping...")
            continue
            
        print(f"Processing: {file_path.name}")
        
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
            
            # Split into prefixes and triples
            lines = content.split('\n')
            for line in lines:
                line = line.strip()
                if line.startswith('@prefix'):
                    # Extract prefix
                    parts = line.split()
                    if len(parts) >= 3:
                        prefix_name = parts[1]
                        prefix_uri = ' '.join(parts[2:])
                        all_prefixes[prefix_name] = prefix_uri
                elif line and not line.startswith('#'):
                    # It's a triple (not a comment or empty)
                    all_triples.append(line)
    
    # Write combined file
    with open(output_path, 'w', encoding='utf-8') as f:
        # Write prefixes first
        for prefix_name, prefix_uri in sorted(all_prefixes.items()):
            f.write(f"@prefix {prefix_name} {prefix_uri}\n")
        
        f.write("\n")
        
        # Write all triples
        f.write('\n'.join(all_triples))
    
    print(f"\n✅ Combined {len(input_files)} files into {output_path}")
    print(f"   Total prefixes: {len(all_prefixes)}")
    print(f"   Total lines: {len(all_triples)}")

if __name__ == "__main__":
    combine_ttl_files()
EOF

echo -e "  ${GREEN}✅${NC} Updated combine_ttls.py"

# Step 2: Update verify_critical_files.sh
echo ""
echo -e "${YELLOW}Step 2: Updating verify_critical_files.sh${NC}"

# Update the check_file function calls in verify_critical_files.sh
sed -i.bak 's|check_file "cmc_stagegate_base.ttl"|check_file "data/required_ttl_files/cmc_stagegate_base.ttl"|g' verify_critical_files.sh
sed -i.bak 's|check_file "cmc_stagegate_drug_products.ttl"|check_file "data/required_ttl_files/cmc_stagegate_drug_products.ttl"|g' verify_critical_files.sh
sed -i.bak 's|check_file "cmc_stagegate_modalities.ttl"|check_file "data/required_ttl_files/cmc_stagegate_modalities.ttl"|g' verify_critical_files.sh
sed -i.bak 's|check_file "cmc_stagegate_temporal.ttl"|check_file "data/required_ttl_files/cmc_stagegate_temporal.ttl"|g' verify_critical_files.sh
sed -i.bak 's|check_file "cmc_stagegate_gist_align.ttl"|check_file "data/required_ttl_files/cmc_stagegate_gist_align.ttl"|g' verify_critical_files.sh
sed -i.bak 's|check_file "cmc_stagegate_gist_examples.ttl"|check_file "data/required_ttl_files/cmc_stagegate_gist_examples.ttl"|g' verify_critical_files.sh

# Clean up backup
rm -f verify_critical_files.sh.bak

echo -e "  ${GREEN}✅${NC} Updated verify_critical_files.sh"

# Step 3: Update README references (if needed)
echo ""
echo -e "${YELLOW}Step 3: Checking for other references${NC}"

# Check for any other references to the TTL files
echo "Checking for remaining references to root TTL files..."
REMAINING=$(grep -r "cmc_stagegate.*\.ttl" . --include="*.py" --include="*.sh" --include="*.md" 2>/dev/null | grep -v "data/required_ttl_files" | grep -v ".bak" | grep -v "Binary file" | wc -l)

if [ $REMAINING -gt 0 ]; then
    echo -e "  ${YELLOW}⚠️${NC}  Found $REMAINING other references that may need updating"
    echo "  Run: grep -r 'cmc_stagegate.*\.ttl' . --include='*.py' --include='*.sh'"
else
    echo -e "  ${GREEN}✅${NC} No other references found"
fi

echo ""
echo -e "${GREEN}✅ Path updates complete!${NC}"
echo ""
echo "Next steps:"
echo "1. Run: ./reorganize_ttl_files.sh to move the files"
echo "2. Run: ./run_pipeline.sh -e to test the pipeline"
echo "3. Commit the changes if everything works"
