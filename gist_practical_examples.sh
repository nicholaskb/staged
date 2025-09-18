#!/bin/bash

# GraphDB endpoint
ENDPOINT="http://localhost:7200/repositories/cmc-stagegate"

echo "========================================================================"
echo "🚀 PRACTICAL GIST ALIGNMENT EXAMPLES"
echo "========================================================================"
echo ""
echo "These queries demonstrate real-world benefits of GIST alignment:"
echo ""

# Function to run a query with explanation
demo_query() {
    local title="$1"
    local explanation="$2"
    local query="$3"
    
    echo "------------------------------------------------------------------------"
    echo "📊 $title"
    echo "------------------------------------------------------------------------"
    echo "💡 $explanation"
    echo ""
    
    result=$(curl -s -X POST "$ENDPOINT" \
        -H "Content-Type: application/sparql-query" \
        -H "Accept: application/sparql-results+json" \
        -d "$query" 2>/dev/null)
    
    # Parse and display results
    echo "$result" | python3 -c "
import sys, json
try:
    data = json.load(sys.stdin)
    bindings = data.get('results', {}).get('bindings', [])
    if not bindings:
        print('  No results found')
    else:
        # Print results in a readable format
        for i, b in enumerate(bindings[:5]):
            print(f'\n  Result {i+1}:')
            for key, val in b.items():
                value = val.get('value', '')
                if value.startswith('http'):
                    value = value.split('#')[-1].split('/')[-1]
                print(f'    {key}: {value[:60]}')
        if len(bindings) > 5:
            print(f'\n  ... and {len(bindings) - 5} more results')
        print(f'\n  ✅ Total: {len(bindings)} results')
except Exception as e:
    print(f'  Error: {e}')
"
    echo ""
}

# Example 1: Find all planned activities in chronological order
demo_query \
    "EXAMPLE 1: Timeline of Planned Events" \
    "Using gist:PlannedEvent, we can query ANY planned activity across the system" \
    "PREFIX ex: <https://w3id.org/cmc-stagegate#>
PREFIX gist: <https://ontologies.semanticarts.com/gist/>
PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>

SELECT ?event ?label ?eventType WHERE {
    ?event a ?eventType ;
           rdfs:label ?label .
    ?eventType rdfs:subClassOf* gist:PlannedEvent .
}
ORDER BY ?label
LIMIT 10"

# Example 2: Task hierarchy navigation
demo_query \
    "EXAMPLE 2: Task Decomposition Hierarchy" \
    "gist:hasSubTask enables traversing ANY task breakdown structure" \
    "PREFIX ex: <https://w3id.org/cmc-stagegate#>
PREFIX gist: <https://ontologies.semanticarts.com/gist/>
PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>

SELECT ?parentType ?childType ?relationship WHERE {
    VALUES (?property ?parentType ?childType) {
        (ex:definesProcess ex:StagePlan ex:Process)
        (ex:hasUnitOperation ex:Process ex:UnitOperation)
        (ex:hasPlan ex:Stage ex:StagePlan)
        (ex:hasGate ex:Stage ex:StageGate)
    }
    ?property rdfs:subPropertyOf ?relationship .
    FILTER(STRSTARTS(STR(?relationship), STR(gist:)))
}
ORDER BY ?parentType"

# Example 3: Find all measurable aspects
demo_query \
    "EXAMPLE 3: Measurable Quality Aspects" \
    "gist:Aspect unifies ALL measurable characteristics" \
    "PREFIX ex: <https://w3id.org/cmc-stagegate#>
PREFIX gist: <https://ontologies.semanticarts.com/gist/>
PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>

SELECT ?aspectType (COUNT(?instance) as ?count) WHERE {
    ?instance a ?aspectType .
    ?aspectType rdfs:subClassOf* gist:Aspect .
}
GROUP BY ?aspectType
ORDER BY DESC(?count)"

# Example 4: Material participation in processes
demo_query \
    "EXAMPLE 4: Process Participation Pattern" \
    "gist:hasParticipant enables tracking ANY entity involved in processes" \
    "PREFIX ex: <https://w3id.org/cmc-stagegate#>
PREFIX gist: <https://ontologies.semanticarts.com/gist/>
PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>

SELECT DISTINCT ?participationProperty ?gistProperty WHERE {
    VALUES ?participationProperty { 
        ex:consumesMaterial 
        ex:assessedAtGate
    }
    ?participationProperty rdfs:subPropertyOf ?gistProperty .
    FILTER(CONTAINS(STR(?gistProperty), 'Participant'))
}"

# Example 5: Specification conformance pattern
demo_query \
    "EXAMPLE 5: Universal Specification Pattern" \
    "gist:Specification enables unified quality/compliance queries" \
    "PREFIX ex: <https://w3id.org/cmc-stagegate#>
PREFIX gist: <https://ontologies.semanticarts.com/gist/>
PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>

SELECT ?specType (COUNT(?spec) as ?specCount) (SUM(?cqaCount) as ?totalCQAs) WHERE {
    SELECT ?spec ?specType (COUNT(?cqa) as ?cqaCount) WHERE {
        ?spec a ?specType ;
              ex:hasCQA ?cqa .
        ?specType rdfs:subClassOf* gist:Specification .
    }
    GROUP BY ?spec ?specType
}
GROUP BY ?specType"

# Example 6: Evidence-based relationships
demo_query \
    "EXAMPLE 6: Evidence Traceability" \
    "gist:isBasedOn provides universal evidence linking" \
    "PREFIX ex: <https://w3id.org/cmc-stagegate#>
PREFIX gist: <https://ontologies.semanticarts.com/gist/>

SELECT ?evidenceRel ?gistPattern WHERE {
    VALUES ?evidenceRel { ex:hasEvidence }
    ?evidenceRel rdfs:subPropertyOf ?gistPattern .
    FILTER(STRSTARTS(STR(?gistPattern), STR(gist:)))
}"

# Example 7: Collections and membership
demo_query \
    "EXAMPLE 7: Collection Patterns" \
    "gist:Collection enables batch/lot management across domains" \
    "PREFIX ex: <https://w3id.org/cmc-stagegate#>
PREFIX gist: <https://ontologies.semanticarts.com/gist/>
PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>

SELECT ?collectionType ?description WHERE {
    VALUES ?collectionType { ex:Lot }
    ?collectionType rdfs:subClassOf gist:Collection ;
                    rdfs:comment ?description .
}"

echo "========================================================================"
echo "🎯 GIST ALIGNMENT BENEFITS DEMONSTRATED"
echo "========================================================================"
echo ""
echo "The GIST alignment provides:"
echo ""
echo "1. 🔄 SEMANTIC INTEROPERABILITY"
echo "   - Your CMC data can integrate with ANY GIST-based system"
echo "   - Shared understanding across domains"
echo ""
echo "2. 🔍 UNIFIED QUERY PATTERNS"
echo "   - Query planned events regardless of specific type"
echo "   - Navigate hierarchies with consistent patterns"
echo "   - Track participation universally"
echo ""
echo "3. 📊 CROSS-DOMAIN ANALYTICS"
echo "   - Aggregate measurements across different aspect types"
echo "   - Universal specification conformance checking"
echo "   - Evidence traceability across systems"
echo ""
echo "4. 🚀 FUTURE-PROOF DESIGN"
echo "   - Ready for GIST v13 enhancements"
echo "   - Extensible without breaking existing queries"
echo "   - Industry-standard semantic patterns"
echo ""
echo "✅ Your CMC Stage-Gate ontology is now part of the GIST ecosystem!"
