feat: Enhanced ontology with new properties and complete data transformation

## Summary
Major update to CMC Stage-Gate ontology and ETL pipeline to support expanded Excel input with new data columns and improved organization.

## Key Changes

### Ontology Enhancements
- Added 4 new properties to base ontology:
  - `ex:hasCategory` for functional area classification (25 unique categories)
  - `ex:plannedDate` for planned completion dates
  - `ex:actualDate` for actual completion dates  
  - `ex:reference` for document references

### Data Processing Updates
- Fixed file selection bug in generate_cmc_ttl.py (now correctly selects *__SGD.csv)
- Updated column mappings for new Excel structure
- Successfully generated 12,570 triples from 3,979 Excel rows
- Created 37 stages with 2,205+ deliverables

### Folder Structure Reorganization
- New structure: `data/current/` for active data
- Archives: `data/previous_input_YYMMDD/` and `data/extracted_YYMMDD/`
- Output: `output/current/` for generated TTLs
- Historical: `output/ttl_YYMMDD_*/` for previous versions

### Documentation Added
- ONTOLOGY_ANALYSIS.md - Complete ontology structure analysis
- STAKEHOLDER_DATA_TRANSFORMATION_GUIDE.md - Business-friendly explanation
- PROTEGE_LOADING_GUIDE.md - Instructions for ontology visualization
- TEXT_HANDLING_GUIDE.md - How complex text is processed
- MULTILINE_TEXT_EXAMPLE.md - Handling of bullet points and formatting

### Script Updates
- All ETL scripts updated for new folder structure
- Paths dynamically resolve to current directories
- Support for timestamped archiving

## Statistics
- Input: 265KB Excel with 13 columns
- Output: 1.1MB TTL with 12,570 triples  
- Categories: 1,173 classified deliverables
- Multi-line text: 114 items preserved with formatting
- Validation: All files pass Rapper RDF validation

## Testing
✅ Syntax validation passed
✅ New properties verified in output
✅ GIST alignment confirmed
✅ Complex text handling validated
✅ Multi-line bullet points preserved
