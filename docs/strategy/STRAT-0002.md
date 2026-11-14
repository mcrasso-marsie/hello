---
artifact_type: strategy
id: STRAT-0002
status: Draft
---

# Strategy Document: Provide users both word and non-whitespace Unicode character counts in one invocation now, while making the intentional output compatibility break explicit.

## Executive Summary

**Thesis:** Provide users both word and non-whitespace Unicode character counts in one invocation now, while making the intentional output compatibility break explicit.

**From Problem Graph:** DG-0002

## Goals (What We Aim to Achieve)

### Goal 1: Provide both requested text measures on every successful single-file inspection.
**Why:** Users currently receive only the word count and cannot obtain the requested character measure from the command.  
**Success Metric:** 100% of representative successful-invocation tests produce the exact combined output with correct counts.  
**Owner:** CLI maintainer (proposed)

### Goal 2: Preserve existing invocation, word semantics and specified failure behavior.
**Why:** The requested enhancement changes successful output, not the command interface or error contract.  
**Success Metric:** 100% of applicable approved invocation, word-count and error regression checks pass.  
**Owner:** CLI maintainer (proposed)

## Success Criteria (Observable & Verifiable)

| Criterion | Measurement | Target | Baseline | Cadence |
|---|---|---|---|---|
| Successful output reports both counts in the required format. | Successful-invocation tests covering ordinary, empty and whitespace-only UTF-8 files. | 100% pass; each successful invocation emits one line in the format `words: <N> characters: <M>`. | SPEC-0001 specifies a bare integer, so its successful-output contract does not match the new format. | Every change and Quality Gate run |
| Character counts represent non-whitespace Unicode code points rather than UTF-8 bytes. | Character-count and command tests including `café`, whitespace and combining characters. | 100% pass; `café` counts as 4. | SPEC-0001 does not report character counts. | Every change and Quality Gate run |
| Existing invocation, word counts and specified error behavior remain intact. | Applicable SPEC-0001 regression tests for arguments, word semantics, missing and unreadable files, invalid UTF-8 and traceback-free errors. | 100% pass, excluding the superseded bare-integer success-output expectation. | SPEC-0001 defines the existing behavior; current measured test results not supplied. | Every change and Quality Gate run |
| The required project Quality Gate remains satisfied. | Results of the four commands recorded in AGENTS.md. | All four commands exit 0 before the change lands. | Existing constitution requires all four checks; current run results not supplied. | Before any change lands |

## Non-Goals (What We Deliberately Skip in v1)

- **Preserve compatibility with clients that parse successful output as a bare integer.:** The mandated labeled combined line changes the existing success contract; no compatibility flag is allowed.
- **Detect or reject binary files as a separate category.:** The approved specification requires invalid UTF-8 rejection, not binary detection; adding a new error behavior would expand the contract.
- **Provide additional statistics, batch processing, standard-input processing or non-UTF-8 support.:** These capabilities extend beyond the requested single-file enhancement.

## Strategic Approach (The "How")

### Core Strategy

Extend single-file inspection to report both measures on every successful invocation, accepting a breaking output change while preserving the existing invocation, word-count semantics and specified error behavior.

### Rationale Against Alternatives

**Why NOT Make character reporting optional while retaining the existing default output.:**  
Would preserve existing consumers by default, but conflicts with the requirement to report both counts every time and add no flags.

**Why NOT Offer character counting through a separate command or invocation.:**  
Avoids changing existing output, but requires users to take an additional action and does not provide both measures through the existing invocation.

**Why NOT Report a byte count instead of a Unicode code-point count.:**  
May be simpler for consumers concerned with file size, but misrepresents non-ASCII text and fails the requested character definition.

## Scope Boundaries (What Ships in v1)

### In Scope

- Character counts for readable UTF-8 files, excluding whitespace and counting Unicode code points.
- The exact combined successful-output contract for the existing single-path command.
- Preservation of existing word-count, invocation and specified error behavior.
- Documentation and regression coverage for the changed contract.
- hello
- hello-cli
- word-count-command
- word-counter

### Out of Scope (Deferred)

- Rebuilding the existing single-path command, word-count capability or specified error handling.
- A compatibility mode, new flags or a separate invocation.
- Binary detection as a new error behavior.
- Additional text statistics, batch or standard-input processing, and non-UTF-8 file support.
- Network access, persistent state, configuration files or third-party runtime dependencies. 

## What Could Stop This — Dependencies, Assumptions, Risks

### Dependencies

| Dependency | Owner | Status |
|---|---|---|
| Approval of an updated specification that supersedes SPEC-0001's successful-output requirement while retaining its unaffected requirements. | Specification owner | Pending |
| Approval of architecture changes to reflect character-count ownership and the expanded command and system responsibilities. | Architecture owner | Pending |
| Access to the existing regression suite and four required Quality Gate checks. | Project maintainer | Available per project handoff; execution pending |

### Assumptions

| Assumption | Validator | How it is checked | If false |
|---|---|---|---|
| Whitespace for character exclusion follows the same text whitespace semantics used by the existing word rule, including spaces, tabs and newlines. | Specification owner | Confirm the interpretation in the updated specification and check representative Unicode whitespace and non-whitespace examples. | Resolve the intended whitespace definition before finalizing the specification. |
| The intentional output break is acceptable for existing consumers without a compatibility mode. | Product owner | Review affected consumer expectations and approve the changed output contract. | Reopen the no-flags and always-combined-output constraints before proceeding. |

### Risks

| Risk | Likelihood | Impact | Mitigation |
|---|---|---|---|
| Consumers expecting a bare integer may fail or misinterpret the new output. | Unknown; consumer inventory not provided | Breaking change for successful invocations. | Clearly document the changed contract and communicate it to known consumers before release. |
| Unicode and whitespace edge cases may yield misleading character counts. | Medium | Users receive incorrect text statistics. | Validate representative non-ASCII, whitespace-only and combining-character cases against the agreed definition. |
| The output change or related work may inadvertently alter existing error or argument behavior. | Medium | Existing scripts and users experience unexpected failures or diagnostics. | Retain regression coverage for the approved invocation, error messages and exit statuses. |

## Example-First Walkthrough

### Scenario: Inspect a non-ASCII text file

**Today:**
- A user invokes `wordcount PATH` for a readable UTF-8 file containing `café`.
- The command reports `1` followed by a newline.

**With this strategy:**
- The user invokes the same `wordcount PATH` command without flags.
- The command reports `words: 1 characters: 4` followed by a newline.
- A consumer expecting only an integer must adapt to the new output.

### Scenario: Inspect a file that does not exist

**Today:**
- The user supplies a nonexistent path.
- The command writes the specified file-not-found line to stderr, writes nothing to stdout and exits with status 1.

**With this strategy:**
- The user supplies the same nonexistent path.
- The existing specified error behavior remains unchanged; no counts are printed.

## Validation Checklist

- [ ] Problem Graph (DG-[ID]) is validated and reviewed
- [ ] Core strategy is one sentence (thesis)
- [ ] Goals are outcome-focused, not solution-focused (failures, not fixes)
- [ ] Success criteria are measurable and tied to business value
- [ ] Non-goals have explicit rationale (not just "v2")
- [ ] Every seriously considered direction that was rejected is recorded, with the tradeoff that decided it
- [ ] Core strategy states a direction, not a mechanism — no technology, component, signature or parameter is named
- [ ] Example-first walkthrough covers happy path + edge case
- [ ] Scope boundaries are precise (what ships, what's deferred)
- [ ] Assumptions are verifiable; risks are tracked
- [ ] Timeline is achievable; no optimistic estimation
- [ ] DRI and reviewers are aligned

## Gate 1 Review (Adversarial Requirement Review)

**Architecture Review** (verify no solution pollution):
- [ ] Strategy is outcome-focused: it names a **direction** and its consequences
- [ ] No **mechanism** is baked in — no technology, component, signature or parameter (that's SPEC's job). Choosing a direction is not pollution; choosing its implementation is
- [ ] Rejected directions are recorded with their tradeoffs, so the reviewer can attack the reasoning rather than re-derive the options
- [ ] Scope vs effort tradeoff is realistic

**Business/Product Review** (verify goals are aligned):
- [ ] Success metrics are measurable and business-relevant
- [ ] Non-goals are acceptable to stakeholders
- [ ] Timeline and investment are approved

**Approval Policy:** `(agent; human)` — Agent drafts, human (DRI + reviewers) approves before advancing to SPEC phase.

**Blockers / Rework Needed:**
- (none)

## Sign-Off

**Authored by:** openrouter:openai/gpt-6.1-terra-pro  
**Reviewed by:** _(pending)_ — _(pending)_

**Ready for SPEC:** [ ] Yes [ ] No
