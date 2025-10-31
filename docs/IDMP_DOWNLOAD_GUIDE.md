# IDMP Ontology Download Guide

## Should You Download the Full IDMP Ontology?

### Quick Answer
**Start with what we have, download full IDMP later if needed.**

## Current Coverage (What You Already Have)

### ✅ Core IDMP Elements in Your System
```turtle
# Key identifiers
idmp:mpid           # ISO 11615 - Medicinal Product ID
idmp:phpid          # ISO 11616 - Pharmaceutical Product ID  
idmp:substanceId    # ISO 11238 - Substance ID
ex:substanceUNII    # FDA UNII codes

# EDQM references
idmp:hasDoseForm    # Links to EDQM dose forms
idmp:hasRouteOfAdministration  # Links to EDQM routes
```

### ✅ This Covers 80% of Development Needs
- Drug identification ✓
- Substance tracking ✓
- Basic regulatory identifiers ✓
- Dose form/route mapping ✓

## Full IDMP Ontology Considerations

### Size & Complexity
- **Full ISO IDMP**: ~50MB+ of RDF/OWL
- **5 ISO Standards**: 11615, 11616, 11238, 11239, 11240
- **Thousands of classes**: Manufacturing, packaging, devices, etc.
- **Complex relationships**: May slow down queries

### When You NEED Full IDMP

✅ **Download Full IDMP When:**
1. **Regulatory Submission**: Preparing for FDA/EMA submission
2. **IDMP Compliance Mandate**: Organization requires full compliance
3. **Manufacturing Integration**: Need detailed process ontologies
4. **Global Operations**: Multi-region regulatory requirements
5. **Clinical Trial Registry**: Submitting to WHO ICTRP

❌ **You DON'T Need It For:**
1. **Development Tracking**: Current system sufficient
2. **Stage-Gate Management**: Already covered
3. **Portfolio Management**: Current identifiers enough
4. **Internal Reporting**: Overkill for dashboards

## Recommended Approach

### Phase 1: Current State (NOW) ✅
```bash
# You have everything needed for:
- Drug development tracking
- Stage-gate progression  
- Basic IDMP identifiers
- SME assignments
- Deliverable management
```

### Phase 2: EDQM Vocabularies (NEXT)
```bash
# Download controlled vocabularies only
wget https://standardterms.edqm.eu/standardterms/api/v1/lists/rdf

# Lighter weight (~5MB)
# Gives you all dose forms, routes, units
# Can map to your existing properties
```

### Phase 3: IDMP Subset (LATER)
```bash
# Download specific modules as needed
- ISO 11615 (Medicinal Products) - If doing regulatory
- ISO 11238 (Substances) - If tracking complex molecules
- ISO 11239 (Dose Forms) - If need manufacturing detail
```

### Phase 4: Full IDMP (IF REQUIRED)
```bash
# Full implementation for regulatory compliance
- Complete ISO suite
- FHIR R5 integration
- HL7 v3 messaging
- ICH M5 eCTD alignment
```

## How to Download IDMP Components

### Option 1: EDQM Standard Terms (Recommended Start)
```bash
# Download EDQM RDF
curl -o edqm_terms.rdf \
  https://standardterms.edqm.eu/standardterms/api/v1/lists/rdf

# Import to your ontology
rapper -i rdfxml -o turtle edqm_terms.rdf > edqm_terms.ttl

# Add to combination
python3 scripts/etl/combine_ttls.py \
  --files cmc_stagegate_base.ttl \
          edqm_terms.ttl \
  --out cmc_with_edqm.ttl
```

### Option 2: EMA SPOR (Substances)
```bash
# EMA Substance Management
# https://spor.ema.europa.eu/rmswi/#/
# Requires registration
```

### Option 3: FDA Substance Registration
```bash
# FDA UNII/SRS
# https://precision.fda.gov/uniisearch
# Download JSON/XML, convert to RDF
```

### Option 4: Full ISO IDMP (Complex)
```bash
# Purchase from ISO or get from:
# - Your regulatory affairs team
# - Industry consortium (PhUSE, CDISC)
# - Vendor solutions (Veeva, IQVIA)
```

## Integration Complexity

### Current System (Simple) ✅
```
Your Ontology (300 classes)
     ↓
Basic IDMP refs (10 properties)
     ↓
Works great!
```

### With Full IDMP (Complex) ⚠️
```
Your Ontology (300 classes)
     +
Full IDMP (5,000+ classes)
     +
EDQM (2,000+ terms)
     +  
FHIR R5 (1,000+ resources)
     =
Complex, slow, hard to maintain
```

## Recommendation

### For Now: ✅ **USE CURRENT SYSTEM**
- You have core IDMP identifiers
- Can reference external vocabularies
- Sufficient for development tracking
- Fast and maintainable

### Next Quarter: 📅 **ADD EDQM TERMS**
- Download standard terms only
- Map to your dose forms
- Enhance regulatory readiness

### When Needed: 🎯 **ADD SPECIFIC MODULES**
- Don't download everything
- Pick what you actually use
- Keep it manageable

## Decision Matrix

| Your Need | Current System | + EDQM | + Full IDMP |
|-----------|---------------|---------|-------------|
| Track drugs through stages | ✅ Perfect | ✅ | ✅ |
| Basic regulatory IDs | ✅ Perfect | ✅ | ✅ |
| Dose form codes | ✅ Basic | ✅ Perfect | ✅ |
| FDA IND/NDA submission | ✅ Good | ✅ Better | ✅ Perfect |
| EMA MAA submission | ⚠️ Basic | ✅ Good | ✅ Perfect |
| WHO compliance | ❌ | ⚠️ Partial | ✅ Perfect |
| Query performance | ✅ Fast | ✅ Fast | ⚠️ Slow |
| Maintenance effort | ✅ Easy | ✅ Moderate | ❌ Complex |

## Final Answer

**No, don't download full IDMP yet.** 

1. **Use current system** for 3-6 months
2. **Add EDQM terms** when you need dose form codes
3. **Consider full IDMP** only when regulatory requires it
4. **Keep it simple** until complexity is justified

Your current setup with basic IDMP references is the sweet spot! 🎯
