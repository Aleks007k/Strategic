# Strategic Provider Reasoning Integration

## Purpose

Integrate the strategic expert reasoning model into the new pipeline providers.

The new pipeline does not use markdown prompt files.
Provider prompts are constructed directly in Python.

## Updated Providers

Modified:

- backend/engines/providers/anthropic_provider.py
- backend/engines/providers/ollama_provider.py

## Added Reasoning Framework

Providers now instruct experts to:

1. Understand mission:
   - question;
   - goal;
   - constraints.

2. Identify assumptions.

3. Identify key factors.

4. Generate risks connected to key factors.

5. Generate opportunities connected to key factors.

6. Write summary after reasoning.

7. Estimate confidence after analysis.

## Output Schema

Current provider output:

- summary
- key_factors
- risks
- opportunities
- confidence

Recommendations are removed from the new provider schema.

## Confidence Integration

Confidence now flows:

LLM provider
→ AnalysisEngine normalization
→ AnalysisResult
→ StrategicSynthesisEngine
→ readiness assessment

This enables readiness evaluation based on actual confidence values.

## Current Limitation

Assumptions are part of the strategic reasoning model and AnalysisResult design, but provider schemas currently do not return them.

Future task:

Add assumptions support consistently across:

- provider schemas;
- prompts;
- normalization;
- tests.

## Verification

Confirmed:

- reasoning framework included in provider prompts;
- schema compatibility preserved;
- confidence values pass correctly;
- MockProvider unchanged;
- full pipeline execution unaffected;
- legacy pipeline unchanged.