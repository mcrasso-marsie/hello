---
artifact_type: strategy
id: STRAT-0002
status: Approved
---

# Strategy Document: Extend hello's pure text-counting core and default command output to report both word counts and non-whitespace character counts in a single invocation, delivering complete file counts by default without adding dependencies or breaking the core/I/O boundary.

## Executive Summary

**Thesis:** Extend hello's pure text-counting core and default command output to report both word counts and non-whitespace character counts in a single invocation, delivering complete file counts by default without adding dependencies or breaking the core/I/O boundary.

**From Problem Graph:** DG-0002

## Goals (What We Aim to Achieve)

### Goal 1: Users can accurately measure non-whitespace character volume alongside word count for any valid UTF-8 text input.
**Why:** Word count alone does not reflect character volume excluding formatting whitespace and line breaks.  
**Success Metric:** 100% of acceptance scenarios covering empty, whitespace-only, multi-whitespace, punctuation, and non-ASCII inputs produce exact expected non-whitespace character counts.  
**Owner:** hello maintainers

### Goal 2: Default file inspection delivers both word count and non-whitespace character count in a single run without extra flags.
**Why:** Users need both metrics immediately upon inspecting a file without running a second tool or remembering extra options.  
**Success Metric:** 100% of successful default CLI invocations report both counts while maintaining 0 regressions on error-handling and architecture-boundary guardrails.  
**Owner:** hello maintainers

## Success Criteria (Observable & Verifiable)

| Criterion | Measurement | Target | Baseline | Cadence |
|---|---|---|---|---|
| Dual-count availability in default CLI output | Automated CLI acceptance tests on readable UTF-8 files | Both word count and non-whitespace character count reported on 100% of successful default invocations | Only word count reported by default (1 metric; 0 character-count metrics) | Every CI / Quality Gate run |
| Non-whitespace character counting accuracy across whitespace and Unicode inputs | Unit and BDD test suites covering empty, whitespace-only, tabs/newlines, punctuation, and non-ASCII UTF-8 inputs | 100% pass rate on all character-counting scenarios | Only whitespace-separated word counting tested (SPEC-0001) | Every CI / Quality Gate run |
| Quality Gate and architecture boundary compliance | Format, lint, strict type-check, test suite, and architecture dependency/layering checks | All 4 Quality Gate commands exit 0 with 0 runtime dependencies and 0 I/O in the counting core | All 4 Quality Gate commands pass under SPEC-0001 with 0 runtime dependencies | Before every change lands (ADR-0003) |

## Non-Goals (What We Deliberately Skip in v1)

- **Counting total characters including whitespace, line counts, or raw byte lengths.:** Keeps scope focused on the two requested metrics and avoids expanding into a general multi-metric inspection tool before demand is established.
- **Supporting multiple file arguments, directory recursion, standard input streaming, or non-UTF-8 encodings.:** Preserves the single-file UTF-8 operating model of the existing architecture and avoids complicating CLI argument and error handling.
- **Adding third-party runtime dependencies or packaging for external distribution indexes.:** Preserves the local, standard-library-only footprint and avoids external dependency maintenance overhead.

## Strategic Approach (The "How")

### Core Strategy

Expand the existing dependency-free text-counting capability to compute non-whitespace character counts alongside word counts, and shift the default command output to report both metrics together in a single invocation—trading strict backward compatibility of single-number default output for immediate dual-metric visibility without extra flags, while preserving the strict separation between pure counting rules and input/output handling.

### Rationale Against Alternatives

**Why NOT Keep single word-count output as the default and expose non-whitespace character counting only via an opt-in option or separate command.:**  
Preserves backward compatibility for single-number consumers, but forces users who need both counts on every inspection to pass extra arguments or invoke multiple commands, failing the core need for default dual reporting.

**Why NOT Compute non-whitespace character counts directly inside the command-line I/O shell rather than extending the pure counting core.:**  
Leaves the counting core untouched in the short term, but splits text-counting rules across layers, violates the established core/I/O boundary, and prevents independent reuse and pure unit testing of character counting.

**Why NOT Report raw string or byte length (including whitespace) instead of filtering out whitespace characters.:**  
Simpler to compute from raw file size or string length, but counts indentation and line endings that users explicitly want excluded, distorting counts across formatting styles.

## Scope Boundaries (What Ships in v1)

### In Scope

- hello
- hello-cli
- word-count-command
- word-counter
- Computing non-whitespace character counts (excluding spaces, tabs, newlines, and other whitespace) within the pure, I/O-free counting core alongside word counts
- Reporting both word count and non-whitespace character count by default when inspecting a readable UTF-8 file
- Updating existing user documentation and default-output test expectations to reflect dual-count reporting

### Out of Scope (Deferred)

- Re-implementing single-file UTF-8 reading, missing/unreadable/invalid-UTF-8 error messages, or exit status codes already delivered by SPEC-0001
- Total all-character counts (including whitespace), line counts, or byte-size metrics
- Batch multi-file inputs, directory traversal, or standard input streaming
- Non-UTF-8 encodings or third-party runtime dependencies

## What Could Stop This — Dependencies, Assumptions, Risks

### Dependencies

| Dependency | Owner | Status |
|---|---|---|
| Existing word-counting capability, UTF-8 file-reading shell, error-handling behavior, and Quality Gate suite from SPEC-0001 as the baseline. | hello maintainers | available |
| Approved specification defining the exact default dual-count output presentation and character-counting edge cases before implementation. | spec author / product owner | needed (next phase: SPEC) |

### Assumptions

| Assumption | Validator | How it is checked | If false |
|---|---|---|---|
| Existing users and callers can adapt to a default command output that reports both word count and non-whitespace character count rather than a lone integer. | Product owner and maintainers during Strategy/SPEC gate review | Confirm during Strategy and SPEC review that replacing the single-integer default output and updating existing CLI test expectations is intended rather than retaining single-number output as default. | Re-open strategy scope to preserve single-number output as default and gate dual counts behind an opt-in option. |
| Unicode whitespace boundaries (consistent with the existing word rule's whitespace definition) match what users mean by non-whitespace characters excluding spaces, tabs, and line breaks. | Product owner reviewing SPEC acceptance scenarios | Verify concrete examples containing spaces, tabs, newlines, punctuation, and non-ASCII UTF-8 characters in SPEC acceptance criteria. | Refine the character-exclusion definition in the specification before implementation. |

### Risks

| Risk | Likelihood | Impact | Mitigation |
|---|---|---|---|
| Changing default standard output from one integer to two counts will break existing automated tests or callers expecting a single integer line. | high | Existing CLI assertions and any downstream scripts parsing a single integer will fail until updated. | Audit and update affected default-output tests and documentation together with the change, and choose an unambiguous presentation format during SPEC. |
| Ambiguity around Unicode whitespace or multi-codepoint characters could cause reported character counts to differ from user intuition on non-ASCII text. | low | Users inspecting non-ASCII files could see unexpected character counts. | Align character whitespace exclusion with the existing word-separation whitespace rule and verify explicit non-ASCII examples in SPEC acceptance criteria. |

## Example-First Walkthrough

### Scenario: Inspecting a readable UTF-8 text file

**Today:**
- User runs the command on a readable UTF-8 file containing 'Hello, world!\n'.
- The counting core computes only the whitespace-separated word count (2).
- The command prints only the single integer word count and exits with status 0.

**With this strategy:**
- User runs the command on the same readable UTF-8 file containing 'Hello, world!\n'.
- The counting core computes both the word count (2) and the non-whitespace character count (12, excluding the space and newline).
- The command reports both the word count and the non-whitespace character count by default and exits with status 0.

### Scenario: Inspecting an empty or whitespace-only file

**Today:**
- User runs the command on a file containing only spaces, tabs, and newlines.
- The command prints only a word count of 0 and exits with status 0.

**With this strategy:**
- User runs the command on a file containing only spaces, tabs, and newlines.
- The counting core computes 0 words and 0 non-whitespace characters.
- The command reports both counts as 0 by default and exits with status 0.

### Scenario: Handling missing, unreadable, or non-UTF-8 files

**Today:**
- User runs the command on a missing, unreadable, or non-UTF-8 path.
- The command prints a single-line error message to standard error, writes nothing to standard output, and exits with status 1.

**With this strategy:**
- User runs the command on a missing, unreadable, or non-UTF-8 path.
- Existing SPEC-0001 error handling remains unchanged: a single-line error message is written to standard error, nothing to standard output, and the process exits with status 1.

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

**Authored by:** openrouter:google/gemini-4-hydrogen  
**Reviewed by:** Marco — mcrasso@marsie.io

**Ready for SPEC:** [x] Yes [ ] No
