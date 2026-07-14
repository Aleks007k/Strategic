# Strategic Pipeline Design Principles

## Separation of Responsibilities

Each component should have one clear responsibility.

The architecture separates:

- reasoning generation;
- data normalization;
- synthesis;
- quality evaluation;
- presentation.

Components should not silently absorb responsibilities from other layers.

## Data Before Presentation

Structured data is the source of truth.

Rules:

- analysis objects contain information;
- synthesis objects combine information;
- formatting only displays information.

Do not store generated presentation text inside analytical structures.

## Deterministic Where Possible

Operations that do not require intelligence should remain deterministic.

Examples:

- counting;
- aggregation;
- validation;
- scoring;
- formatting.

This improves:

- reproducibility;
- testing;
- debugging.

## Reasoning Where Necessary

Tasks requiring understanding should remain with reasoning systems.

Examples:

- identifying important assumptions;
- evaluating uncertainty;
- generating risks;
- finding opportunities;
- creating strategic conclusions.

Do not replace reasoning with artificial rules.

## Preserve Traceability

The system must preserve:

- which expert produced information;
- why factors appeared;
- how agreement was calculated;
- where uncertainty exists.

A final conclusion should always be traceable back to source analysis.

## Avoid Hidden Coupling

New architecture should not depend on legacy-specific structures.

Reuse is allowed for:

- general infrastructure;
- shared abstractions;
- independent utilities.

Avoid importing:

- legacy agents;
- legacy contexts;
- legacy output formats.

## Incremental Migration

Development follows:

1. Build new capability.
2. Verify independently.
3. Compare with legacy behavior.
4. Replace only after parity.

Never remove a working system before the replacement is proven.