# Product Instance SPARQL Queries

## Overview
This collection of SPARQL queries demonstrates temporal tracking of drug products through stage-gate processes using W3C Time Ontology patterns.

## Query Catalog

### 📊 Timeline & History Queries

#### 01. Drug Timeline (`01_drug_timeline.sparql`)
- **Purpose**: Shows complete progression history of a specific drug
- **Use Case**: Audit trail, historical analysis
- **Key Features**: Start/end dates for each stage, duration tracking, current stage identification
- **Temporal Elements**: `time:Interval`, `time:hasBeginning`, `time:hasEnd`

#### 11. Stage Transition Gantt (`11_stage_transition_gantt.sparql`)
- **Purpose**: Generates data for Gantt chart visualization
- **Use Case**: Portfolio visualization, timeline displays
- **Key Features**: All drugs, all stages, formatted for charts
- **Temporal Elements**: Complete intervals with status flags

### 📈 Portfolio Analysis Queries

#### 02. Current Portfolio Status (`02_current_portfolio_status.sparql`)
- **Purpose**: Snapshot of all drugs and their current stages
- **Use Case**: Executive dashboards, portfolio reviews
- **Key Features**: Days in current stage, indication tracking
- **Temporal Elements**: Open-ended intervals for active stages

#### 06. Drug Development Velocity (`06_drug_velocity.sparql`)
- **Purpose**: Calculates speed of progression through pipeline
- **Use Case**: Performance metrics, efficiency analysis
- **Key Features**: Stages per year, average days per stage
- **Temporal Elements**: Duration calculations across multiple stages

#### 10. Portfolio Launch Forecast (`10_portfolio_forecast.sparql`)
- **Purpose**: Projects market launch dates based on historical velocity
- **Use Case**: Revenue forecasting, resource planning
- **Key Features**: Confidence levels, modality-specific projections
- **Temporal Elements**: Historical velocity extrapolation

### 🔍 Performance & Risk Queries

#### 03. Stage Duration Analysis (`03_stage_duration_analysis.sparql`)
- **Purpose**: Compares actual vs projected timelines
- **Use Case**: Process improvement, delay analysis
- **Key Features**: Variance calculations, delay reasons
- **Temporal Elements**: `projectedInterval` vs `actualInterval`

#### 05. Stage Bottleneck Analysis (`05_stage_bottlenecks.sparql`)
- **Purpose**: Identifies problematic stages across portfolio
- **Use Case**: Process optimization, resource allocation
- **Key Features**: Average/max durations, delay frequency
- **Temporal Elements**: Statistical analysis of durations

#### 09. At-Risk Drugs (`09_at_risk_drugs.sparql`)
- **Purpose**: Flags drugs behind schedule or blocked
- **Use Case**: Risk management, intervention planning
- **Key Features**: Risk scoring, overdue calculations
- **Temporal Elements**: Days overdue based on projected dates

### 🚪 Gate & Transition Queries

#### 04. Gate Transitions (`04_gate_transitions.sparql`)
- **Purpose**: History of gate review decisions
- **Use Case**: Governance tracking, decision audit
- **Key Features**: Reviewer tracking, decision outcomes
- **Temporal Elements**: `time:Instant` for transition moments

#### 07. Planned vs Actual (`07_planned_vs_actual.sparql`)
- **Purpose**: Variance analysis between plan and execution
- **Use Case**: Planning accuracy, forecasting improvement
- **Key Features**: Variance classification, delay categorization
- **Temporal Elements**: Comparison of interval endpoints

### 📋 Deliverable Queries

#### 08. Deliverable Timeline (`08_deliverable_timeline.sparql`)
- **Purpose**: Links deliverables to stage timeframes
- **Use Case**: Compliance tracking, work planning
- **Key Features**: Owner assignment, completion tracking
- **Temporal Elements**: Deliverable dates within stage intervals

## How to Execute

### Using GraphDB
```sparql
# In GraphDB Workbench
1. Open Repository
2. Go to SPARQL Query
3. Copy query content
4. Click Execute
```

### Using Command Line (with Jena/RDF4J)
```bash
# Example with Apache Jena
sparql --data=output/current/cmc_stagegate_all.ttl \
       --query=queries/product_instance/01_drug_timeline.sparql
```

### Using Python (with rdflib)
```python
from rdflib import Graph

# Load data
g = Graph()
g.parse("output/current/cmc_stagegate_all.ttl", format="turtle")
g.parse("data/example_temporal_tracking.ttl", format="turtle")

# Load and execute query
with open("queries/product_instance/01_drug_timeline.sparql") as f:
    query = f.read()
    
results = g.query(query)
for row in results:
    print(row)
```

## Temporal Patterns Used

### Time Intervals
```sparql
?occupancy ex:validDuring ?interval .
?interval time:hasBeginning ?begin ;
          time:hasEnd ?end .
```

### Open-Ended Intervals (Current States)
```sparql
?interval time:hasBeginning ?begin .
# No time:hasEnd for ongoing stages
```

### Duration Calculations
```sparql
BIND(?endDate - ?startDate AS ?duration)
BIND(NOW() - ?startDate AS ?daysInCurrentStage)
```

### Projected vs Actual
```sparql
?occupancy ex:projectedInterval ?projected ;
           ex:actualInterval ?actual .
```

## Key Ontology Elements

### Classes
- `ex:StageOccupancy` - Period in a stage
- `ex:StageTransition` - Gate passage event
- `time:Interval` - Time period
- `time:Instant` - Moment in time

### Properties
- `ex:validDuring` - Links to time interval
- `ex:hasStageHistory` - Drug to occupancies
- `ex:occupiedStage` - Which stage
- `ex:isCurrentStage` - Boolean flag
- `ex:stageDuration` - ISO 8601 duration

## Example Drug Timeline

```
Drug: ABC-789
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
Stage 0 |████████| Jan-Mar 2022 (90 days)
        Gate 0 ✓
Stage 1 |█████████| Mar-Jun 2022 (92 days)
        Gate 1 ✓
Stage 2 |██████████████████| Jun-Dec 2022 (180 days) ⚠️ Delayed
        Gate 2 ✓
Stage 3 |████████████| Dec 2022-Jun 2023 (196 days)
        Gate 3 ✓
Stage 4 |████████████████████████| Jul 2023-Aug 2024 (427 days)
        Gate 4 ✓
Stage 5 |█████████░░░░░░| Sep 2024-Present (In Progress)
```

## Business Value

1. **Historical Analysis**: Complete audit trail of progression
2. **Bottleneck Identification**: Find process inefficiencies
3. **Risk Management**: Early warning for delays
4. **Resource Planning**: Forecast workload based on velocity
5. **Portfolio Optimization**: Data-driven stage gate decisions
6. **Compliance**: Full traceability for regulatory

## Customization

To adapt for your drugs:
1. Replace `ex:Drug-ABC789` with your drug IRIs
2. Adjust stage count (13 for Protein, 11 for CGT)
3. Add custom properties to SELECT clauses
4. Modify filters for your risk thresholds
5. Extend with your business rules

## Related Documentation
- [Temporal Tracking Guide](../../docs/TEMPORAL_TRACKING_GUIDE.md)
- [Drug Product Integration](../../docs/DRUG_PRODUCT_STAGE_GATE_INTEGRATION.md)
- [Example Data](../../data/example_temporal_tracking.ttl)
