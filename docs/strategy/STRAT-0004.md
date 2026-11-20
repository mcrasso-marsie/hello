---
artifact_type: strategy
id: STRAT-0004
status: Approved
---

# Strategy Document: Let wordcount count piped text through an explicit '-' argument now, closing a gap deferred across three strategies without changing any existing contract.

## Executive Summary

**Thesis:** Let wordcount count piped text through an explicit '-' argument now, closing a gap deferred across three strategies without changing any existing contract.

**From Problem Graph:** DG-0004

## Goals (What We Aim to Achieve)

### Goal 1: Users can count text piped into wordcount without writing a temporary file.
**Why:** Pipeline use is the core gap DG-0004 names.  
**Success Metric:** 'printf "a b\n" | wordcount -' prints 'words: 2 characters: 2 lines: 1' and exits 0.  
**Owner:** project maintainer

### Goal 2: Stdin and file input give identical counts for identical bytes.
**Why:** The word, character and line rules must not depend on the source.  
**Success Metric:** Every equivalence test sample gives the same output line from both sources.  
**Owner:** project maintainer

### Goal 3: Invalid UTF-8 on stdin fails like a file error and names <stdin>.
**Why:** Users need the same clear, single-line error contract for both sources.  
**Success Metric:** Exit status 1, one stderr line naming <stdin>, empty stdout, no traceback.  
**Owner:** project maintainer

## Success Criteria (Observable & Verifiable)

| Criterion | Measurement | Target | Baseline | Cadence |
|---|---|---|---|---|
| Stdin counting works | Acceptance tests in tests/features and tests/test_cli.py | All stdin scenarios pass, including empty stdin printing 'words: 0 characters: 0 lines: 0' | No stdin support, '-' is treated as a file path | Every Quality Gate run |
| Source equivalence | Tests comparing file and stdin output for the same bytes | 100% identical output lines | Not measurable, stdin unsupported | Every Quality Gate run |
| Existing contracts kept | SPEC-0001 to SPEC-0003 regression tests | All pass unchanged, including exit status 2 with no argument | All pass today | Every Quality Gate run |
| Quality Gate clean | Four AGENTS.md Quality Gate commands | All exit 0 | All exit 0 today | Every change |

## Non-Goals (What We Deliberately Skip in v1)

- **Counting several inputs in one invocation or printing totals.:** It keeps the single-input, single-line output contract unchanged.
- **Non-UTF-8 encodings or encoding options for stdin.:** It keeps one decoding rule for every source.
- **Reading stdin when no argument is given.:** It keeps the exit status 2 usage contract the handoff requires.
- **New output fields or a different output shape for stdin.:** It keeps one output line for every source, so scripts need no special case.

## Strategic Approach (The "How")

### Core Strategy

Let the user explicitly choose standard input as the text source. Stdin text flows through the same single decode and counting path as a file, so counts, output shape and error contracts stay identical. Only the error text names <stdin> instead of a path.

### Rationale Against Alternatives

**Why NOT Read standard input implicitly when no argument is given, as wc does.:**  
It breaks the kept contract that no argument is a usage error with exit status 2.

**Why NOT Detect piped input automatically and read it when present.:**  
Behavior would depend on the calling environment. It is harder to test and conflicts with the no-argument usage error.

**Why NOT Add a separate command or entry point dedicated to standard input.:**  
It duplicates the output and error contracts in two places, so they can drift apart.

**Why NOT Give stdin its own read, decode and error path beside the file path.:**  
The rules and messages could diverge between sources. The architecture already forbids a second decoding path for counting.

**Why NOT Copy standard input to a temporary file and reuse the file path unchanged.:**  
It adds filesystem writes and cleanup. Error messages would name a temporary path instead of <stdin>.

## Scope Boundaries (What Ships in v1)

### In Scope

- Explicit '-' argument selects standard input as the text source
- Stdin text counted with the existing word, character and line rules
- Same three-field output line for stdin
- Empty stdin prints all zeros
- Invalid UTF-8 on stdin: exit 1, one stderr line naming <stdin>
- README and acceptance test updates for stdin
- Architecture ownership update for stdin input
- hello
- hello-cli
- word-count-command

### Out of Scope (Deferred)

- Changes to the word, character or line rules
- Changes to file-path error messages or exit statuses
- Multiple inputs or totals
- Implicit or auto-detected stdin
- Other encodings or new flags
- Word, character and line counting, which already exist

## What Could Stop This — Dependencies, Assumptions, Risks

### Dependencies

| Dependency | Owner | Status |
|---|---|---|
| An architecture update that moves stdin processing and the '-' argument out of the hello system and hello-cli 'Does NOT own' lists. | architecture owner | needed |
| The existing word, character and line counters, unchanged, reused for stdin text. | project maintainer | available |
| The four Quality Gate commands recorded in AGENTS.md. | project maintainer | available |

### Assumptions

| Assumption | Validator | How it is checked | If false |
|---|---|---|---|
| Users accept an explicit '-' argument for stdin, as in common Unix tools. | project maintainer | Review the README usage section and the feature request in DG-0004 against the delivered behavior. | Re-open DISCOVER on how users expect to invoke stdin counting. |
| Stdin text decoded as UTF-8 gives the same counts as the same bytes in a file. | acceptance tests | Feed identical byte sequences, including CRLF and non-ASCII samples, by file and by stdin and compare output lines. | Treat it as a defect in the shared decode path before release. |
| Users rarely need to count a file literally named '-' by that bare name. | project maintainer | Document the './-' workaround in the README and watch for reports. | Revisit the stdin marker choice in a later strategy. |

### Risks

| Risk | Likelihood | Impact | Mitigation |
|---|---|---|---|
| Stdin decoding could differ from file decoding, for example through newline translation. | medium | CR and CRLF line counts could differ between stdin and file input. | Require byte-level equivalence tests for CR, CRLF and LF between both sources. |
| Reading stdin could raise an unexpected error case. | low | A traceback could reach stderr, breaking the single-line error contract. | Cover stdin error cases in the no-traceback acceptance tests. |
| Argument handling changes could alter the no-argument or many-argument behavior. | low | The exit status 2 usage contract could break. | Keep the existing usage-error regression tests and add a case for '-' with a second argument. |
| An interactive terminal on stdin waits for end of input. | medium | A user could think the command hangs. | State in the README that '-' reads until end of input. |

## Example-First Walkthrough

### Scenario: Counting piped text

**Today:**
- User runs 'cat notes.txt | wordcount -'.
- wordcount treats '-' as a file path.
- It prints 'wordcount: error: file not found: -' and exits 1.

**With this strategy:**
- User runs 'cat notes.txt | wordcount -'.
- wordcount reads and decodes standard input once.
- It prints 'words: <N> characters: <M> lines: <L>' and exits 0, the same as 'wordcount notes.txt'.

### Scenario: Invalid bytes on stdin

**Today:**
- User pipes binary data into 'wordcount -'.
- wordcount reports file not found for '-' and exits 1.

**With this strategy:**
- User pipes binary data into 'wordcount -'.
- wordcount prints one stderr line naming <stdin>, nothing on stdout, no traceback, and exits 1.

### Scenario: No argument

**Today:**
- User runs 'wordcount'.
- It prints usage to stderr and exits 2.

**With this strategy:**
- User runs 'wordcount'.
- It still prints usage to stderr and exits 2, without reading stdin.

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
