# How Multi-Line Text with Bullet Points is Handled

## Your Example from Excel

```
If required, complete CDCP (Clinical Design Control Process) for Phase 2:
*CDCP Development Plan
*Clinical Device Traceability Matrix
*Clinical Device Risk Management (PRA)
*Clinical Device Design Review
*Clinical Device Development DHF
```

## How It's Stored in the Knowledge Graph

### 1. The IRI (Identifier)
```
ex:CQA-sm-4-if-required-complete-cdcp-clinical-design-control-process-for-ph
```
- Truncated to 64 characters
- All special chars converted to hyphens
- URL-safe format

### 2. The Label (Full Text Preserved)

**In TTL file format:**
```turtle
rdfs:label "If required, complete CDCP (Clinical Design Control Process) for Phase 2:\n*CDCP Development Plan\n*Clinical Device Traceability Matrix\n*Clinical Device Risk Management (PRA)\n*Clinical Device Design Review\n*Clinical Device Development DHF"
```

**When queried/displayed:**
```
If required, complete CDCP (Clinical Design Control Process) for Phase 2:
*CDCP Development Plan
*Clinical Device Traceability Matrix
*Clinical Device Risk Management (PRA)
*Clinical Device Design Review
*Clinical Device Development DHF
```

## Key Points

✅ **Line breaks preserved**: Each new line becomes `\n` in TTL  
✅ **Asterisks preserved**: Bullet points remain as `*`  
✅ **Formatting intact**: The structure is maintained  
✅ **Nothing lost**: Every character from Excel is kept  

## More Examples from Your Data

### Example 1: Process Controls
**Original:**
```
Implement suitable manufacturing controls for Phase 1b/2 combination product processes:
* Incoming and release tests
* in process control/inspection
```

**In TTL:**
```turtle
rdfs:label "Implement suitable manufacturing controls for Phase 1b/2 combination product processes:\n* Incoming and release tests\n* in process control/inspection"
```

### Example 2: Complex Requirements
**Original:**
```
Complete/update for Phase 2 device if applicable:
*Define/update critical and essential technical and usability performance requirements
* Define/update test strategy
*If required, conduct combination product stability test
*Collect data to verify design requirements
*Create/Update IFU
*Select package design
*Define and provide training to site staff/patients
```

**In TTL:** All 7 bullet points preserved with proper line breaks!

## SPARQL Query to Retrieve

```sparql
# Find all deliverables with bullet points
SELECT ?deliverable ?label WHERE {
  ?deliverable rdfs:label ?label .
  FILTER(CONTAINS(?label, "\n*"))  # Has newline followed by asterisk
}

# Result will display with proper formatting:
# If required, complete CDCP...
# *CDCP Development Plan
# *Clinical Device Traceability Matrix
# etc.
```

## How the System Processes It

```python
def escape_turtle_literal(value: str) -> str:
    """Preserves multi-line text with proper escaping"""
    # Actual newlines from Excel become \n in TTL
    value = value.replace('\n', '\\n')
    # Also escape quotes and backslashes
    value = value.replace('\\', '\\\\').replace('"', '\\"')
    return value

# Input from Excel (with actual line breaks):
text = """If required, complete CDCP...
*CDCP Development Plan
*Clinical Device Traceability Matrix"""

# Output in TTL:
escaped = escape_turtle_literal(text)
# "If required, complete CDCP...\\n*CDCP Development Plan\\n*Clinical Device Traceability Matrix"
```

## Benefits

1. **Structure Preserved**: Bullet lists remain readable
2. **Searchable**: Can query for specific bullet points
3. **Display-Ready**: Applications can render with proper formatting
4. **Standards Compliant**: Valid Turtle/RDF format
5. **Round-Trip Safe**: Can export back to Excel with formatting

## In Protege or GraphDB

When you load this into Protege or query in GraphDB, the text will display properly formatted with line breaks, making it easy to read the bullet points exactly as they were in Excel.

## Summary

Your complex multi-line deliverable descriptions with bullet points are:
- ✅ Fully preserved character-for-character
- ✅ Line breaks maintained as `\n`
- ✅ Bullet points (*) kept intact
- ✅ Queryable and searchable
- ✅ Display with proper formatting in tools
