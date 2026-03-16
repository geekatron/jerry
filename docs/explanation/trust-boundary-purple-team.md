# Trust Boundaries and Purple Team Automation

> Understanding-oriented explanation of the trust model governing data exchange between `/red-team` and `/blue-team` skills, and the reasoning behind the three-session purple team coordination model. Covers why metadata-only transfer was chosen, why the taint model is asymmetric, why three sessions are required, and how the D3FEND feedback loop creates a compounding improvement cycle.

## Document Sections

| Section | Purpose |
|---------|---------|
| [What This Document Covers](#what-this-document-covers) | Scope of this explanation |
| [Why a Trust Boundary Exists Between Skills](#why-a-trust-boundary-exists-between-skills) | The nature of the red-to-blue data boundary |
| [Why the Taint Model Is Asymmetric](#why-the-taint-model-is-asymmetric) | Adversary-modeled versus analysis-derived |
| [Why Metadata-Only Transfer](#why-metadata-only-transfer) | The design decision against inline content |
| [Why Three Sessions](#why-three-sessions) | Context window arithmetic and coordination topology |
| [The D3FEND Feedback Loop](#the-d3fend-feedback-loop) | How gaps compound into improvement over engagements |
| [Trade-Offs in the Design](#trade-offs-in-the-design) | What the current model gives up |
| [Relationship to Broader Security Principles](#relationship-to-broader-security-principles) | How this connects to zero-trust and information security theory |

---

## What This Document Covers

This document explains the trust model that governs data exchange in a purple team exercise between the `/red-team` and `/blue-team` skills, and the reasoning behind the three-session coordination model.

For the structural description of the exchange envelopes (RBEE, CFE, DGE) and their required fields, see `docs/reference/tool-cli-patterns.md`. For the architectural decision that created the composable skill model these boundaries operate within, see `docs/explanation/hybrid-bc-architecture.md`. The source design document is `projects/PROJ-023-exploit-framework/work/design/phase-5-redblue-composition.md`.

---

## Why a Trust Boundary Exists Between Skills

Both `/red-team` and `/blue-team` operate entirely within Zone 1 (Analysis) during a purple team exercise. Red-team findings are produced by `red-reporter`, which is a read-only reporting agent -- it does not execute exploits. Blue-team agents operate exclusively on local files. No live system access crosses between the two skills.

Given that both skills run in the same Jerry framework runtime, in the same process, with access to the same filesystem, one might ask why a trust boundary is necessary at all. The answer is that the trust boundary is not about network isolation or process isolation -- it is a data trust boundary: it governs what content format and taint level are permitted to travel between the two skills' agent contexts.

The issue is the nature of the content, not the nature of the channel. A red-team finding for a credential-dumping technique contains references to real malware hashes, command-and-control domains, exploit scripts, and authentication material. When a blue-team agent loads this content into its context window to write a detection rule, the content that models adversary behavior is now present in the detection analysis context. If that content is unstructured -- free text extracted from a narrative report -- there are two problems: the extraction is unreliable (natural language parsing produces errors), and the content may include text that resembles instructions, which is a prompt injection surface.

The trust boundary resolves this by specifying what form the data must take before it crosses. The RBEE (Red-Blue Exchange Envelope) schema enforces that only structured, schema-validated data crosses from red to blue: technique IDs in a specific regex format, file hashes as 64-character hex strings, domains validated for format, artifacts referenced by path rather than by content. The finding narrative -- which is free text that could contain anything -- is explicitly excluded from the RBEE. Blue-team agents never read the narrative; they read the structured extraction.

This is the meaning of the Phase 5 design principle: "metadata-only transfer." The RBEE transfers the metadata about what happened (which technique, what indicators, what taint level) without transferring the unstructured content of what happened.

---

## Why the Taint Model Is Asymmetric

The taint model classifies data crossing the trust boundary. Red-to-blue data is tagged with one of three taint levels: `adversary-produced` (malware artifacts created by the threat actor), `adversary-controlled` (infrastructure the threat actor controlled), or `engagement-generated` (artifacts created by the red team during the exercise). Blue-to-red data is tagged with a single taint level: `analysis-derived`.

The asymmetry reflects the fundamentally different epistemic status of the two data flows.

Red-team findings model adversary behavior. A hash, domain, or command sequence in a red-team finding represents something an attacker created or used. Even though `red-reporter` is a trusted Jerry framework agent, the content it describes carries the taint of its adversarial origin. A YARA rule written to detect a specific malware hash is only as valuable as the hash's authenticity; the detection rule embeds an assumption that the hash corresponds to real malicious behavior. This is why the taint level must be preserved across the boundary -- blue-team agents need to know whether they are building a detection rule for a verified threat actor artifact or for a hash that the red team generated during an exercise.

Blue-to-red data does not carry this kind of taint. Coverage feedback (CFE) and D3FEND gap analysis (DGE) are analytical conclusions produced from defensive methodology. The CFE says "technique T1059.001 has partial detection coverage in the log domain." The DGE says "technique T1566 has no detection rule, which is a high-priority gap." These are the outputs of a structured analytical process. They describe the state of the defensive posture, not the behavior of an adversary. `red-lead` and `red-vuln` receive these envelopes to make scoping decisions, not to model attack behavior -- so no adversary taint propagates from blue to red.

The asymmetry has a practical consequence: the blue-to-red direction requires significantly less sanitization. The CFE and DGE schemas validate technique and countermeasure ID formats, but they do not need the elaborate content-stripping that the red-to-blue direction requires. The structured nature of coverage feedback -- it is essentially a lookup table of technique ID to coverage status -- means the injection surface is narrow. An ID that fails the ATT&CK regex pattern is simply rejected; there is no free-text field that could carry a disguised instruction.

---

## Why Metadata-Only Transfer

The decision to restrict RBEE transfers to metadata rather than content is the most consequential design choice in the trust boundary model, and it is worth examining why content transfer was rejected.

The alternative would have been to transfer artifact content directly -- embedding the raw IOC values, YARA-targetable strings, or STIX bundles inline in the envelope. This would simplify the blue-team workflow: `blue-ioc` could receive a complete RBEE and immediately write a detection rule without needing to read separate artifact files.

The reasons for rejecting this approach are threefold.

First, inline content creates a prompt injection surface. The RBEE schema enforces strict formats for structured fields (technique IDs, hashes, IP addresses), but free-text fields like `indicator_summary` and `finding_narrative` are unconstrained. If the red-team finding describes a phishing email with a malicious subject line that happens to resemble an instruction (a realistic scenario in social engineering engagements), that text in a blue-team agent's context window is a potential injection vector. By keeping artifact content in files and referencing files by path, the blue-team agent can inspect the artifact file without loading arbitrary content into the main reasoning context.

Second, inline content balloons the context window. A single engagement with 12 findings, each containing a STIX bundle, multiple IOC strings, and evidence descriptions, could easily add 20,000--50,000 tokens to the exchange envelope. Across 12 RBEE envelopes in Session 2, that context overhead could exhaust the available budget before `blue-detect` has written a single YARA rule. File path references keep the envelope payload small -- a few hundred tokens per envelope -- and let agents selectively read artifact files when they need the content.

Third, inline content makes validation harder. A file hash embedded in a `file_indicators` array can be validated against the `^[a-f0-9]{64}$` pattern by the schema. The same hash in a free-text `notes` field cannot be reliably extracted or validated. Schema-enforced structure is the only reliable sanitization mechanism at scale.

The trade-off is operational complexity: blue-team agents must read artifact files, not just envelope fields. The design accepts this complexity because the security and context efficiency benefits outweigh it.

---

## Why Three Sessions

The three-session purple team model emerges from two forces: context window arithmetic and coordination topology.

**Context window arithmetic.** A complete purple team exercise runs eight phases, from scoping through reporting. Phase 4 analysis established that running all eight phases in a single session would require 210,000--280,000 tokens -- more than the 200,000-token context window. With cross-skill exchange envelopes adding an estimated 3,000--5,000 tokens of overhead per engagement, the single-session model is not merely tight; it is impossible.

The earlier Phase 4 design recommended a two-session split: phases 1--4 in Session 1, phases 5--8 in Session 2. However, this split was conservative about token usage, projecting Session 1 at 120,000--165,000 tokens. With a 190,000-token effective budget (200,000 minus the 5% output reserve from CB-01), that leaves 25,000--70,000 tokens of headroom -- which sounds reasonable until you account for the IP-5 pipeline.

The IP-5 pipeline (the red-to-blue indicator extraction and transformation) is the highest-context-pressure operation in the exercise. It requires both skills' agent contexts to be active simultaneously: `red-reporter`'s findings, `blue-ioc`'s rule generation logic, `blue-detect`'s validation methodology, and the RBEE envelope schemas. When both skills compete for the same context window, the available budget for actual work shrinks significantly.

The three-session model solves this by isolating the cross-skill context pressure into Session 2. Session 1 runs purely within `/red-team` plus scoping (no blue-team context required). Session 2 runs the IP-5 pipeline (both skills active, highest context pressure, but now bounded to a single defined session). Session 3 runs purely within `/blue-team` plus `/eng-team` for analysis and reporting. Each session has a focused context topology that stays within budget.

**Coordination topology.** Sessions are connected by checkpoint files that persist across the context window boundary. The checkpoint schema carries all the information the next session needs to resume: which phases completed, which artifacts were produced, the D3FEND coverage baseline, the exchange envelope manifest, and the token usage from the prior session. The receiving session validates that all referenced artifacts exist before proceeding -- this is the RV-02 check from the handoff protocol.

The checkpoint mechanism is conceptually analogous to a function call returning a structured result. The context window is the call stack; it is cleared between sessions. The checkpoint is the return value; it persists. Blue-team agents in Session 3 do not have direct access to Session 1's reasoning, but they have access to everything Session 1 decided to persist: the findings, the rules, the coverage baseline.

---

## The D3FEND Feedback Loop

The D3FEND integration creates a compounding improvement mechanism that operates across engagements rather than within a single engagement.

Within a single engagement, the D3FEND flow is: `blue-d3fend` maps the techniques in the engagement to D3FEND countermeasures, identifies which countermeasures are deployed (Verified), which are partially deployed (Partial), and which are absent (Unverified or Uncovered). This produces a D3FEND Gap Envelope (DGE) that `red-lead` can use when scoping a future engagement.

The feedback loop is that the DGE from engagement N informs the technique selection for engagement N+1. Techniques where the defender has no detection rule (DGE priority: `high`) are the most valuable candidates for the next RoE allowlist, because testing them produces useful information: either the defender builds a detection rule (progress) or the gap persists and is documented again (confirmed gap). Techniques where detection is Verified are less valuable to include, because the test outcome is predictable.

This creates a progressive quality improvement cycle: each engagement covers the highest-priority gaps, which either get closed (the blue team builds detection rules) or confirmed as persistent. Over multiple engagements, the gap set shrinks as the defensive posture matures. The exercise stops being a repeated survey of the same gaps and starts being a targeted test of newly identified weaknesses.

The mechanism has a constraint: the DGE records a `d3fend_kb_version` field, and `red-lead` must verify D3FEND KB version currency before incorporating gaps from a prior DGE. This constraint exists because the D3FEND knowledge base evolves -- new countermeasures are added, existing ones are modified. A DGE produced against D3FEND v0.15.0 might classify a technique as having no countermeasure, when D3FEND v1.0 added a countermeasure that has since been deployed. Without version verification, stale gap recommendations would mislead the scoping process. The version field is therefore not administrative metadata; it is a staleness detection mechanism.

The D3FEND integration also connects the purple team model to the broader detection posture in a way that ATT&CK coverage matrices alone cannot. ATT&CK tells you which techniques you have seen; D3FEND tells you which defensive techniques you have deployed against those ATT&CK techniques. The intersection of "we emulated this ATT&CK technique" and "we have no D3FEND countermeasure for this ATT&CK technique" is the highest-priority finding class: a known attack vector with no corresponding defensive control.

---

## Trade-Offs in the Design

The purple team model as designed accepts several constraints that limit its applicability in some scenarios.

**Large engagement overhead.** The three-session model is designed for engagements with 10--20 findings. An engagement with 50 or more findings produces 50+ RBEE envelopes. Session 2's context budget was estimated assuming a manageable envelope count; at 50 envelopes, even the metadata-only approach adds significant overhead. Large engagements may require a four-session model, with multiple batch-processing passes through the IP-5 pipeline. The checkpoint schema supports this extension (the `exchange_envelope_manifest` tracks counts), but the session entry prompts would need modification.

**Single engagement scope at a time.** The session model assumes one purple team engagement per context. Running concurrent engagements in the same context window would mix checkpoint states and exchange envelope directories. This is a deliberate constraint; the complexity of concurrent engagement management would overwhelm the coordination architecture. Users who need concurrent engagement tracking must use separate Jerry project directories.

**Tier C tool gap.** Six of the techniques in a representative engagement map to D3FEND countermeasures that require Tier C tools (Suricata, Zeek, Falco, Tetragon) for validation. These tools are not executed within the Jerry framework -- they are user-deployed infrastructure. The DGE records these as `untested` gaps rather than confirmed gaps, and the gap priority is set to `medium` rather than `high`. This means the feedback loop has a zone of partial information: the defender may have Suricata deployed and may have excellent detection for T1566 (phishing) via URL analysis, but the Jerry framework cannot verify this, so it conservatively records the gap as untested.

**Sequential session dependency.** Each session depends on the prior session's checkpoint. If a session fails midway (context exhaustion, unexpected error), the checkpoint at the prior boundary is the recovery point. Work performed within the failed session must be redone. The checkpoint validation checks (verify all artifacts exist, verify token budget from prior session) are defensive measures against partial failures, but they do not eliminate the recovery cost.

---

## Relationship to Broader Security Principles

The trust boundary model in PROJ-023 is an application of zero-trust principles to inter-agent data exchange. Zero trust's core axiom -- never trust, always verify -- is typically discussed in the context of network access control, but it applies equally to data trust in an agentic system.

The Jerry framework's P-003 constraint (no recursive subagents) and the RBEE's metadata-only transfer policy both implement the principle of least privilege in different dimensions. P-003 limits the delegation capability of agents: no agent can grant itself the authority to spawn further agents. The metadata-only transfer limits the information surface that crosses between skills: no agent can load adversary-modeled content into its context without explicit schema-controlled sanitization.

The asymmetric taint model connects to information security's concept of information flow control. In classical information flow theory, high-integrity data should not be contaminated by low-integrity data. Red-team findings that model adversary behavior are not low-integrity in the traditional sense -- they are produced by a trusted agent -- but they carry a different kind of taint: adversarial modeling. The blue-team agents' analytical conclusions should not be contaminated by unverified adversary-modeled content. The RBEE schema enforces this by stripping free text and requiring all content to be in validated structured form before it influences blue-team reasoning.

The three-session model also reflects a broader principle in secure system design: separation of duties at temporal boundaries. Session 1 is an offensive operations session; it ends before blue-team context is introduced. Session 2 is a cross-skill validation session with both contexts present but in a structured pipeline. Session 3 is a defensive analysis session; offensive context is no longer needed. The temporal separation prevents the offensive and defensive reasoning from conflating, which would undermine the adversarial authenticity of the test (if the red team knows the detection coverage before emulation, it can choose evasion paths that defeat the detection rules, which is realistic but defeats the purpose of measuring baseline detection capability).

These connections are not incidental. The architecture was designed with these principles as explicit inputs, and the resulting constraints -- metadata-only transfer, asymmetric taint, three-session separation -- are the structural expression of those principles in an LLM-based agentic framework.

---

*Source: `projects/PROJ-023-exploit-framework/work/design/phase-5-redblue-composition.md` (Phase 5 Red-Blue Composition design, SEC-MAJOR-3 resolution).*
