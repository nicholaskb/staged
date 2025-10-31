# MindMap to Ontology Integration Proposal

## Overview
Integrate the MindMap HTML visualization (LM SGates Mmap Updates Q3 2023) into the CMC Stage-Gate ontology to create specific nodes for modality-specific stage gates (e.g., "Protein Stage Gate", "CGT Stage Gate").

## Current Situation

### What We Have:
1. **MindMap File**: `LM SGates Mmap Updates Q3 2023 Import All SG Fx (3).html`
   - Visual hierarchy of stage gates
   - Interactive navigation structure
   - Embedded .mmap data (base64 encoded)

2. **Current Ontology**:
   - `ex:Stage` - Generic stage class
   - `ex:StageGate` - Generic gate review class
   - `ex:modality` property - For Protein/CGT distinction
   - SME and FunctionalArea classes (planned)

### What's Missing:
- Modality-specific stage gate instances
- Hierarchical structure from MindMap
- Visual navigation linkages

## Proposed Solution

### 1. New Classes for Modality-Specific Gates

```turtle
# Modality-specific Stage Gate classes
ex:ModalityStageGate  a rdfs:Class ;
    rdfs:subClassOf ex:StageGate ;
    rdfs:label "Modality-Specific Stage Gate" ;
    rdfs:comment "A stage gate specific to a particular modality (Protein or CGT)" .

ex:ProteinStageGate  a rdfs:Class ;
    rdfs:subClassOf ex:ModalityStageGate ;
    rdfs:label "Protein Stage Gate" ;
    rdfs:comment "Stage gate specific to Protein modality development" .

ex:CGTStageGate  a rdfs:Class ;
    rdfs:subClassOf ex:ModalityStageGate ;
    rdfs:label "CGT Stage Gate" ;
    rdfs:comment "Stage gate specific to Cell and Gene Therapy modality" .

# Visual Structure Support
ex:MindMapNode  a rdfs:Class ;
    rdfs:subClassOf gist:Content ;
    rdfs:label "MindMap Node" ;
    rdfs:comment "A node in the visual MindMap hierarchy" .

ex:MindMapStructure  a rdfs:Class ;
    rdfs:subClassOf gist:Collection ;
    rdfs:label "MindMap Structure" ;
    rdfs:comment "The complete MindMap visualization structure" .
```

### 2. New Properties for Hierarchical Structure

```turtle
# Hierarchical navigation properties
ex:hasParentNode  a rdf:Property ;
    rdfs:domain ex:MindMapNode ;
    rdfs:range ex:MindMapNode ;
    rdfs:comment "Links to parent node in MindMap hierarchy" .

ex:hasChildNode  a rdf:Property ;
    rdfs:domain ex:MindMapNode ;
    rdfs:range ex:MindMapNode ;
    rdfs:comment "Links to child nodes in MindMap hierarchy" .

ex:representsStageGate  a rdf:Property ;
    rdfs:domain ex:MindMapNode ;
    rdfs:range ex:StageGate ;
    rdfs:comment "Links MindMap node to the stage gate it represents" .

ex:nodePosition  a rdf:Property ;
    rdfs:domain ex:MindMapNode ;
    rdfs:range xsd:integer ;
    rdfs:comment "Position/order of node in parent's children" .

ex:nodeExpanded  a rdf:Property ;
    rdfs:domain ex:MindMapNode ;
    rdfs:range xsd:boolean ;
    rdfs:comment "Whether node is expanded in default view" .

ex:visualMetadata  a rdf:Property ;
    rdfs:domain ex:MindMapNode ;
    rdfs:range xsd:string ;
    rdfs:comment "JSON metadata for visual rendering (colors, icons, etc.)" .
```

### 3. Implementation Approach

#### Step 1: Extract MindMap Data
Create a Python script to:
```python
# scripts/etl/extract_mindmap_data.py
import base64
import json
import xml.etree.ElementTree as ET
from bs4 import BeautifulSoup

def extract_mindmap_structure(html_file):
    """Extract hierarchical structure from MindMap HTML"""
    # 1. Parse HTML and extract base64 mmap data
    # 2. Decode and parse the .mmap XML structure
    # 3. Build hierarchical node structure
    # 4. Return as structured data
    
def map_to_ontology_nodes(mindmap_data):
    """Convert MindMap nodes to ontology instances"""
    # Create ex:MindMapNode instances
    # Link to existing stage gates
    # Preserve hierarchy with hasParentNode/hasChildNode
```

#### Step 2: Generate Ontology Instances

Example instances:
```turtle
# Protein-specific stage gates from MindMap
ex:protein_stage_0  a ex:ProteinStageGate ;
    rdfs:label "Stage 0 - Protein" ;
    ex:modality "Protein" ;
    ex:hasStage ex:stage_0 ;
    ex:hasMindMapNode ex:mm_node_protein_0 .

ex:mm_node_protein_0  a ex:MindMapNode ;
    rdfs:label "Stage 0 - Exploratory Development" ;
    ex:representsStageGate ex:protein_stage_0 ;
    ex:hasChildNode ex:mm_node_protein_0_1, ex:mm_node_protein_0_2 ;
    ex:nodePosition 1 ;
    ex:visualMetadata '''{"color": "#4053A0", "icon": "protein"}''' .

# CGT-specific stage gates
ex:cgt_stage_0  a ex:CGTStageGate ;
    rdfs:label "Stage 0 - CGT" ;
    ex:modality "CGT" ;
    ex:hasStage ex:stage_0 ;
    ex:hasMindMapNode ex:mm_node_cgt_0 .
```

### 4. Benefits of Integration

1. **Visual Navigation**: Preserve the intuitive MindMap structure in the ontology
2. **Modality Separation**: Clear distinction between Protein and CGT paths
3. **Stakeholder Alignment**: Use familiar visual structure from existing tools
4. **Query Capability**: SPARQL queries can traverse the hierarchy
5. **Visualization Ready**: Metadata preserved for rendering tools

### 5. Example SPARQL Queries

```sparql
# Find all Protein stage gates
SELECT ?gate ?label ?stage
WHERE {
  ?gate a ex:ProteinStageGate ;
        rdfs:label ?label ;
        ex:hasStage ?stage .
}

# Navigate MindMap hierarchy
SELECT ?parent ?child ?childLabel
WHERE {
  ?parent ex:hasChildNode ?child .
  ?child rdfs:label ?childLabel ;
         ex:representsStageGate/ex:modality "Protein" .
}

# Find visual structure for a specific stage
SELECT ?node ?metadata ?position
WHERE {
  ?node ex:representsStageGate ex:protein_stage_2 ;
        ex:visualMetadata ?metadata ;
        ex:nodePosition ?position .
}
```

### 6. Integration with Existing Data

The MindMap structure can be linked to existing data:
- Stage gates from SGD.csv
- Quality attributes from deliverables
- SME assignments from SME.csv
- Timelines and milestones

### 7. Next Steps

1. **Extract MindMap Data**: Parse the HTML file and decode the .mmap structure
2. **Create Mapping Script**: Map extracted nodes to ontology instances
3. **Generate TTL File**: Create `cmc_stagegate_mindmap.ttl`
4. **Update Pipeline**: Add MindMap extraction to `run_pipeline.sh`
5. **Validate Integration**: Test queries and relationships
6. **Document Usage**: Update README with MindMap integration examples

## Technical Implementation Notes

The .mmap file in the HTML is base64-encoded and appears to be a zipped XML structure. We'll need to:
1. Extract the base64 string from the HTML
2. Decode to binary
3. Unzip if necessary
4. Parse the XML structure
5. Build the hierarchical representation

This approach maintains the visual intuition while adding semantic richness to the ontology.
