"""Filesystem helper functions used by agents."""

from __future__ import annotations

from pathlib import Path
from typing import Optional

from loguru import logger


class FileManager:
  name = "file_manager"

  def __init__(self, root: Optional[Path] = None) -> None:
    self.root = root or Path.cwd()

  def run(self, operation: str, relative_path: str, content: str | None = None) -> str:
    target = self.root / relative_path
    logger.debug(f"FileManager {operation} -> {target}")
    if operation == "read":
      return target.read_text(encoding="utf-8")
    if operation == "write":
      target.parent.mkdir(parents=True, exist_ok=True)
      target.write_text(content or "", encoding="utf-8")
      return "written"
    if operation == "append":
      target.parent.mkdir(parents=True, exist_ok=True)
      with target.open("a", encoding="utf-8") as fh:
        fh.write(content or "")
      return "appended"
    raise ValueError(f"Unsupported operation {operation}")


