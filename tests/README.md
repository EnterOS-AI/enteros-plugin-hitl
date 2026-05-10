# Test Coverage Rationale — molecule-hitl

## Why This Plugin Has Limited Unit-Test Coverage

`molecule-hitl` is a **skill-only plugin**. The HITL gate implementation lives in
`builtin_tools/hitl.py` in molecule-core — it is tested in the core test suite.
This plugin's contribution is the policy layer: the SKILL.md that tells an agent
*when* to use HITL gates and *how* to configure them.

There are no hooks, no Python code, and no adapters in this plugin.

## What We Test (and Why)

| What | Why |
|------|-----|
| `plugin.yaml` schema | Verifies skill is registered correctly |
| `skills/hitl-gates/SKILL.md` frontmatter + sections | Ensures skill is documented with all required sections (when-to-use, decorator form, pause/resume form, config, anti-patterns, test plan) |
| `known-issues.md` structure | Documents severity definitions |
| `README.md` sections | Verifies install instructions are present |
| `validate-plugin.py` exit 0 | Smoke test — shared CI validator passes |

## What We Cannot Unit-Test Here

- **`@requires_approval` decorator** — tested in molecule-core's test suite
- **`pause_task` / `resume_task` tools** — runtime tools, not plugin code
- **End-to-end approval flow** — requires a running workspace with channels configured

## Integration Tests

If you want to test the full HITL approval flow, write integration tests in the
`workspace-template/` test suite that:

1. Install `molecule-hitl` on a test workspace
2. Configure `hitl.channels` in `config.yaml`
3. Call a function decorated with `@requires_approval`
4. Verify the approval appears in `GET /approvals/pending`
5. Approve/deny and verify the agent behavior
