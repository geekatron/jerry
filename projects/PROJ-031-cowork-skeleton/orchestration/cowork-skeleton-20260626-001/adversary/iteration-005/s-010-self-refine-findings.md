# S-010 Self-Refine — Consolidated Cross-Artifact Consistency (iteration-005)

> **Agent:** ps-architect (CREATOR, Group A / S-010 Self-Refine) — NOT a blind adversary.
> **Project:** PROJ-031-cowork-skeleton · **PS:** cowork-skeleton-20260626-001 · **Criticality:** C4 · **Gate:** ≥ 0.92
> **Mandate:** drive UP the iteration-004 **Internal Consistency 0.62** by hunting cross-artifact drift BEFORE the blind adversaries review.
> **Edit boundary honored:** fixed IN PLACE only ADR-001 + ADR-003 (owned). requirements/ and security/ are READ-ONLY → recorded as routed findings. No locked decision or requirements-mirror-dependent value (per-job perms, D7 poll design, file counts ~1,417/~6,344, RTB-1..5, SC-06 meaning) was changed.
> **Date:** 2026-06-29

---

## Document Sections

| Section | Purpose |
|---------|---------|
| [1. Consistency Defects FOUND](#1-consistency-defects-found) | Every cross-artifact drift located, by category |
| [2. Fixes APPLIED (ADR-side)](#2-fixes-applied-adr-side) | 13 owner edits, before → after |
| [3. Findings ROUTED](#3-findings-routed-to-other-owners) | nse-requirements + security, exact location + precise change |
| [4. Posture & Readiness](#4-self-assessed-internal-consistency-posture--readiness) | Self-assessment + blind-tournament verdict |
| [5. Verification Honesty (P-022)](#5-verification-honesty-p-022) | What I verified vs did not |

---

## 1. Consistency Defects FOUND

Hunted across all five artifacts (ADR-002 confirmed `Status: Superseded by ADR-003` — used only to confirm nothing references it as *active*).

### D-1 — File-count drift (source repo: 6,348 vs canonical 6,344)
ADR-003 Dimension-1 Option C said `CoWork clones main (~6,348 files)`. Every other doc (ADR-001 L0/Context/Option C, requirements L0/REQ-002) uses **~6,344**. `6,348` is a lone typo. **Owned → FIXED.**

### D-2 — File-count drift (skeleton size: stale 1,749 / 1,744)
- `security/phase2-stride-threat-model.md` L81 pipeline diagram: `default branch = skeleton ~1,749 files` (ADR-003's parallel diagram L86 correctly says **~1,417**). **STALE.** → ROUTE security.
- `requirements/phase1-requirements.md` carries three now-stale numbers post-correction: REQ-005 note quotes ADR-001 as saying `tests/ "retained today (1,744 ≪ 5,000)"`; checklist L534 says `ADR-003 diagrams show ~1,749 files`; iteration-1 note L596 says L0 was set to `~1,744 (~1,745 with stub)`. ADR-001 (iter-4) and ADR-003 (iter-4 A-6) have both moved to **~1,417**, so all three requirements notes are obsolete. → ROUTE nse-requirements.

### D-3 — Threat-ID COLLISION: `SC-06` means two different things
- STRIDE model: **SC-06 = "Two-repo drift / staleness"** (L198 row, L244 summary; banded `2×3=6 G`).
- ADR-003 + requirements: **SC-06 = "Trusted-Maintainer rogue build"** (ADR-003 L148, RTB-2, risk table; requirements REQ-051; banded LOW×HIGH YELLOW).
ADR-003 even asserts the trusted-maintainer path "was absent from the Phase-2 STRIDE model" — true for the *threat*, but the *identifier* `SC-06` was already taken by the drift threat. Anyone cross-referencing `SC-06` gets conflicting definitions + bands. This is the single highest-impact Internal-Consistency / Traceability defect in the package. **Owned side DISCLOSED (FIX-2); global reconciliation ROUTED to security (Phase-3 STRIDE).**

### D-4 — Stale ADR-002 "active owner" pointers throughout ADR-001
ADR-001 still pointed to **superseded ADR-002** as the *live* owner of the integrity architecture / credential in 6 places (L45 L0 "integrity architecture lives in ADR-002"; L57 "ADR-002 selects the push credential"; L196 telemetry "see ADR-002"; L302 "published expected SHA (ADR-002 …)"; L312 "ADR-002's monitor"; L315 "owned by ADR-002 §Continuous Integrity Monitoring"; Related Decisions L369 "ADR-002 | DEPENDS_ON"; nav L33). ADR-003 (D4/D7) is the actual owner. ADR-001's Related Decisions table also **omitted ADR-003 entirely**. **Owned → FIXED.**

### D-5 — Direct contradiction: ADR-001 still stated the false claim ADR-003 says it "corrected"
ADR-003 D5 (L204): *"We also correct the false ADR-001 claim … its tamper-evidence prose implied monitoring was the compensating control for a wrong-but-well-formed tag."* But ADR-001 L298 **still literally stated** monitoring is that control. STRIDE (L294/L331) and ADR-003 D5 agree: a rogue-but-well-formed tag is CI-attested, so monitoring is blind — **provenance** is the control. **Owned → FIXED.**

### D-6 — Monitor-topology drift in STRIDE (event-driven leg still "live")
STRIDE SC-03 (L195) still lists the integrity monitor as `event-driven + scheduled legs`. ADR-003 **D7** and requirements **REQ-035 / NFR-006** RETIRED the cross-repo event-driven leg as platform-impossible (a source-repo workflow cannot subscribe to another repo's push events). STRIDE SC-03 is the last place describing it as live. → ROUTE security.

### D-7 — Monitor-cadence drift (minor): "≤ daily" vs "≤ 6-hourly"
STRIDE frames the backstop at `≤ daily (tighten toward hourly)` (L332, L386). ADR-003 D7 + REQ-035 + NFR-006 specify **≤ 6-hourly**. The 25 h meta-monitor heartbeat (SC-05 / REQ-044) is consistent everywhere. Cadence wording should be harmonized. → ROUTE security (low severity).

### Categories checked and found CONSISTENT (no drift)
- **Distribution model** — ADR-001 (amended), ADR-003, STRIDE, requirements all describe the **dedicated `geekatron/jerry-cowork` repo, default branch = skeleton, org-registered, no `#ref`/branch-pin**. STRIDE L96-103 + L185 explicitly frame `#ref` and `GITHUB_TOKEN` as the OLD model. ✓
- **Token permissions** — per-job isolation (attestation job `id-token`+`attestations`, NO `contents`; push job `contents:write` only) is identical in ADR-003 D4, REQ-020, and the verification table. No workflow-level broad grant anywhere. ✓
- **Trust-framing (P-022)** — org-owner is a RESIDUAL trusted insider (RTB-1..5) across ADR-003 + STRIDE; both say "bounded, not closed / not prevented". No "fully resolved / supply-chain eliminated" overclaim found. ✓
- **Threat-Basis banding** — spot-verified ADR-003 "before→after" vs STRIDE: DR-01 `12 Y → 5 G` (STRIDE L168 ✓), SC-02 `10 Y` (L194 ✓), SC-04 `5 G` (L196 ✓). ✓
- **Terminology** — "sole bypass actor", "faithful-derivative gate", "App installation token / single-repo deploy key", `gh attestation verify`, "tip SHA non-forgeable / `Source-Commit` trailer forgeable" used identically across docs. ✓

### Non-actionable observation (NOT a defect)
`security/phase2-attack-surface.md` (red-recon, 2026-06-28) shows the pre-decision state: pipeline strips `projects/` only (L40) and names `PAT or deploy key` (L43), V-06/V-07 recommend a fine-grained PAT + PR-required-for-bot. These are point-in-time **threat-intel inputs** that ADR-003 deliberately **refines** (rejects PAT for App/deploy-key D3; rejects PR-required for sole-bypass-actor D2; adds `tests/` strip). Rewriting historical recon to match later decisions would be wrong. **No change recommended**; flagged so the blind adversaries don't mis-read the input as the chosen approach.

---

## 2. Fixes APPLIED (ADR-side)

**13 edits — 2 in ADR-003, 11 in ADR-001 — grouped into 4 consistency themes. No decision or mirror-dependent value altered.**

### ADR-003 (owned)

| # | Location | Before | After |
|---|----------|--------|-------|
| FIX-1 | Dim-1 Option C row | `CoWork clones main (~6,348 files)` | `… (~6,344 files)` (re-syncs to canonical) |
| FIX-2 | SC-06 intro (L148) | "This path was absent from the Phase-2 STRIDE model … pending the Phase-3 STRIDE update." | + **Identifier-collision note**: discloses STRIDE already uses `SC-06` for two-repo drift; states the trusted-maintainer build is `SC-06` in this ADR + REQ-051; mandates Phase-3 STRIDE to reconcile by renumbering the drift threat. *(SC-06 meaning unchanged — additive P-022 disclosure.)* |

### ADR-001 (owned) — D-4 ADR-002 supersession cluster

| # | Location | Before → After |
|---|----------|----------------|
| FIX-3 | Related Decisions table | ADR-002 `DEPENDS_ON` "supplies the push credential…" → **added ADR-003 `AMENDED_BY` row** (Phase-2 AoR: D2/D3/D4/D7) **and** changed ADR-002 to `SUPERSEDED_BY ADR-003` (historical, MUST NOT implement). |
| FIX-4 | L315 operationalization bullet | "…owned by ADR-002 §Continuous Integrity Monitoring." → added **Phase-2 supersession** note: Release-notes anchor + event-driven leg **RETIRED**; anchor = immutable-release + attestation; monitor = scheduled ≤6 h read-only poll; ownership → **ADR-003 D4/D7**. |
| FIX-5 | L57 Context | "ADR-002 selects the **push credential**." → "the **push credential** is selected in **ADR-003 D3** (supersedes the ADR-002 `GITHUB_TOKEN` decision)." |
| FIX-6 | Consequences Neg-3 (L345) | "branch-protection posture (ADR-002)" → "the dedicated-repo protection posture (**ADR-003 D2** — org-level ruleset, CI sole bypass actor)". |
| FIX-7 | Consequences Pos-7 (L339) | "and ADR-002's continuous integrity monitoring" → "and **ADR-003's D4 attestation anchor + D7** continuous integrity monitoring". |
| FIX-8 | Nav table (L33) | "Links to ADR-002 and work items" → "Links to **ADR-003 (amends), ADR-002 (superseded)**, and work items". |
| FIX-9 | L0 (L45) | "this deliberately unsigned, **unprotected branch stays trustworthy** (the integrity architecture **lives in ADR-002**)." → "unsigned branch stays **tamper-evident** (integrity architecture **now owned by ADR-003** — D4 attestation + D7 monitor)." |
| FIX-10 | Clone-weight telemetry row (L196) | "(… clones `cowork-skeleton` every cycle — **see ADR-002**)" → "(… clones the skeleton every cycle — **see ADR-003 D7**)". |
| FIX-12 | Tag-immutability precondition (L302) | "the **published expected SHA** (ADR-002 §Continuous Integrity Monitoring) … durable integrity reference." → "the **build-provenance attestation** binding the published tip SHA (**ADR-003 D4**) … durable integrity reference." |
| FIX-13 | Tamper-evidence bullet (L312) | "this is why **ADR-002's monitor** compares the tip SHA, not the trailer." → "this is why **ADR-003's D7 monitor** compares the tip SHA via `gh attestation verify`, not the trailer." |

### ADR-001 (owned) — D-5 rogue-tag false-claim correction

| # | Location | Before → After |
|---|----------|----------------|
| FIX-11 | RT-003 scope-boundary note (L298) | "the deterministic-SHA integrity monitoring (ADR-002 …) **is the compensating detective control for a wrong-but-well-formed tag**." → "the **provenance** control for a wrong-but-well-formed tag is decided in **ADR-003 D5** … **Correction (aligned with ADR-003 D5):** the deterministic-SHA *monitor* can**not** catch a rogue-but-well-formed tag — CI faithfully builds *and attests* it — so monitoring is **not** the control here; **provenance is**." |

> Post-edit verification (grep): `6,348` gone from ADR-003; SC-06 collision note present; ADR-001 retains **5** ADR-002 mentions — all now framed as superseded (nav, L57, L315 supersession clause, Related-Decisions row) or historical (iter-3 changelog L407). **Zero** active "owned by / lives in / selects (ADR-002)" pointers remain.

---

## 3. Findings ROUTED (to other owners)

### → nse-requirements (READ-ONLY for me) — `requirements/phase1-requirements.md`

| Ref | Exact location | Defect | Precise change |
|-----|----------------|--------|----------------|
| R-REQ-1 | REQ-005 inline "Note for ps-architect" (L89) | Quotes ADR-001 body as saying `tests/ "retained today (1,744 ≪ 5,000)"` and asks ps-architect to fix it. **Obsolete** — ADR-001 (iter-4) already strips `tests/` and uses ~1,417 throughout. | Delete the stale "Note for ps-architect (ADR-001 inconsistency)" paragraph (the ADR-001 body inconsistency is resolved); keep the "REQ-005 ↔ ADR-001 c-003 must stay in sync" sentence. |
| R-REQ-2 | Self-refine checklist (L534) | "File count discrepancy noted: **ADR-003 diagrams show ~1,749 files**" — ADR-003 now shows ~1,417; the residual ~1,749 lives only in the STRIDE diagram. | Update to: "ADR-001 + ADR-003 show ~1,417; STRIDE diagram L81 still shows stale ~1,749 (routed to security)." |
| R-REQ-3 | Iteration-1 note (L596) + L508 | L596 records L0 set to "~1,744 (~1,745 with stub)"; L508 says "ADR-001 body inconsistency noted in REQ-005 for ps-architect; ADR-001 not edited." Both stale vs current ~1,417 / fixed ADR-001. | Mark these as superseded by the iteration-5 corrections (or append "(superseded: now ~1,417; ADR-001 corrected iter-4)"). Historical-note severity — low. |

### → security (READ-ONLY for me)

| Ref | File · location | Defect | Precise change |
|-----|-----------------|--------|----------------|
| R-SEC-1 | `phase2-stride-threat-model.md` L81 (diagram) | `skeleton ~1,749 files` (stale). | Change to **~1,417 files** to match ADR-001/ADR-003/requirements. |
| R-SEC-2 | `phase2-stride-threat-model.md` SC-03 mitigation (L195) | Lists monitor as `event-driven + scheduled legs`; the cross-repo event-driven leg is RETIRED (ADR-003 D7, REQ-035). | Replace "event-driven + scheduled legs" with "**scheduled (≤ 6 h) read-only poll from the source repo**; cross-repo event-driven leg RETIRED (platform-impossible — ADR-003 D7)." |
| R-SEC-3 | `phase2-stride-threat-model.md` L332 / L386 (cadence) | "≤ daily (tighten toward hourly)" vs the decided **≤ 6-hourly**. | Harmonize the backstop cadence wording to **≤ 6-hourly** (keep 25 h meta-monitor). Low severity. |
| R-SEC-4 | `phase2-stride-threat-model.md` SC-06 row (L198) + summary (L244) | **Threat-ID collision (D-3):** `SC-06` = "two-repo drift" here, but = "trusted-maintainer rogue build" in ADR-003/REQ-051. | In the **Phase-3 STRIDE update**, renumber the drift threat (e.g., → `SC-07`) and adopt `SC-06 = trusted-maintainer rogue build` to agree with ADR-003 + REQ-051. (ADR-003 now carries a disclosure note pointing here.) **Coordinate with nse-requirements** so all three artifacts land on one `SC-06`. |

> **Coordination note:** R-SEC-4 + the ADR-003 FIX-2 disclosure + REQ-051 form one tri-artifact reconciliation. Whichever ID convention the Phase-3 STRIDE adopts, ADR-003 + requirements + STRIDE must end on a single `SC-06` meaning. I did **not** change ADR-003's `SC-06` (locked / mirror-dependent) — only disclosed the collision.

---

## 4. Self-Assessed Internal-Consistency Posture & Readiness

**Posture: materially improved vs iteration-004 (0.62).** The two structural defects most likely to have depressed Internal Consistency are now resolved on the owned side:

1. **Self-contradiction eliminated** — ADR-001 no longer asserts the rogue-tag claim that ADR-003 says it corrected (D-5). The two ADRs now tell one story: monitoring detects tampering of a *legitimate* build; **provenance (D5)** is the rogue-tag control.
2. **Supersession made coherent** — ADR-001 no longer presents the superseded ADR-002 as the live owner of the credential/integrity architecture; Related Decisions now lists ADR-003 (amends) + ADR-002 (superseded) (D-4).
3. **File-count re-synced** on the owned side (6,344) (D-1).
4. **The SC-06 collision is now disclosed rather than silent** (D-3) — a P-022 win even though the global rename is a Phase-3 security action.

**Residual cross-artifact drift remaining (all in READ-ONLY files, all routed):** STRIDE stale ~1,749 (R-SEC-1), STRIDE live event-driven leg (R-SEC-2), cadence wording (R-SEC-3), the global SC-06 rename (R-SEC-4), and three stale requirements notes (R-REQ-1..3). None is an ADR-side defect; each has an exact location + precise change above. The blind adversaries (and the orchestrator routing fixes to nse-requirements/security) will still surface these — that is expected and correct; I am handing them precise targets rather than leaving them latent.

**Readiness verdict:** **READY for the blind tournament.** The owned ADRs (ADR-001, ADR-003) are internally consistent with each other and with the requirements mirror on every locked value (file counts ~1,417/~6,344, per-job perms, D7 scheduled poll, RTB-1..5, SC-06 meaning, tag-provenance control). The remaining inconsistencies are confined to non-owned artifacts and are pre-routed. I do **not** assert a numeric score (that is adv-scorer / the blind judges' role).

---

## 5. Verification Honesty (P-022)

- **Verified by grep across all 5 files:** the file-count set (6,344/6,348/1,417/1,749/1,744); ADR-002 active-reference inventory in ADR-001 (pre- and post-edit); SC-06 dual definition (read both the STRIDE SC-06 row and the ADR-003 SC-06 block).
- **Verified by full read:** ADR-001 (all 408 lines), ADR-003 (all 564 lines), attack-surface (all 347 lines), STRIDE via targeted greps + section reads, requirements L1-211 + traceability rows 309-316 + checklist 292-297 + self-refine notes.
- **NOT fully verified (stated plainly):** I did **not** line-by-line reconcile every requirements row 212-260 (WS-4/WS-5) and 317-380 (full Allocation Matrix / Risk Implications) against their ADR sources; my REQ↔ADR↔threat checks targeted the security/integrity spine (REQ-020/022/035-051, NFR-006) where drift concentrates. A residual REQ-table inconsistency outside that spine could exist. The ADR-003 banding "before→after" claims were **spot-verified** (DR-01/SC-02/SC-04), not exhaustively (all rows).
- **No numeric confidence asserted** for Internal Consistency — improvement is argued qualitatively from the specific defects closed; the score is for the blind judges.

---

*Generated by jerry:ps-architect (S-010 Self-Refine, CREATOR). 13 ADR-side fixes applied; 7 findings routed (4 security + 3 requirements). Per P-003 no sub-agents spawned; per P-020 no user-approved decision changed.*
