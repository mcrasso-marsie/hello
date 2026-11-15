---
artifact_type: strategy
id: STRAT-0003
status: Approved
---

# Strategy Document: Complete the wordcount report by always appending a clearly defined, Unicode-aware line count to the existing success line, now that users have asked for it and the boundary rule is settled, without disturbing anything already built.

## Executive Summary

**Thesis:** Complete the wordcount report by always appending a clearly defined, Unicode-aware line count to the existing success line, now that users have asked for it and the boundary rule is settled, without disturbing anything already built.

**From Problem Graph:** DG-0003

## Goals (What We Aim to Achieve)

### Goal 1: Users get the line count of a file from the same single `wordcount PATH` invocation that already reports words and characters
**Why:** Removes the need for a separate tool, which is the core issue in DG-0003  
**Success Metric:** 100% of successful runs print a `lines: <L>` field on the single stdout line  
**Owner:** project owner

### Goal 2: Line counts are unambiguous and agree with the agreed boundary rule on every file shape
**Why:** DG-0003 rates an ambiguous rule as high severity for correctness  
**Success Metric:** All DG-0003 boundary examples (LF, CRLF, lone CR, U+2028, form feed, whitespace-only, unterminated final segment, empty) report the agreed counts  
**Owner:** project owner

### Goal 3: Existing behaviour stays intact: invocation, word and character results, UTF-8 handling and error paths
**Why:** The handoff and the SPEC-0001/0002 guardrails require it  
**Success Metric:** 0 regressions across the existing guardrail tests, and all four Quality Gate commands exit 0  
**Owner:** project maintainers

## Success Criteria (Observable & Verifiable)

| Criterion | Measurement | Target | Baseline | Cadence |
|---|---|---|---|---|
| Success output includes the line count | CLI acceptance tests on stdout of `wordcount PATH` | Exactly one line `words: <N> characters: <M> lines: <L>` on every successful run | `words: <N> characters: <M>` with no line count | Every Quality Gate run |
| Line-boundary correctness | Acceptance examples from DG-0003 | 'a\\nb' gives 1; '\\n\\n' gives 2 (with 0 words and 0 characters); 'a\\r\\n' gives 1; empty file gives 0; lone CR, U+2028 and form feed each count as a terminator | No line rule exists | Every Quality Gate run |
| No regression of existing behaviour | Existing SPEC-0001/0002 tests and guardrails | 100% pass; error paths still print nothing to stdout, and exit statuses 1 and 2 are unchanged | 100% pass today | Every Quality Gate run |
| Quality Gate passes | ruff format check, ruff check, mypy --strict, pytest | All four exit 0 | All four exit 0 | Before any change lands |

## Non-Goals (What We Deliberately Skip in v1)

- **Making the line count optional or configurable:** Keeps the invocation unchanged and simple, at the cost of no way to get the old two-field output
- **Matching wc -l output exactly:** The agreed Unicode-aware rule is clearer for mixed-platform text, at the cost of differing from a familiar tool on some files
- **Other statistics (bytes, longest line, per-line output) or stdin or batch input:** Keeps scope small, consistent with the architecture's stated non-ownership; those requests wait for their own discovery
- **Preserving byte-for-byte compatibility of the previous success line:** Delivers the requested one-line report, at the cost of breaking consumers of the old format

## Strategic Approach (The "How")

### Core Strategy

Extend the existing single-invocation report so every successful run also states the file's line count, appended to the same stdout line. The line rule is defined once, Unicode-aware and independent of the word and character rules, and is kept as pure counting logic separate from the command shell, as the existing counters are. The change is purely additive: invocation, word and character results, UTF-8 handling and every error path behave exactly as they do today, so the only visible difference for users is one extra field on success.

### Rationale Against Alternatives

**Why NOT Make the line count opt-in behind a new flag or option:**  
Contradicts the approved Problem Graph and handoff, which require no new flag. It also changes the invocation surface that SPEC-0002 guards and leaves the default output without the count users asked for.

**Why NOT Adopt the narrower POSIX wc -l convention of counting only LF line feeds:**  
Familiar, but the human explicitly chose a broader rule. Files with lone CR, U+2028 or form feed would report counts that disagree with the agreed definition and its tests.

**Why NOT Count line segments, including an unterminated final segment:**  
Matches some editors' intuition, but conflicts with the confirmed example that 'a\nb' reports 1. It also makes an unterminated single-line file report 1 where the agreed rule reports 0, which reopens a settled boundary.

**Why NOT Fold line counting into the existing word or character counting responsibility:**  
Adds no new unit, but blurs the architecture boundary in which each counter owns exactly one rule. It also risks regressions in the word and character results that SPEC-0001 and SPEC-0002 guard.

**Why NOT Report the line count on a separate stdout line or in a separate command:**  
Leaves the existing line untouched, but breaks the agreed single-line `words: <N> characters: <M> lines: <L>` format. Users would also lose the one-invocation, one-line report that is the point of the change.

## Scope Boundaries (What Ships in v1)

### In Scope

- Always appending ` lines: <L>` to the existing success stdout line
- A single line-counting rule: every boundary the standard library line-splitting recognises terminates a line, CRLF counts once, and an unterminated final segment is not counted
- Line counting as pure logic with no I/O, beside the existing word and character rules
- README documentation of the new output line and the line rule, including how it differs from wc -l
- Updating existing tests that assert the old two-field line
- hello
- hello-cli
- word-count-command

### Out of Scope (Deferred)

- New flags, options or changes to the single positional PATH invocation
- Any change to the word rule (word-counter) or the character rule (character-counter)
- Any change to UTF-8 decoding, error messages, exit statuses or argparse usage behaviour
- Third-party runtime dependencies
- stdin, multiple files, non-UTF-8 encodings or other statistics

## What Could Stop This — Dependencies, Assumptions, Risks

### Dependencies

| Dependency | Owner | Status |
|---|---|---|
| Approved discovery DG-0003, which fixes the line-boundary rule, the output format and the invocation | project owner | approved |
| Approved SPEC-0001 and SPEC-0002 behaviour (word rule, character rule, error messages, exit statuses), which this change must leave intact | project owner | approved and built |
| The four Quality Gate commands from AGENTS.md / ADR-0003 (format, lint, strict type-check, test) runnable in the project environment | project maintainers | available |
| An architecture update to ARCH-0001 recording line counting as a pure counting responsibility and the extended output line | project architect | to be proposed alongside the spec |

### Assumptions

| Assumption | Validator | How it is checked | If false |
|---|---|---|---|
| Users and any scripts consuming the output accept a format change on the success line, as they did when SPEC-0002 replaced the bare integer | project owner | Owner confirmation during strategy and spec review, and the README is updated to state the new line format | Return to DISCOVER to weigh output compatibility against the always-on requirement |
| The Python standard library's own line-boundary definition is stable across the supported Python versions, so the agreed rule yields the same counts everywhere the project runs | test suite on the pinned .python-version | Acceptance examples covering LF, CRLF, lone CR, U+2028, form feed, whitespace-only and unterminated-final-segment files pass under the Quality Gate | Define the terminator set explicitly in the spec instead of by reference to the library behaviour |
| The line count can be derived from the same decoded text already used for words and characters, so no new reading or decoding path is needed | spec-writer and code reviewer | Review that error-path guardrail tests (missing, unreadable, invalid UTF-8) still pass unchanged and print nothing to stdout | Revisit the scope with the owner before touching error handling |

### Risks

| Risk | Likelihood | Impact | Mitigation |
|---|---|---|---|
| The broad terminator set surprises users who expect wc -l results, for example on files containing form feeds or lone CRs | medium | Perceived incorrect counts and bug reports | Document the rule and its difference from wc -l in the README, with the confirmed examples |
| Changing the success line breaks existing tests and downstream consumers that match `words: <N> characters: <M>` exactly | high | Failing existing CLI and feature tests, and broken user scripts | Update affected tests deliberately in the spec, and state the format change in the README as SPEC-0002 did |
| Wiring in a new count accidentally alters word or character results, or error-path behaviour | low | Regression of approved SPEC-0001/0002 behaviour | Carry the SPEC-0002 regression guardrails forward unchanged, and require all four Quality Gate commands to pass |
| The CRLF single-terminator case or the unterminated-final-segment case is implemented inconsistently | medium | Off-by-one line counts on Windows-origin or unterminated files | Make the DG-0003 examples ('a\\nb' gives 1, '\\n\\n' gives 2, 'a\\r\\n' gives 1, empty file gives 0) mandatory acceptance cases |

## Example-First Walkthrough

### Scenario: Ordinary multi-line file

**Today:**
- User runs `wordcount notes.txt` on 'hello world\nbye\n'
- Output is `words: 3 characters: 13`
- User runs a separate tool to learn the file has 2 lines

**With this strategy:**
- User runs `wordcount notes.txt`
- Output is `words: 3 characters: 13 lines: 2`
- No second tool is needed

### Scenario: Unterminated final line and CRLF

**Today:**
- File 'a\nb' gives `words: 2 characters: 2`, with no line information
- File 'a\r\n' gives `words: 1 characters: 1`

**With this strategy:**
- File 'a\nb' gives `words: 2 characters: 2 lines: 1`, because the trailing 'b' has no terminator
- File 'a\r\n' gives `words: 1 characters: 1 lines: 1`, because CRLF is one break

### Scenario: Whitespace-only and empty files

**Today:**
- File '\n\n' gives `words: 0 characters: 0`
- Empty file gives `words: 0 characters: 0`

**With this strategy:**
- File '\n\n' gives `words: 0 characters: 0 lines: 2`
- Empty file gives `words: 0 characters: 0 lines: 0`

### Scenario: Error paths unchanged

**Today:**
- A missing file prints `wordcount: error: file not found: PATH` to stderr, nothing to stdout, and exits 1

**With this strategy:**
- Identical: same stderr line, nothing on stdout, exit 1, and no line count is ever printed on error

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
**Reviewed by:** Marco — mcrasso@marsie.io

**Ready for SPEC:** [x] Yes [ ] No
