"""Adapter for plugging in MCP/LLM-backed web search services."""

from __future__ import annotations

from typing import List

from loguru import logger


class WebSearchTool:
  name = "web_search"

  def __init__(self, provider: str = "brave") -> None:
    self.provider = provider

  def run(self, query: str, top_k: int = 3) -> List[dict]:
    logger.warning("Web search not yet wired up. Query=%s provider=%s", query, self.provider)
    return [{"title": "placeholder result", "snippet": "Replace with real MCP integration.", "url": ""}]


