# Strategic Readiness Gate Model

## Purpose

Define the final quality checkpoint before strategic analysis is presented to the user.

The readiness gate does not generate analysis.
It evaluates whether the existing analysis output is sufficient for delivery.

## Why a Readiness Gate Exists

A strategic intelligence system should not treat every generated output as equally reliable.

The system must distinguish between:

- complete analysis;
- incomplete analysis;
- conflicting analysis;
- analysis requiring additional review.

## Current Inputs

The readiness gate uses existing synthesis data:

- confidence_summary;
- factor_agreement;
- common_factors;
- conflicting_factors;
- experts_count.

No additional AI generation is required.

## Initial Deterministic Rules

The first version should remain deterministic.

Possible signals:

### Expert Coverage

Check whether multiple expert perspectives exist.

Low coverage:
- one expert only;
- missing perspectives.

### Agreement Level

Evaluate whether important factors are supported by multiple experts.

Higher agreement:
- repeated factors across experts;
- stronger factor agreement scores.

Lower agreement:
- mostly unique factors;
- conflicting viewpoints.

### Confidence Signal

Use available confidence values when present.

If confidence data is missing:
- do not invent confidence;
- mark confidence as unavailable.

## Output

The readiness gate should produce a simple structured decision:

Example:

```json
{
  "ready": true,
  "needs_review": false,
  "reasons": []
}

# Readiness Gate Decision Model

## Purpose

Define how the system decides whether a synthesized strategic analysis is ready to be presented.

The readiness gate does not improve the analysis.
It evaluates whether the existing output is sufficient.

## Input Signals

The readiness gate uses:

- experts_count
- confidence_summary
- factor_agreement
- common_factors
- conflicting_factors

## Decision Principles

A result should require review when:

- too few expert perspectives exist;
- confidence information is unavailable;
- expert agreement is very low;
- conflicting signals dominate.

## Initial Decision States

Possible states:

### Ready

The analysis has enough structural support for presentation.

### Needs Review

The analysis contains uncertainty or insufficient agreement.

### Insufficient Data

The system cannot evaluate readiness because important signals are missing.

## Output Example

```json
{
  "status": "needs_review",
  "reasons": [
    "low expert agreement",
    "missing confidence data"
  ]
}