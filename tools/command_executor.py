"""Tool that executes shell commands with timeout + logging."""

from __future__ import annotations

import subprocess
from typing import Dict, Sequence

from loguru import logger


class CommandExecutor:
  name = "command_executor"

  def __init__(self, cwd: str | None = None, timeout: int = 600) -> None:
    self.cwd = cwd
    self.timeout = timeout

  def run(self, command: str | Sequence[str]) -> Dict[str, str | int]:
    logger.debug(f"Running command: {command}")
    proc = subprocess.run(
        command,
        shell=isinstance(command, str),
        cwd=self.cwd,
        capture_output=True,
        text=True,
        timeout=self.timeout,
        encoding="utf-8",
        errors="ignore",
    )
    return {
        "returncode": proc.returncode,
        "stdout": proc.stdout,
        "stderr": proc.stderr,
    }


