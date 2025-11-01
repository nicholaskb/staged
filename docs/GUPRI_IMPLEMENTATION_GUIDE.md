# GUPRI Implementation Guide for CMC Stage-Gate Ontology

## What are GUPRIs?

**GUPRI** = **G**lobally **U**nique, **P**ersistent, **R**esolvable **I**dentifiers

GUPRIs are a fundamental best practice in semantic web and linked data, ensuring that every resource has an identifier that is:
- **Globally Unique**: No two resources share the same identifier anywhere
- **Persistent**: The identifier remains stable over time, even if data changes
- **Resolvable**: The identifier can be dereferenced to retrieve information about the resource

## Current Implementation Issues

### Current Pattern (Non-GUPRI Compliant)
```python
# Simple string manipulation
stream_id = safe_id(value_stream)  # "CGT" → "cgt"
stage_id = safe_id(stage_num)      # "Stage 0" → "stage-0"
stage_iri = f"ex:Stage-{stream_id}-{stage_id}"  # ex:Stage-cgt-stage-0
```

### Problems
1. **Not Globally Unique**: Different datasets might generate same IDs
2. **Not Persistent**: If source text changes, ID changes
3. **Not Stable**: Minor text variations create different IDs
4. **Case Sensitivity Lost**: Information loss in conversion

## GUPRI Best Practices

### 1. Use Persistent URL Services
```turtle
# Good - Uses w3id.org persistent URL service
@prefix ex: <https://w3id.org/cmc-stagegate#> .

# Better - Include version/context in namespace
@prefix cmc: <https://w3id.org/cmc-stagegate/2024/> .
```

### 2. Include Stable Identifiers
```python
# Use UUIDs for true uniqueness
import uuid

def generate_gupri(entity_type: str, source_data: dict) -> str:
    # Create deterministic UUID from source data
    namespace_uuid = uuid.UUID('6ba7b810-9dad-11d1-80b4-00c04fd430c8')
    
    # Create stable seed from essential properties
    seed = f"{entity_type}:{source_data.get('stream')}:{source_data.get('stage')}"
    entity_uuid = uuid.uuid5(namespace_uuid, seed)
    
    return f"ex:{entity_type}_{entity_uuid}"
```

### 3. Maintain ID Mappings
```python
# Store mappings for consistency
ID_MAPPINGS = {}  # Should be persisted

def get_or_create_gupri(entity_type: str, natural_key: str) -> str:
    mapping_key = f"{entity_type}:{natural_key}"
    
    if mapping_key not in ID_MAPPINGS:
        # Generate new GUPRI
        ID_MAPPINGS[mapping_key] = generate_gupri(entity_type, natural_key)
    
    return ID_MAPPINGS[mapping_key]
```

## Recommended Implementation

### Option 1: Deterministic UUIDs (Recommended)
```python
import uuid
import hashlib

def create_gupri(entity_type: str, *key_components) -> str:
    """
    Create a GUPRI using deterministic UUID v5.
    
    Args:
        entity_type: Type of entity (Stage, QualityAttribute, SME, etc.)
        key_components: Unique identifying components
    
    Returns:
        GUPRI in format ex:EntityType_UUID
    """
    # CMC Stage-Gate namespace UUID (generate once, reuse)
    NAMESPACE_UUID = uuid.UUID('a7c6f3e0-8b5d-4e2a-9f1c-3d7e5a9b2c4e')
    
    # Create deterministic seed
    seed = ":".join(str(c) for c in [entity_type] + list(key_components))
    
    # Generate UUID v5 (deterministic from namespace + seed)
    entity_uuid = uuid.uuid5(NAMESPACE_UUID, seed)
    
    # Return formatted GUPRI
    return f"ex:{entity_type}_{str(entity_uuid)}"

# Usage examples:
stage_gupri = create_gupri("Stage", "CGT", "0")
# → ex:Stage_f47ac10b-58cc-4372-a567-0e02b2c3479

deliverable_gupri = create_gupri("QualityAttribute", "CGT", "0", "Process Validation")
# → ex:QualityAttribute_6ba7b810-9dad-11d1-80b4-00c04fd430c8
```

### Option 2: Hierarchical Identifiers
```python
def create_hierarchical_gupri(entity_type: str, hierarchy: list, name: str) -> str:
    """
    Create hierarchical GUPRI preserving structure.
    
    Args:
        entity_type: Type of entity
        hierarchy: List of hierarchical components
        name: Entity name
    
    Returns:
        Hierarchical GUPRI
    """
    # Clean components
    clean_hierarchy = [safe_id(h) for h in hierarchy]
    clean_name = safe_id(name)
    
    # Create short hash for uniqueness
    hash_input = f"{entity_type}:{':'.join(hierarchy)}:{name}"
    short_hash = hashlib.sha256(hash_input.encode()).hexdigest()[:8]
    
    # Build hierarchical IRI
    path = "/".join(clean_hierarchy)
    return f"ex:{entity_type}/{path}/{clean_name}_{short_hash}"

# Usage:
stage_gupri = create_hierarchical_gupri("Stage", ["CGT"], "Stage-0")
# → ex:Stage/cgt/stage-0_a3f5c789

deliverable_gupri = create_hierarchical_gupri(
    "QualityAttribute", 
    ["CGT", "Stage-0"], 
    "Process Validation"
)
# → ex:QualityAttribute/cgt/stage-0/process-validation_b4d6e890
```

### Option 3: Mixed Approach (Human-Readable + Unique)
```python
def create_mixed_gupri(entity_type: str, readable_part: str, unique_keys: list) -> str:
    """
    Create GUPRI with human-readable component and unique suffix.
    """
    # Clean readable part
    clean_readable = safe_id(readable_part)[:30]  # Limit length
    
    # Create unique suffix from keys
    hash_input = ":".join(str(k) for k in unique_keys)
    unique_suffix = hashlib.sha256(hash_input.encode()).hexdigest()[:12]
    
    return f"ex:{entity_type}_{clean_readable}_{unique_suffix}"

# Usage:
stage_gupri = create_mixed_gupri("Stage", "cgt-entry-ed", ["CGT", "0"])
# → ex:Stage_cgt-entry-ed_a3f5c7890b4d
```

## Implementation Steps

### 1. Update generate_cmc_ttl.py

```python
# Add at top of file
import uuid
import json
from pathlib import Path

# CMC namespace UUID (consistent across all runs)
CMC_NAMESPACE_UUID = uuid.UUID('a7c6f3e0-8b5d-4e2a-9f1c-3d7e5a9b2c4e')

# ID mapping cache
ID_MAPPING_FILE = Path("output/current/id_mappings.json")
ID_MAPPINGS = {}

def load_id_mappings():
    """Load existing ID mappings."""
    global ID_MAPPINGS
    if ID_MAPPING_FILE.exists():
        with open(ID_MAPPING_FILE) as f:
            ID_MAPPINGS = json.load(f)

def save_id_mappings():
    """Save ID mappings for persistence."""
    ID_MAPPING_FILE.parent.mkdir(parents=True, exist_ok=True)
    with open(ID_MAPPING_FILE, 'w') as f:
        json.dump(ID_MAPPINGS, f, indent=2)

def create_gupri(entity_type: str, *key_components) -> str:
    """Create or retrieve GUPRI for entity."""
    # Create cache key
    cache_key = f"{entity_type}:{':'.join(str(k) for k in key_components)}"
    
    # Return existing if available
    if cache_key in ID_MAPPINGS:
        return ID_MAPPINGS[cache_key]
    
    # Generate new GUPRI
    seed = cache_key
    entity_uuid = uuid.uuid5(CMC_NAMESPACE_UUID, seed)
    gupri = f"ex:{entity_type}_{str(entity_uuid)}"
    
    # Cache for consistency
    ID_MAPPINGS[cache_key] = gupri
    
    return gupri
```

### 2. Update URI Generation

Replace current pattern:
```python
# OLD
stage_iri = f"ex:Stage-{stream_id}-{stage_id}"

# NEW
stage_iri = create_gupri("Stage", value_stream, stage_num)
```

### 3. Benefits of GUPRI Implementation

1. **Data Integration**: Same entities across different sources get same IDs
2. **Version Stability**: IDs persist across data updates
3. **Linkability**: External systems can reliably reference our entities
4. **Traceability**: Can track entity provenance through ID
5. **FAIR Compliance**: Supports Findable, Accessible, Interoperable, Reusable data principles

## Testing GUPRI Implementation

```python
def test_gupri_properties():
    """Test that GUPRIs meet requirements."""
    
    # Test: Globally Unique
    id1 = create_gupri("Stage", "CGT", "0")
    id2 = create_gupri("Stage", "Protein", "0")
    assert id1 != id2, "Different entities must have different IDs"
    
    # Test: Persistent
    id3 = create_gupri("Stage", "CGT", "0")
    id4 = create_gupri("Stage", "CGT", "0")
    assert id3 == id4, "Same entity must always get same ID"
    
    # Test: Deterministic
    id5 = create_gupri("Stage", "CGT", "Stage 0")
    id6 = create_gupri("Stage", "CGT", "Stage 0")
    assert id5 == id6, "ID generation must be deterministic"
```

## Migration Strategy

1. **Phase 1**: Add GUPRI generation alongside current IDs
2. **Phase 2**: Add `owl:sameAs` links between old and new IDs
3. **Phase 3**: Transition to GUPRIs as primary identifiers
4. **Phase 4**: Deprecate old ID patterns

## References

- [Cool URIs for the Semantic Web](https://www.w3.org/TR/cooluris/)
- [Best Practices for Publishing Linked Data](https://www.w3.org/TR/ld-bp/)
- [Persistent Identifiers](https://w3id.org/)
- [FAIR Data Principles](https://www.go-fair.org/fair-principles/)
