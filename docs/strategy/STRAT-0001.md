---
artifact_type: strategy
id: STRAT-0001
status: Approved
---

# Strategy Document: Give the hello project its first user-facing capability now: a minimal, dependency-free command that reports a text file's word count, built and documented to a clear, enforced quality bar.

## Executive Summary

**Thesis:** Give the hello project its first user-facing capability now: a minimal, dependency-free command that reports a text file's word count, built and documented to a clear, enforced quality bar.

**From Problem Graph:** DG-0001

## Goals (What We Aim to Achieve)

### Goal 1: A user can get the word count of a text file by running one command with the file path.
**Why:** This is the primary requested capability, and the project currently has no user-facing entry point.  
**Success Metric:** The reported count matches the expected count on 100% of the agreed sample files.  
**Owner:** Project owner

### Goal 2: Bad input fails clearly instead of crashing.
**Why:** Error handling was the least certain part of the request, and stack traces block non-expert users.  
**Success Metric:** Every defined error case (missing file, unreadable file, undecodable content) yields a one-line message and a non-zero exit, with 0 uncaught exceptions in tests.  
**Owner:** Project owner

### Goal 3: Every change is checked against a defined, minimal quality bar on a current Python version.
**Why:** The owner asked for best practices and the latest Python, but the toolchain table is empty, so nothing is enforced today.  
**Success Metric:** The AGENTS.md Toolchain table lists 4 Quality Gate commands (format, lint, type-check, test), all passing on the target Python version.  
**Owner:** Project owner

### Goal 4: A new user can install and run the command from the README alone.
**Why:** The README currently gives no install or run path, so adoption needs outside help.  
**Success Metric:** A fresh-clone walkthrough following only the README reaches a correct word count with 0 extra steps.  
**Owner:** Project owner

## Success Criteria (Observable & Verifiable)

| Criterion | Measurement | Target | Baseline | Cadence |
|---|---|---|---|---|
| Word-count correctness | Automated tests against the agreed sample fixtures | 100% of fixtures match | No capability exists | Every change, via the Quality Gate |
| Graceful error handling | Automated tests for each defined error case | All cases produce a clear message and a non-zero exit | No capability exists | Every change |
| Quality Gate defined and green | AGENTS.md Toolchain commands run locally and pass | 4 commands defined, all passing | 0 commands defined | Every change |
| Runtime dependency footprint | Runtime dependencies declared in pyproject.toml | 0 third-party runtime dependencies | 0 | At each review |
| Documented onboarding | Manual fresh-clone run following only the README | Succeeds with no outside help | README has no install or run instructions | Before each release |

## Non-Goals (What We Deliberately Skip in v1)

- **Counting lines, characters or bytes, or producing other text statistics.:** This keeps the tool single-purpose and cheap to test. Users who need more statistics must use other tools for now.
- **Counting multiple files at once or reading from standard input.:** This avoids designing aggregation and output formats nobody asked for. Pipelines and batch use are not supported in v1.
- **Language-aware word segmentation (for example, scripts without spaces between words).:** The simple whitespace rule stays predictable. Counts for such languages will not match linguistic expectations.
- **Publishing the package to a public package index.:** It avoids release and versioning overhead. Users install from the repository as the README describes.

## Strategic Approach (The "How")

### Core Strategy

Add one small, single-purpose command to the existing hello package. It takes the path of one text file and reports how many words it contains. It is built only on what the language runtime already provides, guarded by a quality bar that is defined once and enforced on every change, and documented well enough that a new user can install and run it without help. Breadth, configurability and outside dependencies are deliberately traded away for a capability that is correct, predictable and cheap to maintain.

### Rationale Against Alternatives

**Why NOT Build the command on a third-party command-line framework.:**  
Every external dependency needs a documented rationale under AGENTS.md. A one-argument command gains almost nothing from a framework, and it would add install weight, lockfile churn and supply-chain surface.

**Why NOT Delegate counting to the operating system's existing word-count utility and wrap it.:**  
Behavior would depend on the platform. The utility is missing or differs on some systems, so results would vary across machines and would not be testable in isolation.

**Why NOT Ship a general text-statistics tool (lines, characters, multiple files, stdin, output formats) from the start.:**  
It multiplies the surface to test, document and maintain for options nobody asked for. It delays the one requested capability and conflicts with the minimalist scope.

**Why NOT Expose word counting only as an importable library function, with no command.:**  
It does not meet the stated need. The user wants to run a command with a file path and see a number, not write code.

## Scope Boundaries (What Ships in v1)

### In Scope

- A word-count command added to the existing hello package that accepts one text file path and prints its word count
- Clear error reporting and non-zero exit for missing, unreadable or undecodable files
- A defined word rule, stated in documentation and backed by tests
- Quality Gate commands recorded in the AGENTS.md Toolchain table and enforced on every change
- Project configured for the current stable Python release
- README install and run instructions for the command

### Out of Scope (Deferred)

- The existing src layout, py.typed marker and lockfile setup, which already exist and are not re-planned
- Other text statistics (lines, characters, bytes)
- Multiple files, directories or standard input
- Encodings other than UTF-8 and streaming for very large files
- Third-party runtime dependencies
- Publishing to a package index

## What Could Stop This — Dependencies, Assumptions, Risks

### Dependencies

| Dependency | Owner | Status |
|---|---|---|
| A current stable Python runtime, available to the project's existing environment and lockfile tooling. | Project owner | Available |
| The existing src-layout hello package and pyproject.toml, which the new command is added to. | Project owner | Available |
| Quality Gate commands (format, lint, type-check, test) recorded in the AGENTS.md Toolchain table. | Project owner | Not yet defined; the table is empty |

### Assumptions

| Assumption | Validator | How it is checked | If false |
|---|---|---|---|
| A 'word' means a run of non-whitespace characters separated by whitespace, matching the common word-count convention. | Project owner | The owner reviews the expected counts for a small sample set before SPEC is finalized. The set covers punctuation, multiple spaces, tabs, newlines and an empty file. | Revise the word definition in SPEC before implementation. The strategy direction is unchanged. |
| Input files are UTF-8 (or ASCII) text and small enough to process comfortably on a developer machine. | Project owner | The owner confirms the intended inputs. Test fixtures include a UTF-8 file with non-ASCII characters. | Add explicit handling for other encodings or streaming of large files as a scoped follow-up. |
| Requiring the newest stable Python release does not exclude the intended users. | Project owner | The owner confirms the target environments when the version pin is set in SPEC. | Pin to the oldest Python version those environments support and record the rationale. |

### Risks

| Risk | Likelihood | Impact | Mitigation |
|---|---|---|---|
| A missing, unreadable, binary or wrongly encoded file causes an unhandled crash with a stack trace. | Medium | Poor first-user experience and an unclear failure. | Treat each error case as a first-class scenario. It produces a clear one-line message and a non-zero exit, and each case is covered by tests. |
| 'Best practices' expands into heavy tooling and ceremony that outweighs a tiny tool. | Medium | Slower changes and a maintenance burden with no user value. | Limit the Quality Gate to formatting, linting, type-checking and tests. Each command is recorded in AGENTS.md, and any further tool requires a written rationale. |
| The word definition differs from what the user intuitively expects on edge cases. | Low | Counts are seen as wrong and trust in the tool is lost. | Validate the definition against sample files with the owner, and state it in the README. |

## Example-First Walkthrough

### Scenario: Count words in a file

**Today:**
- The user has notes.txt and wants to know how many words it contains.
- The hello package has no command to run.
- The user counts by hand or looks for another tool.

**With this strategy:**
- The user runs the hello word-count command with the path notes.txt.
- The command prints the number of words, for example 342.
- The user has the answer in one step.

### Scenario: Wrong file path

**Today:**
- No command exists, so there is no behavior to rely on.

**With this strategy:**
- The user mistypes the path as notse.txt.
- The command prints a one-line message saying the file was not found, with no stack trace.
- The command exits with a non-zero status, and the user corrects the path.

### Scenario: New user onboarding

**Today:**
- A new user clones the repository.
- The README says nothing about how to install or run anything.
- The user has to ask the owner or read the source.

**With this strategy:**
- A new user clones the repository and opens the README.
- They follow the stated install and run steps.
- They count words in a sample file without outside help.

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
