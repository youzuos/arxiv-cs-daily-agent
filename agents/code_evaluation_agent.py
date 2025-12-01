"""Agent that validates code quality via automated checks."""

from __future__ import annotations

from typing import Any, Dict

from loguru import logger

from .base_agent import AgentMessage, BaseAgent


class CodeEvaluationAgent(BaseAgent):
  """Runs lint/tests and reports pass/fail back to orchestrator."""

  def think(self, message: AgentMessage) -> AgentMessage:
    command = message.metadata.get("command", "npm run test")
    logger.info(f"CodeEvaluationAgent running {command}")
    result = self.dispatch_tool("command_executor", command)
    status = "passed" if result.get("returncode") == 0 else "failed"
    summary = {
        "task_id": message.metadata.get("task_id"),
        "description": message.metadata.get("description"),
        "command": command,
        "status": status,
        "stdout": result.get("stdout"),
        "stderr": result.get("stderr"),
        "returncode": result.get("returncode"),
    }
    return AgentMessage(
        sender=self.name,
        content="evaluation-result",
        metadata=summary,
    )

  def dispatch_tool(self, tool_name: str, *args, **kwargs) -> Dict[str, Any]:
    return super().dispatch_tool(tool_name, *args, **kwargs)


