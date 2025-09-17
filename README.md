# CMC Stage‑Gate Ontology and TTL Generator

This folder contains a minimal, reuse‑first ontology for stage‑gated CMC program management plus scripts to parse the provided Excel, generate TTL instances, and load them into GraphDB.

## Contents
- `cmc_stagegate_base.ttl`: Base ontology (application profile) using external vocabularies
  - Reuses: PROV‑O, P‑Plan, QUDT, GS1, and provides hooks for EDQM, UNII/GSRS, FHIR
  - Core classes: `ex:Stage`, `ex:StageGate`, `ex:StagePlan`, `ex:Process`, `ex:UnitOperation`, `ex:Material`, `ex:Lot`, `ex:Specification`, `ex:QualityAttribute` (CQA), `ex:AnalyticalMethod`, `ex:AnalyticalResult`
  - Core properties: `ex:hasPlan`, `ex:hasGate`, `ex:hasSpecification`, `ex:hasCQA`, `ex:evaluatedBy`, `ex:hasEvidence`
- `generate_cmc_ttl.py`: Parses the spreadsheet (via extracted CSV) and generates instances TTL
- `analyze_columns.py`: Column profiling (values, uniqueness, comma‑separated detection) with ontology mapping guidance
- `export_to_graphdb.py`: CLI uploader to a GraphDB repository (RDF4J API) with retries and env‑based config
- `extract_xlsx.py`: Helper to export all sheets from `/data/*.xlsx` to `/data/extracted/*.csv`

Data files
- Input workbook: `data/Protein and CGT_SGD Template Final_ENDORSED JAN 2023.xlsx`
- Extracted sheets (CSV): `data/extracted/Protein_and_CGT_SGD_Template_Final_ENDORSED_JAN_2023__*.csv`
- Generated instances: `cmc_stagegate_instances.ttl`

## Setup
Requirements
- Python 3.10+
- Optional (for Excel header preview): `pandas`, `openpyxl`

Install (optional)
```bash
pip install pandas openpyxl
```

## Generate TTL from Excel
1) Extract all sheets to CSV (optional if already extracted):
```bash
python3 extract_xlsx.py --input-dir /Users/nicholasbaro/Python/staged/data --combine
```

2) Generate instances TTL:
```bash
python3 generate_cmc_ttl.py
```
This will:
- Treat the second row in the SGD CSV as the true header row
- Create per‑stage `ex:Specification` and link all CQAs (`ex:QualityAttribute`) for that stage via `ex:hasCQA`
- Add `rdfs:comment` from the `Explanation/Translation` column when present
- Create provisional `prov:Agent` nodes from `Owner` and link CQAs via `prov:wasAttributedTo` (multi‑owner supported)
- Escape newlines/tabs to ensure GraphDB compatibility

## Column → Ontology mapping (current)
- `Value Stream` → IRI segment for Stage/Plan/Gate/Spec (e.g., `cgt`, `protein`)
- `Stage Gate` → IRI segment for stage number (e.g., `1`, `2`)
- `Stage Gate Description` → `rdfs:label` for `ex:Stage`; used in labels for Plan/Gate/Spec
- `Deliverable` → `ex:QualityAttribute` with `rdfs:label`; linked to stage `ex:Specification` via `ex:hasCQA`
- `Explanation/Translation` → `rdfs:comment` on the `ex:QualityAttribute`
- `Owner` → `prov:Agent` with `rdfs:label`; QA linked via `prov:wasAttributedTo` (supports comma‑separated multi‑owners)
- `Functional Area/Subteam` → planned: `prov:Agent` or `ex:FunctionalArea` associated to stages/gates
- `Category`, `Status`, `To be presented at`, `VPAD-specific?` → reserved for future mapping when populated

## Export to GraphDB
Environment variables (recommended)
- `GRAPHDB_URL`: e.g., `http://localhost:7200`
- `GRAPHDB_REPOSITORY`: repository ID, e.g., `test`
- `GRAPHDB_CONTEXT`: named graph IRI, e.g., `https://w3id.org/cmc-stagegate`
- `GRAPHDB_USER`, `GRAPHDB_PASSWORD`: if basic auth is required

Dry run
```bash
python3 export_to_graphdb.py --repository test
```

Upload (no dry‑run)
```bash
GRAPHDB_URL=http://localhost:7200 \
GRAPHDB_REPOSITORY=test \
GRAPHDB_CONTEXT=https://w3id.org/cmc-stagegate \
python3 export_to_graphdb.py --no-dry-run
```

Troubleshooting
- Check repo exists: `curl -s http://localhost:7200/repositories`
- Count triples: `curl -s http://localhost:7200/repositories/test/size`
- If 400 on upload: ensure TTL special characters are escaped (the generator already does this), and the repo accepts `text/turtle`.

## Example SPARQL queries
Stages with counts of CQAs
```sparql
PREFIX ex: <https://w3id.org/cmc-stagegate#>
SELECT ?stage ?stageLabel (COUNT(?cqa) AS ?numCQAs)
WHERE {
  ?stage a ex:Stage ; rdfs:label ?stageLabel ; ex:hasSpecification ?spec .
  ?spec ex:hasCQA ?cqa .
}
GROUP BY ?stage ?stageLabel
ORDER BY ?stageLabel
```

Stage rollup (Stage, Spec, CQA, Owners)
```sparql
PREFIX ex:   <https://w3id.org/cmc-stagegate#>
PREFIX prov: <http://www.w3.org/ns/prov#>
SELECT ?stageLabel ?spec ?cqaLabel (GROUP_CONCAT(DISTINCT ?ownerLabel; separator=", ") AS ?owners)
WHERE {
  ?stage a ex:Stage ; rdfs:label ?stageLabel ; ex:hasSpecification ?spec .
  ?spec  ex:hasCQA ?cqa .
  ?cqa   rdfs:label ?cqaLabel .
  OPTIONAL {
    ?cqa prov:wasAttributedTo ?owner .
    ?owner rdfs:label ?ownerLabel .
  }
}
GROUP BY ?stageLabel ?spec ?cqaLabel
ORDER BY ?stageLabel ?cqaLabel
```

Orphan CQAs (no owner)
```sparql
PREFIX ex:   <https://w3id.org/cmc-stagegate#>
PREFIX prov: <http://www.w3.org/ns/prov#>
SELECT ?stageLabel ?cqa ?cqaLabel
WHERE {
  ?stage a ex:Stage ; rdfs:label ?stageLabel ; ex:hasSpecification ?spec .
  ?spec  ex:hasCQA ?cqa .
  ?cqa   rdfs:label ?cqaLabel .
  FILTER NOT EXISTS { ?cqa prov:wasAttributedTo ?anyOwner }
}
ORDER BY ?stageLabel ?cqaLabel
```

Top contributing owners
```sparql
PREFIX ex:   <https://w3id.org/cmc-stagegate#>
PREFIX prov: <http://www.w3.org/ns/prov#>
SELECT ?ownerLabel (COUNT(?cqa) AS ?numCQAs)
WHERE {
  ?spec ex:hasCQA ?cqa .
  ?cqa prov:wasAttributedTo ?owner .
  ?owner rdfs:label ?ownerLabel .
}
GROUP BY ?ownerLabel
ORDER BY DESC(?numCQAs)
```

Keyword search in CQAs (e.g., "plasmid")
```sparql
PREFIX ex: <https://w3id.org/cmc-stagegate#>
SELECT ?stageLabel ?cqaLabel
WHERE {
  ?stage a ex:Stage ; rdfs:label ?stageLabel ; ex:hasSpecification ?spec .
  ?spec ex:hasCQA ?cqa .
  ?cqa  rdfs:label ?cqaLabel .
  FILTER(CONTAINS(LCASE(?cqaLabel), "plasmid"))
}
ORDER BY ?stageLabel ?cqaLabel
```

## Design notes & assumptions
- We prioritized readable IRIs derived from the spreadsheet to make joins and debugging easier.
- Owners are treated as provisional `prov:Agent` resources; a future step can reconcile them to official org directories or role vocabularies.
- `Functional Area/Subteam`, `Category`, `Status`, `To be presented at`, `VPAD-specific?` are placeholders pending better source data.
- Stage specifications (`ex:Specification`) act as a grouping node for CQAs; acceptance criteria can be added later with QUDT.

## Next steps (business questions)
- What decisions/KPIs should this drive (on‑time/at‑risk/late by stage, bottlenecks, owner load)?
- What are authoritative sources for due dates/status (Jira/Smartsheet/ERP) to integrate for live tracking?
- Should owners map to individuals or roles, and where is the source of truth?
- Which stage gates require approvals/signatures to model with PROV (who/when/why)?

## License
Internal use. Add a license if sharing externally.
