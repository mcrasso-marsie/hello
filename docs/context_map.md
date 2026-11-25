---
artifact_type: context map
id: CTXMAP-hello
scope: project
status: Generated
generated_from: 82941ccf11248e9ab2d47892042922752309f7cc
---

# Context Map: hello

## Index

### Repositories

| Repository | Role | Architecture |
|------------|------|--------------|
| git@github.com:mcrasso-marsie/hello.git |  |  |

### Units

| Unit | Kind | Location | Depends on |
|------|------|----------|------------|
| hello (hello) | system | docs/architecture.md#8-system-decomposition |  |
| hello command-line package (hello-cli) | container | docs/architecture.md#8-system-decomposition |  |
| Word-count command (word-count-command) | component | docs/architecture.md#8-system-decomposition | Word counter, Character counter, Line counter |
| Word counter (word-counter) | component | docs/architecture.md#8-system-decomposition |  |
| Character counter (character-counter) | component | docs/architecture.md#8-system-decomposition |  |
| Line counter (line-counter) | component | docs/architecture.md#8-system-decomposition |  |

## Glossary

| Term | Context | Means | Owned by |
|------|---------|-------|----------|
|  |  |  |  |

## Routing Table

| If the work concerns | Go to | Kind |
|----------------------|-------|------|
| Word-count command (SPEC-0001) | docs/specs/SPEC-0001.md | spec |
| Character count in word-count output (SPEC-0002) | docs/specs/SPEC-0002.md | spec |
| Line count in word-count output (SPEC-0003) | docs/specs/SPEC-0003.md | spec |
| Standard input through an explicit '-' argument (SPEC-0004) | docs/specs/SPEC-0004.md | spec |
| Standard-library-only runtime (ADR-0001) | docs/adrs/ADR-0001.md | ADR |
| Pure word counter separated from command I/O (ADR-0002) | docs/adrs/ADR-0002.md | ADR |
| Minimal Quality Gate toolchain: ruff, mypy, pytest (ADR-0003) | docs/adrs/ADR-0003.md | ADR |
| One-line error and exit-status contract for CLI commands (ADR-0004) | docs/adrs/ADR-0004.md | ADR |
| Visible-character rule in a pure character counter (ADR-0005) | docs/adrs/ADR-0005.md | ADR |
| Explicit line-terminator rule in a pure line counter (ADR-0007) | docs/adrs/ADR-0007.md | ADR |
| Three-field labeled success output for wordcount (supersedes ADR-0006) (ADR-0008) | docs/adrs/ADR-0008.md | ADR |
| Explicit '-' stdin marker sharing the file decode path (ADR-0009) | docs/adrs/ADR-0009.md | ADR |
| Architecture (ARCH-0001) | docs/architecture.md | architecture |

## Validation Checklist

**Mechanical**

- [ ] Every pointer in every section resolves to a file, and an anchored
      pointer resolves to a heading that exists
- [ ] No routing entry points at a directory, at another index, or at a
      file whose answer is a further redirect (the two-lookup rule)
- [ ] Every spec and every ADR owned at this scope is reachable from the
      Routing Table
- [ ] The Index is complete for this scope: every project (org), every
      mapped repository (project), or every unit (repo)
- [ ] Only the tables this scope uses are present; the others are deleted
- [ ] No row repeats a row from the map above it in the chain, at any
      scope and in any section
- [ ] `generated_from` matches the current head of the mapped
      repositories; a spec or architecture change since then means the map
      is stale
- [ ] No entry spans more than one line, and no section contains prose
      paragraphs
- [ ] No entry names a skill, a persona, or a workflow stage
- [ ] No entry summarizes, quotes or restates the content of the file it
      points at
- [ ] Term and Context together are unique across the Glossary

**Judgment**

- [ ] Routing entries are written in the vocabulary a person would use
      when asking, not in the system's internal names
- [ ] Each glossary term carries its meaning AT THIS SCOPE; terms whose
      ordinary meaning already applies have been left out
- [ ] The Index's granularity matches what an agent would need to locate,
      neither one row per repository nor one row per file
- [ ] Each map refines the level above rather than restating it, and holds
      only what is true at its own scope
- [ ] An org map exists only where the organization runs several projects,
      and carries only vocabulary and routing every project shares
