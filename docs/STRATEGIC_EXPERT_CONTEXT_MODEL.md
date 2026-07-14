# Strategic Expert Context Model

## Purpose

The AnalysisEngine adapter enriches expert analysis input with strategic context before sending data to providers.

The goal is to ensure that future LLM-based experts receive enough mission context without coupling the new pipeline to legacy agents.

## Provider Input Contract

The provider interface remains unchanged:

{
  "agent": "...",
  "reasoning_context": {}
}

All additional information is placed inside reasoning_context.

## Current Reasoning Context

The analysis context now includes:

### Existing fields

- mission
- skills
- methodologies
- analysis_steps
- question

### Strategic fields

- goals
- constraints
- time_horizon
- expert_scope
- decision_type

## Data Sources

Currently available:

goals:
- sourced from mission.goal

constraints:
- sourced from mission.constraints

question:
- sourced from mission.question

Future-compatible fields:

time_horizon:
- currently not present in the data model

expert_scope:
- currently not present in the data model

decision_type:
- currently not present in the data model

These fields are passed as None when unavailable.

No values are invented.

## Design Principle

AnalysisEngine acts as an adaptation boundary.

Upstream components produce reasoning packages.

AnalysisEngine converts them into provider-compatible reasoning_context.

Providers remain unchanged.

## Verification

Confirmed:

- provider input shape unchanged;
- strategic fields pass correctly when available;
- missing fields handled safely;
- reasoning package is not mutated;
- MockProvider continues working;
- normalized AnalysisResult shape unchanged;
- StrategicExecutor full flow works;
- synthesis and readiness stages unaffected.

Changed file:

- backend/engines/reasoning_analysis_engine.py