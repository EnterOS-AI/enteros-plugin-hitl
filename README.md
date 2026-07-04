# molecule-hitl

Human-in-the-loop gates for async agent tasks. Wraps `builtin_tools/hitl.py` — adds an approval requirement decorator, pause/resume tools, and multi-channel notification (dashboard, Slack, email) to any callable.

## How it works

Plugins declare functions or tool calls that require human approval before execution. When triggered, the agent pauses and notifies via configured channels. A human reviews and approves or rejects from the dashboard or Slack.

RBAC roles can be configured to bypass approval for trusted roles (e.g., `oncall-engineer`).

## Features

- **`@requires_approval` decorator** — mark any async callable as gate-required
- **`pause_task` / `resume_task` tools** — agent-side pause and resume
- **Multi-channel notification** — dashboard, Slack, email
- **RBAC bypass** — configurable role exemptions
- **Timeout handling** — configurable max wait; timeout action configurable

## Install

### In org template (org.yaml)

```yaml
plugins:
  - molecule-hitl
```

### From URL (community install)

```
github://Molecule-AI/molecule-ai-plugin-molecule-hitl
```

## Configuration

In workspace `config.yaml`:

```yaml
hitl:
  channels:
    dashboard: true
    slack: true
    email: true
  timeout_minutes: 30
  timeout_action: reject  # or: escalate
  bypass_roles:
    - oncall-engineer
    - security-admin
```

## Runtimes

- `claude_code` — supported

## Skills

- `hitl-gates` — agent-side guidance on when to call pause/resume

## Architecture

```
skills/
  hitl-gates/
    SKILL.md       # Agent-side guidance (when/how to use HITL gates)
    scripts/
      hitl_tools.py  # Re-exports pause_task / resume_task / list_paused_tasks
                     # for the skill loader's auto-discovery
adapters/
  claude_code.py  # Installs skill via AgentskillsAdaptor; HITL tools land on
                   # the Claude Code agent's tool list via scripts/hitl_tools.py
```

## Known issues

See [known-issues.md](known-issues.md).

## License

Business Source License 1.1 — © Molecule AI.
