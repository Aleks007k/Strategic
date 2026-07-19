"""
Strategic AI Core Backend
Reasoning package analysis engine
"""

import re

from core.analysis_result import AnalysisResult
from knowledge.knowledge_loader import KnowledgeLoader

# Mirrors the domain each legacy agent is hardcoded to load
# (StrategicAnalyst -> geopolitics, EconomicAnalyst -> economics,
# TechnologyAnalyst -> technology), applied to the new pipeline's
# default expert names.
EXPERT_DOMAIN_MAP = {
    "Economic Strategist": "economics",
    "Geopolitical Strategist": "geopolitics",
    "Technology Strategist": "technology",
}


class AnalysisEngine:
    def __init__(self, llm_provider=None):
        self.llm_provider = llm_provider
        self.knowledge_loader = KnowledgeLoader()

    def analyze(self, reasoning_package) -> dict:
        if self.llm_provider is not None:
            agent_name = reasoning_package.get("agent")
            mission = reasoning_package.get("mission", {})
            question = mission.get("question")
            goal = mission.get("goal")
            constraints = [
                c for c in mission.get("constraints", [])
                if isinstance(c, str) and c
            ]
            skills_list = [
                s for s in reasoning_package.get("skills", [])
                if isinstance(s, str) and s
            ]
            domain_knowledge = self._load_domain_knowledge(agent_name)

            # Internal scaffold for the future Hypothesis Layer (see
            # docs/STRATEGIC_HYPOTHESIS_LAYER.md). Deterministic; not yet
            # resolved, not sent to the provider, and not exposed in the
            # returned result.
            null_contradicting = []
            null_contradicting.extend(f"Specific constraint present: '{c}'." for c in constraints)
            null_contradicting.extend(f"Specific skill/lens present: '{s}'." for s in skills_list)
            if isinstance(goal, dict) and goal.get("name"):
                null_contradicting.append(f"Specific goal present: '{goal.get('name')}'.")
            null_supporting = [] if null_contradicting else [
                "No constraints, skills, or goal were specified, "
                "consistent with an undifferentiated baseline situation."
            ]

            # Hypotheses are built in two passes: first statement/evidence for
            # every hypothesis (needed to compute the diagnosticity matrix
            # across all of them), then status is assigned once every
            # hypothesis's evidence - and therefore the matrix - is known.
            hypotheses = [
                {
                    "statement": (
                        f"The situation described by '{question}' "
                        "does not differ materially from the current baseline; no unusual action is required."
                    ),
                    "type": "null",
                    "supporting_evidence": null_supporting,
                    "contradicting_evidence": null_contradicting,
                }
            ]
            allow_contradiction_flags = [False]
            sources = [None]
            # Evidence provenance ("domain_knowledge"/"question"), tracked
            # alongside the evidence itself as it's generated - not inferred
            # later from string content. Index-aligned with hypotheses; the
            # null hypothesis's evidence isn't domain/question-derived, so it
            # has no provenance entries.
            provenance_maps = [{}]

            for constraint in constraints:
                constraint_supporting, constraint_provenance = self._find_supporting_evidence(
                    constraint, question, domain_knowledge
                )
                constraint_contradicting = []
                hypotheses.append({
                    "statement": (
                        f"The outcome is primarily constrained by '{constraint}', and the situation "
                        "should be understood through this limiting factor rather than the baseline alone."
                    ),
                    "type": "constraint",
                    "supporting_evidence": constraint_supporting,
                    "contradicting_evidence": constraint_contradicting,
                })
                allow_contradiction_flags.append(True)
                sources.append(constraint)
                provenance_maps.append(constraint_provenance)

            for skill in skills_list:
                skill_supporting, skill_provenance = self._find_supporting_evidence(
                    skill, question, domain_knowledge
                )
                skill_contradicting = []
                hypotheses.append({
                    "statement": (
                        f"The expert perspective is primarily shaped by '{skill}', and the situation "
                        "should be examined through this analytical lens rather than the baseline alone."
                    ),
                    "type": "skill",
                    "supporting_evidence": skill_supporting,
                    "contradicting_evidence": skill_contradicting,
                })
                allow_contradiction_flags.append(True)
                sources.append(skill)
                provenance_maps.append(skill_provenance)

            # Internal scaffold: deterministic ACH-style diagnosticity matrix
            # (see docs/STRATEGIC_HYPOTHESIS_LAYER.md §5). Exact string equality
            # only. Not exposed, not sent to the provider. Built from evidence
            # alone, before status, so status evaluation can be
            # diagnosticity-aware.
            all_evidence = []
            for hypothesis in hypotheses:
                all_evidence.extend(hypothesis.get("supporting_evidence") or [])
                all_evidence.extend(hypothesis.get("contradicting_evidence") or [])
            all_evidence = list(dict.fromkeys(all_evidence))

            diagnosticity_matrix = {}
            for evidence in all_evidence:
                marks = {}
                for hypothesis_index, hypothesis in enumerate(hypotheses):
                    supporting = hypothesis.get("supporting_evidence") or []
                    contradicting = hypothesis.get("contradicting_evidence") or []
                    if evidence in supporting:
                        marks[str(hypothesis_index)] = "C"
                    elif evidence in contradicting:
                        marks[str(hypothesis_index)] = "I"
                    else:
                        marks[str(hypothesis_index)] = "N/A"
                diagnosticity_matrix[evidence] = marks

            # Derived from each hypothesis's explicit "type" field: competitors
            # are only hypotheses that share the same type (skill vs. skill,
            # constraint vs. constraint) - the type field is the single source
            # of truth for hypothesis origin, not index position.
            indices_by_type = {}
            for index, hypothesis in enumerate(hypotheses):
                indices_by_type.setdefault(hypothesis.get("type"), set()).add(str(index))

            for hypothesis_index, hypothesis in enumerate(hypotheses):
                hypothesis_type = hypothesis.get("type")
                hypothesis["status"] = self._evaluate_status(
                    hypothesis["supporting_evidence"],
                    hypothesis["contradicting_evidence"],
                    allow_contradiction_to_reject=allow_contradiction_flags[hypothesis_index],
                    diagnosticity_matrix=diagnosticity_matrix,
                    hypothesis_index=hypothesis_index,
                    hypothesis_type=hypothesis_type,
                    competitor_indices=indices_by_type.get(hypothesis_type),
                )

            # Internal scaffold: deterministic evidence quality weighting based
            # on provenance (see docs/STRATEGIC_HYPOTHESIS_LAYER.md). Not
            # exposed, not sent to the provider, and not consulted by
            # ranking/status/scoring/assumptions. Computed before causal
            # graphs so graph construction can attach quality nodes.
            provenance_weights = {"domain_knowledge": 2, "question": 1}

            evidence_quality = {}
            for hypothesis_index in range(len(hypotheses)):
                for evidence, provenance in provenance_maps[hypothesis_index].items():
                    weight = provenance_weights.get(provenance, 0)
                    current = evidence_quality.get(evidence)
                    if current is None or weight > current["weight"]:
                        evidence_quality[evidence] = {"provenance": provenance, "weight": weight}

            for evidence in all_evidence:
                if evidence not in evidence_quality:
                    evidence_quality[evidence] = {"provenance": None, "weight": 0}

            # Internal scaffold for the future Causal Reasoning Layer (see
            # docs/STRATEGIC_HYPOTHESIS_LAYER.md). Deterministic; not yet
            # consulted by evidence/ranking, not sent to the provider, and
            # not exposed in the returned result.
            causal_graphs = [
                self._build_causal_graph(
                    hypothesis,
                    source=sources[index],
                    evidence_provenance=provenance_maps[index],
                    evidence_quality=evidence_quality,
                )
                for index, hypothesis in enumerate(hypotheses)
            ]

            # Empty scaffold for the future Decision Impact layer (see
            # docs/STRATEGIC_HYPOTHESIS_LAYER.md). No inference yet - lists
            # stay empty. Not exposed, not sent to the provider, and not
            # consulted by ranking/status/scoring/assumptions.
            decision_impacts = [
                {
                    "hypothesis_index": index,
                    "statement": hypothesis["statement"],
                    "hypothesis_type": hypothesis.get("type"),
                    "hypothesis_status": hypothesis.get("status"),
                    "supports_action": [],
                    "blocks_action": [],
                    # Scaffold only: no actions exist yet, so no action
                    # strings/IDs are inserted regardless of status.
                    "impact_state": "unresolved",
                    # Scaffold only: not derived from hypothesis_type/status/
                    # statement/evidence/constraints/skills.
                    "impact_category": None,
                    "related_actions": [],
                    # Scaffold only: not derived from statement/evidence/
                    # skills/constraints/status.
                    "affected_decision_areas": [],
                }
                for index, hypothesis in enumerate(hypotheses)
            ]

            # decision_action_schema is a shape reference only - it documents
            # the fields a future decision action will have. It is never
            # instantiated or added to decision_model["actions"].
            decision_action_schema = {
                "id": None,
                "description": None,
                "triggered_by_hypotheses": [],
                "blocked_by_hypotheses": [],
                "confidence": None,
            }

            # First deterministic decision criterion, mirroring the existing
            # decision_evaluations criterion string. Not yet connected to
            # evaluations - registry only.
            decision_criteria = {
                "criteria": [
                    {
                        "id": "criterion_1",
                        "name": "supported_by_surviving_hypothesis",
                        "description": "Action is supported by a surviving hypothesis",
                        "weight": 1,
                        "category": "support",
                    }
                ],
            }

            # First deterministic decision action candidates: one per
            # surviving hypothesis only, built from existing data alone (no
            # inference beyond status). Local only - not connected to
            # decision_action_registry, decision_model, or anything else yet.
            #
            # decision_action_links connects each generated action back to its
            # originating hypothesis. The hypothesis index comes straight from
            # this generation loop, not parsed from the action ID or any
            # hypothesis text.
            generated_actions = []
            decision_action_links = []
            for hypothesis_index, hypothesis in enumerate(hypotheses):
                if hypothesis["status"] == "surviving":
                    action_id = f"action_{hypothesis_index}"
                    generated_actions.append({
                        "id": action_id,
                        "name": hypothesis["statement"],
                        "description": None,
                        "category": None,
                        "required_resources": [],
                        "risks": [],
                        "expected_outcomes": [],
                    })
                    decision_action_links.append({
                        "hypothesis_index": hypothesis_index,
                        "action_id": action_id,
                        "relationship": "supports",
                    })

            # decision_action_registry: structural registration only - id,
            # name, description, category. required_resources/risks/
            # expected_outcomes/score/readiness/evidence/provenance/
            # diagnosticity stay exclusively in their own existing structures.
            decision_action_registry = [
                {
                    "id": action["id"],
                    "name": action["name"],
                    "description": action["description"],
                    "category": action["category"],
                }
                for action in generated_actions
            ]

            # decision_model registers candidate actions by ID only - it does
            # not duplicate generated_actions' content (name/description/
            # category/resources/risks/outcomes stay only in
            # generated_actions). links mirrors decision_action_links exactly
            # - no new links, no evaluation. Not sent to the provider.
            decision_model = {
                "actions": [
                    {"action_id": entry["id"], "registry_id": entry["id"]}
                    for entry in decision_action_registry
                ],
                "links": [
                    {
                        "action_id": link["action_id"],
                        "hypothesis_index": link["hypothesis_index"],
                        "relationship": link["relationship"],
                    }
                    for link in decision_action_links
                ],
            }

            # Consistency trace only - checks that decision_action_registry,
            # generated_actions, and decision_model agree with each other.
            # No new actions, no ranking, no conclusions - pure existence
            # checks.
            decision_registry_consistency_trace = {
                entry["id"]: {
                    "action_id": entry["id"],
                    "exists_in_generated_actions": any(
                        action["id"] == entry["id"] for action in generated_actions
                    ),
                    "exists_in_decision_model": any(
                        item["registry_id"] == entry["id"] for item in decision_model["actions"]
                    ),
                }
                for entry in decision_action_registry
            }

            # First deterministic decision evaluations: one purely structural
            # entry per decision_action_links entry. No aggregation,
            # normalization, confidence calculation, action comparison, or
            # recommendation generation - just a fixed criterion/impact
            # reflecting that the action is backed by a surviving hypothesis.
            decision_evaluations = [
                {
                    "action_id": link["action_id"],
                    "criterion_id": decision_criteria["criteria"][0]["id"],
                    "criterion": "supported_by_surviving_hypothesis",
                    "impact": 1,
                    "supporting_hypotheses": [link["hypothesis_index"]],
                    "blocking_hypotheses": [],
                }
                for link in decision_action_links
            ]

            # Score aggregation, now resolving each evaluation's criterion
            # weight through the decision_criteria registry rather than using
            # impact alone. Still a plain sum - no comparison, sorting,
            # best-action selection, or normalization.
            criterion_weights = {
                criterion["id"]: criterion["weight"]
                for criterion in decision_criteria["criteria"]
            }

            decision_scores = {action["id"]: 0 for action in generated_actions}
            for evaluation in decision_evaluations:
                weight = criterion_weights[evaluation["criterion_id"]]
                decision_scores[evaluation["action_id"]] += evaluation["impact"] * weight

            # Explanation structure only - shows how each action's score was
            # formed. Does not compute a new score or replace decision_scores.
            decision_score_breakdown = {action["id"]: [] for action in generated_actions}
            for evaluation in decision_evaluations:
                weight = criterion_weights[evaluation["criterion_id"]]
                decision_score_breakdown[evaluation["action_id"]].append({
                    "criterion_id": evaluation["criterion_id"],
                    "impact": evaluation["impact"],
                    "weight": weight,
                    "contribution": evaluation["impact"] * weight,
                })

            # Traceability only - connects each generated action back to the
            # supporting_evidence of the hypothesis that produced it, via the
            # existing decision_action_links. decision_action_links only ever
            # contains surviving hypotheses (see the generation loop above),
            # so unresolved hypotheses and contradicting evidence never
            # appear here without any extra filtering.
            decision_action_evidence = {action["id"]: [] for action in generated_actions}
            for link in decision_action_links:
                hypothesis = hypotheses[link["hypothesis_index"]]
                for evidence in hypothesis["supporting_evidence"]:
                    decision_action_evidence[link["action_id"]].append({
                        "hypothesis_index": link["hypothesis_index"],
                        "evidence": evidence,
                    })

            # Structural provenance only - where each action came from
            # (hypothesis identity/type/status + evidence provenance), read
            # entirely from existing hypotheses/provenance_maps. No quality
            # or score calculation. decision_action_links only ever contains
            # surviving hypotheses, so unresolved ones never appear here.
            decision_action_provenance = {
                action["id"]: {
                    "hypothesis_index": None,
                    "hypothesis_type": None,
                    "hypothesis_status": None,
                    "evidence_provenance": [],
                }
                for action in generated_actions
            }
            for link in decision_action_links:
                hypothesis_index = link["hypothesis_index"]
                hypothesis = hypotheses[hypothesis_index]
                provenance_lookup = provenance_maps[hypothesis_index]
                decision_action_provenance[link["action_id"]] = {
                    "hypothesis_index": hypothesis_index,
                    "hypothesis_type": hypothesis["type"],
                    "hypothesis_status": hypothesis["status"],
                    "evidence_provenance": [
                        {
                            "evidence": evidence,
                            "provenance": provenance_lookup.get(evidence),
                        }
                        for evidence in hypothesis["supporting_evidence"]
                    ],
                }

            # Quality trace only - re-exposes each action's evidence quality
            # (provenance/weight) from the existing evidence_quality registry.
            # No recalculation, no scoring, no ranking.
            decision_action_quality_trace = {
                action_id: [
                    {
                        "evidence": evidence,
                        "provenance": evidence_quality[evidence]["provenance"],
                        "weight": evidence_quality[evidence]["weight"],
                    }
                    for evidence in [item["evidence"] for item in items]
                ]
                for action_id, items in decision_action_evidence.items()
            }

            # Internal scaffold: unified evidence evaluation, combining the
            # existing diagnosticity_matrix and evidence_quality without
            # computing anything new. Not exposed, not sent to the provider,
            # and not consulted by ranking/status/scoring/assumptions. Built
            # here (rather than nearer its later ranking use) so the decision
            # action diagnosticity trace below can read it too.
            evidence_evaluation = {
                evidence: {
                    "quality": evidence_quality.get(evidence, {"provenance": None, "weight": 0}),
                    "diagnosticity": marks,
                }
                for evidence, marks in diagnosticity_matrix.items()
            }

            # Diagnosticity trace only - re-exposes each action's evidence
            # diagnosticity marks from the existing evidence_evaluation
            # registry. No recalculation, no scoring, no ranking.
            decision_action_diagnosticity_trace = {
                action_id: [
                    {
                        "evidence": evidence,
                        "diagnosticity": evidence_evaluation[evidence]["diagnosticity"],
                    }
                    for evidence in [item["evidence"] for item in items]
                ]
                for action_id, items in decision_action_evidence.items()
            }

            # Score trace only - re-exposes each action's already-computed
            # final score and breakdown. No recalculation, no ranking, no
            # comparison.
            decision_action_score_trace = {
                action["id"]: {
                    "final_score": decision_scores[action["id"]],
                    "breakdown": decision_score_breakdown[action["id"]],
                }
                for action in generated_actions
            }

            # Completeness trace only - reflects presence of already existing
            # per-action structures. No calculation, no interpretation of
            # whether an action is good or bad.
            decision_action_completeness_trace = {
                action["id"]: {
                    "has_evidence": bool(decision_action_evidence[action["id"]]),
                    "has_provenance": bool(
                        decision_action_provenance[action["id"]]["evidence_provenance"]
                    ),
                    "has_quality_trace": bool(decision_action_quality_trace[action["id"]]),
                    "has_diagnosticity_trace": bool(
                        decision_action_diagnosticity_trace[action["id"]]
                    ),
                    "has_score_trace": bool(decision_action_score_trace[action["id"]]),
                }
                for action in generated_actions
            }

            # Readiness summary only - derives ready/missing purely from the
            # existing completeness trace. No comparison, no best-action
            # selection, no recommendations.
            decision_action_readiness = {}
            for action in generated_actions:
                action_id = action["id"]
                completeness = decision_action_completeness_trace[action_id]

                missing = []
                if completeness["has_evidence"] is False:
                    missing.append("evidence")
                if completeness["has_provenance"] is False:
                    missing.append("provenance")
                if completeness["has_quality_trace"] is False:
                    missing.append("quality_trace")
                if completeness["has_diagnosticity_trace"] is False:
                    missing.append("diagnosticity_trace")
                if completeness["has_score_trace"] is False:
                    missing.append("score_trace")

                decision_action_readiness[action_id] = {
                    "action_id": action_id,
                    "ready": len(missing) == 0,
                    "missing": missing,
                }

            # Summary only - collects already existing per-action data into
            # one structural view. No comparison, sorting, best-action
            # selection, new scoring, or recommendations.
            decision_action_summary = {
                action["id"]: {
                    "action_id": action["id"],
                    "name": action["name"],
                    "readiness": decision_action_readiness[action["id"]],
                    "score": decision_scores[action["id"]],
                    "evidence_count": len(decision_action_evidence[action["id"]]),
                    "has_complete_trace": (
                        decision_action_completeness_trace[action["id"]]["has_evidence"]
                        and decision_action_completeness_trace[action["id"]]["has_provenance"]
                        and decision_action_completeness_trace[action["id"]]["has_quality_trace"]
                        and decision_action_completeness_trace[action["id"]]["has_diagnosticity_trace"]
                        and decision_action_completeness_trace[action["id"]]["has_score_trace"]
                    ),
                }
                for action in generated_actions
            }

            # Explainability trace only - assembles already existing
            # per-action structures into one combined view. No
            # recalculation, no text generation, no interpretation.
            decision_action_explainability_trace = {
                action["id"]: {
                    "action_id": action["id"],
                    "summary": decision_action_summary[action["id"]],
                    "evidence": decision_action_evidence[action["id"]],
                    "quality": decision_action_quality_trace[action["id"]],
                    "diagnosticity": decision_action_diagnosticity_trace[action["id"]],
                    "score": decision_action_score_trace[action["id"]],
                    "readiness": decision_action_readiness[action["id"]],
                }
                for action in generated_actions
            }

            # Combined index only - links every generated action to its
            # existing traces (registry/summary/explainability/readiness/
            # consistency) for direct lookup. No recalculation, no new
            # inference. Placed here (rather than right after
            # decision_registry_consistency_trace) because summary,
            # readiness, and explainability aren't built until this point.
            decision_action_registry_by_id = {
                entry["id"]: entry for entry in decision_action_registry
            }
            decision_action_trace_index = {
                action["id"]: {
                    "action_id": action["id"],
                    "registry": decision_action_registry_by_id[action["id"]],
                    "summary": decision_action_summary[action["id"]],
                    "explainability": decision_action_explainability_trace[action["id"]],
                    "readiness": decision_action_readiness[action["id"]],
                    "consistency": decision_registry_consistency_trace[action["id"]],
                }
                for action in generated_actions
            }

            # Identity/link integrity check only - verifies the already
            # assembled decision_action_trace_index is internally consistent.
            # No inspection of evidence/quality/diagnosticity/scores/
            # hypotheses/statements, no ranking, no score changes.
            decision_action_integrity_check = {}
            for action_id, trace in decision_action_trace_index.items():
                issues = []
                if trace["action_id"] != action_id:
                    issues.append("action_id_mismatch")
                if trace["registry"]["id"] != action_id:
                    issues.append("registry_mismatch")
                if trace["summary"]["action_id"] != action_id:
                    issues.append("summary_mismatch")
                if trace["readiness"]["action_id"] != action_id:
                    issues.append("readiness_mismatch")
                if trace["consistency"]["action_id"] != action_id:
                    issues.append("consistency_mismatch")

                decision_action_integrity_check[action_id] = {
                    "action_id": action_id,
                    "valid": len(issues) == 0,
                    "issues": issues,
                }

            # Validation summary only - aggregates the already existing
            # integrity check results. No recalculation, no new inspection,
            # no comparison between actions.
            decision_action_validation_summary = {
                action_id: {
                    "action_id": action_id,
                    "valid": integrity["valid"],
                    "issue_count": len(integrity["issues"]),
                    "issues": integrity["issues"],
                }
                for action_id, integrity in decision_action_integrity_check.items()
            }

            # Final assembled trace only - bundles the already-built decision
            # layers per action. No recalculation, no new inspection, no
            # ranking or selection.
            decision_action_final_trace = {
                action["id"]: {
                    "action_id": action["id"],
                    "summary": decision_action_summary[action["id"]],
                    "score": decision_action_score_trace[action["id"]],
                    "readiness": decision_action_readiness[action["id"]],
                    "validation": decision_action_validation_summary[action["id"]],
                    "integrity": decision_action_integrity_check[action["id"]],
                }
                for action in generated_actions
            }

            # Export projection only - a clean structural view of
            # decision_action_final_trace. No recalculation, no new
            # inspection, no ranking or selection.
            decision_action_export_view = {
                action_id: {
                    "action_id": action_id,
                    "summary": trace["summary"],
                    "score": trace["score"],
                    "ready": trace["readiness"]["ready"],
                    "valid": trace["validation"]["valid"],
                    "issues": trace["validation"]["issues"],
                }
                for action_id, trace in decision_action_final_trace.items()
            }

            # Audit log only - fixed, hardcoded source labels documenting
            # where each export field came from. Not calculated dynamically,
            # no inspection of quality/evidence/hypotheses/scores/provenance.
            decision_action_audit_log = {
                action_id: {
                    "action_id": action_id,
                    "sources": {
                        "summary": "decision_action_final_trace.summary",
                        "score": "decision_action_final_trace.score",
                        "ready": "decision_action_final_trace.readiness.ready",
                        "valid": "decision_action_final_trace.validation.valid",
                        "issues": "decision_action_final_trace.validation.issues",
                    },
                }
                for action_id in decision_action_export_view
            }

            # Status summary only - a deterministic boolean combination of
            # existing export fields. No inspection of hypotheses/evidence/
            # diagnosticity/provenance/scores/ranking/quality.
            decision_action_status_summary = {
                action_id: {
                    "action_id": action_id,
                    "ready": export_view["ready"],
                    "valid": export_view["valid"],
                    "status": (
                        "ready" if export_view["ready"] and export_view["valid"] else "needs_review"
                    ),
                }
                for action_id, export_view in decision_action_export_view.items()
            }

            # Final compact overview only - combines existing decision views.
            # No inspection of evidence content/provenance/diagnosticity/
            # hypotheses, no comparison, sorting, or selection between
            # actions.
            decision_action_overview = {
                action_id: {
                    "action_id": action_id,
                    "status": decision_action_status_summary[action_id]["status"],
                    "score": decision_action_export_view[action_id]["score"],
                    "evidence_count": len(decision_action_evidence[action_id]),
                    "ready": decision_action_status_summary[action_id]["ready"],
                    "valid": decision_action_status_summary[action_id]["valid"],
                }
                for action_id in decision_action_status_summary
            }

            # Readiness report only - transforms existing overview status/
            # ready/valid fields. No inspection of evidence/provenance/
            # diagnosticity/scores/hypotheses/quality, no comparison or
            # selection between actions.
            decision_action_readiness_report = {
                action_id: {
                    "action_id": action_id,
                    "status": overview["status"],
                    "passed": overview["ready"] and overview["valid"],
                    "checks": {
                        "ready": overview["ready"],
                        "valid": overview["valid"],
                    },
                }
                for action_id, overview in decision_action_overview.items()
            }

            # Release gate only - a deterministic mapping of the existing
            # readiness report's passed field. No inspection of evidence/
            # provenance/diagnosticity/scores/hypotheses/quality, no
            # comparison or selection between actions.
            decision_action_release_gate = {
                action_id: {
                    "action_id": action_id,
                    "released": report["passed"],
                    "reason": "all_checks_passed" if report["passed"] else "checks_failed",
                }
                for action_id, report in decision_action_readiness_report.items()
            }

            # Final structural status projection only - combines the existing
            # release gate and overview. No calculation, no inspection of
            # evidence/provenance/diagnosticity/hypotheses/quality, no
            # comparison or selection between actions.
            decision_action_final_status = {
                action_id: {
                    "action_id": action_id,
                    "released": gate["released"],
                    "reason": gate["reason"],
                    "status": decision_action_overview[action_id]["status"],
                    "score": decision_action_overview[action_id]["score"],
                }
                for action_id, gate in decision_action_release_gate.items()
            }

            # Final immutable-style snapshot only - collects existing final
            # structures. No recalculation, no inspection of evidence/
            # provenance/diagnosticity/hypotheses/quality, no comparison or
            # selection between actions.
            decision_action_final_snapshot = {
                action_id: {
                    "action_id": action_id,
                    "status": decision_action_final_status[action_id],
                    "trace": decision_action_final_trace[action_id],
                    "audit": decision_action_audit_log[action_id],
                }
                for action_id in decision_action_final_status
            }

            # Final human-readable structural report only - reshapes the
            # existing final snapshot. Only allowed computation is a bool()
            # presence check. No inspection of evidence/provenance/
            # diagnosticity/hypotheses/quality, no recalculation, comparison,
            # or ranking.
            decision_action_final_report = {
                action_id: {
                    "action_id": action_id,
                    "status": snapshot["status"]["status"],
                    "released": snapshot["status"]["released"],
                    "score": snapshot["status"]["score"],
                    "validation": snapshot["status"]["reason"],
                    "trace_available": bool(snapshot["trace"]),
                    "audit_available": bool(snapshot["audit"]),
                }
                for action_id, snapshot in decision_action_final_snapshot.items()
            }

            # Final lookup index only - references existing final report
            # entries unchanged. No inspection of evidence/provenance/
            # diagnosticity/hypotheses/quality, no recalculation, comparison,
            # or ranking.
            decision_action_final_index = {
                action_id: {
                    "action_id": entry["action_id"],
                    "report": entry,
                }
                for action_id, entry in decision_action_final_report.items()
            }

            # First deterministic Action Generator scaffold - independent of
            # generated_actions/decision_* structures above, no shared state.
            # One action per surviving hypothesis only, using existing
            # statement/status alone. No inspection of evidence/provenance/
            # diagnosticity, no scoring, no ranking, no selection.
            action_generator_output = []
            for hypothesis_index, hypothesis in enumerate(hypotheses):
                if hypothesis["status"] == "surviving":
                    action_generator_output.append({
                        "id": f"generated_action_{hypothesis_index}",
                        "hypothesis_index": hypothesis_index,
                        "title": hypothesis["statement"],
                        "description": None,
                        "expected_outcomes": [],
                        "required_resources": [],
                        "risks": [],
                    })

            # Registry layer for action_generator_output only - stable
            # identity fields (id/hypothesis_index/title). No inspection of
            # evidence/provenance/diagnosticity/scores, no connection to
            # generated_actions/decision_model, no decision links.
            action_generator_registry = [
                {
                    "id": action["id"],
                    "hypothesis_index": action["hypothesis_index"],
                    "title": action["title"],
                }
                for action in action_generator_output
            ]

            # Metadata layer for action_generator_registry only - structural
            # presence only. has_title is the sole real check (bool of the
            # title text); the remaining has_* fields are fixed False
            # placeholders since those fields are never generated today - no
            # inference, no description/outcome/resource/risk generation.
            action_candidate_metadata = {
                action["id"]: {
                    "action_id": action["id"],
                    "hypothesis_index": action["hypothesis_index"],
                    "has_title": bool(action["title"]),
                    "has_description": False,
                    "has_expected_outcomes": False,
                    "has_required_resources": False,
                    "has_risks": False,
                }
                for action in action_generator_registry
            }

            # Completeness check for action_candidate_metadata only - pure
            # boolean validation, no inspection of actual values, no
            # generation/filling of missing fields. "complete" requires all
            # five fields present (equivalent to an empty "missing" list),
            # matching the expected result (False, since only title exists
            # today) rather than a title-only check.
            action_candidate_completeness = {}
            for action_id, metadata in action_candidate_metadata.items():
                missing = [
                    field_name
                    for field_name, exists in {
                        "title": metadata["has_title"],
                        "description": metadata["has_description"],
                        "expected_outcomes": metadata["has_expected_outcomes"],
                        "required_resources": metadata["has_required_resources"],
                        "risks": metadata["has_risks"],
                    }.items()
                    if not exists
                ]
                action_candidate_completeness[action_id] = {
                    "action_id": action_id,
                    "complete": len(missing) == 0,
                    "missing": missing,
                }

            # Readiness state mapping only - derived purely from
            # action_candidate_completeness. No inspection of action content/
            # title/hypotheses/evidence/provenance/diagnosticity/scores, no
            # generation or fixing of missing fields.
            action_candidate_readiness = {
                action_id: {
                    "action_id": action_id,
                    "ready": completeness["complete"],
                    "missing": completeness["missing"],
                    "status": "ready" if completeness["complete"] else "incomplete",
                }
                for action_id, completeness in action_candidate_completeness.items()
            }

            # Action Templates: a fixed, deterministic template per hypothesis
            # type (null/constraint/skill). Each surviving hypothesis is
            # matched only to its own type's template - no AI, no inference,
            # no template-driven wording. Per explicit instruction, id/title
            # use the same naming scheme as action_generator_output exactly
            # (id=template_action_{index}, title=statement unchanged, no
            # prefix/suffix) - this is temporary and may change later.
            # Independent of action_generator_output/action_generator_registry
            # above; neither is modified.
            action_templates = {
                "null": "null_template",
                "constraint": "constraint_template",
                "skill": "skill_template",
            }

            action_template_output = []
            for hypothesis_index, hypothesis in enumerate(hypotheses):
                if hypothesis["status"] == "surviving":
                    matched_template = action_templates.get(hypothesis["type"])
                    action_template_output.append({
                        "id": f"template_action_{hypothesis_index}",
                        "hypothesis_index": hypothesis_index,
                        "template": matched_template,
                        "title": hypothesis["statement"],
                        "description": None,
                        "expected_outcomes": [],
                        "required_resources": [],
                        "risks": [],
                    })

            # Action Template Materialization Layer: fills each template
            # action's placeholder fields from a fixed, static template
            # definition matched only by the existing "template" field - no
            # hypothesis/evidence inspection, no inference, no mutation of
            # action_template_output itself.
            action_template_definitions = {
                "null_template": {
                    "description": "Maintain the current baseline strategy without deviation.",
                    "expected_outcomes": ["Situation remains within expected baseline parameters."],
                    "required_resources": [],
                    "risks": ["Baseline assumption proves incorrect if conditions change unexpectedly."],
                },
                "constraint_template": {
                    "description": "Address the identified constraint directly to reduce its limiting effect.",
                    "expected_outcomes": ["The constraint's limiting effect is reduced or managed."],
                    "required_resources": ["Budget or resource allocation to address the constraint."],
                    "risks": ["The constraint may not be fully resolvable within available resources."],
                },
                "skill_template": {
                    "description": "Apply the relevant expert lens to guide further analysis and action.",
                    "expected_outcomes": ["Analysis grounded in the relevant expert perspective is produced."],
                    "required_resources": ["Access to the relevant domain expertise."],
                    "risks": ["The expert lens may not capture factors outside its own domain."],
                },
            }

            action_template_materialized_output = []
            for source in action_template_output:
                template = action_template_definitions[source["template"]]
                action_template_materialized_output.append({
                    "id": source["id"],
                    "hypothesis_index": source["hypothesis_index"],
                    "template": source["template"],
                    "title": source["title"],
                    "description": template["description"],
                    "expected_outcomes": template["expected_outcomes"],
                    "required_resources": template["required_resources"],
                    "risks": template["risks"],
                })

            # Structural evaluation of materialized action candidates only -
            # pure bool() presence checks on already materialized fields. No
            # inspection of hypothesis/evidence/decision structures, no
            # filling of missing fields, no mutation of
            # action_template_materialized_output.
            action_candidate_evaluation = {
                action["id"]: {
                    "action_id": action["id"],
                    "has_description": bool(action["description"]),
                    "has_expected_outcomes": bool(action["expected_outcomes"]),
                    "has_required_resources": bool(action["required_resources"]),
                    "has_risks": bool(action["risks"]),
                    "structurally_ready": all([
                        bool(action["description"]),
                        bool(action["expected_outcomes"]),
                        bool(action["required_resources"]),
                        bool(action["risks"]),
                    ]),
                }
                for action in action_template_materialized_output
            }

            # Action Candidate Pool: pure projection combining
            # action_template_materialized_output and
            # action_candidate_evaluation. No ranking, scoring, selection, or
            # comparison between candidates - a plain lookup structure only.
            action_candidate_pool = {
                action["id"]: {
                    "action_id": action["id"],
                    "hypothesis_index": action["hypothesis_index"],
                    "template": action["template"],
                    "title": action["title"],
                    "description": action["description"],
                    "evaluation": action_candidate_evaluation[action["id"]],
                }
                for action in action_template_materialized_output
            }

            # Clean deterministic input for future candidate assessment -
            # action_id/template/title/description only. No evaluation,
            # scores, readiness, ranking, or decisions included.
            action_candidate_assessment_input = {
                action_id: {
                    "action_id": candidate["action_id"],
                    "template": candidate["template"],
                    "title": candidate["title"],
                    "description": candidate["description"],
                }
                for action_id, candidate in action_candidate_pool.items()
            }

            # Action Candidate Assessment Scaffold: empty placeholder only.
            # No inspection of title/description/hypotheses/evidence/
            # provenance/diagnosticity/scores/decision structures - criteria
            # and status stay unresolved until a later step.
            action_candidate_assessment = {
                action_id: {
                    "action_id": action_id,
                    "template": source["template"],
                    "assessment_status": "pending",
                    "criteria": {},
                }
                for action_id, source in action_candidate_assessment_input.items()
            }

            # Action Candidate Assessment Criteria Schema: fixed key set only,
            # all values None placeholders. No calculation, no inspection of
            # title/description/hypotheses/evidence/provenance/diagnosticity/
            # scores/decision structures.
            action_candidate_assessment_criteria = {
                action_id: {
                    "action_id": action_id,
                    "template": source["template"],
                    "criteria": {
                        "feasibility": None,
                        "impact": None,
                        "risk": None,
                        "cost": None,
                        "time_horizon": None,
                    },
                }
                for action_id, source in action_candidate_assessment.items()
            }

            # Action Candidate Assessment Context: clean context object for
            # future assessment agents, combining action_candidate_pool and
            # action_candidate_assessment_criteria only. No calculation, no
            # inspection of hypothesis statements/evidence/provenance/
            # diagnosticity/scores/decision structures, no missing-info
            # generation.
            action_candidate_assessment_context = {
                action_id: {
                    "action_id": action_id,
                    "template": candidate["template"],
                    "action": {
                        "title": candidate["title"],
                        "description": candidate["description"],
                    },
                    "criteria": action_candidate_assessment_criteria[action_id]["criteria"],
                }
                for action_id, candidate in action_candidate_pool.items()
            }

            # Assessment Agent Contract Scaffold: fixed agent schema only, all
            # agents "pending" with result None. No agent execution, no
            # calculation, no inspection of action text/description/
            # hypotheses/evidence/provenance/diagnosticity/scores/decision
            # structures.
            assessment_agent_contract = {
                action_id: {
                    "action_id": action_id,
                    "agents": {
                        "feasibility": {"status": "pending", "result": None},
                        "impact": {"status": "pending", "result": None},
                        "risk": {"status": "pending", "result": None},
                        "cost": {"status": "pending", "result": None},
                        "time_horizon": {"status": "pending", "result": None},
                    },
                }
                for action_id in action_candidate_assessment_context
            }

            # Feasibility Agent Scaffold: connection point only, no
            # execution. input is a direct reference to the existing
            # context; output stays None. No calculation, no inspection of
            # title/description/hypotheses/evidence/provenance/
            # diagnosticity/scores/decision structures.
            feasibility_agent_scaffold = {
                action_id: {
                    "action_id": action_id,
                    "agent": "feasibility",
                    "status": "pending",
                    "input": action_candidate_assessment_context[action_id],
                    "output": None,
                }
                for action_id in assessment_agent_contract
            }

            # Feasibility Agent Result Schema: fixed output shape only, no
            # execution. All result values remain None. No calculation, no
            # inspection of title/description/hypotheses/evidence/
            # provenance/diagnosticity/scores/decision structures.
            feasibility_agent_result_schema = {
                action_id: {
                    "action_id": action_id,
                    "agent": "feasibility",
                    "status": "pending",
                    "result": {
                        "score": None,
                        "reasoning": None,
                        "confidence": None,
                    },
                }
                for action_id in feasibility_agent_scaffold
            }

            # Feasibility Agent Execution Interface Scaffold: connection
            # interface only, no model call, no execution. input/
            # result_schema are direct references to existing structures.
            # No calculation, no inspection of action content/title/
            # description/hypotheses/evidence/provenance/diagnosticity/
            # scores/decision structures.
            feasibility_agent_execution = {
                action_id: {
                    "action_id": action_id,
                    "agent": "feasibility",
                    "input": feasibility_agent_scaffold[action_id]["input"],
                    "result_schema": feasibility_agent_result_schema[action_id]["result"],
                    "status": "ready",
                }
                for action_id in feasibility_agent_scaffold
            }

            # Feasibility Agent Prompt Contract Scaffold: fixed static prompt
            # fields only, no prompt sent anywhere, no LLM call. input_
            # reference/output_schema are direct references to the existing
            # execution interface. No inspection of action content/title/
            # description/hypotheses/evidence/provenance/diagnosticity/
            # scores/decision structures.
            feasibility_agent_prompt_contract = {
                action_id: {
                    "action_id": action_id,
                    "agent": "feasibility",
                    "system_role": "feasibility analyst",
                    "instruction": "Evaluate only practical feasibility of the action.",
                    "constraints": [
                        "Do not evaluate impact.",
                        "Do not evaluate risk.",
                        "Do not evaluate cost.",
                        "Do not evaluate time horizon.",
                        "Return only structured JSON output.",
                    ],
                    "input_reference": feasibility_agent_execution[action_id]["input"],
                    "output_schema": feasibility_agent_execution[action_id]["result_schema"],
                    "status": "pending",
                }
                for action_id in feasibility_agent_execution
            }

            # Feasibility Agent Runner Scaffold: future execution container
            # only - nothing is executed, no LLM call, no prompt sent.
            # prompt_contract is a direct reference to the existing entry. No
            # inspection of action content/title/description/hypotheses/
            # evidence/provenance/diagnosticity/scores/decision structures.
            feasibility_agent_runner = {
                action_id: {
                    "action_id": action_id,
                    "agent": "feasibility",
                    "prompt_contract": feasibility_agent_prompt_contract[action_id],
                    "status": "ready",
                    "result": None,
                }
                for action_id in feasibility_agent_prompt_contract
            }

            # Feasibility Agent Executor Mock: deterministic mock execution
            # only, no LLM/AI/external API/real feasibility analysis. All
            # result values remain None - status moves to "completed" to
            # simulate flow, but no scores/reasoning/confidence are ever
            # produced. No inspection of title/description/hypotheses/
            # evidence/provenance/diagnosticity/decision structures.
            feasibility_agent_execution_result = {
                action_id: {
                    "action_id": action_id,
                    "agent": "feasibility",
                    "status": "completed",
                    "result": {
                        "score": None,
                        "reasoning": None,
                        "confidence": None,
                    },
                }
                for action_id in feasibility_agent_runner
            }

            # Feasibility Agent Result Validator: pure key-presence check on
            # the mock result, no value inspection, no quality evaluation, no
            # feasibility conclusions. No inspection of title/description/
            # hypotheses/evidence/provenance/diagnosticity/decision
            # structures.
            feasibility_agent_result_validation = {}
            for action_id, execution_result in feasibility_agent_execution_result.items():
                result = execution_result["result"]
                required_fields = ["score", "reasoning", "confidence"]
                feasibility_agent_result_validation[action_id] = {
                    "action_id": action_id,
                    "valid": all([
                        "score" in result,
                        "reasoning" in result,
                        "confidence" in result,
                    ]),
                    "missing": [
                        field_name
                        for field_name in required_fields
                        if field_name not in result
                    ],
                    "extra_fields": [
                        field_name
                        for field_name in result.keys()
                        if field_name not in required_fields
                    ],
                }

            # Feasibility Agent Provider Adapter Interface: integration
            # interface only, no provider selected, no call made. input is a
            # direct reference to the existing prompt_contract. No LLM/API
            # call, no scores/reasoning/confidence created, no inspection of
            # action content/title/description/hypotheses/evidence/
            # provenance/diagnosticity/decision structures.
            feasibility_agent_provider_adapter = {
                action_id: {
                    "action_id": action_id,
                    "agent": "feasibility",
                    "provider": None,
                    "input": feasibility_agent_runner[action_id]["prompt_contract"],
                    "output": None,
                    "status": "not_executed",
                }
                for action_id in feasibility_agent_runner
            }

            # Feasibility Agent Provider Request Builder: assembles the
            # deterministic request package a future provider would receive.
            # All fields copied directly from existing structures - no
            # provider selection, no request sending, no prompt text
            # modification, no inspection of action quality/evidence/
            # hypotheses/provenance/diagnosticity/decision structures.
            feasibility_agent_provider_request = {
                action_id: {
                    "action_id": action_id,
                    "agent": "feasibility",
                    "provider": None,
                    "system_role": feasibility_agent_prompt_contract[action_id]["system_role"],
                    "instruction": feasibility_agent_prompt_contract[action_id]["instruction"],
                    "constraints": feasibility_agent_prompt_contract[action_id]["constraints"],
                    "input": feasibility_agent_provider_adapter[action_id]["input"],
                    "output_schema": (
                        feasibility_agent_provider_adapter[action_id]["input"]["output_schema"]
                        if "output_schema" in feasibility_agent_provider_adapter[action_id]["input"]
                        else None
                    ),
                    "status": "ready",
                }
                for action_id in feasibility_agent_provider_adapter
            }

            # Feasibility Agent Provider Executor Interface: execution
            # interface container only - no model call, no request sent, no
            # feasibility result generated. request is a direct reference to
            # the existing provider request. No inspection of action
            # content/titles/descriptions/hypotheses/evidence/provenance/
            # diagnosticity/decision structures.
            feasibility_agent_provider_executor = {
                action_id: {
                    "action_id": action_id,
                    "agent": "feasibility",
                    "request": feasibility_agent_provider_request[action_id],
                    "provider": None,
                    "execution_status": "not_started",
                    "response": None,
                }
                for action_id in feasibility_agent_provider_request
            }

            # Feasibility Agent Mock Provider Execution: deterministic local
            # simulation only, for pipeline testing - no LLM/AI/external
            # API/network call, not a real evaluation. result values are
            # fixed mock constants, not derived from any inspection of
            # title/description/hypothesis/evidence/provenance/
            # diagnosticity/scores/decision structures.
            feasibility_agent_mock_execution = {
                action_id: {
                    "action_id": action_id,
                    "agent": "feasibility",
                    "status": "completed",
                    "request": feasibility_agent_provider_executor[action_id]["request"],
                    "result": {
                        "score": 0.5,
                        "reasoning": "mock_result",
                        "confidence": 0.5,
                    },
                }
                for action_id in feasibility_agent_provider_executor
            }

            # Feasibility Agent Final Result Integration: pure combination of
            # the existing mock result and validation state. No
            # recalculation, no interpretation, no status change, no ranking
            # or comparison between candidates, no inspection of titles/
            # descriptions/hypotheses/evidence/provenance/diagnosticity/
            # decision structures.
            feasibility_agent_final_result = {
                action_id: {
                    "action_id": action_id,
                    "agent": "feasibility",
                    "status": feasibility_agent_mock_execution[action_id]["status"],
                    "result": feasibility_agent_mock_execution[action_id]["result"],
                    "validation": feasibility_agent_result_validation[action_id],
                }
                for action_id in feasibility_agent_mock_execution
            }

            # Feasibility Agent Provider Interface: abstraction boundary
            # contract only, no provider selected, no execution. request_
            # schema/response_schema are direct references to existing
            # structures. No model call, no request sent, no results
            # generated, no inspection of titles/descriptions/hypotheses/
            # evidence/provenance/diagnosticity/scores/decision structures.
            feasibility_agent_provider_interface = {
                action_id: {
                    "action_id": action_id,
                    "agent": "feasibility",
                    "provider_type": None,
                    "execute_status": "available",
                    "request_schema": feasibility_agent_provider_executor[action_id]["request"],
                    "response_schema": feasibility_agent_final_result[action_id]["result"],
                }
                for action_id in feasibility_agent_provider_executor
            }

            # Feasibility Agent Provider Router: routing only, selects
            # "mock" as the provider without calling it. No model call, no
            # results created, no inspection of action content/title/
            # description/hypotheses/evidence/provenance/diagnosticity/
            # scores/decision structures.
            feasibility_agent_provider_router = {
                action_id: {
                    "action_id": action_id,
                    "agent": "feasibility",
                    "provider_type": feasibility_agent_provider_interface[action_id]["provider_type"],
                    "selected_provider": "mock",
                    "request": feasibility_agent_provider_interface[action_id]["request_schema"],
                    "status": "ready",
                }
                for action_id in feasibility_agent_provider_interface
            }

            # Feasibility Agent Provider Dispatcher: deterministic dispatch
            # simulation only, bridging routing to the existing mock result.
            # No provider execution happens here, no model call, no new
            # results generated, no inspection of action content/title/
            # description/hypotheses/evidence/provenance/diagnosticity/
            # scores/decision structures.
            feasibility_agent_provider_dispatcher = {
                action_id: {
                    "action_id": action_id,
                    "agent": "feasibility",
                    "provider": feasibility_agent_provider_router[action_id]["selected_provider"],
                    "status": "completed",
                    "response": feasibility_agent_mock_execution[action_id]["result"],
                }
                for action_id in feasibility_agent_provider_router
            }

            # Registry layer for action_template_output only - projection of
            # id/hypothesis_index/template/title. No inspection of
            # hypotheses/evidence/decision structures, no new fields.
            action_template_registry = [
                {
                    "id": action["id"],
                    "hypothesis_index": action["hypothesis_index"],
                    "template": action["template"],
                    "title": action["title"],
                }
                for action in action_template_output
            ]

            # Metadata layer for action_template_registry only - structural
            # presence only. has_title is the sole real check; the remaining
            # has_* fields are fixed False placeholders since those fields
            # are never generated today - no inference, no inspection of
            # hypotheses/evidence/decision structures.
            action_template_metadata = {
                action["id"]: {
                    "action_id": action["id"],
                    "hypothesis_index": action["hypothesis_index"],
                    "template": action["template"],
                    "has_title": bool(action["title"]),
                    "has_description": False,
                    "has_expected_outcomes": False,
                    "has_required_resources": False,
                    "has_risks": False,
                }
                for action in action_template_registry
            }

            # Completeness check for action_template_metadata only - pure
            # boolean validation, no inspection of actual values, no
            # generation/filling of missing fields.
            action_template_completeness = {
                action_id: {
                    "action_id": action_id,
                    "complete": all([
                        metadata["has_title"],
                        metadata["has_description"],
                        metadata["has_expected_outcomes"],
                        metadata["has_required_resources"],
                        metadata["has_risks"],
                    ]),
                    "missing": [
                        field_name
                        for field_name, exists in {
                            "title": metadata["has_title"],
                            "description": metadata["has_description"],
                            "expected_outcomes": metadata["has_expected_outcomes"],
                            "required_resources": metadata["has_required_resources"],
                            "risks": metadata["has_risks"],
                        }.items()
                        if not exists
                    ],
                }
                for action_id, metadata in action_template_metadata.items()
            }

            # Readiness state mapping only - derived purely from
            # action_template_completeness. No inspection of action content/
            # templates/hypotheses/evidence/decision structures, no
            # generation or repair of missing fields.
            action_template_readiness = {
                action_id: {
                    "action_id": action_id,
                    "ready": completeness["complete"],
                    "missing": completeness["missing"],
                    "status": "ready" if completeness["complete"] else "incomplete",
                }
                for action_id, completeness in action_template_completeness.items()
            }

            # Release gate only - a deterministic mapping of the existing
            # readiness's ready field. No inspection of template/title/
            # hypotheses/evidence/provenance/scores, no comparison between
            # actions.
            action_template_release_gate = {
                action_id: {
                    "action_id": action_id,
                    "released": readiness["ready"],
                    "reason": "all_checks_passed" if readiness["ready"] else "checks_failed",
                }
                for action_id, readiness in action_template_readiness.items()
            }

            # Final structural status combination only - combines the
            # existing release gate and readiness. No inspection of
            # templates/titles/hypotheses/evidence/provenance/scores/decision
            # structures, no recalculation, validation, or selection.
            action_template_final_status = {
                action_id: {
                    "action_id": action_id,
                    "released": gate["released"],
                    "reason": gate["reason"],
                    "ready": action_template_readiness[action_id]["ready"],
                    "status": action_template_readiness[action_id]["status"],
                }
                for action_id, gate in action_template_release_gate.items()
            }

            # Final assembled trace only - combines existing template-action
            # structures. action_template_registry is a list, so a by-id
            # lookup is built first (no new data, just an index over
            # existing entries). No recalculation, no new boolean checks, no
            # inspection of hypothesis statements/evidence/provenance/
            # diagnosticity/scores/decision structures.
            action_template_registry_by_id = {
                entry["id"]: entry for entry in action_template_registry
            }
            action_template_final_trace = {
                action_id: {
                    "action_id": action_id,
                    "registry": action_template_registry_by_id[action_id],
                    "metadata": action_template_metadata[action_id],
                    "completeness": action_template_completeness[action_id],
                    "readiness": action_template_readiness[action_id],
                    "release_gate": action_template_release_gate[action_id],
                    "status": action_template_final_status[action_id],
                }
                for action_id in action_template_final_status
            }

            # Export projection only - a clean structural view of
            # action_template_final_trace. No recalculation, no new
            # validation, no inspection of hypothesis statements/evidence/
            # provenance/diagnosticity/scores/decision structures.
            action_template_export_view = {
                action_id: {
                    "action_id": action_id,
                    "template": trace["registry"]["template"],
                    "title": trace["registry"]["title"],
                    "ready": trace["readiness"]["ready"],
                    "released": trace["release_gate"]["released"],
                    "status": trace["status"]["status"],
                    "reason": trace["status"]["reason"],
                }
                for action_id, trace in action_template_final_trace.items()
            }

            # Audit log only - fixed, hardcoded source labels documenting
            # where each export field came from. Not calculated dynamically,
            # no analysis, no action quality check.
            action_template_audit_log = {
                action_id: {
                    "action_id": action_id,
                    "sources": {
                        "template": "action_template_final_trace.registry.template",
                        "title": "action_template_final_trace.registry.title",
                        "ready": "action_template_final_trace.readiness.ready",
                        "released": "action_template_final_trace.release_gate.released",
                        "status": "action_template_final_trace.status.status",
                        "reason": "action_template_final_trace.status.reason",
                    },
                }
                for action_id in action_template_export_view
            }

            # Status summary only - a plain projection of
            # action_template_export_view. No new checks, no calculations,
            # no status changes, no inspection of hypothesis/evidence/
            # provenance/diagnosticity/scores/decision structures.
            action_template_status_summary = {
                action_id: {
                    "action_id": action_id,
                    "template": export_entry["template"],
                    "ready": export_entry["ready"],
                    "released": export_entry["released"],
                    "status": export_entry["status"],
                    "reason": export_entry["reason"],
                }
                for action_id, export_entry in action_template_export_view.items()
            }

            # Final immutable-style snapshot only - collects existing final
            # structures. No recalculation, no inspection of hypothesis/
            # evidence/provenance/diagnosticity/scores/decision structures,
            # no interpretation.
            action_template_final_snapshot = {
                action_id: {
                    "action_id": action_id,
                    "status": action_template_status_summary[action_id],
                    "trace": action_template_final_trace[action_id],
                    "audit": action_template_audit_log[action_id],
                }
                for action_id in action_template_status_summary
            }

            # Final flat report only - reshapes the existing final snapshot.
            # Only allowed computation is bool() presence checks. No
            # inspection of hypothesis/evidence/provenance/diagnosticity/
            # scores/decision structures, no fixing of incomplete actions,
            # no recommendations.
            action_template_final_report = {
                action_id: {
                    "action_id": action_id,
                    "template": snapshot["trace"]["registry"]["template"],
                    "title": snapshot["trace"]["registry"]["title"],
                    "ready": snapshot["status"]["ready"],
                    "released": snapshot["status"]["released"],
                    "status": snapshot["status"]["status"],
                    "reason": snapshot["status"]["reason"],
                    "audit_available": bool(snapshot["audit"]),
                    "trace_available": bool(snapshot["trace"]),
                }
                for action_id, snapshot in action_template_final_snapshot.items()
            }

            # Final lookup index only - references existing final report
            # entries unchanged. No inspection of hypothesis/evidence/
            # provenance/diagnosticity/scores/decision structures, no new
            # fields, no checks, no status computation.
            action_template_final_index = {
                action_id: {
                    "action_id": action_id,
                    "report": entry,
                }
                for action_id, entry in action_template_final_report.items()
            }

            # Internal scaffold: deterministic shared-evidence detection across
            # causal graphs (see docs/STRATEGIC_HYPOTHESIS_LAYER.md). Evidence
            # nodes only (supports/contradicts edges) - source and status nodes
            # are excluded. Not exposed, not sent to the provider, and not
            # consulted by ranking/status/assumptions.
            evidence_occurrences = {}
            for hypothesis_index, (hypothesis, graph) in enumerate(zip(hypotheses, causal_graphs)):
                raw_evidence_nodes = [
                    edge["from"]
                    for edge in graph["edges"]
                    if edge["relation"] in ("supports", "contradicts")
                ]
                evidence_nodes = list(dict.fromkeys(raw_evidence_nodes))
                for evidence in evidence_nodes:
                    evidence_occurrences.setdefault(evidence, []).append({
                        "hypothesis_index": hypothesis_index,
                        "statement": hypothesis.get("statement"),
                        "provenance": provenance_maps[hypothesis_index].get(evidence),
                    })

            shared_evidence_nodes = {
                evidence: occurrences
                for evidence, occurrences in evidence_occurrences.items()
                if len(occurrences) >= 2
            }

            dominant_hypothesis, closest_rival_hypothesis = self._rank_hypotheses(
                hypotheses, shared_evidence_nodes=shared_evidence_nodes, evidence_evaluation=evidence_evaluation
            )

            llm_input = {
                "agent": agent_name,
                "reasoning_context": {
                    "mission": reasoning_package.get("mission"),
                    "skills": reasoning_package.get("skills"),
                    "methodologies": reasoning_package.get("methodologies"),
                    "analysis_steps": reasoning_package.get("analysis_steps"),
                    "question": question,
                    "goals": goal,
                    "constraints": mission.get("constraints"),
                    "time_horizon": reasoning_package.get("time_horizon"),
                    "expert_scope": reasoning_package.get("expert_scope"),
                    "decision_type": reasoning_package.get("decision_type"),
                    "domain_knowledge": domain_knowledge,
                },
            }
            result = self.llm_provider.generate_analysis(llm_input)
            result = result if isinstance(result, dict) else {}

            assumptions = list(result.get("assumptions") or [])
            if (
                dominant_hypothesis is not None
                and closest_rival_hypothesis is not None
                and dominant_hypothesis.get("status") == "surviving"
            ):
                hedge = (
                    f'Assumes: "{dominant_hypothesis.get("statement")}" '
                    f'rather than "{closest_rival_hypothesis.get("statement")}".'
                )
                if hedge not in assumptions:
                    assumptions.append(hedge)

            return {
                "agent": reasoning_package.get("agent"),
                "summary": result.get("summary"),
                "key_factors": result.get("key_factors", []),
                "risks": result.get("risks", []),
                "opportunities": result.get("opportunities", []),
                "assumptions": assumptions,
                "confidence": result.get("confidence"),
            }

        if isinstance(reasoning_package, dict):
            agent_name = reasoning_package.get("agent")
        else:
            agent_name = getattr(reasoning_package, "agent", None)

        output = AnalysisResult().to_dict()
        output["agent"] = agent_name
        return output

    def _load_domain_knowledge(self, agent_name):
        domain_name = EXPERT_DOMAIN_MAP.get(agent_name)
        if domain_name is None:
            return None

        try:
            return self.knowledge_loader.load_domain(domain_name)
        except OSError:
            return None

    @classmethod
    def _evaluate_status(
        cls,
        supporting_evidence,
        contradicting_evidence,
        allow_contradiction_to_reject=True,
        diagnosticity_matrix=None,
        hypothesis_index=None,
        hypothesis_type=None,
        competitor_indices=None,
    ) -> str:
        has_contradiction = bool(contradicting_evidence)

        # The null hypothesis has no real competing alternative of its own
        # type, so it never uses diagnostic support logic - it falls back to
        # plain evidence presence, exactly as when no matrix is supplied.
        if diagnosticity_matrix is None or hypothesis_type == "null":
            has_support = bool(supporting_evidence)
        else:
            has_support = any(
                cls._is_diagnostic_support(
                    evidence, hypothesis_index, diagnosticity_matrix, competitor_indices=competitor_indices
                )
                for evidence in supporting_evidence
            )

        if allow_contradiction_to_reject and has_contradiction:
            return "rejected"
        if has_support and not has_contradiction:
            return "surviving"
        return "unresolved"

    @staticmethod
    def _is_diagnostic_support(evidence, hypothesis_index, diagnosticity_matrix, competitor_indices=None) -> bool:
        marks = diagnosticity_matrix.get(evidence)
        if not marks:
            return False

        this_key = str(hypothesis_index)
        if marks.get(this_key) != "C":
            return False

        # Competitors are only hypotheses of the same type (skill vs. skill,
        # constraint vs. constraint - see indices_by_type in analyze()), so
        # evidence shared with a different-type hypothesis can no longer
        # manufacture diagnosticity: only a genuine same-type rival showing
        # "N/A" or "I" can make this evidence discriminate anything.
        if not competitor_indices:
            return False

        return any(
            mark != "C"
            for key, mark in marks.items()
            if key in competitor_indices and key != this_key
        )

    @staticmethod
    def _score_hypothesis(
        hypothesis,
        shared_evidence_nodes=None,
        evidence_evaluation=None,
        hypothesis_index=None,
    ) -> float:
        status = hypothesis.get("status")
        supporting = hypothesis.get("supporting_evidence") or []
        contradicting = hypothesis.get("contradicting_evidence") or []

        status_weight = 1 if status == "surviving" else 0

        if shared_evidence_nodes is None:
            evidence_score = len(supporting) - len(contradicting)
            unique_supporting = supporting
        else:
            unique_supporting = [
                evidence for evidence in supporting
                if evidence not in shared_evidence_nodes
            ]
            evidence_score = len(unique_supporting) - len(contradicting)

        # Evidence quality only ever adds to evidence already counted as
        # discriminating above (unique_supporting) - shared/non-discriminating
        # evidence, already excluded there, cannot gain quality points either.
        quality_score = 0
        if evidence_evaluation is not None:
            this_key = str(hypothesis_index)
            for evidence in unique_supporting:
                evaluation = evidence_evaluation.get(evidence)
                if not evaluation:
                    continue
                if evaluation.get("diagnosticity", {}).get(this_key) != "C":
                    continue
                quality_score += evaluation.get("quality", {}).get("weight", 0)

        return status_weight + evidence_score + quality_score

    @classmethod
    def _rank_hypotheses(cls, hypotheses, shared_evidence_nodes=None, evidence_evaluation=None):
        candidates = [
            (index, hypothesis)
            for index, hypothesis in enumerate(hypotheses)
            if hypothesis.get("status") != "rejected"
        ]
        ranked = sorted(
            candidates,
            key=lambda pair: (
                -cls._score_hypothesis(
                    pair[1],
                    shared_evidence_nodes=shared_evidence_nodes,
                    evidence_evaluation=evidence_evaluation,
                    hypothesis_index=pair[0],
                ),
                pair[0],
            ),
        )

        dominant = ranked[0][1] if len(ranked) >= 1 else None
        closest_rival = ranked[1][1] if len(ranked) >= 2 else None
        return dominant, closest_rival

    @staticmethod
    def _build_causal_graph(hypothesis, source=None, evidence_provenance=None, evidence_quality=None) -> dict:
        statement = hypothesis.get("statement")
        status = hypothesis.get("status")
        hypothesis_type = hypothesis.get("type")
        supporting = hypothesis.get("supporting_evidence") or []
        contradicting = hypothesis.get("contradicting_evidence") or []
        provenance_lookup = evidence_provenance or {}
        quality_lookup = evidence_quality or {}

        nodes = [statement]
        nodes.extend(supporting)
        nodes.extend(contradicting)

        edges = [
            {"from": evidence, "to": statement, "relation": "supports"}
            for evidence in supporting
        ]
        edges.extend(
            {"from": evidence, "to": statement, "relation": "contradicts"}
            for evidence in contradicting
        )

        # Provenance is looked up from the map generated alongside the
        # evidence itself (see _find_supporting_evidence), never inferred
        # from the evidence string's text. Evidence with no known provenance
        # (e.g. the null hypothesis's presence-based evidence) gets none.
        for evidence in supporting + contradicting:
            provenance = provenance_lookup.get(evidence)
            if provenance is not None:
                nodes.append(provenance)
                edges.append({"from": evidence, "to": provenance, "relation": "has_provenance"})

        # Quality nodes only for evidence with a real (nonzero) weight - a
        # weight of 0 means unknown/no provenance, and creating a node for it
        # would be a fake zero-quality node, which is explicitly avoided.
        for evidence in supporting + contradicting:
            quality_info = quality_lookup.get(evidence)
            weight = quality_info.get("weight") if quality_info else None
            if weight:
                quality_node = str(weight)
                nodes.append(quality_node)
                edges.append({"from": evidence, "to": quality_node, "relation": "has_quality"})

        if source is not None:
            nodes.append(source)
            edges.append({"from": source, "to": statement, "relation": "derives"})

        nodes.append(status)
        edges.append({"from": statement, "to": status, "relation": "has_status"})

        if hypothesis_type is not None:
            nodes.append(hypothesis_type)
            edges.append({"from": statement, "to": hypothesis_type, "relation": "has_type"})

        # Empty scaffold for the future Decision Impact layer. No nodes/edges
        # yet - populated in a later step.
        return {"nodes": nodes, "edges": edges, "decision_links": []}

    @staticmethod
    def _extract_keywords(text) -> list:
        if not isinstance(text, str):
            return []
        words = re.findall(r"\w+", text.lower())
        keywords = [word for word in words if len(word) >= 3]
        return list(dict.fromkeys(keywords))

    @classmethod
    def _find_supporting_evidence(cls, subject, question, domain_knowledge):
        domain_text = domain_knowledge.lower() if isinstance(domain_knowledge, str) else ""
        question_text = question.lower() if isinstance(question, str) else ""

        evidence = []
        provenance = {}
        for keyword in cls._extract_keywords(subject):
            if domain_text and keyword in domain_text:
                item = f"Domain knowledge references '{keyword}'."
                evidence.append(item)
                provenance[item] = "domain_knowledge"
            if question_text and keyword in question_text:
                item = f"The question directly references '{keyword}'."
                evidence.append(item)
                provenance[item] = "question"

        return evidence, provenance
