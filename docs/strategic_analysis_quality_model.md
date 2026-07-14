# Strategic Analysis Quality Model

## Purpose

Define what makes an expert analysis strategically useful and how the system should evaluate analysis quality.

## Analysis Quality Principles

A high-quality strategic analysis must:

- answer the actual question, not a simplified version;
- separate facts, assumptions, and predictions;
- identify the few variables that truly influence the outcome;
- connect risks and opportunities to those variables;
- expose uncertainty instead of hiding it;
- explain what could change the conclusion.

## Expert Analysis Structure

Every expert analysis should contain:

### Summary

A compressed conclusion based on the complete reasoning chain.

### Key Factors

The most influential and uncertain variables affecting the outcome.

A factor is important only if:

- changing it can significantly change the result;
- its current state is uncertain.

### Assumptions

Load-bearing beliefs required for the conclusion.

An assumption is valid only if:

- it affects the conclusion;
- it can be tested or disproven.

### Risks

Conditions that can prevent the desired outcome.

Risks should include:

- external risks;
- execution risks;
- assumption failure risks;
- second-order risks.

### Opportunities

Conditions that can create better-than-expected outcomes.

Opportunities should include:

- asymmetric advantages;
- second-order benefits;
- positive reversals of identified risks.

## Reasoning Order

The expert should think in this order:

1. Understand mission, question, goal, and constraints.
2. Define the type of problem:
   - prediction;
   - recommendation;
   - evaluation.
3. Identify expert perspective boundaries.
4. Extract assumptions.
5. Identify key factors.
6. Generate risks and opportunities from those factors.
7. Write summary.
8. Estimate confidence.

## Deterministic vs Reasoning Tasks

Deterministic:

- extracting mission data;
- aggregating expert outputs;
- counting agreement;
- comparing structured fields.

Requires reasoning:

- selecting important assumptions;
- generating risks;
- generating opportunities;
- identifying true key factors;
- estimating confidence quality.

## Current Pipeline Status

Implemented:

- expert analysis structure;
- synthesis aggregation;
- factor agreement calculation;
- confidence aggregation framework.

Not yet implemented:

- real expert reasoning quality evaluation;
- review and challenge mechanisms;
- decision gating based on analysis quality.