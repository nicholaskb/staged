# Protege Loading Guide for CMC Stage-Gate Ontology

**Date:** October 31, 2025  
**Purpose:** Guide for loading TTL files into Protege for ontology visualization

## Quick Start Recommendations

### 🎯 **Option 1: Ontology Structure Only (Recommended for First-Time Viewing)**
**Load these 2 files** for clean ontology structure:

```
1. cmc_stagegate_base.ttl          (6.5 KB)  ← Core classes & properties
2. cmc_stagegate_gist_align.ttl    (7.6 KB)  ← GIST alignments
```

**What you'll see:**
- All 11 core classes (Stage, StageGate, Material, etc.)
- All 29 properties (hasPlan, hasGate, etc.)
- GIST alignment mappings
- Class hierarchies and property domains/ranges

**Loading time:** ~2-3 seconds  
**Best for:** Understanding ontology structure, browsing classes/properties

---

### 🎯 **Option 2: Structure + Examples (Recommended for Learning)**
**Load these 3 files** to see concrete examples:

```
1. cmc_stagegate_base.ttl          (6.5 KB)
2. cmc_stagegate_gist_align.ttl    (7.6 KB)
3. cmc_stagegate_gist_examples.ttl (12 KB)  ← Concrete examples
```

**What you'll see:**
- Everything from Option 1, PLUS:
- Example instances (PPQ Stage, Lot 000123, etc.)
- Complete patterns (Stage→Gate→Evidence)
- Material flow examples
- Measurement examples with QUDT

**Loading time:** ~3-5 seconds  
**Best for:** Learning ontology patterns, seeing real-world usage

---

### 🎯 **Option 3: Full Data (For Data Analysis)**
**Load the combined file** for all instances:

```
output/current/cmc_stagegate_all.ttl  (711 KB)  ← Complete dataset
```

**What you'll see:**
- Everything from Option 2, PLUS:
- 26 actual Stages (13 CGT, 13 Protein)
- 2,205 Deliverables (QualityAttributes)
- All relationships from your Excel data
- Categories, dates, references

**Loading time:** ~30-60 seconds (may be slow)  
**Best for:** Analyzing your actual data, SPARQL queries on instances

**⚠️ Warning:** This file is large (7,483 triples). Protege may be slow when navigating instances.

---

## Step-by-Step Loading Instructions

### Method 1: Load Individual Files (Recommended)

1. **Open Protege**
2. **File → Open** (or drag-and-drop)
3. **Select files in this order:**
   - First: `cmc_stagegate_base.ttl`
   - Then: `cmc_stagegate_gist_align.ttl`
   - Optionally: `cmc_stagegate_gist_examples.ttl`
4. **Protege will ask:** "Merge with existing ontology?" → **Yes**

### Method 2: Load Combined File

1. **Open Protege**
2. **File → Open**
3. **Select:** `output/current/cmc_stagegate_all.ttl`
4. **Wait for loading** (may take 30-60 seconds)

---

## What to Explore in Protege

### Classes Tab
- **ex:Stage** - Development phases
- **ex:StageGate** - Review points
- **ex:QualityAttribute** - Deliverables/CQAs
- **ex:Material** - Drug substances/products
- **ex:Lot** - Batches
- **ex:Process** - Manufacturing processes

### Object Properties Tab
- **ex:hasPlan** - Stage → Plan
- **ex:hasGate** - Stage → Gate
- **ex:hasCQA** - Specification → QualityAttribute
- **ex:hasEvidence** - Specification → Result
- **ex:assessedAtGate** - Result → Gate

### Data Properties Tab
- **ex:plannedDate** - NEW: Planned dates
- **ex:actualDate** - NEW: Actual dates
- **ex:hasCategory** - NEW: Category classification
- **ex:reference** - NEW: Document references
- **ex:decision** - Gate outcomes

### Individuals Tab (if loading examples/all.ttl)
- Browse actual stages, deliverables, and relationships
- Use SPARQL queries to explore data

---

## SPARQL Query Examples (in Protege)

### Find all QualityAttributes with categories:
```sparql
SELECT ?qa ?category WHERE {
  ?qa a ex:QualityAttribute ;
      ex:hasCategory ?category .
}
LIMIT 20
```

### Find stages and their gates:
```sparql
SELECT ?stage ?gate WHERE {
  ?stage a ex:Stage ;
         ex:hasGate ?gate .
}
```

### Count deliverables by category:
```sparql
SELECT ?category (COUNT(?qa) as ?count) WHERE {
  ?qa a ex:QualityAttribute ;
      ex:hasCategory ?category .
}
GROUP BY ?category
ORDER BY DESC(?count)
```

---

## Troubleshooting

### Issue: Protege is slow
- **Solution:** Load only `base.ttl` + `gist_align.ttl` first
- Avoid loading large instance files unless needed

### Issue: Prefixes not resolving
- **Solution:** Ensure all 3 base files are loaded
- Check **Active Ontology → Ontology prefixes** in Protege

### Issue: GIST classes not showing
- **Solution:** GIST is external - Protege may need internet connection
- Or download GIST ontology separately and import

### Issue: "File not found" errors
- **Solution:** Use absolute paths or ensure files are in correct directories
- Check file paths match the guide above

---

## File Dependencies

**Loading order matters!** Load in this sequence:

1. **cmc_stagegate_base.ttl** (foundation)
2. **cmc_stagegate_gist_align.ttl** (adds alignments)
3. **cmc_stagegate_gist_examples.ttl** (adds examples)
4. **cmc_stagegate_all.ttl** (adds all data) - optional

---

## Quick Reference

| File | Size | Purpose | Load Time |
|------|------|---------|-----------|
| `cmc_stagegate_base.ttl` | 6.5 KB | Core ontology | 2 sec |
| `cmc_stagegate_gist_align.ttl` | 7.6 KB | GIST mappings | 2 sec |
| `cmc_stagegate_gist_examples.ttl` | 12 KB | Examples | 3 sec |
| `cmc_stagegate_all.ttl` | 711 KB | Full dataset | 30-60 sec |

**Recommended:** Start with Option 1 (base + align), then add examples if needed!
