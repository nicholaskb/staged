# How Complex Text Values are Handled

## Overview

The system robustly handles all types of complex text including:
- Special characters: `()[]{}/<>&`
- Long descriptions (multiple sentences)
- Line breaks and formatting
- Special notations like `[P&MS] M3.`
- Scientific terminology and abbreviations

## Two-Part Strategy

### 1. IRI Generation (Identifier)

For the unique identifier (`ex:CQA-...`), the system:
- Converts to lowercase
- Replaces all non-alphanumeric characters with hyphens
- Truncates to 64 characters to ensure valid URIs
- Creates a URL-safe identifier

**Example:**
```
Input: "API form (salt/polymorph) locked for late development..."
IRI:   ex:CQA-sm-4-api-form-salt-polymorph-locked-for-late-development-except-for-a
```

### 2. Label Preservation (Full Text)

For the `rdfs:label`, the system:
- Preserves the COMPLETE original text
- Properly escapes special characters for Turtle format:
  - `"` becomes `\"`
  - `\` becomes `\\`
  - Newlines become `\n`
- Maintains all formatting, brackets, parentheses

**Example:**
```turtle
rdfs:label "API form (salt/polymorph) locked for late development (except for ASD formulations) based on continuous efforts to understand the polymorphic landscape . API form selection report needs to be updated to document final form selection and endorsed by Solid State Expert Team even when no form switch is required.  [P&MS] M3."
```

## Real Examples from Your Data

### Example 1: Complex Scientific Text
```
Original Excel:
"API form (salt/polymorph) locked for late development (except for ASD formulations)..."

In Knowledge Graph:
ex:CQA-sm-4-api-form-salt-polymorph-locked... 
    a ex:QualityAttribute ;
    rdfs:label "[FULL TEXT PRESERVED]" ;
    ex:hasCategory "Product Design & Knowledge" .
```

### Example 2: Text with Special Characters
```
Original: "TPP draft [DRAFT] v1.0 (2025)"
IRI: ex:CQA-cgt-0-tpp-draft-draft-v1-0-2025
Label: "TPP draft [DRAFT] v1.0 (2025)"  ← Exact preservation
```

### Example 3: Multi-line Text
```
Original: "Deliverable description
Line 2 of description
Line 3 with details"

IRI: ex:CQA-...-deliverable-description-line-2-of-description-line-3...
Label: "Deliverable description\nLine 2 of description\nLine 3 with details"
```

## Character Handling Reference

| Character Type | In IRI | In Label | Example |
|---------------|---------|-----------|---------|
| Parentheses `()` | Converted to `-` | Preserved | (salt/polymorph) |
| Brackets `[]` | Converted to `-` | Preserved | [P&MS] |
| Slash `/` | Converted to `-` | Preserved | salt/polymorph |
| Ampersand `&` | Converted to `-` | Preserved | P&MS |
| Spaces | Converted to `-` | Preserved | API form |
| Periods `.` | Converted to `-` | Preserved | M3. |
| Quotes `"` | Converted to `-` | Escaped as `\"` | "quoted text" |
| Numbers | Preserved | Preserved | M3, v1.0, 2025 |

## Length Limits

- **IRI**: Maximum 64 characters (after conversion)
- **Label**: NO LIMIT - full text preserved
- **Comments**: NO LIMIT - full text preserved
- **Category**: NO LIMIT - full text preserved

## Special Cases

### Case 1: Empty or Missing Values
```python
if not deliverable:
    # Skipped - no triple generated
```

### Case 2: Only Special Characters
```
Input: "!!!/???"
IRI: ex:CQA-cgt-0-unnamed  # Falls back to "unnamed"
Label: "!!!/???"  # Still preserved
```

### Case 3: Unicode/International Characters
```
Input: "Étude clinique (Phase 3) - 試験"
IRI: ex:CQA-...-tude-clinique-phase-3  # ASCII only
Label: "Étude clinique (Phase 3) - 試験"  # Unicode preserved
```

## Implementation Code

```python
def safe_id(text: str) -> str:
    """Create URL-safe identifier"""
    text = text.strip().lower()
    text = re.sub(r"[^a-z0-9]+", "-", text)
    text = text.strip("-")
    return text or "unnamed"

def escape_turtle_literal(value: str) -> str:
    """Escape special characters for Turtle format"""
    value = value.replace('\\', '\\\\').replace('"', '\\"')
    value = value.replace('\r', '\\n').replace('\n', '\\n')
    value = value.replace('\t', '\\t')
    return value

# Usage:
deliv_id = safe_id(deliverable)[:64]  # Truncate for IRI
qa_iri = f"ex:CQA-{stream_id}-{stage_id}-{deliv_id}"
label = escape_turtle_literal(deliverable)  # Full text
```

## Benefits of This Approach

1. **No Data Loss**: Every character from Excel is preserved
2. **Valid URIs**: IRIs are always valid for RDF/OWL
3. **Queryable**: Can search by partial IRI or full text
4. **Human Readable**: Labels maintain original formatting
5. **Standards Compliant**: Follows W3C Turtle specification

## SPARQL Query Examples

### Find by Partial Text
```sparql
SELECT ?deliverable ?label WHERE {
  ?deliverable rdfs:label ?label .
  FILTER(CONTAINS(?label, "[P&MS]"))
}
```

### Find by Category and Text Pattern
```sparql
SELECT ?deliverable WHERE {
  ?deliverable rdfs:label ?label ;
               ex:hasCategory "Product Design & Knowledge" .
  FILTER(REGEX(?label, "salt.*polymorph"))
}
```

## Summary

Your complex deliverable descriptions are handled perfectly:
- ✅ Full text preserved in labels
- ✅ Special characters properly escaped
- ✅ Safe IRIs generated for system use
- ✅ No length restrictions on content
- ✅ Searchable and queryable
- ✅ Standards compliant
