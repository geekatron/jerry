# Refutation Panel — Remediation-Value Lens — Iteration 10 — S-011 (Chain-of-Verification)

> Lens: REMEDIATION-VALUE. Question per finding: would fixing this materially change real
> adoption outcomes, or is it churn (optional polish / already scheduled elsewhere / adds
> machinery against the ratified subtraction doctrine)? Default: REFUTE if uncertain.

## Target

`projects/PROJ-031-cowork-skeleton/orchestration/adr-convention-20260702-001/adversary/iteration-010/s-011-findings.md`
— 1 Critical finding claimed: **CV-001-i010**.

---

## CV-001-i010: Canonical Location Model omits the actual location pattern of the two grandfathered `EPIC002` dialect ADRs; L-4 would misfire on them

**Verdict: REFUTED (remediation-value lens)**

**What the finder claims:** `ADR-EPIC002-001-strategy-selection.md` / `ADR-EPIC002-002-enforcement-architecture.md` live in `projects/PROJ-001-oss-release/decisions/` (a project `decisions/` folder) but carry the `EPIC{NNN}` dialect prefix, a (location, ID-form) pairing the Canonical Location Model table does not literally enumerate (ADR ~L384-393; rule-draft ~L77-88, both confirmed by direct read: row "Project (permitted dialect)" only lists ID form `ADR-PROJ{NNN}-NNN`; row "Entity-embedded (permitted)" allows the full `{PROJ|EPIC|FEAT|STORY}` set but its canonical home is `projects/.../work/.../{ENTITY}/`, not `decisions/`). The finder further argues Migration-Plan **M-11** (ADR ~L546, confirmed: "Retrofit real YAML frontmatter... onto... `ADR-EPIC002-001-strategy-selection`, `ADR-EPIC002-002-enforcement-architecture`...") is a scheduled git-modification of exactly these two files, which would expose them to L-4 for the first time, and that the grandfather-exemption wording at ADR ~L693 ("grandfathered-exempt from **L-1/L-2**") does not on its face extend to L-4.

**Why this is real but not remediation-worthy:**

1. **The lint (including L-4) is DESIGNED, NOT BUILT** — `scripts/lint_adr_convention.py` does not exist (ADR ~L659, "Claim-Status: the lint is DESIGNED, NOT BUILT... nothing today prevents a non-compliant ADR from merging"). The entire scenario the finding worries about — L-4 "misfiring" — cannot happen today; it is a conditional, twice-deferred concern (both **M-6**, build the lint, and **M-11**, retrofit the frontmatter, are unscheduled `TBD-Task` rows per ADR ~L530-547) about how a not-yet-written program might someday behave.

2. **D-4 itself states a blanket grandfather principle that resolves the ambiguity the finder relies on.** ADR ~L223 (Decision D-4): "The **15 pre-existing** dialect ADRs remain valid legacy-dialect instances **in place**." This is stated once, comprehensively, with no per-rule carve-out. The narrower "grandfathered-exempt from L-1/L-2" phrase the finder cites (ADR ~L693) sits inside a paragraph explicitly titled "L-1 wording, not a sixth rule" (ADR ~L693 heading) — i.e., that paragraph is scoped to clarifying L-1's own grandfather note, not to affirmatively excluding L-4/L-3/L-7 from grandfather coverage. Read against D-4's blanket "valid... in place" framing (Internal Consistency requires reading the whole document, not an isolated clause), a future implementer building M-6 would almost certainly extend grandfather protection across all 5 rules — the entire architectural point of "grandfathered" is that these files are NOT to be broken by the lint.

3. **M-11 does not actually change filename or location** — it retrofits YAML frontmatter only (ADR ~L546: "Retrofit real YAML frontmatter (`id`/`scope`/`origin_project`)"). L-4 ("ID↔location") is a function of filename-prefix vs. containing directory (ADR ~L689) — a property M-11 does not touch. Even under the finding's own worst-case reading (grandfather narrowly scoped to L-1/L-2, so a modified file is newly exposed to L-4), the (location, ID-form) pairing itself is not new — it exists on disk today and has for months; nothing about M-11 changes what L-4 would evaluate.

4. **The proposed correction is optional-polish-grade disclosure hygiene for a hypothetical tool defect, not a defect in the convention's actual, currently-operative value.** The document's real-world value today is MEDIUM-tier authoring guidance ("delivers value with zero tooling," ADR ~L659); this finding touches zero authoring behavior for new ADRs and affects only a deferred, dual-contingent (M-6 **and** M-11 must both land) corner of an unbuilt enforcement mechanism on 2 already-grandfathered legacy files. Fixing it (a table row or a residual sentence) would not change any real adopter's experience — the convention already tells authors precisely what to do (subject-slug default; dialect only for certain never-promoting locals), and the M-11 frontmatter retrofit is explicitly labeled "optional schema-completeness, not a lint-gating requirement" (ADR ~L546) regardless of this finding.

5. **The rule draft is already at its self-acknowledged line-budget ceiling** — the companion draft's own changelog (rule-draft ~L251-253) discloses it is "now marginally above the 250-line self-guidance (253 lines)... above the ~2.5k soft target — disclosed." Nine prior iterations have already added residual rows (R-9 through R-17) for structurally analogous narrow location/grandfather edge cases. Continuing to accept "one more disclosure row" for an increasingly narrow, twice-deferred, textually-already-resolvable-via-D-4 edge case is the subtraction doctrine's diminishing-returns failure mode, not a material adoption-outcome fix.

**Disposition:** REFUTED under the remediation-value lens. The finding is evidenced and not fabricated, but its fix would not materially change real adoption outcomes — it is optional polish on a hypothetical defect in a lint that does not exist, resolvable in practice by the document's own dominant "grandfathered... in place" principle (D-4), and gated behind two unscheduled future actions (M-6, M-11) neither of which is committed.

---

## Summary

| ID | Verdict | Basis |
|----|---------|-------|
| CV-001-i010 | REFUTED | Unbuilt lint (advisory-only); D-4's blanket grandfather-in-place principle resolves the narrow L-1/L-2-only reading the finder relies on; M-11 changes frontmatter only, not filename/location; fix is disclosure-only polish for a doubly-deferred (M-6 + M-11) hypothetical tool-behavior edge case on 2 already-grandfathered files — no material change to real adoption outcomes. |

**Verified: 0. Refuted: 1 (all Criticals in the target report).**
