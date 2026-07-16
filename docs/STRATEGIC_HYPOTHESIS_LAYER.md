# Strategic Hypothesis Layer

## Purpose

Design the Hypothesis Layer as the next cognitive layer of the Strategic Pipeline, building on the Causal Reasoning Layer.

This is a design document only. No code, no implementation, no repository changes beyond this file.

The Causal Reasoning Layer gives an expert a way to represent *the mechanism* behind a situation — what causes what, and how confidently. But a single causal graph, however well-built, is still one story. An expert who builds one graph and reasons forward from it has silently committed to one interpretation of the situation before checking whether a different interpretation fits the same facts better. The Hypothesis Layer exists to prevent that: it forces the expert to consider **multiple competing explanations** before any one of them is allowed to generate risks, opportunities, or a conclusion.

This directly closes the audit's highest-priority missing mechanism: hypothesis generation and alternative explanations were identified as **critical** gaps, alongside base-rate reasoning (which this layer also partially restores, via a mandatory null hypothesis — see §4).

## 1. What a hypothesis is in this system

A hypothesis is a candidate explanation of the current situation, or a candidate prediction about the outcome variable, stated in a form that could be **wrong** — not a conclusion, not a summary, and not the same thing as a causal graph. A causal graph explains *how* something would happen; a hypothesis states *which* of several plausible somethings is actually happening or will happen.

Concretely, for a question like "should we expand into the EU market," candidate hypotheses are not "yes" and "no" — they are competing accounts of the *situation*, each of which implies a different answer:

- H1: "Demand is real and underserved; a first-mover advantage is available now."
- H2: "Demand appears real but is a temporary artifact of current conditions (e.g. a currency effect or a short-lived subsidy) and will not persist."
- H3: "Demand is real, but regulatory barriers make near-term entry impractical regardless of demand."
- H0 (the mandatory null/status-quo hypothesis, see §4): "Nothing about the current situation is unusual enough to justify deviating from the current strategy."

Each of these, if true, would produce a *different* causal graph, a different set of risks, and a different recommendation. The current pipeline effectively always jumps straight to something like H1 without ever having stated or tested the alternatives — this is the exact failure mode ACH (Analysis of Competing Hypotheses, the method's origin in intelligence tradecraft) was built to prevent.

## 2. Why hypotheses must come before causal modeling, not after

The Causal Reasoning Layer document positioned causal-graph construction as the first act of expert analysis. This document revises that ordering, deliberately and explicitly.

If an expert builds *one* causal graph first, every subsequent step — tracing forward for effects, deriving risks, assigning confidence — happens *inside* the frame that graph already committed to. The graph itself becomes unfalsifiable in practice, because nothing in the pipeline ever asks "what if the premise of this graph is wrong." This is anchoring, and it is precisely how single-narrative analysis goes wrong even when every individual causal link in the graph is locally well-reasoned.

The correct order is:

1. Generate multiple competing hypotheses **first**, before any graph is built, anchored only to the mission's outcome variable and the raw question — not yet to any specific mechanism.
2. For **each** hypothesis, construct a causal graph (using the Causal Reasoning Layer's method from the prior document) that would have to hold for that hypothesis to be true.
3. Evaluate the hypotheses against each other using the evidence available (domain knowledge), not by asking "does the evidence support this hypothesis" but by asking "does the evidence *distinguish* this hypothesis from its rivals" (§5).
4. Only the surviving, evidence-supported hypothesis (or hypotheses, if genuinely close) generates risks, opportunities, and the final confidence — not a single graph built in isolation.

The Causal Reasoning Layer is not replaced by this — it is **run once per hypothesis**, not once per expert.

## 3. Structure of a hypothesis

Each hypothesis carries:

- **Statement** — a single, falsifiable sentence describing the candidate situation or prediction.
- **Supporting causal graph** — the mechanism (per the Causal Reasoning Layer) that would produce this hypothesis's predicted outcome, built specifically to test this hypothesis, not shared wholesale with the others (though nodes may legitimately be shared where the underlying reality is genuinely shared — e.g. "oil price" is exogenous and identical across hypotheses about a market's demand).
- **Predicted evidence** — what we would expect to observe in the domain knowledge / available facts *if this hypothesis were true*, stated before checking whether it actually is true.
- **Predicted evidence if false** — what we would instead expect to observe if a rival hypothesis were true instead. This is what makes evidence evaluation possible at all (§5) — without a stated contrast, "supporting evidence" is meaningless.
- **Status** — surviving, rejected, or unresolved, assigned after evidence evaluation, never before.

## 4. How hypotheses should be generated

- **Anchor to the outcome variable, not to the mechanism.** Hypotheses are generated by asking "what are the different things that could actually be true about this situation," not by extending a mechanism that's already been assumed.
- **Require a minimum spread, not a single best guess.** At minimum: one hypothesis representing the most obvious/expected interpretation, one representing a plausible alternative interpretation of the *same* facts, and one mandatory **null hypothesis** — "the situation is not meaningfully different from the base rate / status quo, and no unusual action is warranted." The null hypothesis is not a formality: it is the pipeline's only current mechanism for base-rate reasoning (a critical gap identified separately in the audit), and it should be genuinely tested, not included and dismissed by default.
- **Hypotheses should be substantively different, not cosmetic variants.** Two hypotheses that would produce the same recommendation are one hypothesis, not two — the test is "would acting on this hypothesis lead to a different decision than acting on that one."
- **Bounded count.** In practice, 3–4 hypotheses (including the null) is enough to force genuine consideration of alternatives without producing an unreviewable sprawl. More than that should be a signal the question itself is underspecified, not that more hypotheses are automatically better.

## 5. Evaluating hypotheses against evidence: diagnosticity

This is the single most important — and most commonly skipped — step in hypothesis-driven analysis, and the reason a naive implementation of this layer would fail to improve anything.

The wrong way to evaluate hypotheses: for each hypothesis, look for evidence that supports it, and pick the one with the most supporting evidence. This fails because most available evidence is **consistent with every hypothesis** and therefore proves nothing. If a piece of domain knowledge is equally consistent with H1, H2, and H3, citing it as "supporting" H1 is an error, not an insight — it would have supported any hypothesis equally.

The correct method (diagnosticity, from ACH): for each piece of evidence, ask whether it is consistent with *some* hypotheses and *inconsistent* with others. Only evidence that discriminates between hypotheses is informative. Concretely, for each piece of evidence:

- Mark it consistent (C), inconsistent (I), or not applicable (N/A) against **every** hypothesis, not just the one it was found while investigating.
- Evidence with the same mark across all hypotheses is non-diagnostic and should not move any hypothesis's standing, no matter how compelling it feels.
- A hypothesis accumulates support not from the *count* of consistent evidence, but from surviving contact with evidence that was capable of ruling it out and didn't.
- A hypothesis with even one piece of strongly inconsistent evidence against it should be down-weighted sharply, more than a hypothesis is up-weighted by a large pile of merely-consistent (non-diagnostic) evidence. Disconfirmation is more informative than confirmation.

## 6. Scoring and surviving hypotheses

After evidence evaluation, hypotheses are ranked, not simply reduced to a single winner:

- **Dominant survivor**: one hypothesis has no significant disconfirming evidence and clearly better diagnostic support than the others. This becomes the primary basis for risks/opportunities/confidence (§7), and the analysis can proceed with high stated confidence.
- **Narrow survivor**: one hypothesis edges out the others, but at least one rival remains only weakly disconfirmed. The analysis should proceed on the leading hypothesis, but confidence must reflect the margin (see §7), and the close rival's implications should be carried forward as an explicit hedge, not discarded.
- **Unresolved**: no hypothesis is clearly favored by diagnostic evidence. This is itself an important, honest finding — it means the available domain knowledge is insufficient to distinguish between materially different futures, and the output should say so directly rather than arbitrarily picking one hypothesis to sound decisive.

Rejected hypotheses are never deleted from the record — each is kept with its statement and the specific disconfirming evidence that ruled it out. This is what makes the analysis auditable: a reader can see not just what was concluded, but what else was seriously considered and why it was set aside, which is itself a mark of credible strategic work (and directly answers the audit's "could I be wrong" self-reflection gap — the rejected hypotheses *are* the record of that question having been asked).

## 7. How this changes risks, opportunities, assumptions, and confidence

- **Risks and opportunities** are drawn from the surviving (or dominant) hypothesis's causal graph, exactly as described in the Causal Reasoning Layer document — but if the result was a *narrow* survivor (§6), the pipeline should also carry forward the highest-severity risk implied by the close rival hypothesis, explicitly labeled as arising from a rejected-but-not-decisively-rejected alternative. This is how the layer prevents false confidence on close calls, which the current pipeline has no mechanism to detect at all.
- **Assumptions** gain a new category beyond the Causal Reasoning Layer's per-edge assumptions: "assumes H[n] is correct rather than H[m]," specifically naming the closest rival that was not chosen. This assumption is directly stress-testable in the same way causal-edge assumptions are (§8 of the prior document): ask what changes downstream if the rejected hypothesis were actually true instead.
- **Confidence** is no longer only the compounded edge-confidence within one graph (as the Causal Reasoning Layer specified) — it is now a **composite** of (a) the internal strength of the winning hypothesis's causal graph, and (b) the margin by which it beat its closest rival. A hypothesis with a strong internal graph but only a narrow win over a serious rival should report *lower* confidence than one with an equally strong graph and no serious rival at all — something a single-graph model has no way to represent, since it never constructed a rival to lose to.
- **Summary** should name the hypothesis the conclusion rests on, not just state the conclusion — e.g. "assessment assumes demand is real and durable (H1), rather than a temporary currency effect (H2, considered and set aside due to X)" — making the analysis's own framing visible rather than implicit.

## 8. Where this fits in the pipeline

This layer sits at the very start of expert analysis, **before** the Causal Reasoning Layer's graph construction — the causal layer is now invoked once per hypothesis rather than once per expert:

```
... Reasoning -> Domain knowledge
  -> [NEW] Hypothesis generation (per expert)
       - generate 3-4 competing hypotheses, including the mandatory null
  -> [REVISED] Causal model construction, run once per hypothesis
       - each hypothesis gets the causal graph that would support it
  -> [NEW] Evidence evaluation against all hypotheses (diagnosticity, §5)
  -> [NEW] Hypothesis scoring (dominant / narrow / unresolved, §6)
  -> Risks / Opportunities / Assumptions  <-- derived from the surviving hypothesis's graph (+ hedge if narrow)
  -> Summary (names the winning hypothesis and the closest rejected rival)
  -> Confidence (composite of graph strength + hypothesis margin, §7)
-> Synthesis ...
```

As with the Causal Reasoning Layer, this is scoped to a single expert's internal reasoning. A further, separate future capability — already identified in the cognitive audit as the *other* top-critical gap — is giving experts visibility into each other's hypotheses and evidence before finalizing, so that hypothesis competition can happen across the council, not just within one expert. That remains explicitly out of scope here.

## 9. Recommended implementation approach (one only)

Require hypothesis generation and evidence evaluation to be explicit, visible reasoning steps that produce their own recorded output — a list of hypotheses with their status and the specific evidence that discriminated between them — before any risk, opportunity, or confidence value is produced. The discipline this enforces is not "generate more text," it is "commit to nothing until at least one genuine alternative has been stated and specifically checked against evidence capable of ruling it out." Do not attempt, in this step, to also implement cross-hypothesis Bayesian updating, formal probability scoring, or multi-round hypothesis refinement — those are legitimate future refinements, but the layer already produces its core value the moment a second, real alternative exists and is checked before the first one is allowed to become the answer.
