"""HITL tools re-exported for the skill loader's auto-discovery.

The skill loader scans this scripts/ directory for @tool-decorated functions
and registers them on the Claude Code agent's tool list.

The actual implementation lives in builtin_tools/hitl.py (present in every
workspace image). This module simply re-exports the three public tools so the
skill loader can find them without needing to know the builtin_tools import path.
"""
from builtin_tools.hitl import list_paused_tasks, pause_task, resume_task  # noqa: F401
