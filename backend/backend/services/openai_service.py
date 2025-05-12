"""Unified gateway to OpenAI Chat completions."""
from __future__ import annotations

import os
from typing import List

import openai

from models import Task


class OpenAIService:
    """Thin wrapper over openai.ChatCompletion."""

    def __init__(self, model: str | None = None) -> None:
        api_key = os.getenv("OPENAI_API_KEY")
        if not api_key:
            raise RuntimeError("OPENAI_API_KEY env var is missing")

        openai.api_key = api_key
        self.model = model or os.getenv("OPENAI_MODEL", "gpt-3.5-turbo")

    # ---------------- private helpers -------------------------------
    def _chat(self, system: str, user: str, temperature: float = 0.7) -> str:
        response = openai.ChatCompletion.create(
            model=self.model,
            messages=[
                {"role": "system", "content": system},
                {"role": "user", "content": user},
            ],
            temperature=temperature,
        )
        return response.choices[0].message.content.strip()

    # ---------------- public API ------------------------------------
    def generate_day_plan(self, tasks: List[Task]) -> str:
        bullet_list = "\n".join(
            f"- {t.title} (до {t.due.strftime('%d.%m') if t.due else 'когда-нибудь'})"
            for t in tasks
            if not t.completed
        ) or "(нет активных задач)"
        prompt = (
            "Составь краткий, прагматичный план на сегодняшний день, учитывая приоритеты "
            "и ближайшие сроки. Формат: 1) Время — Действие. Максимум 5–7 пунктов.\n\n"
            + bullet_list
        )
        return self._chat("Ты опытный помощник по тайм‑менеджменту.", prompt)

    def suggest_tasks(self, idea: str, k: int = 5) -> List[str]:
        prompt = f"Предложи {k} конкретных коротких задач, связанных с: {idea}. Выдай маркированный список."
        raw = self._chat("Ты генератор идей по личной продуктивности.", prompt)
        return [ln.lstrip("-•* ").strip() for ln in raw.splitlines() if ln.strip()]
