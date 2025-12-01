"""Agent that executes concrete development tasks."""

from __future__ import annotations

from typing import Any, Dict, List

from loguru import logger

from .base_agent import AgentMessage, BaseAgent


class CodeGenerationAgent(BaseAgent):
  """Wraps LLM/tool workflow that modifies the workspace."""

  def think(self, message: AgentMessage) -> AgentMessage:
    logger.info(f"CodeGenerationAgent handling task: {message.metadata.get('task_id')}")
    task_summary = self._execute_task(message.metadata or {}, message.content)
    return AgentMessage(
        sender=self.name,
        content="task-complete",
        metadata=task_summary,
    )

  def _execute_task(self, metadata: Dict[str, Any], instruction: str) -> Dict[str, Any]:
    logger.debug(f"Executing instruction: {instruction}")
    actions: List[Dict[str, Any]] = metadata.get("actions", [])
    files_touched: List[str] = []

    for action in actions:
      op = action.get("operation")
      path = action.get("path")
      if op in {"write", "append"}:
        if not path:
          logger.warning(f"Skipping malformed file action: {action}")
          continue
        content = action.get("content", "")
        result = self.dispatch_tool("file_manager", op, path, content)
        logger.info(f"Applied {op} on {path} -> {result}")
        files_touched.append(path)
      elif op == "script":
        command = action.get("command")
        if not command:
          logger.warning(f"Skipping script action without command: {action}")
          continue
        result = self.dispatch_tool("command_executor", command)
        logger.info(f"Executed script {command} -> code {result.get('returncode')}")
        files_touched.append(action.get("description", command))
      elif op == "llm":
        prompt = action.get("prompt")
        target_path = action.get("path")
        fallback_script = action.get("fallback_script")
        if not prompt or not target_path:
          logger.warning(f"Skipping LLM action without prompt/path: {action}")
          continue
        logger.info(f"🚀 Attempting LLM generation for {target_path}")
        try:
          completion = self.dispatch_tool("llm_client", prompt)
          # 清理 LLM 输出：移除 markdown 代码块标记
          cleaned = completion.strip()
          if cleaned.startswith("```"):
            # 移除开头的 ```json 或 ```
            lines = cleaned.split("\n")
            if lines[0].startswith("```"):
              lines = lines[1:]
            # 移除结尾的 ```
            if lines and lines[-1].strip() == "```":
              lines = lines[:-1]
            cleaned = "\n".join(lines)
          
          # 验证并清理 JSON
          import json
          try:
            data = json.loads(cleaned)
            # 去重：基于 title 和 id
            seen = set()
            unique_data = []
            for item in data:
              key = (item.get("id"), item.get("title"))
              if key not in seen and key[0] and key[1]:
                seen.add(key)
                unique_data.append(item)
            
            if len(unique_data) < len(data):
              logger.info(f"Removed {len(data) - len(unique_data)} duplicate papers")
            
            cleaned = json.dumps(unique_data, indent=2, ensure_ascii=False)
          except json.JSONDecodeError as e:
            logger.warning(f"JSON parsing failed, writing raw content: {e}")
          
          self.dispatch_tool("file_manager", "write", target_path, cleaned)
          logger.info(f"✅ LLM generated {len(unique_data) if 'unique_data' in locals() else 'unknown'} unique papers written to {target_path}")
          files_touched.append(target_path)
        except Exception as e:
          logger.warning(f"LLM call failed: {e}. Falling back to script method.")
          if fallback_script:
            result = self.dispatch_tool("command_executor", fallback_script)
            logger.info(f"Fallback script executed: {fallback_script} -> code {result.get('returncode')}")
            files_touched.append(fallback_script)
          else:
            logger.error(f"No fallback script provided for LLM failure. Task may be incomplete.")
      else:
        logger.warning(f"Unknown action operation {op}")

    notes = "Executed scripted actions" if actions else "No actions provided; task recorded only."
    return {
        "task_id": metadata.get("task_id"),
        "status": "completed",
        "notes": notes,
        "files_touched": files_touched,
    }


