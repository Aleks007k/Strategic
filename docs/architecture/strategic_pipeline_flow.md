# Strategic Pipeline Flow

## Purpose

This document defines the execution flow of the strategic intelligence pipeline.

The goal is to keep the architecture modular:
- execution logic produces structured data;
- synthesis combines expert outputs;
- readiness evaluation decides whether the result is reliable enough;
- presentation converts structured output into user-facing text.

The pipeline must avoid mixing orchestration, reasoning, synthesis, and presentation responsibilities.

---

# Current Pipeline
