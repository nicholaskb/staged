#!/bin/bash
# Run pipeline without extraction (assumes CSVs already exist)
# This skips the pandas-dependent extraction step

echo "=== CMC Stage-Gate Pipeline (No Extraction) ==="
echo ""

# Check if CSVs exist
if [ ! -f "data/current/Protein_and_CGT_SGD_Template_Final_ENDORSED_JAN_2023_MOD_NB__SGD.csv" ]; then
    echo "❌ Error: CSV files not found in data/current/"
    echo "Please run extraction first: python3 scripts/etl/extract_xlsx.py"
    exit 1
fi

echo "✅ CSV files found. Starting pipeline..."
echo ""

# Step 1: Generate TTL
echo "Step 1a: Generating main TTL from CSV..."
python3 scripts/etl/generate_cmc_ttl.py
if [ $? -ne 0 ]; then
    echo "❌ Main TTL generation failed"
    exit 1
fi
echo "✅ Main TTL generation complete"
echo ""

echo "Step 1b: Generating SME TTL from CSV..."
python3 scripts/etl/generate_sme_ttl.py
if [ $? -ne 0 ]; then
    echo "❌ SME TTL generation failed"
    exit 1
fi
echo "✅ SME TTL generation complete"
echo ""

# Step 2: Combine TTLs
echo "Step 2: Combining TTL files..."
python3 scripts/etl/combine_ttls.py
if [ $? -ne 0 ]; then
    echo "❌ TTL combination failed"
    exit 1
fi
echo "✅ TTL combination complete"
echo ""

# Step 3: Validate
echo "Step 3: Validating all TTL files..."
python3 scripts/validation/verify_ttl_files.py
if [ $? -ne 0 ]; then
    echo "❌ Validation failed"
    exit 1
fi
echo ""

echo "=== ✅ PIPELINE COMPLETE ==="
echo ""
echo "Generated files:"
echo "  • output/current/cmc_stagegate_instances.ttl"
echo "  • output/current/cmc_stagegate_all.ttl"
echo ""
echo "Statistics:"
ls -lh output/current/*.ttl | awk '{print "  • " $9 ": " $5}'
echo ""
echo "Next steps:"
echo "  • Load into Protege for visualization"
echo "  • Deploy to GraphDB if needed"
echo "  • Query with SPARQL"
