# Strategic Project Status

_Last updated: 2026-07-14_

## 1. Current architecture status

Two pipelines currently exist side by side in `backend/main.py`:

- **New Strategic Pipeline** (`StrategicExecutor` and its component chain) — the active development focus, now producing the primary displayed answer.
- **Legacy pipeline** (`StrategicSession`, `TaskPlanner`, the 3 hardcoded agents, `ResponseEngine`) — fully intact and unmodified, still executed on every run, explicitly labeled `=== Legacy pipeline output (comparison/debug only) ===`.

The new pipeline is structurally complete end-to-end (clarification → mission → reasoning → analysis → synthesis → readiness → review → localized response → persistence) but has not reached full feature parity with legacy — see Blockers below. Legacy has not been removed.

## 2. Completed components

**New pipeline:**
- Domain model: `SkillDefinition`/`SkillRegistry`/`SkillCatalog`, `AgentProfile`, `ExpertCatalog`, `Council`, `StrategicGoal`, `StrategicMission`/`MissionBuilder`, `AgentExecution`, `AnalysisSession`
- Workflow tracking: `StrategicWorkflow` (stages split into `IMPLEMENTED_STAGES` vs `PLANNED_STAGES` for honesty), `WorkflowState`, `StrategicOrchestrator`
- Clarification: `InformationGap`, `ClarificationContext`, `InformationManager`, `InputAnalysisEngine` (field-aware gap detection against long-term memory)
- Long-term memory: memory-side `UserContext`, persisted via `PreferencesManager` (load-modify-save, preserves unrelated preference keys)
- Reasoning: `SkillExecutionEngine`, `MethodologyPlanner`, `ReasoningBuilder`, `ReasoningPipeline`
- Analysis adaptation: `AnalysisResult`, `AnalysisEngine` (`reasoning_analysis_engine.py`) — builds `reasoning_context` (mission/skills/methodologies/analysis_steps/question/goals/constraints/time_horizon/expert_scope/decision_type/domain_knowledge), normalizes provider output to a fixed 6-field shape
- Providers: `MockProvider` (deterministic, context-driven content — summary/key_factors/risks/opportunities/assumptions/confidence), `AnthropicProvider`/`OllamaProvider` (upgraded to the same 6-field schema with reasoning-framework prompts)
- Synthesis: `StrategicSynthesisEngine` — perspectives, combined risks/opportunities, common/conflicting factors, factor agreement scoring, confidence averaging, `format_response()`, `assess_readiness()`
- Review gate: `StrategicReviewEngine` (deterministic `review_status`/`review_reasons`)
- Response localization: `StrategicResponseLocalizer` (ru/en labels via `LocalizationManager`, tone/detail_level-aware) — additive alongside `response_text`, not yet the primary output
- Persistence: `StrategicSessionResult`, saved automatically by `StrategicExecutor` under the `strategic_sessions` memory category on every `execute()` call
- `StrategicExecutor` — orchestrates the full chain, always returns `question`/`mission`/`selection`/`session`/`synthesis`/`readiness`/`response_text`/`review`/`localized_response_text`/`workflow_state`

**Legacy (still present, unmodified):**
- `UserContext` (session-scoped)/`UserProfile`/`PreferencesManager` (shared with new pipeline)
- Memory system: `MemoryManager`/`MemoryClassifier`/`MemoryRetriever`
- `KnowledgeLoader` (now also reused by the new pipeline for domain knowledge)
- `TaskPlanner`, `AnalysisContext`, `AgentReasoning`, `AnalysisBuilder`, `OutputValidator`
- `ResponseEngine` (ru/en, tone/detail_level aware, own private label set)
- 3 hardcoded agents: Strategic Analyst, Economic Analyst, Technology Analyst
- `LLMEngine`/`LLMRouter`/`UsageTracker`, provider fallback chain
- `engines/analysis_engine.py` (legacy synthesis — distinct class from the new `StrategicSynthesisEngine`)
- `ReviewContext` + `ConsensusEngine` (only `build_consensus()` is actually called; `ReviewEngine`/`ArgumentEngine`/`DebateEngine`/`DecisionEngine`/`EvaluationEngine` exist but are never invoked by either pipeline)

## 3. Current pipeline flow (new pipeline)

```
question
  -> InputAnalysisEngine (gap detection against long-term memory)
  -> InformationManager (clarification Q&A loop, driven by main.py)
  -> ExpertSelectionEngine (keyword-based, deterministic)
  -> MissionBuilder
  -> ReasoningPipeline (SkillExecutionEngine -> MethodologyPlanner -> ReasoningBuilder)
  -> AnalysisEngine (adapts reasoning_context incl. domain knowledge, calls llm_provider)
  -> StrategicSynthesisEngine (synthesize -> assess_readiness -> format_response)
  -> StrategicReviewEngine (review_status / review_reasons)
  -> StrategicResponseLocalizer (localized_response_text)
  -> StrategicSessionResult persisted to memory/strategic_sessions/
  -> result returned to main.py, printed as the primary answer
```

The legacy flow (`TaskPlanner` → 3 agents → legacy `AnalysisEngine.synthesize()` → `ReviewContext` → `ResponseEngine`) still runs immediately afterward, unchanged, for comparison.

## 4. Remaining blockers before v1.0

- **No real LLM content in the live wiring.** `main.py` constructs `AnalysisEngine(llm_provider=MockProvider())` — `AnthropicProvider`/`OllamaProvider` are implemented and schema-correct but untested end-to-end in this environment (no `ANTHROPIC_API_KEY`, no local Ollama reachable).
- **No consensus/review/debate/decision implementation reachable from the new pipeline.** `StrategicWorkflow.PLANNED_STAGES` (`arguments`/`review`/`debate`/`decision`/`probability`) are explicitly named as not-yet-implemented; `consensus` today is deterministic factor-counting only, not argumentation.
- **`localized_response_text` is additive only**, not yet the primary displayed/returned answer — `response_text` (fixed English) remains the primary field by contract.
- **No automated test suite** — `tests/` is empty; all verification to date has been ad-hoc scripts run per change.
- **Legacy pipeline still executes unconditionally** in `main.py` by design (for comparison); a real production entry point still needs a decision on when/how to retire it.
- **`ExpertCatalog` is explicitly a temporary hardcoded default** (3 experts), marked with its own TODO for replacement by a generic expert provider.

## 5. Future V2 capabilities (planned, not implemented)

- A real consensus/review/debate/decision layer for the new pipeline (the five `PLANNED_STAGES`).
- Wiring `ExpertEvaluation`/`WeightedSynthesisEngine` (built as standalone foundations, never connected to `StrategicExecutor`) for weighted, confidence-adjusted synthesis.
- A generic/dynamic expert provider to replace the hardcoded `ExpertCatalog` default set.
- Promoting `localized_response_text` to the primary response once real-provider content quality is proven.
- Full retirement of the legacy pipeline once the above close the remaining gap to feature parity (per the existing Architecture Decision on legacy deprecation).

## 6. Migration status: Legacy -> New Strategic Pipeline

Migration has proceeded incrementally and is substantial: gap detection, clarification, expert selection, mission building, reasoning generation, per-expert analysis, synthesis, a readiness gate, a review gate, domain-knowledge grounding, preference-aware localization, and automatic session persistence are all implemented and wired into `StrategicExecutor`. The new pipeline's output is now displayed as the primary answer in `main.py`, with legacy explicitly demoted to a labeled comparison/debug block.

**Not yet complete.** The most recent architecture audit found the new pipeline is not yet a safe full replacement: it currently lacks real LLM-generated content in its live wiring, has no implemented consensus/review/debate/decision layer, and has not been validated with domain-knowledge-grounded output from a real provider. Legacy remains fully in place until these gaps close.
