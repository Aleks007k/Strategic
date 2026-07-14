# Strategic Pipeline Output Contract

## Purpose

Define the final data contract produced by the strategic pipeline.

The pipeline should separate:

- structured internal analysis;
- readiness evaluation;
- user-facing presentation.

## StrategicExecutor Output

StrategicExecutor returns structured data.

Main sections:

- question
- mission
- selection
- session
- synthesis
- workflow_state

## Synthesis Contract

The synthesis object contains:

- experts_count
- perspectives
- combined_risks
- combined_opportunities
- common_factors
- conflicting_factors
- factor_agreement
- confidence_summary

## Workflow State

Workflow state describes execution progress.

It should represent actual completed capabilities.

Stage names must not imply functionality that does not exist.

Example:

Incorrect:

"consensus completed"

when only factor counting was performed.

Correct:

"synthesis completed"

when aggregation finished.

## Response Formatting

Formatting converts structured synthesis into readable text.

Rules:

- no modification of analysis data;
- no new conclusions;
- no hidden reasoning;
- deterministic output.

## Architecture Boundary

StrategicExecutor:

- coordinates execution.

AnalysisEngine:

- produces expert analysis.

StrategicSynthesisEngine:

- combines analysis.

Readiness Gate:

- evaluates quality.

Formatter:

- presents results.

Each layer has one responsibility.