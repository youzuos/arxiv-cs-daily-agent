"""Simple orchestrator that routes tasks to role-specific agents."""

from __future__ import annotations

from collections import deque
from typing import Deque, Dict, List

from loguru import logger

from agents.base_agent import AgentMessage
from agents.code_evaluation_agent import CodeEvaluationAgent
from agents.code_generation_agent import CodeGenerationAgent
from agents.planning_agent import PlanningAgent
from orchestrator.task_types import Task, TaskStatus


class MultiAgentOrchestrator:
  def __init__(self, planning_agent: PlanningAgent, code_agent: CodeGenerationAgent,
               eval_agent: CodeEvaluationAgent) -> None:
    self.planning_agent = planning_agent
    self.code_agent = code_agent
    self.eval_agent = eval_agent
    self.tasks: Dict[str, Task] = {}
    self.queue: Deque[str] = deque()

  def bootstrap(self, requirement: str) -> None:
    planner_msg = AgentMessage(sender="user", content=requirement)
    plan = self.planning_agent.think(planner_msg)
    for payload in plan.metadata.get("tasks", []):
      task = Task(**payload)
      self.tasks[task.task_id] = task
    self._refresh_queue()
    logger.info(f"Planner populated {len(self.tasks)} tasks")

  def _refresh_queue(self) -> None:
    self.queue.clear()
    for task_id, task in self.tasks.items():
      if task.status == TaskStatus.PENDING and self._dependencies_met(task):
        self.queue.append(task_id)

  def _dependencies_met(self, task: Task) -> bool:
    return all(self.tasks[dep].status == TaskStatus.COMPLETED for dep in task.depends_on)

  def run(self) -> None:
    while self.queue:
      task_id = self.queue.popleft()
      task = self.tasks[task_id]
      task.status = TaskStatus.IN_PROGRESS
      logger.info(f"Dispatching {task_id} to {task.owner}")
      if task.owner == "code_generation":
        metadata = {"task_id": task.task_id, **task.metadata}
        result = self.code_agent.think(AgentMessage(sender="orchestrator", content=task.description,
                                                    metadata=metadata))
      else:
        metadata = {"task_id": task.task_id, **task.metadata}
        result = self.eval_agent.think(AgentMessage(sender="orchestrator", content=task.description,
                                                    metadata=metadata))
      task.result = result.metadata
      task.status = TaskStatus.COMPLETED
      self._refresh_queue()

  def summary(self) -> List[Dict[str, str]]:
    return [{"task_id": tid, "status": task.status, "owner": task.owner} for tid, task in self.tasks.items()]


