"""Claude Code adaptor — uses the generic rule+skill+hooks installer.

The hitl-gates skill ships scripts/hitl_tools.py which re-exports
pause_task / resume_task / list_paused_tasks from builtin_tools.hitl.
The skill loader auto-discovers them as LangChain @tool-decorated functions
and registers them on the Claude Code agent's tool list.
"""
from plugins_registry.builtins import AgentskillsAdaptor as Adaptor  # noqa: F401
