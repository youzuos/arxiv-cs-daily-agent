"""Common abstractions shared by all agents."""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any, Dict, List, Optional, Protocol

from loguru import logger


@dataclass
class AgentMessage:
  """Structured message exchanged between agents."""

  sender: str
  content: str
  metadata: Dict[str, Any] = field(default_factory=dict)


class Tool(Protocol):
  """Lightweight protocol each tool implementation should satisfy."""

  name: str

  def run(self, *args, **kwargs) -> Any:
    ...


class BaseAgent:
  """Base class that provides logging and tool access."""

  def __init__(self, name: str, tools: Optional[List[Tool]] = None) -> None:
    self.name = name
    self.tools = tools or []

  def dispatch_tool(self, tool_name: str, *args, **kwargs) -> Any:
    for tool in self.tools:
      if tool.name == tool_name:
        logger.debug(f"{self.name} invoking tool {tool_name}")
        return tool.run(*args, **kwargs)
    raise ValueError(f"Tool {tool_name} not registered for {self.name}")

  def think(self, message: AgentMessage) -> AgentMessage:
    raise NotImplementedError("Agents must implement think()")


