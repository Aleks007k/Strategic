# Strategic Prompt Model

## Purpose

Define how strategic expert prompts should guide reasoning before producing AnalysisResult output.

Prompts should shape expert thinking while preserving the existing output contract.

## Reasoning Sequence

Experts should follow this order:

1. Understand the mission

Extract:

- question;
- goal;
- constraints;
- expert perspective and scope.

The expert must answer the actual strategic question, not a related but different one.

2. Identify assumptions and key factors

Determine:

- what must be true for the conclusion to hold;
- what information is uncertain;
- which variables have the largest influence on the outcome.

3. Generate risks and opportunities

Risks and opportunities should be connected to the same key factors.

Risks:

- external changes;
- execution failures;
- assumption failures;
- second-order consequences.

Opportunities:

- asymmetric upside;
- strategic advantages;
- positive second-order effects.

4. Write summary

The summary is produced after reasoning.

It should compress:

- main conclusion;
- important drivers;
- major uncertainty.

5. Assess confidence

Confidence is evaluated after the analysis is complete.

It reflects:

- information quality;
- assumption strength;
- uncertainty level.

## Output Compatibility

Prompts must preserve the existing AnalysisResult structure:

- summary
- key_factors
- risks
- opportunities
- assumptions
- confidence

Do not introduce new output fields without changing the data model.

## Current Architecture Note

Current prompt files:

- prompts/strategic_analyst.md
- prompts/economic_analyst.md
- prompts/technology_analyst.md

are used by the legacy agent pipeline.

The new pipeline providers currently build prompts internally in Python code.

Therefore:

- prompt improvements here affect legacy agents;
- new pipeline prompt improvement requires a separate provider-layer task.

## Design Principle

Prompt improvements should improve reasoning quality without creating architectural coupling.

Prompts define thinking behavior.

Backend defines data contracts.