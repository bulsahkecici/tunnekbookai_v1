# Codex Workflow

## Normal task

1. Start a new Codex session for each major phase.
2. Let the root `AGENTS.md` apply automatically.
3. Read `docs/ai/CURRENT_STATE.md` and `docs/ai/NEXT_PHASE.md` only when needed.
4. Search before reading.
5. Open only relevant files.
6. Run targeted tests.
7. Inspect the targeted diff.
8. Stop when the task is complete.

Use one agent for normal local work. When Codex trusts the project, its config
disables subagents, Fast mode, and app/connectors. User-configured MCP servers
remain unchanged unless disabled individually by their configured ID.

## Good prompt

> Fix DOC000123 metadata/provenance issue.
> Search first.
> Do not scan the corpus.
> Run targeted tests only.

## Bad prompt

> Read the entire repository and corpus and understand everything.
