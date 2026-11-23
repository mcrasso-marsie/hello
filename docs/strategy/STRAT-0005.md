---
artifact_type: strategy
id: STRAT-0005
status: Draft
---

# Strategy Document: Show the raw byte size of the input beside the character count, so users stop needing a second tool, now that file and stdin share one path.

## Executive Summary

**Thesis:** Show the raw byte size of the input beside the character count, so users stop needing a second tool, now that file and stdin share one path.

**From Problem Graph:** DG-0005

## Goals (What We Aim to Achieve)

### Goal 1: Users learn the byte size of their input from the same wordcount run that gives the other counts
**Why:** Users who size buffers, uploads or storage now need a second tool  
**Success Metric:** 100% of successful runs print a byte field equal to the raw input size  
**Owner:** word-count-command maintainers

### Goal 2: The byte count is identical for a file and for standard input through '-' with the same bytes
**Why:** DG-0005 requires parity, and the existing output is already identical across both sources  
**Success Metric:** All SPEC-0004 byte samples give identical four-field lines for file and '-'  
**Owner:** word-count-command maintainers

## Success Criteria (Observable & Verifiable)

| Criterion | Measurement | Target | Baseline | Cadence |
|---|---|---|---|---|
| Byte count matches raw input size for non-ASCII text | Automated test on 'café' encoded as UTF-8 | 5 bytes reported beside 4 characters | No byte field exists | Every Quality Gate run |
| File and standard input parity including bytes | Parity tests over the SPEC-0004 byte samples | 100% identical output lines | 100% identical three-field lines, no byte field | Every Quality Gate run |
| Existing counts, errors and invocation unchanged | Existing guardrail tests from SPEC-0001 to SPEC-0004 | All pass, with only the expected success line updated | All pass | Every Quality Gate run |

## Non-Goals (What We Deliberately Skip in v1)

- **Reporting a byte count for input that is not valid UTF-8:** Keeps the existing single-line error and empty stdout. Users with undecodable input still need another tool.
- **Other statistics such as longest line or per-line output:** Keeps the change small and focused on the approved byte-size problem.
- **Totals or several inputs in one invocation:** Keeps the single-input contract. Users who need totals must sum runs themselves.
- **Comprehension quizzes for this feature:** The user declined them. Review relies on the walkthrough and README instead.

## Strategic Approach (The "How")

### Core Strategy

Report the byte size of the input in the success line beside the character count. Measure it from the raw input as read, once, the same way for a file and for standard input. Keep every other count, error and invocation unchanged.

### Rationale Against Alternatives

**Why NOT Derive the byte count from the decoded text by turning it back into bytes:**  
It measures the decoded text, not the raw input. The count could drift from the true input size if decoding ever changes.

**Why NOT Read the byte size from the file system's own record of file size:**  
Standard input has no such record, so file and '-' would take different paths. Parity between them would break.

**Why NOT Offer the byte count only behind a new opt-in command-line flag:**  
The user wants it shown next to characters by default. A new flag also breaks the guardrail of no new arguments.

**Why NOT Document that users should run a separate byte-counting tool:**  
It leaves the core problem unsolved. Users still need a second tool to size buffers, uploads or storage.

## Scope Boundaries (What Ships in v1)

### In Scope

- A byte field in the success line, placed beside the character field
- Byte count measured from the raw input, read once, for files and for '-'
- README.md documents the new output line, the byte rule, and that the three-field form no longer applies
- Updating existing tests only where they assert the success line
- hello
- hello-cli
- word-count-command

### Out of Scope (Deferred)

- Changes to the word, character or line rules (existing, unchanged)
- The '-' standard input invocation itself (existing, from SPEC-0004)
- New command-line flags or arguments
- Byte counts for invalid UTF-8 input
- Non-UTF-8 encodings, totals or several inputs
- Third-party runtime dependencies

## What Could Stop This — Dependencies, Assumptions, Risks

### Dependencies

| Dependency | Owner | Status |
|---|---|---|
| The approved shared read and decode path for file and standard input from SPEC-0004 | word-count-command maintainers | available |
| An architecture update that moves bytes from the hello system's 'Does NOT own' list into what it owns | architecture owner (ARCH-0001) | needed |
| The four Quality Gate commands recorded in AGENTS.md | project maintainers | available |

### Assumptions

| Assumption | Validator | How it is checked | If false |
|---|---|---|---|
| 'Next to the characters count' means the byte field sits right after the character field and before the line field. | The user who asked for the byte count | Confirm the field order during strategy review, before SPEC fixes the exact output line | Move the field to the position the user names. The strategy direction does not change. |
| Users expect invalid UTF-8 input to keep failing with the existing error, with no byte count printed. | The user who asked for the byte count | Confirm during strategy review that the error behavior stays unchanged | Re-open DEFINE on whether undecodable input should report bytes only. |
| The raw bytes a file holds equal the bytes the same content sends on standard input. | The existing file-and-stdin parity tests from SPEC-0004, extended with the byte field | Feed each SPEC-0004 byte sample through a file and through '-' and compare the full output lines | Re-open DISCOVER on what differs between the two sources. |

### Risks

| Risk | Likelihood | Impact | Mitigation |
|---|---|---|---|
| Adding a fourth field changes the success line again and breaks scripts that parse the three-field form | medium | Users' scripts could misread counts after upgrading | Document the new line in README.md and state that the three-field form no longer applies |
| Existing tests assert the three-field line and must be updated | high | The Quality Gate fails until those tests change, and an edit could weaken a guardrail | Limit test edits to the expected success line and keep every other assertion unchanged |
| The byte count could be taken from a second read of the input | low | Standard input cannot be read twice, so the '-' path could report a wrong count | Require one read per run, shared by the byte count and the decode |

## Example-First Walkthrough

### Scenario: Sizing a non-ASCII file

**Today:**
- The user runs wordcount on a file holding 'café'.
- The output shows words: 1 characters: 4 lines: 0.
- The user runs a second tool to learn the file is 5 bytes.

**With this strategy:**
- The user runs wordcount on the same file.
- The output shows the 5-byte size beside the 4 characters, with words and lines unchanged.
- The user needs no second tool.

### Scenario: Piping the same bytes through standard input

**Today:**
- The user pipes 'a\r\nb\r\n' into wordcount -.
- The output matches the file run but gives no byte size.

**With this strategy:**
- The user pipes the same bytes into wordcount -.
- The output shows 6 bytes, and the line is identical to the file run.

### Scenario: Undecodable input

**Today:**
- The user passes a file with bytes that are not valid UTF-8.
- wordcount prints one error line and exits with status 1.

**With this strategy:**
- The same run prints the same error line and exits with status 1.
- No byte count is printed.

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

**Authored by:** openrouter:anthropic/claude-opus-5.5  
**Reviewed by:** _(pending)_ — _(pending)_

**Ready for SPEC:** [ ] Yes [ ] No
