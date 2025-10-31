# Temporal Tracking for Drug Stage Progression

## Overview
Using W3C Time Ontology to track **when** drugs move through stages, not just **where** they are.

## What We Added

### New Ontology: `cmc_stagegate_temporal.ttl`
- **StageOccupancy**: Period a drug spends in a stage
- **StageTransition**: Movement between stages
- **Time intervals**: Start/end dates for each stage
- **Duration tracking**: How long in each stage
- **Delay tracking**: Why stages took longer than planned

## How It Works

### Traditional (Simple) Approach
```turtle
ex:Drug-ABC123 
    ex:currentStage ex:Stage-5 .  # Just knows current stage
```

### Enhanced Temporal Approach
```turtle
ex:Drug-ABC123 
    ex:currentStage ex:Stage-5 ;
    ex:hasStageHistory ex:Occupancy-Stage5 .

ex:Occupancy-Stage5
    ex:occupiedStage ex:Stage-5 ;
    ex:validDuring [
        time:hasBeginning [ time:inXSDDate "2024-09-01"^^xsd:date ] ;
        # No end date - still in progress
    ] ;
    ex:stageDuration "P60D"^^xsd:duration ;  # 60 days so far
    ex:isCurrentStage true .
```

## Key Concepts

### 1. Stage Occupancy
Tracks the **time period** a drug spends in each stage:
```turtle
ex:Occupancy-ABC789-Stage2 a ex:StageOccupancy ;
    ex:occupiedStage ex:Stage-protein-2 ;
    ex:validDuring [
        time:hasBeginning "2022-06-16"^^xsd:date ;
        time:hasEnd "2022-12-15"^^xsd:date 
    ] ;
    ex:stageDuration "P180D"^^xsd:duration ;  # ISO 8601: 180 days
    ex:delayReason "Manufacturing scale-up issues" .
```

### 2. Stage Transitions
Records the **moment** of gate reviews:
```turtle
ex:Transition-ABC789-Gate4 a ex:StageTransition ;
    ex:fromStage ex:Stage-4 ;
    ex:toStage ex:Stage-5 ;
    ex:transitionedVia ex:Gate-4 ;
    ex:atTimePoint [ time:inXSDDate "2024-09-01"^^xsd:date ] ;
    ex:decision ex:Approved .
```

### 3. Projected vs Actual
Compare planned timeline to reality:
```turtle
ex:Occupancy-Stage2
    ex:projectedInterval [  # Was supposed to take 120 days
        time:hasEnd "2022-10-15"^^xsd:date
    ] ;
    ex:actualInterval [     # Actually took 180 days
        time:hasEnd "2022-12-15"^^xsd:date
    ] ;
    ex:delayReason "Scale-up issues" .
```

## Business Value

### 1. Historical Analysis
```sparql
# Average time in Stage 5 across all drugs
SELECT AVG(?days) WHERE {
    ?drug ex:hasStageHistory ?occ .
    ?occ ex:occupiedStage ex:Stage-5 ;
         ex:stageDuration ?duration .
    # Convert to days...
}
```

### 2. Bottleneck Identification
```sparql
# Which stages have the most delays?
SELECT ?stage COUNT(?delay) WHERE {
    ?occ ex:occupiedStage ?stage ;
         ex:delayReason ?delay .
} GROUP BY ?stage ORDER BY DESC(COUNT(?delay))
```

### 3. Timeline Forecasting
```sparql
# When will drugs reach market based on historical pace?
SELECT ?drug ?projectedLaunch WHERE {
    ?drug ex:currentStage ?stage ;
          ex:hasStageHistory ?history .
    # Calculate based on average stage durations...
}
```

### 4. Compliance Tracking
```sparql
# Which drugs missed regulatory milestones?
SELECT ?drug ?milestone ?plannedDate ?actualDate WHERE {
    ?drug ex:hasStageHistory ?occ .
    ?occ ex:projectedInterval/time:hasEnd ?plannedDate ;
         ex:actualInterval/time:hasEnd ?actualDate .
    FILTER(?actualDate > ?plannedDate)
}
```

## Implementation Pattern

### Step 1: Add Temporal Ontology
```bash
# Add to your base ontology
cat cmc_stagegate_temporal.ttl >> cmc_stagegate_base.ttl
```

### Step 2: Create Stage History
When drug enters new stage:
```turtle
# Create new occupancy
ex:Occupancy-DRUG-StageN a ex:StageOccupancy ;
    ex:occupiedStage ex:Stage-N ;
    ex:validDuring [
        time:hasBeginning [ time:inXSDDate "2024-11-01"^^xsd:date ]
    ] ;
    ex:isCurrentStage true .

# Mark previous as not current
ex:Occupancy-DRUG-StageN-1 
    ex:isCurrentStage false ;
    ex:validDuring/time:hasEnd [ time:inXSDDate "2024-10-31"^^xsd:date ] .
```

### Step 3: Track Transitions
At gate review:
```turtle
ex:Transition-DRUG-GateN a ex:StageTransition ;
    ex:fromStage ex:Stage-N ;
    ex:toStage ex:Stage-N+1 ;
    ex:atTimePoint [ time:inXSDDateTime "2024-10-31T14:30:00"^^xsd:dateTime ] ;
    ex:decision ex:Approved ;
    prov:wasAssociatedWith ex:SME-reviewer .
```

## Comparison with Example

Your example (`example_triples.txt`) shows domain groupings with validity periods:
```turtle
jctao:DG_Immunology_Rheumatology_2024
    jctao:validDuring [
        time:hasBeginning [ time:inXSDDate "2024-01-01"^^xsd:date ] ;
        time:hasEnd [ time:inXSDDate "2028-12-31"^^xsd:date ]
    ] .
```

Our implementation applies the same pattern to drug stages:
```turtle
ex:Occupancy-ABC789-Stage5
    ex:validDuring [
        time:hasBeginning [ time:inXSDDate "2024-09-01"^^xsd:date ] ;
        # No end - still active
    ] .
```

## Benefits Over Simple Date Properties

| Simple Properties | Temporal Intervals | Benefit |
|------------------|-------------------|---------|
| `ex:startDate "2024-01-01"` | Full time:Interval with beginning/end | Can query overlaps, durations |
| Single current stage | Complete stage history | Track progression patterns |
| No duration info | ISO 8601 durations | Calculate velocities |
| No delay tracking | Projected vs actual | Identify bottlenecks |

## Query Examples

### Timeline Visualization
```sparql
# Get complete timeline for a drug
SELECT ?stage ?begin ?end ?duration WHERE {
    ex:Drug-ABC789 ex:hasStageHistory ?occ .
    ?occ ex:occupiedStage ?stage ;
         ex:validDuring ?interval ;
         ex:stageDuration ?duration .
    ?interval time:hasBeginning/time:inXSDDate ?begin .
    OPTIONAL { ?interval time:hasEnd/time:inXSDDate ?end }
} ORDER BY ?begin
```

### Current Portfolio Status
```sparql
# All drugs with their current stage start dates
SELECT ?drug ?stage ?since WHERE {
    ?drug a ex:DrugProduct ;
          ex:hasStageHistory ?occ .
    ?occ ex:isCurrentStage true ;
         ex:occupiedStage ?stage ;
         ex:validDuring/time:hasBeginning/time:inXSDDate ?since .
}
```

## Files Created

1. **`cmc_stagegate_temporal.ttl`** - Temporal ontology extension
2. **`data/example_temporal_tracking.ttl`** - Example with ABC-789
3. **`docs/TEMPORAL_TRACKING_GUIDE.md`** - This guide

## Next Steps

1. ✅ Review temporal ontology
2. ⬜ Add to existing drugs
3. ⬜ Create historical data
4. ⬜ Build timeline dashboards
5. ⬜ Set up delay alerts
