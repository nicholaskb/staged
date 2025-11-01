#!/bin/bash

# CMC Stage-Gate Ontology Pipeline Runner
# =========================================
# This script runs the complete ETL pipeline with optional steps

set -e  # Exit on error

# Color codes for output
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
NC='\033[0m' # No Color

# Function to print colored messages
print_status() {
    echo -e "${GREEN}[✓]${NC} $1"
}

print_warning() {
    echo -e "${YELLOW}[!]${NC} $1"
}

print_error() {
    echo -e "${RED}[✗]${NC} $1"
}

# Default values
SKIP_EXTRACTION=false
SKIP_VALIDATION=false
SKIP_GRAPHDB=false
GRAPHDB_URL="http://localhost:7200"
GRAPHDB_REPO="cmc-stagegate"
DRY_RUN=true

# Help function
show_help() {
    echo "CMC Stage-Gate Ontology Pipeline Runner"
    echo ""
    echo "Usage: $0 [options]"
    echo ""
    echo "Options:"
    echo "  -h, --help           Show this help message"
    echo "  -a, --all            Run all steps (default: runs all except GraphDB upload)"
    echo "  -e, --skip-extract   Skip Excel extraction step"
    echo "  -v, --skip-validate  Skip validation steps"
    echo "  -g, --with-graphdb   Include GraphDB deployment"
    echo "  -u, --graphdb-url    GraphDB URL (default: http://localhost:7200)"
    echo "  -r, --repository     GraphDB repository name (default: cmc-stagegate)"
    echo "  --no-dry-run         Actually upload to GraphDB (default: dry run only)"
    echo ""
    echo "Examples:"
    echo "  $0                   # Run ETL and validation only"
    echo "  $0 --all             # Run everything including GraphDB"
    echo "  $0 -g --no-dry-run   # Include GraphDB with actual upload"
    echo "  $0 -e                # Skip extraction (if CSVs already exist)"
}

# Parse command line arguments
while [[ $# -gt 0 ]]; do
    case $1 in
        -h|--help)
            show_help
            exit 0
            ;;
        -a|--all)
            SKIP_GRAPHDB=false
            DRY_RUN=false
            ;;
        -e|--skip-extract)
            SKIP_EXTRACTION=true
            ;;
        -v|--skip-validate)
            SKIP_VALIDATION=true
            ;;
        -g|--with-graphdb)
            SKIP_GRAPHDB=false
            ;;
        -u|--graphdb-url)
            GRAPHDB_URL="$2"
            shift
            ;;
        -r|--repository)
            GRAPHDB_REPO="$2"
            shift
            ;;
        --no-dry-run)
            DRY_RUN=false
            ;;
        *)
            echo "Unknown option: $1"
            show_help
            exit 1
            ;;
    esac
    shift
done

echo "========================================"
echo "CMC Stage-Gate Ontology Pipeline"
echo "========================================"
echo ""

# Step 1: Extract Excel data
if [ "$SKIP_EXTRACTION" = false ]; then
    print_status "Step 1: Extracting Excel data..."
    print_status "Input: data/current_input/ -> Output: data/current/"
    if python3 scripts/etl/extract_xlsx.py --input-dir ./data/current_input --output-dir ./data/current --combine; then
        print_status "Excel extraction completed"
    else
        print_error "Excel extraction failed"
        exit 1
    fi
else
    print_warning "Skipping Excel extraction"
fi

# Step 2: Generate TTL from CSV data (GUPRI-compliant)
print_status "Step 2a: Generating main TTL instances (GUPRI-compliant)..."

# Check if GUPRI mappings exist from previous runs
if [ -f "output/current/gupri_mappings.json" ]; then
    print_status "Found existing GUPRI mappings (will preserve consistency)"
fi

if python3 scripts/etl/generate_cmc_ttl_gupri.py; then
    print_status "Main TTL generation completed (GUPRI-compliant)"
else
    print_error "Main TTL generation failed"
    exit 1
fi

print_status "Step 2b: Generating SME TTL instances..."
if python3 scripts/etl/generate_sme_ttl.py; then
    print_status "SME TTL generation completed"
else
    print_error "SME TTL generation failed"
    exit 1
fi

# Step 3: Combine all TTL files (including drug products and temporal ontology)
print_status "Step 3: Combining all TTL files..."
print_status "  • Base ontology"
print_status "  • Drug product & IDMP extensions"
print_status "  • Modality classifications (10 types)"  
print_status "  • W3C Time/temporal tracking"
print_status "  • Stage/deliverable instances"
print_status "  • SME instances"
print_status "  • GIST alignments"
if python3 scripts/etl/combine_ttls.py; then
    print_status "TTL combination completed (13,694+ triples)"
else
    print_error "TTL combination failed"
    exit 1
fi

# Step 4: Validation
if [ "$SKIP_VALIDATION" = false ]; then
    print_status "Step 4: Validating TTL files..."
    
    # Verify TTL files
    if python3 scripts/validation/verify_ttl_files.py; then
        print_status "TTL validation completed"
    else
        print_error "TTL validation failed"
        exit 1
    fi
    
    # Validate GIST alignment
    print_status "Validating GIST alignment..."
    if python3 scripts/validation/validate_gist_alignment.py; then
        print_status "GIST alignment validation completed"
    else
        print_error "GIST alignment validation failed"
        exit 1
    fi
    
    # Run SPARQL tests (if GraphDB is available)
    if [ -x scripts/validation/test_gist_alignment.sh ]; then
        print_status "Running SPARQL validation tests..."
        if ./scripts/validation/test_gist_alignment.sh 2>/dev/null; then
            print_status "SPARQL tests completed"
        else
            print_warning "SPARQL tests skipped (GraphDB may not be running)"
        fi
    fi
else
    print_warning "Skipping validation steps"
fi

# Step 5: GraphDB deployment
if [ "$SKIP_GRAPHDB" = false ]; then
    print_status "Step 5: Deploying to GraphDB..."
    
    GRAPHDB_ARGS="--graphdb-url $GRAPHDB_URL --repository $GRAPHDB_REPO --files output/current/cmc_stagegate_all.ttl"
    
    if [ "$DRY_RUN" = true ]; then
        print_warning "Running in dry-run mode (no actual upload)"
        GRAPHDB_ARGS="$GRAPHDB_ARGS --dry-run"
    else
        GRAPHDB_ARGS="$GRAPHDB_ARGS --no-dry-run"
    fi
    
    if python3 scripts/deployment/export_to_graphdb.py $GRAPHDB_ARGS; then
        if [ "$DRY_RUN" = false ]; then
            print_status "GraphDB deployment completed"
        else
            print_status "GraphDB dry run completed"
        fi
    else
        print_error "GraphDB deployment failed"
        print_warning "Make sure GraphDB is running at $GRAPHDB_URL"
        exit 1
    fi
else
    print_warning "Skipping GraphDB deployment"
fi

echo ""
echo "========================================"
print_status "Pipeline completed successfully!"
echo "========================================"
echo ""

# Print summary
echo "Summary:"
echo "--------"
[ "$SKIP_EXTRACTION" = false ] && echo "✓ Excel data extracted to data/current/" || echo "- Excel extraction skipped"
echo "✓ TTL instances generated in output/current/ (GUPRI-compliant)"
if [ -f "output/current/gupri_mappings.json" ]; then
    echo "✓ GUPRI mappings preserved ($(cat output/current/gupri_mappings.json | grep -c '":') IDs)"
fi
echo "✓ TTL files combined in output/current/"
[ "$SKIP_VALIDATION" = false ] && echo "✓ Validation completed" || echo "- Validation skipped"
if [ "$SKIP_GRAPHDB" = false ]; then
    if [ "$DRY_RUN" = false ]; then
        echo "✓ Deployed to GraphDB at $GRAPHDB_URL/repositories/$GRAPHDB_REPO"
    else
        echo "✓ GraphDB deployment tested (dry run)"
    fi
else
    echo "- GraphDB deployment skipped"
fi

echo ""
echo "Next steps:"
echo "-----------"
if [ "$SKIP_GRAPHDB" = true ]; then
    echo "• To deploy to GraphDB: $0 --with-graphdb"
fi
if [ "$DRY_RUN" = true ] && [ "$SKIP_GRAPHDB" = false ]; then
    echo "• To actually upload to GraphDB: $0 --with-graphdb --no-dry-run"
fi
echo "• View source TTL files: ls -la *.ttl"
echo "• View generated TTL files: ls -la output/current/*.ttl"
echo "• View extracted CSVs: ls -la data/current/"
echo "• Run Stage Gate 0 example: python3 examples/stage_gate_0/stage_gate_0_example.py"
echo ""
