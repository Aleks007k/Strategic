# Strategic — Architecture Decisions

This document records the key architectural decisions behind the Strategic backend, why each decision was made, and where each piece is expected to grow. It exists so future changes are made *with* the system's intent rather than against it.

---

## 1. Project Vision

Strategic is a **multi-agent strategic reasoning system**, not a simple chatbot.

The goal is not to produce a single fast answer to a question. The goal is to produce a strategic answer that has been:

- analyzed from multiple expert perspectives,
- debated and cross-examined between those perspectives,
- checked for consensus and disagreement,
- evaluated for whether it is actually ready to be trusted,
- and only then formed into a final strategic response.

Speed and a single-model chat loop are explicitly *not* the design target. Depth, traceability, and reasoning quality are.

---

## 2. Architecture Decisions

### Workflow separates process control from individual engines

- **Decision:** The ordered pipeline of stages (`clarification → planning → agents → arguments → review → debate → consensus → decision → probability → response`) is defined once, centrally, in `StrategicWorkflow` — independent of the engines that actually perform each stage's work (`AnalysisEngine`, `ReviewEngine`, `DebateEngine`, `ConsensusEngine`, `DecisionEngine`, etc.).
- **Reason:** If the workflow and the engines were tangled together, changing the *order* of reasoning (e.g. running debate before review) would require touching every engine's code. Separating "what stage comes next" from "what a stage does" keeps each engine focused on one job and lets the sequence itself be reasoned about, tested, and changed independently.
- **Future expansion:** Conditional branches (e.g. skip debate when there's only one expert), parallel stages, or per-mission custom pipelines become possible without rewriting engines.

### WorkflowState stores current analysis progress

- **Decision:** `WorkflowState` tracks `current_stage`, `completed_stages`, and free-form `data` for an in-progress run, separately from the static pipeline definition.
- **Reason:** A pipeline definition is just a map; something needs to record *where a specific run actually is* on that map, including partial results accumulated along the way. Keeping this as a distinct object (not baked into the workflow definition, and not baked into `session.py`) means progress can be inspected, paused, resumed, or persisted independently of both the pipeline shape and the session that's driving it.
- **Future expansion:** Persisting `WorkflowState` to disk enables resumable, long-running missions; exposing it externally enables progress UIs.

### Skills are objects with methodology, use cases and limitations, not simple labels

- **Decision:** A skill (`SkillDefinition`) is a structured object — `name`, `description`, `category`, `methodology`, `use_cases`, `limitations` — not just a string tag.
- **Reason:** A bare label like `"economics"` tells the system nothing about *when* to use the skill, *how* it reasons, or *where it breaks down*. Capturing methodology and limitations up front means matching, selection, and (eventually) prompting can be grounded in what a skill actually is, not just its name — and it keeps a place to record known weaknesses instead of silently trusting every skill equally.
- **Future expansion:** Limitations can feed directly into the evaluation/confidence layers; methodology can inform how an LLM provider is prompted per skill.

### SkillRegistry stores skill definitions

- **Decision:** `SkillRegistry` is a generic, name-keyed store for skills, accepting either a `SkillDefinition` object or (for backward compatibility) a plain string, and serializing whichever was stored via a duck-typed `to_dict()`.
- **Reason:** Storage and lookup are a separate concern from *what a skill is*. Keeping `SkillRegistry` generic (and dependency-free — no import of `SkillDefinition`) means it can hold any future skill representation without needing to change, and existing string-based registrations keep working unmodified.
- **Future expansion:** Backing the registry with persistent storage, tagging, or search doesn't require touching `SkillDefinition` at all.

### AgentProfile represents expert identity and capabilities

- **Decision:** `AgentProfile` (`name`, `role`, `description`, `skills`) represents *who an expert is*, independent of the runtime agent classes (`StrategicAnalyst`, `EconomicAnalyst`, `TechnologyAnalyst`) that actually execute.
- **Reason:** Identity/capability metadata and execution logic are different lifecycles — a profile can be catalogued, selected, and reasoned about without ever running anything. Keeping them separate also means new experts can be *described* (added to a catalog, assigned to a council) before any corresponding executable agent exists.
- **Future expansion:** Profiles become the natural unit for dynamically generating or configuring agents rather than hardcoding one Python class per expert.

### ExpertCatalog stores available experts

- **Decision:** `ExpertCatalog` holds the full set of known `AgentProfile`s and seeds a deterministic default set (Economic/Geopolitical/Technology Strategist), with each profile's skills cross-validated against a `SkillCatalog` rather than trusted as free-text.
- **Reason:** There needs to be a single source of truth for "which experts exist and what can they do," separate from any one mission. Validating skill assignments against the actual `SkillCatalog` (rather than hardcoding matching strings and hoping they stay in sync) keeps expert definitions honest as the skill catalog evolves.
- **Future expansion:** Loading experts from configuration/data files instead of hardcoded Python, or supporting per-organization custom expert rosters.

### Council represents the selected group of experts for a mission

- **Decision:** `Council` (`experts`, `purpose`) is a *subset* of the catalog, assembled for one specific mission, with duplicate-prevention on add.
- **Reason:** Not every mission needs every expert. Separating "all experts that exist" (`ExpertCatalog`) from "the experts convened for this question" (`Council`) keeps missions scoped and makes the reasoning process auditable — you can see exactly who was asked, not just who was available.
- **Future expansion:** Council composition could become the output of `ExpertSelectionEngine` automatically, rather than manually assembled.

### StrategicGoal defines optimization target

- **Decision:** `StrategicGoal` (`name`, `description`, `priority`, `criteria`) captures *what a good outcome looks like* for a mission, as a first-class object distinct from the question itself.
- **Reason:** A question ("How will Europe change economically?") and a goal ("optimize for identifying investable trends over ten years") are not the same thing, and conflating them makes it impossible to evaluate whether an answer actually succeeded. An explicit goal with criteria gives the evaluation layers something concrete to check against.
- **Future expansion:** Criteria could become machine-checkable conditions feeding directly into `EvaluationEngine`, rather than descriptive text.

### StrategicMission connects question, goal, council and constraints

- **Decision:** `StrategicMission` is the top-level unit of work — it ties together the question, the goal, the council convened to answer it, and any constraints, without importing any of those classes (pure duck typing on `.to_dict()`).
- **Reason:** A mission is the natural "unit of reasoning" the rest of the system operates on. Keeping it dependency-free from its own components means the mission object stays stable even as `StrategicGoal`, `Council`, or their internals evolve independently.
- **Future expansion:** Missions become the natural persistence/audit unit — a full record of what was asked, why, by whom, and under what constraints.

### AgentExecution represents a specific expert run

- **Decision:** `AgentExecution` (`agent`, `mission`, `skills_used`, `instructions`) captures one concrete execution of one expert against one mission, recording exactly which skills were actually invoked.
- **Reason:** `AgentProfile` describes what an expert *can* do in general; `AgentExecution` records what one expert *actually did* on one occasion. That distinction is what makes later review, debate, and evaluation possible — you can't cross-examine a capability, only an actual output tied to actual skills used.
- **Future expansion:** A natural audit trail for cost tracking, quality scoring per skill, or replaying a specific expert's reasoning.

### Consensus, Review, Debate and Decision layers exist to improve reasoning quality

- **Decision:** `ConsensusEngine`, `ReviewEngine`, `DebateEngine`, and `DecisionEngine` form a deliberate chain: measure agreement → generate cross-agent feedback → resolve support/challenge per pair → classify each agent's output as accepted, rejected, or needing review.
- **Reason:** A single agent's answer is just an opinion. Comparing multiple experts' answers, letting them (structurally) challenge each other, and only then deciding what to trust is what turns independent outputs into something closer to a genuine strategic judgment — and it produces an explicit, inspectable trail for *why* a conclusion was accepted or flagged, rather than a black box.
- **Future expansion:** This is the layer most likely to gain real LLM-driven reasoning later (e.g. actual argumentative debate rather than summary-string comparison) — the deterministic scaffolding built first defines the exact shape that future intelligence needs to fill.

### Vertical Slice Development

- **Decision:** After completing the core infrastructure, development should continue primarily through vertical slices instead of creating many isolated foundation classes.
- **Reason:** This allows the system to become executable earlier, exposes architectural weaknesses sooner, improves testing, and gradually transforms the architecture into a working strategic reasoning system.
- **Future expansion:** Each new vertical slice should integrate existing components before introducing new abstractions.

### Value-Driven Components

- **Decision:** Every newly introduced class must add unique architectural value. Components that only duplicate responsibilities of existing classes should not be created.
- **Reason:** Prevents unnecessary complexity, reduces architectural drift, and keeps the Strategic architecture maintainable.
- **Future expansion:** Future architecture reviews may merge or remove components that violate this principle.

### User Memory Before Clarification

- **Decision:** Before requesting additional information from the user, Strategic must first use all reliable long-term knowledge already available about the user.
- **Reason:** Strategic should never ask questions that it already knows the answer to. This creates a significantly more intelligent strategic assistant and reduces unnecessary interaction.
- **Future expansion:** Memory confidence scoring. Memory freshness. User-controlled memory editing.

### Executable Skills

- **Decision:** Skills are not only metadata. In future versions every Skill will become an executable methodology capable of producing structured intermediate reasoning.
- **Reason:** Experts should differ because they execute different methodologies, not because they use different prompts.
- **Future expansion:** Executable methodologies. Skill chaining. Reusable reasoning modules. Probabilistic skill outputs.

### Expert Weighting System

- **Decision:** Strategic does not treat all expert opinions as equal. Expert contributions should be weighted based on relevance, expertise, skills, confidence, and future performance history.
- **Reason:** Strategic decisions require synthesis of specialized knowledge rather than simple averaging of opinions.
- **Future expansion:**
  - domain relevance scoring
  - expertise confidence
  - historical prediction accuracy
  - dynamic weights based on question context
  - user-adjustable weighting preferences

---

## 3. Design Principles

- **Do not optimize only for speed; optimize for quality of strategic reasoning.** A faster wrong answer is not a better answer. Every layer added (review, debate, consensus, evaluation) trades latency for reliability on purpose.
- **Avoid making all agents identical.** Experts exist because different domains require different framing, knowledge, and thinking styles — collapsing them into one generic "answer machine" would defeat the point of a multi-agent system.
- **Preserve expert specialization.** Each agent's skills, knowledge domain, and role should stay distinct and legible, not blended into an undifferentiated general-purpose blob.
- **Prefer modular architecture.** Components (engines, contexts, catalogs) should be independently understandable, testable, and replaceable — no component should need to know the internals of another to do its job.
- **Future AI providers/models should be replaceable.** The provider/router/fallback architecture exists so that swapping or adding an LLM provider is a configuration and provider-class change, never a rewrite of agents, sessions, or engines.
- **Simple deterministic foundations first, intelligence layers later.** Every engine in this system started as a deterministic, keyword-based, or rule-based placeholder with the exact output shape real intelligence will eventually fill. This is deliberate: it proves the architecture and data flow work correctly before any AI cost, latency, or non-determinism is introduced.
