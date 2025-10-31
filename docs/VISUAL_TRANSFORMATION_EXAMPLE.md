# Visual Example: Excel Row to Knowledge Graph

## Before: Excel Row (What stakeholders see)

| Value Stream | Stage Gate | Stage Description | Category | Deliverable | Explanation | Owner | Plan Date |
|--------------|------------|-------------------|----------|-------------|-------------|--------|-----------|
| CGT | Stage 0 | Target ID & Validation | API Development | TPP draft | Target Product Profile defining the drug product | Biology Lead | 2025-12-31 |

## After: Knowledge Graph (What the system creates)

```
                    ┌──────────────────┐
                    │   Stage-CGT-0    │
                    │ "Target ID &     │
                    │  Validation"     │
                    └────────┬─────────┘
                             │ hasDeliverable
                             ▼
                ┌────────────────────────┐
                │ CQA-CGT-Stage0-TPPdraft│
                │   "TPP draft"          │
                └───┬──────┬──────┬─────┘
                    │      │      │
     hasCategory────┤      │      ├────plannedDate
            ▼              │              ▼
    ┌──────────────┐       │      ┌──────────────┐
    │"API           │       │      │"2025-12-31"  │
    │Development"   │       │      └──────────────┘
    └──────────────┘       │
                           │ wasAssociatedWith
                           ▼
                    ┌──────────────┐
                    │ Agent-Biology │
                    │    Lead       │
                    └──────────────┘
```

## What This Means for Stakeholders

### 1. **Your Excel Structure is Preserved**
- Every row becomes a deliverable (Quality Attribute)
- Every column value becomes a property
- Nothing is lost, everything is enriched

### 2. **Relationships Become Explicit**
- The system now "knows" that Biology Lead is responsible for the TPP draft
- It "understands" that TPP draft belongs to Stage 0
- It can "reason" that this is an API Development activity

### 3. **New Capabilities Unlocked**

**Excel Query:** 
- Filter for "Stage 0" + "API Development"
- Manual counting and sorting

**Knowledge Graph Query:**
```sparql
"Show me all API Development deliverables in Stage 0 
 with their owners and due dates"
```
Result: Instant, accurate, and includes relationships

### 4. **Real Business Value**

| Excel Limitation | Knowledge Graph Solution |
|-----------------|-------------------------|
| Can't track dependencies between deliverables | Explicit relationship modeling |
| No audit trail of changes | Full provenance tracking |
| Manual report generation | Automated queries and dashboards |
| Isolated data silos | Integrated with other systems |
| Static structure | Flexible, extensible schema |

## The Power of Semantic Enrichment

Your data gains **meaning** that computers can understand:

- **"TPP draft"** is not just text → It's a `QualityAttribute` instance
- **"Biology Lead"** is not just a name → It's an `Agent` with responsibilities  
- **"2025-12-31"** is not just a date → It's a `plannedDate` for tracking
- **"API Development"** is not just a category → It's a classification for analysis

## Bottom Line for Stakeholders

**You provide:** Excel spreadsheet with stage-gate deliverables  
**We transform:** Each row into interconnected knowledge  
**You receive:** Intelligent system that can answer complex questions

### Example Questions Now Answerable:
- "Which deliverables across all stages are owned by Biology Lead?"
- "What percentage of API Development items met their planned dates?"
- "Show the dependency chain from Stage 0 to Stage 3"
- "Which categories have the most overdue deliverables?"

All from the same Excel data - just smarter!
