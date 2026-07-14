# Strategic Expert Reasoning Model

## Purpose

This document defines how a strategic expert should think before producing analysis. The goal is not to generate fast answers, but to create structured reasoning that separates facts, assumptions, risks, opportunities, and uncertainty.

A strategic expert should first understand the decision context, then reason through dependencies, and only then produce conclusions.

---

# 1. Mission Understanding

Before analysis begins, the expert must extract:

## Question

What exactly is being asked?

The expert must identify:
- the literal question;
- hidden boundaries;
- what is included;
- what is excluded.

Example:

"Should we expand into the EU market?"

is different from:

"How should we expand into the EU market?"

The first is a decision evaluation.
The second is an execution planning problem.

---

## Goal

The expert must understand what success means.

Without a defined goal:
- risks cannot be evaluated;
- opportunities cannot be prioritized;
- recommendations cannot be judged.

A risk matters only if it threatens the desired outcome.

---

## Constraints

The expert identifies limiting factors:

- budget;
- timeframe;
- resources;
- risk tolerance;
- legal limitations;
- existing capabilities.

Constraints define the realistic solution space.

---

## Expert Lens

Every expert must understand:

- what perspective they provide;
- what they are qualified to analyze;
- where their expertise ends.

An economic analyst should not replace a technology analyst.
A geopolitical analyst should not pretend to provide operational advice.

---

# 2. Internal Reasoning Questions

Before producing output, the expert asks:

## What type of question is this?

Possible categories:

- prediction;
- recommendation;
- evaluation;
- comparison;
- explanation.

Different question types require different reasoning approaches.

---

## What could make this analysis wrong?

The expert must search for:

- missing information;
- weak assumptions;
- possible alternative interpretations;
- opposing viewpoints.

---

## What is known and what is inferred?

The expert separates:

Facts:
- verified information;
- available data.

Inference:
- interpretation;
- probability;
- assumptions.

These must not be mixed.

---

## What time horizon applies?

The expert identifies whether the analysis concerns:

- short term;
- medium term;
- long term.

The same factor can have different effects depending on timeframe.

---

# 3. Assumption Identification

An assumption is included only if it is load-bearing.

Test:

"If this assumption becomes false, does the conclusion change?"

If yes — include it.

If no — ignore it.

---

## Types of assumptions

### Necessary assumptions

Required because information is unavailable.

Example:

"Assumes competitor pricing remains stable for the next 12 months."

---

### Convenience assumptions

Simplifications used to make analysis possible.

Example:

"Treats the EU market as one group despite regional differences."

---

## Assumption quality

Good assumptions are:

- specific;
- measurable;
- falsifiable.

Bad:

"Assumes normal market conditions."

Good:

"Assumes interest rates remain below X% during the next year."

---

# 4. Risk Generation

Risks must be connected to the goal.

The expert asks:

"What specific event could prevent achieving the objective?"

---

## Risk categories

### External risks

Examples:

- market changes;
- regulation;
- geopolitics;
- competitors.

---

### Execution risks

Examples:

- lack of resources;
- wrong timing;
- insufficient capabilities.

---

### Assumption failure risks

Every major assumption should have a failure scenario.

Question:

"What happens if this assumption is wrong?"

---

### Second-order risks

The expert considers risks created by attempted solutions.

Example:

Reducing costs may create quality problems.

---

# 5. Opportunity Generation

Opportunities are generated from the same factors as risks.

The expert asks:

"What could make the result better than expected?"

---

The expert searches for:

## Asymmetries

Small inputs creating disproportionate advantages.

---

## Second-order opportunities

Benefits created beyond the original goal.

Example:

Entering one market may create access to new partnerships.

---

## Reverse interpretation

The same factor can create:

- risk;
- opportunity.

The expert must examine both directions.

---

# 6. Key Factor Identification

Key factors are not a separate brainstorm.

They emerge from:

- assumptions;
- risks;
- opportunities;
- mission context.

A key factor must be:

1. influential on the outcome;
2. uncertain.

A factor that is important but already known is not a strategic driver.

The list should remain short.

---

# 7. Reasoning Order

The expert follows this sequence:

1. Understand mission.
2. Define question type.
3. Identify goal and constraints.
4. Understand expert perspective.
5. Identify assumptions.
6. Find key factors.
7. Generate risks and opportunities together.
8. Create summary.
9. Evaluate confidence.

Summary is written last because it compresses reasoning already completed.

Confidence is evaluated last because it depends on the strength of the entire reasoning chain.

---

# 8. Deterministic vs Reasoning Tasks

## Can be deterministic:

- extracting question text;
- extracting constraints;
- counting expert agreement;
- aggregating outputs;
- calculating averages.

---

## Requires real reasoning:

- deciding important assumptions;
- generating specific risks;
- generating opportunities;
- identifying true key factors;
- writing strategic conclusions;
- evaluating genuine confidence.

---

# Current Pipeline

Current architecture separates:

- deterministic aggregation;
- expert reasoning;
- synthesis;
- response formatting.

The remaining goal is connecting real reasoning capability to the existing pipeline without breaking architectural separation.