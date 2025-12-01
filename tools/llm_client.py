"""Wrapper around OpenAI-compatible chat completion API."""

from __future__ import annotations

import os
from pathlib import Path

from dotenv import load_dotenv
from loguru import logger
from openai import OpenAI

ENV_PATH = Path(__file__).resolve().parents[1] / ".env"
if ENV_PATH.exists():
  load_dotenv(ENV_PATH)


class LLMClient:
  name = "llm_client"

  def __init__(self) -> None:
    api_key = os.getenv("OPENAI_API_KEY")
    base_url = os.getenv("OPENAI_BASE_URL", "https://api.openai.com/v1")
    if not api_key:
      raise RuntimeError("OPENAI_API_KEY not set in .env")
    self.model = os.getenv("OPENAI_MODEL", "gpt-4o-mini").strip()
    self.client = OpenAI(api_key=api_key, base_url=base_url)
    logger.info(f"LLMClient initialized with model: {self.model}, base_url: {base_url}")

  def run(self, prompt: str) -> str:
    logger.info(f"🤖 Calling LLM ({self.model}) with prompt length: {len(prompt)} chars")
    try:
      response = self.client.chat.completions.create(
          model=self.model,
          temperature=0.2,
          messages=[
              {"role": "system", "content": "You output valid JSON arrays of arXiv CS paper metadata."},
              {"role": "user", "content": prompt},
          ],
      )
      content = response.choices[0].message.content
      logger.info(f"✅ LLM call successful. Response length: {len(content)} chars")
      return content
    except Exception as e:
      logger.error(f"❌ LLM call failed: {type(e).__name__}: {e}")
      raise


