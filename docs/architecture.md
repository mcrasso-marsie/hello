---
artifact_type: architecture
id: ARCH-0001
version: 1.2
status: Approved
---

# ARCHITECTURE.md

## 1. System Mission

(none yet)

## 2. Business Goals

(none yet)

## 3. Architectural Drivers

(none yet)

## 4. Architectural Style

(none yet)

## 5. Quality Attribute Scenarios

(none yet)

## 6. Tactics

(none yet)

## 7. Architectural Patterns

(none yet)

## 8. System Decomposition

### Context

```mermaid
flowchart LR
classDef added fill:#c8f7c5,stroke:#2e7d32
classDef changed fill:#fff3b0,stroke:#b59f00
classDef removed fill:#f8c8c8,stroke:#c62828
hello["hello<br/>system"]
```

### Container

```mermaid
flowchart LR
classDef added fill:#c8f7c5,stroke:#2e7d32
classDef changed fill:#fff3b0,stroke:#b59f00
classDef removed fill:#f8c8c8,stroke:#c62828
subgraph hello["hello"]
  hello_cli["hello command-line package<br/>container"]
end
```

### Component: hello command-line package

```mermaid
flowchart LR
classDef added fill:#c8f7c5,stroke:#2e7d32
classDef changed fill:#fff3b0,stroke:#b59f00
classDef removed fill:#f8c8c8,stroke:#c62828
subgraph hello_cli["hello command-line package"]
  word_count_command["Word-count command<br/>component"]
  word_counter["Word counter<br/>component"]
  character_counter["Character counter<br/>component"]
  line_counter["Line counter<br/>component"]
end
word_count_command -->|"Passes the decoded file text in an in-process function call and receives the integer word count."| word_counter
word_count_command -->|"Passes the decoded file text in an in-process function call and receives the integer count of non-whitespace visible characters."| character_counter
word_count_command -->|"Passes the same decoded file text given to the word and character counters, in an in-process function call, and receives the integer count of terminated lines."| line_counter
```

| ID | Unit | Level | Parent | Owns | Does NOT own | Deployment | Tech Family |
|----|------|-------|--------|------|--------------|------------|-------------|
| hello | hello | system |  | Giving users local, dependency-free text utilities. It currently reports the word count, the non-whitespace character count and the terminated-line count of one text file in a single invocation. | Other text statistics beyond word, character and line counts (such as bytes, longest line or per-line output), batch or stdin processing, non-UTF-8 encodings, or distribution through a public package index. | Installed from the repository into a local Python environment on the user's machine. | Python (current stable release), standard library only |
| hello-cli | hello command-line package | container | hello | The installable src-layout hello package and its console command. The command takes one file path, prints that file's word, character and line counts on one line, and exits with a status code. | Any network access, persistent state, configuration files, command-line flags beyond the single PATH argument, or third-party runtime dependencies. | Run as a local process on the user's machine after installing the package from the repository into the project environment. | Python standard library; console entry point declared in pyproject.toml; environment managed with the existing lockfile tooling |
| word-count-command | Word-count command | component | hello-cli | Parsing the single file-path argument and reading the file once as UTF-8 text. It passes that same decoded text to the word counter, the character counter and the line counter, and prints the three counts as one line in the form `words: <N> characters: <M> lines: <L>`. It turns a missing file, an unreadable file or undecodable content into a one-line message on standard error, with a non-zero exit status and no counts on standard output; these messages and statuses are unchanged. | The definition of what a word, a visible character or a line is, or counting logic of any kind. It does not decode the file a second time or along a separate path for line counting. |  | Python standard library |
| word-counter | Word counter | component | hello-cli | The word rule: a word is a run of non-whitespace characters separated by whitespace. It counts the words in a given text and returns the number. | File access, encoding, argument handling, output or exit codes; it never touches the filesystem or the process. |  | Python standard library |
| character-counter | Character counter | component | hello-cli | The character rule: a visible character is a non-whitespace character, using the same whitespace definition as the word rule, and a base character followed by combining marks counts once. It counts the visible characters in a given text and returns the number. | The definition of a word, file access, encoding, argument handling, output formatting or exit codes; it never touches the filesystem or the process, and it counts neither bytes nor raw code points. |  | Python standard library |
| line-counter | Line counter | component | hello-cli | The line rule. A line is a segment of text ended by a line terminator, and a final segment with no terminator is not counted. The terminator set is exactly the boundaries str.splitlines() recognises, listed explicitly so the rule does not depend on library behaviour: LF (U+000A), CR (U+000D), the CRLF pair (U+000D U+000A, counted as one terminator), VT (U+000B), FF (U+000C), FS (U+001C), GS (U+001D), RS (U+001E), NEL (U+0085), LS (U+2028) and PS (U+2029). It counts the terminated lines in a given text and returns the number. | The definition of a word or a visible character, file access, encoding or newline translation, argument handling, output formatting or exit codes. It never touches the filesystem or the process, and it does not follow the LF-only wc -l convention. |  | Python standard library |

## 9. Communication Patterns

| From | To | Description |
|------|----|-------------|
| word-count-command | word-counter | Passes the decoded file text in an in-process function call and receives the integer word count. |
| word-count-command | character-counter | Passes the decoded file text in an in-process function call and receives the integer count of non-whitespace visible characters. |
| word-count-command | line-counter | Passes the same decoded file text given to the word and character counters, in an in-process function call, and receives the integer count of terminated lines. |

## 10. Data Architecture

(none yet)

## 11. Cross-cutting Concerns

(none yet)

## 12. Deployment Topology

(none yet)

## 13. Global Anti-Patterns

(none yet)

## 14. Open Architectural Risks

(none yet)

## 15. Architecture Decision Index

(none yet)

## 16. Related Artifacts

(none yet)

## Changelog

| Version | Date | Summary | Triggered by |
|---------|------|---------|--------------|
| 1.0 | 2026-11-12 | First architecture draft: the hello system as one local Python CLI container with a word-count command, split into a command-line shell and a pure, dependency-free counting core. | SPEC-0001 |
| 1.1 | 2026-11-14 | Add a pure character-counter component beside the word counter, and have the command print both counts on one line (a deliberate break from SPEC-0001's bare integer), so users get words and non-whitespace characters in one invocation. | SPEC-0002 |
| 1.2 | 2026-11-14 | Add a pure line-counter component beside the word and character counters, and have the command append ` lines: <L>` to its single success line, so users get words, characters and lines from one invocation (SPEC-0003, from STRAT-0003). | SPEC-0003 |
