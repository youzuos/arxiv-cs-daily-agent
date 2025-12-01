"""Shared dataclasses that describe project tasks and statuses."""

from __future__ import annotations

from dataclasses import dataclass, field
from enum import Enum
from typing import Any, Dict, List, Optional


class TaskStatus(str, Enum):
  PENDING = "pending"
  IN_PROGRESS = "in_progress"
  COMPLETED = "completed"
  FAILED = "failed"


@dataclass
class Task:
  task_id: str
  title: str
  description: str
  owner: str
  depends_on: List[str] = field(default_factory=list)
  status: TaskStatus = TaskStatus.PENDING
  metadata: Dict[str, Any] = field(default_factory=dict)
  result: Optional[Dict[str, Any]] = None


