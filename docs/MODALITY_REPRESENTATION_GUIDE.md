# Modality Representation in CMC Stage-Gate Ontology

## Current State
Currently, modalities are implicitly represented through:
- Stage naming conventions (e.g., `Stage-protein-0`, `Stage-cgt-0`)
- ValueStream references (not fully defined)
- SME assignments per modality

## Recommended Approach: Modality as First-Class Concept

### Option 1: Simple Modality Class (Recommended)

Add this to `cmc_stagegate_base.ttl`:

```turtle
#################################################################
#    Modality Classes and Properties
#################################################################

###  https://w3id.org/cmc-stagegate#Modality
ex:Modality rdf:type owl:Class ;
            rdfs:subClassOf gist:Category ;
            rdfs:label "Therapeutic Modality" ;
            rdfs:comment "A category of therapeutic approach based on the molecular/biological nature of the drug" .

###  https://w3id.org/cmc-stagegate#hasModality
ex:hasModality rdf:type owl:ObjectProperty ;
               rdfs:domain ex:DrugProduct ;
               rdfs:range ex:Modality ;
               rdfs:comment "Links a drug product to its therapeutic modality" .

###  https://w3id.org/cmc-stagegate#modalityType
ex:modalityType rdf:type owl:DatatypeProperty ;
                rdfs:domain ex:Modality ;
                rdfs:range xsd:string ;
                rdfs:comment "The type of modality (e.g., Small Molecule, Protein, Cell Therapy)" .

###  https://w3id.org/cmc-stagegate#hasStagePathway
ex:hasStagePathway rdf:type owl:ObjectProperty ;
                   rdfs:domain ex:Modality ;
                   rdfs:range ex:Stage ;
                   rdfs:comment "Links modality to its specific stage-gate pathway" .
```

### Define Modality Instances

Create `cmc_stagegate_modalities.ttl`:

```turtle
@prefix ex: <https://w3id.org/cmc-stagegate#> .
@prefix rdfs: <http://www.w3.org/2000/01/rdf-schema#> .
@prefix idmp: <http://www.iso.org/idmp#> .

#################################################################
#    Core Modality Instances
#################################################################

ex:Modality-SmallMolecule a ex:Modality ;
    rdfs:label "Small Molecule" ;
    ex:modalityType "Small Molecule" ;
    idmp:substanceType "Chemical" ;
    ex:hasStagePathway ex:Stage-sm-0, ex:Stage-sm-1, ex:Stage-sm-2 ;
    rdfs:comment "Traditional synthetic chemical compounds <1000 Da" .

ex:Modality-Protein a ex:Modality ;
    rdfs:label "Protein Therapeutic" ;
    ex:modalityType "Protein" ;
    idmp:substanceType "Protein/Peptide" ;
    ex:hasStagePathway ex:Stage-protein-0, ex:Stage-protein-1, ex:Stage-protein-2 ;
    rdfs:comment "Recombinant proteins including antibodies, enzymes, cytokines" .

ex:Modality-CellTherapy a ex:Modality ;
    rdfs:label "Cell Therapy" ;
    ex:modalityType "Cell Therapy" ;
    idmp:substanceType "Structurally Diverse" ;
    ex:hasStagePathway ex:Stage-cgt-0, ex:Stage-cgt-1, ex:Stage-cgt-2 ;
    rdfs:comment "Live cell-based therapeutics including CAR-T, stem cells" .

ex:Modality-GeneTherapy a ex:Modality ;
    rdfs:label "Gene Therapy" ;
    ex:modalityType "Gene Therapy" ;
    idmp:substanceType "Nucleic Acid" ;
    ex:hasStagePathway ex:Stage-cgt-0, ex:Stage-cgt-1, ex:Stage-cgt-2 ;
    rdfs:comment "Gene modification therapies using viral or non-viral vectors" .

ex:Modality-mRNA a ex:Modality ;
    rdfs:label "mRNA Therapy" ;
    ex:modalityType "mRNA" ;
    idmp:substanceType "Nucleic Acid" ;
    ex:hasStagePathway ex:Stage-rna-0, ex:Stage-rna-1, ex:Stage-rna-2 ;
    rdfs:comment "Messenger RNA therapeutics and vaccines" .

ex:Modality-ADC a ex:Modality ;
    rdfs:label "Antibody-Drug Conjugate" ;
    ex:modalityType "ADC" ;
    idmp:substanceType "Mixture" ;
    ex:hasStagePathway ex:Stage-adc-0, ex:Stage-adc-1, ex:Stage-adc-2 ;
    rdfs:comment "Antibodies conjugated with cytotoxic drugs" .

ex:Modality-Vaccine a ex:Modality ;
    rdfs:label "Vaccine" ;
    ex:modalityType "Vaccine" ;
    idmp:substanceType "Mixture" ;
    ex:hasStagePathway ex:Stage-vaccine-0, ex:Stage-vaccine-1, ex:Stage-vaccine-2 ;
    rdfs:comment "Preventive or therapeutic vaccines" .

ex:Modality-Oligonucleotide a ex:Modality ;
    rdfs:label "Oligonucleotide" ;
    ex:modalityType "Oligonucleotide" ;
    idmp:substanceType "Nucleic Acid" ;
    ex:hasStagePathway ex:Stage-oligo-0, ex:Stage-oligo-1, ex:Stage-oligo-2 ;
    rdfs:comment "ASO, siRNA, and other short nucleic acid therapeutics" .
```

### Option 2: Hierarchical Modality Taxonomy

For more sophisticated classification:

```turtle
# Base modality class
ex:Modality rdf:type owl:Class .

# Traditional modalities
ex:TraditionalModality rdfs:subClassOf ex:Modality .
ex:SmallMolecule rdfs:subClassOf ex:TraditionalModality .
ex:NaturalProduct rdfs:subClassOf ex:TraditionalModality .

# Biologics
ex:Biologic rdfs:subClassOf ex:Modality .
ex:ProteinTherapeutic rdfs:subClassOf ex:Biologic .
ex:MonoclonalAntibody rdfs:subClassOf ex:ProteinTherapeutic .
ex:Enzyme rdfs:subClassOf ex:ProteinTherapeutic .
ex:Cytokine rdfs:subClassOf ex:ProteinTherapeutic .

# Advanced Therapy Medicinal Products (ATMPs)
ex:ATMP rdfs:subClassOf ex:Modality .
ex:CellTherapy rdfs:subClassOf ex:ATMP .
ex:GeneTherapy rdfs:subClassOf ex:ATMP .
ex:TissueEngineering rdfs:subClassOf ex:ATMP .

# Nucleic acid therapies
ex:NucleicAcidTherapy rdfs:subClassOf ex:Modality .
ex:mRNATherapy rdfs:subClassOf ex:NucleicAcidTherapy .
ex:Oligonucleotide rdfs:subClassOf ex:NucleicAcidTherapy .

# Combination modalities
ex:CombinationModality rdfs:subClassOf ex:Modality .
ex:ADC rdfs:subClassOf ex:CombinationModality .
ex:BispecificAntibody rdfs:subClassOf ex:CombinationModality .
```

## Usage Examples

### Drug Product with Modality

```turtle
ex:Drug-ABC123 a ex:DrugProduct ;
    rdfs:label "ABC-123 CAR-T Therapy" ;
    ex:hasModality ex:Modality-CellTherapy ;
    ex:currentStage ex:Stage-cgt-3 ;
    
    # Modality-specific properties
    ex:cellType "Autologous T-cells" ;
    ex:targetAntigen "CD19" ;
    ex:vectorType "Lentiviral" ;
    
    # IDMP alignment
    idmp:substanceType "Structurally Diverse" ;
    idmp:hasDoseForm edqm:11210000 . # Suspension for infusion
```

### Query by Modality

```sparql
# Find all cell therapies in development
SELECT ?drug ?label ?stage WHERE {
    ?drug a ex:DrugProduct ;
          ex:hasModality ex:Modality-CellTherapy ;
          rdfs:label ?label ;
          ex:currentStage ?stage .
}

# Count drugs by modality
SELECT ?modality (COUNT(?drug) as ?count) WHERE {
    ?drug a ex:DrugProduct ;
          ex:hasModality ?modality .
    ?modality rdfs:label ?modalityLabel .
}
GROUP BY ?modality
```

### Modality-Specific Stage Gates

```turtle
ex:Stage-cgt-3 ex:applicableToModality ex:Modality-CellTherapy ;
               ex:hasModalitySpecificRequirements [
                   ex:requiresVectorTesting true ;
                   ex:requiresCellViability true ;
                   ex:requiresPotencyAssay true
               ] .

ex:Stage-protein-3 ex:applicableToModality ex:Modality-Protein ;
                   ex:hasModalitySpecificRequirements [
                       ex:requiresAggregationStudy true ;
                       ex:requiresGlycosylation true ;
                       ex:requiresImmunogenicity true
                   ] .
```

## Benefits of This Approach

1. **Clear Classification**: Modalities are explicit, not inferred from stage names
2. **IDMP Alignment**: Maps directly to ISO 11238 substance types
3. **Query Flexibility**: Easy to query portfolio by modality
4. **Extensibility**: New modalities can be added without changing schema
5. **Regulatory Compliance**: Aligns with FDA/EMA modality classifications
6. **Analytics**: Enable modality-based reporting and dashboards

## Implementation Steps

1. Add Modality class to `cmc_stagegate_base.ttl`
2. Create modality instances file
3. Update drug product instances to include `ex:hasModality`
4. Link stages to applicable modalities
5. Update SPARQL queries to leverage modality concept
6. Document modality-specific business rules

## Modality-Specific Properties Reference

| Modality | Key Properties | IDMP Type |
|----------|---------------|-----------|
| Small Molecule | MW, LogP, PSA | Chemical |
| Protein | MW, pI, Glycosylation | Protein/Peptide |
| mAb | CDR sequences, Isotype | Protein/Peptide |
| Cell Therapy | Cell type, Viability, Dose | Structurally Diverse |
| Gene Therapy | Vector, Transgene, Titer | Nucleic Acid |
| mRNA | Sequence, Modifications, LNP | Nucleic Acid |
| ADC | DAR, Linker, Payload | Mixture |
