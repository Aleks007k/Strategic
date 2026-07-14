# Strategic Synthesis Model

## Purpose

Define how multiple expert analyses are combined into one strategic view.

Synthesis does not replace expert reasoning.
It organizes multiple perspectives into a structured overview.

## Input

StrategicSynthesisEngine receives:

- multiple AnalysisResult objects from experts.

Each analysis contains:

- agent
- summary
- key_factors
- risks
- opportunities
- assumptions
- confidence

## Synthesis Output

The synthesis layer produces:

- perspectives
- combined_risks
- combined_opportunities
- common_factors
- conflicting_factors
- factor_agreement
- confidence_summary
- experts_count

## Perspectives

Each expert perspective is preserved separately.

Purpose:

- maintain traceability;
- show different analytical viewpoints;
- avoid hiding disagreement.

## Risk and Opportunity Aggregation

Risks and opportunities are combined by list aggregation.

The synthesis layer does not rewrite expert conclusions.

## Factor Agreement

Factor agreement measures how many experts independently identify the same factor.

Example:

Three experts:

- Market growth
- Market growth
- Regulation

Result:

- Market growth → agreement score 0.66
- Regulation → agreement score 0.33

## Common Factors

Factors identified by multiple experts.

They represent areas of stronger agreement.

## Conflicting Factors

Factors identified by only one expert.

They represent areas without confirmation from other perspectives.

They do not necessarily mean direct disagreement.

## Confidence Aggregation

Confidence is calculated as the average of available expert confidence values.

Missing confidence values are ignored.

If no confidence values exist:

- confidence_summary remains unavailable.

## Design Principles

Synthesis should:

- preserve expert outputs;
- avoid inventing information;
- remain deterministic;
- expose agreement and uncertainty.

Synthesis should not:

- create new conclusions;
- hide disagreement;
- replace expert reasoning.