"""Domain models for tasks and achievements."""
from __future__ import annotations

from dataclasses import dataclass
from datetime import date
from typing import Optional


@dataclass
class Task:
    id: str
    title: str
    description: str
    due: Optional[date]
    completed: bool = False


@dataclass
class Achievement:
    id: str
    text: str
    earned_at: date
