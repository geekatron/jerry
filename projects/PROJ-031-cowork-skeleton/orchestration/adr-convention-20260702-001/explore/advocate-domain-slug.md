# Blind Advocate Brief: Scheme B — Domain-Slug Everywhere

> **Role:** Appointed blind advocate FOR identifier scheme B (`ADR-{domain-slug}-NNN`, origin in frontmatter, promotion = pure file move).
> **Blindness declaration (P-022):** I did not read any file under `projects/PROJ-031-cowork-skeleton/orchestration/adr-convention-20260702-001/` other than this output file. All evidence below is drawn from: the research artifact at `projects/PROJ-031-cowork-skeleton/research/adr-convention-standards-research.md`, live `docs/design/` ADRs, `git log`/`git show` provenance, and `projects/PROJ-030-bugs/reviews/BUG-006-adr-naming-evaluation.md`.
> **Status:** COMPLETE — written incrementally per P-002.

## Navigation

| Section | Purpose |
|---------|---------|
| [1. Position](#1-position) | The schemes under evaluation and my assignment |
| [2. Steelman Case for B](#2-steelman-case-for-b) | Strongest evidence-based argument for domain-slug-everywhere |
| [3. Own Weakest Point](#3-own-weakest-point) | Honest self-critique + mitigation |
| [4. Fatal-Weakness Attacks on Rivals](#4-fatal-weakness-attacks-on-rivals) | A/C, D, E, F attacked with quantified evidence |
| [5. Sensitivity Analysis vs. Promotion Frequency](#5-sensitivity-analysis-vs-promotion-frequency) | Does B's case survive if promotion is rare? |
| [6. What Would Change My Mind](#6-what-would-change-my-mind) | Falsifiable conditions |
| [7. Evidence Ledger](#7-evidence-ledger) | Every citation with file path / line / commit SHA |

---

## 1. Position

Schemes under evaluation (per assignment, plus none newly discovered beyond the six given):

- **A.** Project-scoped sequence: `ADR-{PROJECT-ID}-NNN`
- **B (mine).** Domain-slug everywhere: `ADR-{domain-slug}-NNN`, origin in frontmatter, promotion = pure file move
- **C.** Two-namespace (project-scoped at birth, domain-slug after promotion, renumber-on-promotion + tombstone)
- **D.** Date-based: `ADR-YYYYMMDD-slug`
- **E.** Global monotonic: `ADR-NNNN`
- **F.** Scope+slug, no number: `ADR-{SCOPE}-{slug}`

I argue B should govern the **one artifact class in Jerry engineered to migrate scope** — the ADR — while conceding (Section 3) that Jerry's broader entity ontology (PROJ/EPIC/STORY/DEC) is correctly scope-prefixed because those entities do not migrate.

---

## 2. Steelman Case for B

### 2.1 The live repo already converged on B — and paid to get there

The three `docs/design/` ADRs are Jerry's only framework-baselined, C4-criticality ADRs, and **all three were born with project/entity-scoped identity (scheme A/C) and later force-migrated to domain-slug (scheme B)** via a dedicated remediation project:

| ADR (current, domain-slug) | Frontmatter origin (still preserved) | Birth identity (scheme A/C) | Rename commit |
|---|---|---|---|
| `docs/design/ADR-agent-design-001.md` (line 3: `PS-ID: PROJ-007 \| ENTRY: e-004`) | PROJ-007 | `ADR-PROJ007-001-agent-design.md` (added `docs/design/` 2026-02-22, commit `66a5826f`) | `5ef0b2fa` (2026-04-13), git-detected **R099** rename |
| `docs/design/ADR-routing-triggers-001.md` (line 3: `PS-ID: PROJ-007`) | PROJ-007 | `ADR-PROJ007-002-routing-triggers.md` (added 2026-02-22, `66a5826f`) | `5ef0b2fa` (2026-04-13) |
| `docs/design/ADR-output-path-resolution-001.md` (line 8: `Parent: EPIC-002`) | EPIC-002 (PROJ-001-oss-release) | `ADR-EPIC002-001-output-path-resolution.md` (added 2026-03-31, commit `9b36bda2`, whose own message calls it "ADR-EPIC002-001" despite the body noting "Placed in `docs/design/` (framework-wide standard, not project-scoped)") | `41539073` (2026-04-13) |

Verbatim commit messages (both dated 2026-04-13, part of the same BUG-006 C4 remediation cycle):

- `41539073`: *"ADR renamed from ADR-EPIC002-001 to ADR-output-path-resolution-001 using domain-first semantic convention per UX heuristic evaluation (recognition over recall, collision resistance). **~150 references updated across skills.**"*
- `5ef0b2fa`: *"Renamed peer ADRs to domain-first convention for consistency: ADR-PROJ007-001 → ADR-agent-design-001, ADR-PROJ007-002 → ADR-routing-triggers-001. Updated references in active rule/standard files."* — diff touches `.context/rules/agent-development-standards.md` (+/-6 lines), `.context/rules/agent-routing-standards.md` (+/-8 lines), `skills/user-experience/SKILL.md` (+2/-1).

**This is not a hypothetical promotion tax — it is a paid one, with a receipt.** Every framework ADR that exists today was authored under scheme A/C identity and required a dedicated, C4-criticality bug-fix effort (BUG-006, spanning iter2 through iter8 rescoring, a tournament review, and multiple group reviews — see `projects/PROJ-030-bugs/reviews/BUG-006-*`) to correct the resulting usability failure. B's entire value proposition — assign the eventual domain identity at birth so promotion is a `git mv` with zero rename — would have prevented exactly this cost.

**The debt is not even fully repaid today (2026-07-02), 2.5 months later.** Live `grep` for the extinct IDs `ADR-PROJ007-001`/`ADR-PROJ007-002` still finds stale, broken citations inside PROJ-007's own artifacts — i.e., the rename's originating project never fixed its own back-references:

- `projects/PROJ-007-agent-patterns/ORCHESTRATION.yaml:228,242`
- `projects/PROJ-007-agent-patterns/WORKTRACKER.md:106-107`
- `projects/PROJ-007-agent-patterns/work/EN-001-install-agent-pattern-deliverables/EN-001.md:48-49,72-73`

(`CHANGELOG.md:75-76` is a legitimate historical note about the rename and is excluded from this count.) This is the promotion tax's long tail: a scheme-A/C rename event does not terminate when the two "fixer" commits land — it leaves residual, silently-broken citations in the very project that produced the artifact, discoverable only by grepping for a dead ID months later.

### 2.4 Precedent from outside the repo: slug-as-identity is a deliberate, documented choice, not a novelty

Log4brains made an explicit ADR titled *"Use the ADR slug as its unique ID"* and **abandoned sequential numbering specifically because shared numeric sequences caused git merge conflicts** when concurrent branches minted the same next number (research doc lines 98-100, citing log4brains ADR 20201016). Jerry's multi-agent, multi-session, potentially-parallel orchestration model (`ps-architect`, `orch-planner` agents can run across concurrent projects) is a closer match to log4brains' failure conditions than to a small human team's. Subject-encoded identity sidesteps this because the "next NNN" is scoped to a slug chosen once, by subject, not raced over a single shared counter (contrast with rival E, Section 4).

---

## 3. Own Weakest Point

**Honest weakest point: slug-uniqueness is a governance discipline, not a structural guarantee — and B is the one outlier against Jerry's dominant scope-prefixed ontology.**

- Every other Jerry entity ID (`PROJ-NNN`, `EPIC-NNN`, `STORY-NNN`, worktracker `{ParentId}--DEC-NNN-slug` per `adr-convention-standards-research.md:88`) is scope-prefixed and therefore collision-free **for free**, by construction, because the parent scope ID is already globally unique. B has no such free lunch: nothing today stops two unrelated authors from both minting `ADR-security-001` for different subjects. Scope-prefixing (A/C) would never produce that collision because `PROJ-014` and `PROJ-031` cannot collide with each other by definition.
- This is a real cost, not a theoretical one: the research artifact's own BUG-006 F-002 finding (severity 2) is precisely a collision-ambiguity concern, and while the specific corroborating example (`ADR-EPIC002-001` allegedly in both PROJ-022 and PROJ-004) was later shown by `ps-researcher` to be **factually incorrect** (research doc line 200: verified to exist only in PROJ-001-oss-release), the underlying mechanism the finding warns about — namespace collision at scale — is real and unaddressed by B without added tooling.
- Divergence from ontology consistency has a real onboarding/documentation cost: a new contributor has to learn "ADRs are the one entity type that does NOT follow PROJ/EPIC/STORY scope-prefixing," which is one more exception to hold in working memory.

**Mitigation:**
1. **L5 CI lint enforcing global slug uniqueness** across `docs/design/` (deterministic, zero-token, matching the research artifact's own proposed enforcement mechanism at `adr-convention-standards-research.md:182` — "deterministic L5 CI lint"). This converts an informal discipline into an automatically-checked one, closing the gap with scope-prefixing's free collision-avoidance.
2. **Scope the divergence explicitly and narrowly to the ADR artifact class**, not to Jerry's entity ontology generally. The mitigation is definitional, not structural: PROJ/EPIC/STORY/DEC are entities whose scope **is** their identity and never migrates (a project is never re-parented into becoming part of a different project). The ADR is the one artifact class Jerry deliberately designs to migrate scope (Section 2.3) — so the divergence is not framework inconsistency, it is correctly differentiated design for a structurally different lifecycle. This should be stated as an explicit rule-file callout, not left implicit, to pre-empt the "why is this one thing different" onboarding question.
3. **Origin is relocated, never deleted.** All three existing framework ADRs already prove origin survives an identity change losslessly via frontmatter (`PS-ID`, `Parent`) — so any traceability argument for A/C is already satisfied by B without needing the identity string to carry it.

---

## 4. Fatal-Weakness Attacks on Rivals

### 4.1 vs. A (project-scoped sequence) — the promotion tax, quantified

Scheme A is not a hypothetical rival — it is **the exact scheme all three framework ADRs were born under**, and it is **the exact scheme the repo's own Nielsen evaluation found to fail 4/10 heuristics, 2 at major severity** (Section 2.2). Quantified promotion tax, from the live git record:

| What breaks | Who pays | When |
|---|---|---|
| ~150 references across skills (per commit `41539073` message, for the output-path ADR alone) | Whoever performs the BUG-006 C4 remediation cycle — not the original author, not at authoring time, but a dedicated later effort | 2026-04-13, **~2 weeks after** the ADR was authored (2026-03-31, commit `9b36bda2`) |
| References in `.context/rules/agent-development-standards.md` (6 lines) and `.context/rules/agent-routing-standards.md` (8 lines), `skills/user-experience/SKILL.md` (1 line) | Same remediation effort, commit `5ef0b2fa` | 2026-04-13, **7 weeks after** the PROJ-007 ADRs were first installed into `docs/design/` (2026-02-22, commit `66a5826f`) |
| Residual stale citations to the extinct `ADR-PROJ007-001`/`002` IDs in `ORCHESTRATION.yaml`, `WORKTRACKER.md`, `EN-001.md` (6 lines across 3 files) — **never fixed** | Nobody yet — this debt is unpaid as of 2026-07-02 | Indefinite / open |
| A dedicated C4-criticality bug ticket (BUG-006) had to exist at all, consuming a full Nielsen evaluation + tournament review + 6+ rescoring iterations, merely to fix an ID naming choice | The whole framework's review capacity for that cycle | 2026-04 (multi-week C4 process, per `BUG-006-c4-*` files enumerated in `projects/PROJ-030-bugs/reviews/`) |

Additionally, scheme A's identity string is doubly indirect once a project archives: `docs/archive/projects-archive/decisions/` already holds frozen `ADR-031..034` (research doc line 65) — under scheme A, a reader of a promoted, still-live framework ADR would need to know that its origin project has since been archived/renumbered to even parse the ID, a lookup burden Nielsen H2/H6 already penalize at major severity even *without* archival compounding it.

### 4.2 vs. C (two-namespace, renumber-on-promotion + tombstone)

C is presented as the disciplined middle path, but the live record shows **C is what actually happened, and it is exactly as expensive as A's failure mode, just with a name attached.** Every cost quantified in 4.1 IS the "renumber-on-promotion" step C prescribes — C does not avoid that cost, it formalizes paying it every single time a promotion occurs. The tombstone/back-link helps *future* readers after the fact, but does nothing for the citations that already existed *before* the tombstone was created — which is precisely why 6 stale references in PROJ-007's own worktracker artifacts remain broken today: the "renumber + backlink" step happened, but exhaustive backward citation repair did not, and the research artifact concedes (line 113) that **no external source even prescribes the concrete mechanic** for this — "the promotion recipe (ID remap + `PROMOTED_FROM/TO` back-link) is my synthesis," i.e., C is admittedly unproven design, not observed best practice.

C also silently changes what `NNN` means mid-flight: `ADR-PROJ007-001` (1st ADR in PROJ-007) becomes `ADR-agent-design-001` (1st ADR in the agent-design domain) — these are two different sequences wearing the same digits by coincidence. That is not a renumbering, it is a full identity replacement dressed up as a rename. B simply picks the correct sequence once, at birth, and never replaces it.

### 4.3 vs. D (date-based, `ADR-YYYYMMDD-slug`)

D solves Jerry's actual documented collision problem (bare `ADR-NNN` reuse across scopes, research doc lines 70-81) no better than B, while sacrificing every recognition/sortability win. `ADR-20260221-...` is exactly as opaque as `ADR-PROJ007-...` under Nielsen H2/H6 — a date has zero semantic content about domain, same major-severity failure BUG-006 found against entity IDs (Section 2.2). Worse for H7 (sortability): `ls docs/design/ADR-*` under D clusters by **creation date**, not by subject — the opposite of BUG-006 F-004's explicit ask ("all agent-related ADRs cluster together... enable grep queries like `grep -r \"ADR-agent-\" docs/design/`," line 151). D also imports log4brains' merge-conflict rationale into Jerry without Jerry having that specific problem: Jerry's observed collisions are cross-**scope** ID reuse (three different `ADR-001`s in three different contexts, research doc lines 74-77), not two agents racing to claim the same monotonic integer on the same day — a domain-slug-scoped sequence (B) already prevents the former, and the latter is a non-issue at Jerry's per-domain authoring cadence.

### 4.4 vs. E (global monotonic, MADR-style `ADR-NNNN`)

E requires a repo-wide central counter/registry that does not currently exist in Jerry and that the research artifact's own tiering rationale would resist adding (MEDIUM-tier, no new HARD rule, ceiling at 25/25 — `.context/rules/quality-enforcement.md` cited at research doc lines 178-182). E is **precisely the architecture log4brains adopted first and then abandoned** after real production pain: *"ADR numbers must be unique... caused conflicts during git merge when two developers created new ADRs on their respective branches"* (research doc line 100, log4brains ADR 20201016). Jerry's parallel multi-agent orchestration model (concurrent `ps-architect`/`orch-planner` invocations across projects, explicitly designed into the framework) is at *greater*, not lesser, risk of this exact race than the human team log4brains observed it in. E also fails Nielsen H2/H6 identically to D — `ADR-0842` carries no more subject information than `ADR-PROJ007-001` did before its rename.

### 4.5 vs. F (scope+slug, no number)

F is B's closest cousin and the fairest rival — worth steelmanning before attacking (S-003): if `{SCOPE}` is read as domain-slug, F shares all of B's recognition/discoverability wins. But F discards the one thing Nygard/MADR/adr-tools all deliberately keep: a disciplined, monotonic, never-reused sequence number for **multiple decisions on the same subject over time** (a revision that doesn't rise to full supersession). Losing NNN doesn't eliminate the need for disambiguation — it just pushes it into the slug itself. The repo already shows this happening organically and ungoverned: the "Lowercase ad-hoc" family in orchestration drafts (`adr-cli-integration`, `adr-cli-integration-v2` — research doc line 68) is exactly F's failure mode in the wild — informal `-v2`/`-v3` slug suffixing reinvents a sequence number without governance, naming discipline, or tombstone/supersede semantics. B keeps F's referenceability advantage while retaining a governed per-slug sequence instead of an ad-hoc one.

---

## 5. Sensitivity Analysis vs. Promotion Frequency

The user's crux explicitly demands this: does B's case survive if promotion turns out to be rare?

**Measured base rate (filesystem-verified, research doc lines 57-68):** `docs/design/` currently holds exactly **3** ADRs. Project/entity-scoped ADRs currently number **15** (`PROJ010`×6, `PROJ022`×2, `PROJ031`×3, `EPIC002`×2, `STORY015`×1, GH-issue-`150`×1). Raw promotion rate across all ADRs ever created: **3-in-18 ≈ 17%** — not "most ADRs migrate."

**But the raw rate is the wrong denominator.** Of the two projects whose *entire mandate* was to produce framework-general governance (PROJ-007 "agent patterns," and EPIC-002 within PROJ-001 "quality enforcement / output-path resolution"), **100% of their flagship decision artifacts were promoted** (2-for-2 PROJ-007 ADRs; 1 of EPIC-002's 2 ADRs — the output-path one — with the strategy-selection ADR, `ADR-EPIC002-001-strategy-selection.md`, correctly staying project-scoped as pure internal governance). Promotion frequency is therefore **bimodal, not uniform**: near-zero for tactically-scoped, single-project decisions, and high for the subset of ADRs a project author already knows will govern the framework broadly.

**If promotion frequency were driven toward zero as a matter of policy** (i.e., Jerry decided docs/design/ should only ever be populated by hand-authored, never-promoted ADRs), my case weakens substantially: A/C's birth-time simplicity (free collision avoidance, no slug-uniqueness governance needed) would dominate for the near-100% of ADRs that never leave their project, and B's discipline becomes overhead paid broadly for a benefit realized rarely.

**But that is not the observed or foreseeable regime.** Two structural facts push the other way:
1. **The corpus is asymmetric and compounding.** `docs/design/` only grows in one direction over time (nothing is ever demoted back into a project), so even a low per-project promotion rate accumulates into an ever-larger framework corpus — precisely the corpus BUG-006 flagged as "critical at 50+ ADRs" (F-002, line 104) even though "low at current scale (6 ADRs)." The tax scales with corpus size, not promotion frequency.
2. **Jerry's own thesis (Section 2.3) makes promotion-oriented projects a recurring, intentional pattern, not noise.** PROJ-007 and EPIC-002 are not outliers to be dismissed — they are instances of exactly the "accrue knowledge into the framework" pipeline the framework is built to run repeatedly, including future projects like this very one (PROJ-031, whose ADR-convention research is itself a candidate for eventual `docs/design/` promotion).

**Honest concession:** B's strongest form ("every ADR anywhere uses domain-slug from the moment of creation") is defensible only for ADRs whose authors already have framework-relevance intent at birth — which the 2-for-2 / 1-of-2 promoted-ADR evidence suggests is a knowable, declarable property at authoring time, not a retroactive guess. For ADRs with no framework ambition, scheme A's birth-time simplicity is genuinely cheaper and I do not contest that. My case is strongest as **"B for framework-intended ADRs from birth,"** not as "B unconditionally for every ADR in every project."

---

## 6. What Would Change My Mind

1. **A no-promotion policy.** If Jerry adopted (and enforced) a rule that `docs/design/` may only be populated by ADRs hand-authored directly there — never migrated from a project — the 3-for-3 promotion-then-rename pattern (Section 2.1) would stop recurring, and my strongest empirical evidence (the paid tax) would become historical rather than a live warning about future cost.
2. **Automated citation-repair tooling.** If a deterministic tool existed (e.g., a CI-triggered repo-wide grep-and-replace keyed to `git mv` detection) that made "rename ID + update every citation" a single zero-human-effort operation, the quantified promotion tax (~150+ manual reference updates across two dedicated commits, plus 6+ references still stale 2.5 months later) would collapse toward zero. That is the single strongest empirical pillar of my case, and it is falsifiable/buildable — if it existed today, I would concede scheme C is viable at low marginal cost.
3. **Evidence of real domain-slug collisions.** If two unrelated projects independently produced ADRs that collided on the same domain-slug (e.g., two different subjects both wanting `ADR-security-001`), forcing awkward manual disambiguation, that would validate my own weakest point (Section 3) as a materialized cost rather than a theoretical one, and would shift weight back toward scope-prefixing's structural collision-freedom.
4. **A promotion rate that stayed near zero even for framework-mandate projects** (i.e., if future PROJ-007/EPIC-002-like efforts stopped producing promoted ADRs) would falsify the bimodal-frequency argument in Section 5 and remove the strongest rebuttal to the "promotion is rare" objection.

---

## 7. Evidence Ledger

| # | Claim | Source | Type |
|---|---|---|---|
| 1 | 3 framework ADRs currently domain-slug; frontmatter preserves origin (`PS-ID`/`Parent`) | `docs/design/ADR-agent-design-001.md:3`; `docs/design/ADR-routing-triggers-001.md:3`; `docs/design/ADR-output-path-resolution-001.md:8` | Fact (read) |
| 2 | All 3 were added to `docs/design/` under project/entity-scoped IDs first | `git show --stat 66a5826f` (added `ADR-PROJ007-001-agent-design.md`, `ADR-PROJ007-002-routing-triggers.md`); `git show --stat 9b36bda2` (added, per commit message, "ADR-EPIC002-001 Unified Output Path Resolution Protocol") | Fact (git) |
| 3 | Both were later renamed to domain-slug via R099-detected git renames | `git log --all --follow --name-status -- docs/design/ADR-agent-design-001.md` shows `R099 docs/design/ADR-PROJ007-001-agent-design.md → docs/design/ADR-agent-design-001.md` at commit `5ef0b2fa`; `git show --stat 41539073` shows `{...lution.md => ADR-output-path-resolution-001.md}` | Fact (git) |
| 4 | ~150 references updated for the output-path rename; rule-file reference updates for the PROJ-007 pair | `git log -1 41539073` message; `git show --stat 5ef0b2fa` (`.context/rules/agent-development-standards.md` +/-6, `.context/rules/agent-routing-standards.md` +/-8, `skills/user-experience/SKILL.md` +2/-1) | Fact (git) |
| 5 | Stale/broken citations to extinct `ADR-PROJ007-001/002` IDs persist today | `grep -rn "ADR-PROJ007-001\|ADR-PROJ007-002"` → `projects/PROJ-007-agent-patterns/ORCHESTRATION.yaml:228,242`; `WORKTRACKER.md:106-107`; `work/EN-001-.../EN-001.md:48-49,72-73` | Fact (live grep, 2026-07-02) |
| 6 | Nielsen evaluation: current entity-ID convention fails 4/10 heuristics, 2 at major severity | `projects/PROJ-030-bugs/reviews/BUG-006-adr-naming-evaluation.md:12-21,69-153,174-183` | Fact (read) |
| 7 | BUG-006 recommends "Alternative 3 (Domain-First Semantic)" as immediate remediation | `BUG-006-adr-naming-evaluation.md:21,195` | Fact (read) |
| 8 | Log4brains: slug-as-ID decision; abandoned numeric sequence due to git merge conflicts | `adr-convention-standards-research.md:98-100` (citing log4brains ADR 20201016) | Fact (research doc, externally sourced) |
| 9 | Jerry thesis: "Accrues knowledge, wisdom, experience"; filesystem-as-memory | `CLAUDE.md` Identity section (system context) | Fact (read) |
| 10 | ADR counts: 3 promoted vs. 15 project/entity-scoped | `adr-convention-standards-research.md:57-68` | Fact (research doc, filesystem-verified by ps-researcher) |
| 11 | BUG-006 F-002's specific corroborating collision example was factually wrong (corrected by ps-researcher) | `adr-convention-standards-research.md:200` | Fact (research doc P-022 disclosure) — cited to be transparent that I am not relying on the disputed example, only the underlying mechanism |
| 12 | No external source prescribes the concrete promotion ID-remap mechanic; it is synthesis | `adr-convention-standards-research.md:113,158,202` | Inference (labeled by ps-researcher, relayed here) |
| 13 | Worktracker `DEC-NNN` is a distinct, scope-prefixed, non-migrating entity — used to argue B's divergence is correctly differentiated, not inconsistent | `adr-convention-standards-research.md:88` | Fact (research doc) |
| 14 | Ad-hoc `-v2` slug suffixing already happens ungoverned in orchestration drafts (used against rival F) | `adr-convention-standards-research.md:68` | Fact (research doc) |
| 15 | HARD rule ceiling at 25/25 — no new HARD rule for E's registry requirement is realistic | `adr-convention-standards-research.md:178-182`; `.context/rules/quality-enforcement.md` | Fact (rule file) |

**Confidence:** High on all git-provenance and file-content claims (directly read/executed). Medium on the "bimodal promotion frequency" inference in Section 5 (built from a 2-project sample; explicitly labeled as inference, not a large-N statistical claim).


### 2.2 The formal usability verdict against A/C is severe, not marginal

`projects/PROJ-030-bugs/reviews/BUG-006-adr-naming-evaluation.md` is a Nielsen heuristic evaluation of **the then-current convention**, `ADR-{ENTITY_ID}-{NNN}` (line 12) — i.e., scheme A/C's identity model. Verdict (lines 12-21, 174-183):

| Heuristic | Severity | Finding |
|---|---|---|
| H2 (match system/real world) | **3 (major)** | "Entity IDs (\"EPIC002\", \"PROJ007\") are opaque to non-initiates and lack semantic content" (F-001, line 71-83) |
| H6 (recognition over recall) | **3 (major)** | "Users cannot recognize what an ADR addresses without looking it up. `ADR-EPIC002-001` is meaningless without context" (F-003, lines 117-136) |
| H4 (consistency/standards) | 2 (moderate) | Entity-ID prose citations are ambiguous across projects (F-002, lines 92-108) |
| H7 (flexibility/efficiency) | 2 (moderate) | "Directory listings sort by entity ID first... not by decision domain"; power users cannot `grep` or cluster by subject (F-004, lines 139-153) |

Total: **4 of 10 heuristics fail, 2 of them at major severity**, against the current dominant scheme (A/C). The evaluation's own remediation roadmap (lines 187-204) explicitly recommends "Alternative 3 (Domain-First Semantic)... immediately as the baseline for all new ADRs" — i.e., scheme B. This is the argument the framework's own maintainers accepted and acted on (Section 2.1).

### 2.3 Jerry's constitutive thesis says promotion is the point, not the exception

CLAUDE.md's Identity section states the framework's *raison d'être* in one sentence: *"Jerry -- Framework for behavior/workflow guardrails. Accrues knowledge, wisdom, experience."* and *"Core Solution: Filesystem as infinite memory. Persist state to files; load selectively."* An ADR that starts as a project-local decision and is later recognized as framework-general **is the literal mechanism by which "knowledge accrues"** — it is not a rare edge case to be handled awkwardly, it is the pipeline the thesis describes. The evidence in 2.1 shows this pipeline has already fired for **100% of the ADRs that ever reached `docs/design/`** (3 for 3). An identifier scheme that treats promotion as a first-class, zero-cost operation (B) is more aligned with Jerry's own stated purpose than one that treats it as a disruptive identity-replacement event requiring a dedicated bug-fix cycle (A/C, as empirically observed).
