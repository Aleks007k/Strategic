# MockProvider Strategic Schema

## Purpose

MockProvider was upgraded from a minimal fallback into a deterministic strategic analysis provider.

Its purpose is now:

- local development;
- pipeline testing;
- schema verification;
- readiness gate testing.

It is not intended to replace real LLM reasoning.

## Output

MockProvider now produces strategic analysis content:

- summary
- key_factors
- risks
- opportunities
- assumptions
- confidence

Additional legacy compatibility fields remain:

- agent
- recommendations

These fields are preserved because MockProvider is shared with the legacy fallback pipeline.

## Deterministic Generation

MockProvider generates content from available context:

Sources:

- question;
- goals;
- constraints;
- skills;
- user preferences/focus areas.

No randomness is used.

Same input always produces the same output.

## Generated Elements

### Key factors

Built from:

- focus areas;
- expert skills;
- strategic goals.

Duplicates removed.

### Risks

Generated from:

- key factors;
- constraints.

### Opportunities

Generated from:

- key factors.

### Assumptions

Generated as falsifiable statements.

Examples:

- assumes a constraint remains valid;
- assumes current conditions remain stable.

### Confidence

Deterministic score based on available information:

- base confidence;
- additional points for key factors;
- additional points for constraints;
- additional points for goals.

Maximum capped value is applied.

## Compatibility

Verified:

- new AnalysisResult flow works;
- confidence aggregation works;
- readiness gate works;
- legacy OutputValidator remains valid;
- legacy pipeline structure unchanged.

## Architectural Note

MockProvider now supports both:

New pipeline:
Provider → AnalysisEngine → Synthesis → Readiness

Legacy fallback:
Agent → LLM fallback → OutputValidator

Therefore legacy compatibility fields must remain.