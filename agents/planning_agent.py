"""Agent responsible for expanding a natural language brief into executable tasks."""

from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime
from typing import Any, Dict, List

from loguru import logger

from .base_agent import AgentMessage, BaseAgent


@dataclass
class PlannedTask:
  task_id: str
  title: str
  description: str
  depends_on: List[str] = field(default_factory=list)
  owner: str = "code_generation"
  metadata: Dict[str, Any] = field(default_factory=dict)


class PlanningAgent(BaseAgent):
  """Simple heuristic planner (can be replaced with LLM-backed workflow later)."""

  def think(self, message: AgentMessage) -> AgentMessage:
    logger.info(f"PlanningAgent received brief from {message.sender}")
    tasks = self._draft_plan(message.content)
    response = AgentMessage(
        sender=self.name,
        content="generated-plan",
        metadata={"tasks": [task.__dict__ for task in tasks]},
    )
    logger.debug(f"Planner produced {len(tasks)} tasks")
    return response

  def _draft_plan(self, requirement: str) -> List[PlannedTask]:
    # Placeholder deterministic plan tailored for the assignment requirements.
    logger.debug(f"Drafting plan for requirement: {requirement}")
    return [
        PlannedTask(
            task_id="plan-frontend",
            title="Design homepage layout",
            description="Create navigation, hero, categories, and feed sections that mirror the reference mockups.",
            owner="code_generation",
            metadata={
                "actions": [
                    {
                        "operation": "write",
                        "path": "logs/plan-frontend.md",
                        "content": "Drafted homepage structure with navigation, hero, categories, and feed.",
                    }
                ]
            },
        ),
        PlannedTask(
            task_id="plan-data",
            title="Prepare paper data pipeline",
            description="Implement data fetcher/mock JSON to hydrate homepage + detail pages.",
            owner="code_generation",
            depends_on=["plan-frontend"],
            metadata={
                "actions": [
                    {
                        "operation": "llm",
                        "prompt": (
                            "Generate a JSON array with 15 unique arXiv-style computer science papers. "
                            "Each object must have: id (unique, format like 2512.12345 for December 2025 papers), "
                            "title (unique, no duplicates), authors (array of 2-5 author names), "
                            "submittedAt (YYYY-MM-DD, MUST include today's date {today} for at least one paper, "
                            "and use recent dates from the last 2-3 months), "
                            "abstract (2-3 sentences), categories (array of 1-3 cs.* tags like cs.AI, cs.CV, cs.LG, cs.AR, cs.CL, cs.SE, cs.CC), "
                            "and pdfUrl (format: https://arxiv.org/pdf/{{id}}.pdf). "
                            "IMPORTANT: At least 2-3 papers must have today's date ({today}). "
                            "Ensure all papers are unique with different titles, IDs, and varied submission dates. "
                            "Return ONLY valid JSON array, no markdown code blocks."
                        ).format(today=datetime.now().strftime("%Y-%m-%d")),
                        "path": "frontend/src/data/papers.json",
                        "fallback_script": "python scripts/generate_mock_papers.py",
                    },
                ]
            },
        ),
        PlannedTask(
            task_id="plan-detail-page",
            title="Implement dedicated paper page",
            description="Create PDF link, metadata, citation copy buttons.",
            owner="code_generation",
            depends_on=["plan-data"],
            metadata={
                "actions": [
                    {
                        "operation": "script",
                        "command": "python scripts/generate_detail_page.py",
                        "description": "Generate PaperDetail React component",
                    }
                ]
            },
        ),
        PlannedTask(
            task_id="plan-tests",
            title="Validation & QA",
            description="Run automated lint/tests and route feedback to evaluation agent.",
            owner="code_evaluation",
            depends_on=["plan-detail-page"],
            metadata={
                "command": "npm run build --prefix frontend",
                "description": "Ensure React app builds successfully",
            },
        ),
    ]


