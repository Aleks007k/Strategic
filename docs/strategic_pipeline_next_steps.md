# Strategic Pipeline Next Steps

## Current Priority

Move the new strategic pipeline from structural completeness toward analytical capability.

The architecture and data flow are already established.
The next work should improve intelligence quality, not rebuild existing foundations.

## Priority 1 — Real Analysis Provider

Replace MockProvider as the main analysis source.

Goal:

- generate real summaries;
- generate key factors;
- generate risks;
- generate opportunities.

The provider interface already supports this transition.

Required:

- Ollama connection or
- Anthropic API integration.

## Priority 2 — Expert Analysis Quality

Improve expert reasoning output.

Add:

- explicit assumptions;
- confidence estimation;
- stronger key factor selection;
- risk/opportunity connection.

## Priority 3 — Readiness Gate

Add deterministic evaluation before final response.

Purpose:

- identify weak analysis;
- detect insufficient agreement;
- request additional review when needed.

## Priority 4 — Strategic Memory

Create persistent records of:

- completed analyses;
- decisions;
- outcomes;
- lessons learned.

Purpose:

allow future reasoning to use previous strategic experience.

## Priority 5 — Advanced Council Mechanisms

Future capabilities:

- expert challenge;
- debate;
- evidence verification;
- prediction accuracy tracking.

## Development Rule

Do not expand complexity before current stages provide reliable value.

The next implementation step should always be:

- small;
- testable;
- isolated;
- improving real capability.