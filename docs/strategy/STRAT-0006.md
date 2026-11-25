---
artifact_type: strategy
id: STRAT-0006
status: Draft
---

# Strategy Document: Give users the word count of the longest line in one run, without changing any existing field, so line length is visible without extra tools.

## Executive Summary

**Thesis:** Give users the word count of the longest line in one run, without changing any existing field, so line length is visible without extra tools.

**From Problem Graph:** DG-0006

## Goals (What We Aim to Achieve)

### Goal 1: Users see the number of words on the longest line in every wordcount run.
**Why:** The output has no longest-line figure today, so users need extra tools.  
**Success Metric:** 100% of successful runs for a file or '-' print the new figure after lines.  
**Owner:** wordcount project owner

### Goal 2: The new figure always agrees with the existing word and line definitions.
**Why:** A second definition would make the fields disagree.  
**Success Metric:** 0 differences between the longest-line figure and the word count on single-line test inputs.  
**Owner:** wordcount project owner

### Goal 3: Readers understand why lines and the longest-line figure treat the final unterminated segment differently.
**Why:** The two rules differ on purpose, and readers may see this as an error.  
**Success Metric:** The README explains the difference with at least one example.  
**Owner:** wordcount project owner

### Goal 4: Existing output fields and the invocation stay stable.
**Why:** Existing parsers and tests depend on them.  
**Success Metric:** 0 changes to the labels, order and meaning of the first three fields. 0 new arguments.  
**Owner:** wordcount project owner

## Success Criteria (Observable & Verifiable)

| Criterion | Measurement | Target | Baseline | Cadence |
|---|---|---|---|---|
| Output line carries the new trailing field | Automated tests run wordcount on files and on '-' and compare the full line. | Every success case prints 'words: W characters: C lines: L longest_line_words: N' | Three fields and no longest-line figure | Every test run |
| Final-segment behavior is correct | Tests for 'a b c', 'a b\\n' and empty input check lines and the new field together. | 'a b c' gives lines 0 and 3. 'a b\\n' gives lines 1 and 2. Empty input gives lines 0 and the confirmed longest-line value. | No longest-line behavior exists | Every test run |
| Existing contract and guardrails hold | Existing error, usage, dependency and import tests run unchanged apart from the three-field assertions. | All pass. Runtime dependencies stay empty. | All pass on the current three-field output | Every test run |
| Documentation and tests match the new line | Search of README, tests and specs for assertions on the three-field line. | 0 stale assertions remain | The README and several tests assert the three-field line | Once at review, then every Quality Gate run |
| Quality Gate passes | Run the four Toolchain commands from AGENTS.md. | All four exit 0 | All four exit 0 today | Before every change lands |

## Non-Goals (What We Deliberately Skip in v1)

- **Report which line is the longest, its line number or its text.:** It keeps the output to one number as the owner asked. Users who need the location must look elsewhere.
- **Measure line length in characters, bytes or display width.:** The owner asked for words. Other measures would add fields and rules without a stated need.
- **Change how the lines field treats an unterminated final segment.:** It protects existing parsers and the SPEC-0003 rule. The two fields stay different, and the README explains why.
- **Add flags, several inputs, totals or another output format.:** The invocation stays stable. Users get no way to select or hide fields.

## Strategic Approach (The "How")

### Core Strategy

Report how many words the longest line holds as one extra trailing figure on the existing output line. Derive it only from the word and line definitions already in force, so no field can disagree with another. Treat the unterminated final segment as a line for this figure only. Document that difference next to the unchanged lines figure. Keep the existing fields, their meaning and the invocation unchanged for files and standard input.

### Rationale Against Alternatives

**Why NOT Change the existing lines figure to count an unterminated final segment, so both fields share one rule.:**  
It silently changes a shipped field. Existing parsers and the SPEC-0003 line rule would break, and the owner wants existing fields stable.

**Why NOT Give the longest-line measure its own word definition, such as splitting on spaces only.:**  
Words and the longest-line figure could disagree on the same input. The owner requires reuse of the existing word and line definitions.

**Why NOT Make the longest line available only through a new flag or a separate invocation.:**  
It breaks the single-argument invocation that the specs keep stable. It also makes users run twice for one answer.

**Why NOT Print the longest line's number or text beside its word count.:**  
It adds output the owner did not ask for and grows the contract. It could also echo large or sensitive file content.

**Why NOT Delegate the measure to an external tool or a third-party package.:**  
It adds a runtime dependency, which is forbidden. Tools such as wc -L measure display width, not words.

**Why NOT Place the new figure before or between existing fields, or on a second line.:**  
It shifts field positions and breaks parsers that read the three-field line. The owner fixed the label and the last position.

## Scope Boundaries (What Ships in v1)

### In Scope

- Report the word count of the longest line as one trailing field for files and for standard input.
- Count an unterminated final segment as a line for this measure only.
- Reuse the existing word rule and line terminator set, with CRLF as one terminator.
- Update the README, tests and specs that assert the three-field output line.
- Document how the lines field and the longest-line figure differ on the final segment.
- Pass all four Quality Gate commands.
- hello
- hello-cli
- word-count-command
- word-counter
- line-counter

### Out of Scope (Deferred)

- Location or text of the longest line.
- Length measures other than words.
- New flags, arguments or output formats.
- Changes to the word rule, the character rule or the line terminator set.
- Changes to the lines or characters fields.
- Changes to error messages and exit statuses.
- New third-party runtime dependencies.
- Existing capabilities from SPEC-0001 to SPEC-0004, such as the three counts and standard input through '-'.

## What Could Stop This — Dependencies, Assumptions, Risks

### Dependencies

| Dependency | Owner | Status |
|---|---|---|
| Approved word rule from SPEC-0001, reused unchanged to count words in a line. | wordcount project owner | Approved and implemented |
| Approved line terminator set from SPEC-0003, including CRLF as one terminator, reused to split text into lines. | wordcount project owner | Approved and implemented |
| Architecture update. ARCH-0001 lists the longest line as not owned, and it describes a three-count output line. | architect | Not started |
| Standard-input path from SPEC-0004, so the new field behaves the same for files and for '-'. | wordcount project owner | Approved and implemented |
| Quality Gate commands from AGENTS.md, which must all pass on the finished change. | wordcount project owner | Available |

### Assumptions

| Assumption | Validator | How it is checked | If false |
|---|---|---|---|
| An input with no words on any line, such as empty or whitespace-only text, reports a longest-line figure of 0. | wordcount project owner | Owner confirms the value at spec review. The spec states it as an example. | Define the empty-input value in the spec before implementation. Update the walkthrough and the README. |
| A trailing terminator does not create an extra empty final line, so 'a b\\n' reports 2. | wordcount project owner | Owner reviews the spec examples for terminated and unterminated input. | Re-open DISCOVER on the final-segment rule. |
| Reusers of the three-field line are limited to the README and the repository tests. | wordcount project owner | Owner confirms there are no external parsers. The team searches the tracked files for assertions on the output line. | List the affected consumers and add a migration note to the README. |
| The discovery graph's reference to SPEC-0005 means the approved specs SPEC-0001 to SPEC-0004 shown in the existing system. | wordcount project owner | Owner confirms that no other approved spec changes the word rule, the line set or the output line. | Review SPEC-0005 and revise the reused definitions and the scope. |

### Risks

| Risk | Likelihood | Impact | Mitigation |
|---|---|---|---|
| Readers take lines and longest_line_words as inconsistent because only one counts the final unterminated segment. | High | Users distrust the output or file false defects. | State the difference in the README with an example such as 'a b c' giving lines 0 and longest_line_words 3. Explain the reason there. |
| A second definition of word or line creeps in and the fields disagree on some input. | Medium | Wrong figures on edge input, such as mixed terminators or non-ASCII whitespace. | Require a cross-check that the longest-line figure agrees with the word count on single-line inputs. Reuse the existing definitions. |
| Existing assertions on the three-field line fail or are missed, and a change lands with a red Quality Gate. | High | Blocked change or hidden stale tests. | List every affected test, feature and README section in the spec. Run all four Quality Gate commands before landing. |
| SPEC-0004 forbids editing existing tests, and this change must edit tests that assert the three-field line. | Medium | Reviewers read the required edits as a violation of that guardrail. | State in the new spec that it supersedes the three-field assertions. Limit test edits to those assertions. |
| Existing parsers of the three-field line break on the new trailing field. | Low | Broken downstream use of the output. | Keep existing labels, order and meaning unchanged and append the new field last. Document the new line in the README. |

## Example-First Walkthrough

### Scenario: Text with no final terminator

**Today:**
- A user runs wordcount on a file containing 'a b c' with no terminator.
- The output is 'words: 3 characters: 3 lines: 0'.
- The user cannot see how long the line is in words.

**With this strategy:**
- The same file produces 'words: 3 characters: 3 lines: 0 longest_line_words: 3'.
- The final segment counts for the longest-line figure, so it reports 3.
- The lines field stays 0, and the README explains the difference.

### Scenario: Several lines of different length

**Today:**
- A file holds 'one two\nthree four five\nsix\n'.
- The output is 'words: 6 characters: 22 lines: 3'.
- No figure shows the longest line.

**With this strategy:**
- The output is 'words: 6 characters: 22 lines: 3 longest_line_words: 3'.
- The first three fields are unchanged.

### Scenario: Standard input with mixed terminators

**Today:**
- A user pipes 'a b\r\nc d e\rf' into 'wordcount -'.
- The output has three fields and no longest-line figure.

**With this strategy:**
- CRLF counts as one terminator and CR ends a line, as in the existing line rule.
- The unterminated segment 'f' also counts as a line for the longest-line figure.
- The output ends with 'longest_line_words: 3', the same as for a file holding the same bytes.

### Scenario: Empty input

**Today:**
- A user runs wordcount on an empty file.
- The output is 'words: 0 characters: 0 lines: 0'.

**With this strategy:**
- The output ends with a longest-line figure of 0, if the owner confirms that value.
- The first three fields are unchanged.

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

**Authored by:** openrouter:anthropic/claude-sonnet-5.5  
**Reviewed by:** _(pending)_ — _(pending)_

**Ready for SPEC:** [ ] Yes [ ] No
