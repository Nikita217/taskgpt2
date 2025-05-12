"""Google Sheets repository layer."""
from __future__ import annotations

import os
import uuid
from datetime import date, datetime, timedelta
from typing import List, Dict, Any

import gspread
from google.oauth2.service_account import Credentials

from models import Achievement, Task

DATE_FMT = "%Y-%m-%d"
_CACHE_TTL = timedelta(seconds=30)


class SheetsRepository:
    """CRUD operations backed by Google Sheets."""

    def __init__(self) -> None:
        creds_file = os.getenv("GOOGLE_CREDENTIALS_JSON")
        if not creds_file:
            raise RuntimeError("GOOGLE_CREDENTIALS_JSON env var is missing")

        creds = Credentials.from_service_account_file(creds_file)
        client = gspread.authorize(creds)
        self.sheet = client.open_by_key(os.getenv("GOOGLE_SHEETS_ID"))
        self.tasks_ws = self._ensure_ws(
            "Tasks",
            ["id", "title", "description", "due", "completed"],
        )
        self.ach_ws = self._ensure_ws(
            "Achievements",
            ["id", "text", "earned_at"],
        )

        self._cache: Dict[str, tuple[datetime, List[Any]]] = {}

    # -------------- caching helpers ---------------------------------
    def _get_cached(self, key: str):
        if key in self._cache:
            ts, value = self._cache[key]
            if datetime.utcnow() - ts < _CACHE_TTL:
                return value
            del self._cache[key]
        return None

    def _set_cache(self, key: str, value):
        self._cache[key] = (datetime.utcnow(), value)

    # -------------- public API --------------------------------------
    def list_tasks(self) -> List[Task]:
        cached = self._get_cached("tasks")
        if cached is not None:
            return cached
        records = self.tasks_ws.get_all_records()
        tasks = [self._row_to_task(r) for r in records]
        self._set_cache("tasks", tasks)
        return tasks

    def create_task(self, title: str, description: str = "", due: str | None = None) -> Task:
        new_task = Task(id=str(uuid.uuid4()), title=title, description=description, due=self._parse_date(due), completed=False)
        self.tasks_ws.append_row(self._task_to_row(new_task))
        self._invalidate_cache("tasks")
        return new_task

    def update_task(self, task: Task) -> Task:
        cell = self.tasks_ws.find(task.id)
        self.tasks_ws.update(f"A{cell.row}:E{cell.row}", [self._task_to_row(task)])
        self._invalidate_cache("tasks")
        return task

    def delete_task(self, task_id: str) -> None:
        cell = self.tasks_ws.find(task_id)
        self.tasks_ws.delete_row(cell.row)
        self._invalidate_cache("tasks")

    def list_achievements(self) -> List[Achievement]:
        cached = self._get_cached("ach")
        if cached is not None:
            return cached
        records = self.ach_ws.get_all_records()
        achs = [
            Achievement(
                id=r["id"],
                text=r["text"],
                earned_at=datetime.strptime(r["earned_at"], DATE_FMT).date(),
            )
            for r in records
        ]
        self._set_cache("ach", achs)
        return achs

    # -------------- internal helpers --------------------------------
    def _ensure_ws(self, title: str, header: List[str]):
        try:
            ws = self.sheet.worksheet(title)
        except gspread.WorksheetNotFound:
            ws = self.sheet.add_worksheet(title, rows=1000, cols=len(header))
            ws.append_row(header)
        return ws

    @staticmethod
    def _row_to_task(r: dict) -> Task:
        return Task(
            id=r["id"],
            title=r["title"],
            description=r["description"],
            due=datetime.strptime(r["due"], DATE_FMT).date() if r["due"] else None,
            completed=str(r["completed"]).lower() in {"true", "1", "yes"},
        )

    @staticmethod
    def _task_to_row(t: Task):
        return [
            t.id,
            t.title,
            t.description,
            t.due.strftime(DATE_FMT) if t.due else "",
            str(t.completed).upper(),
        ]

    @staticmethod
    def _parse_date(date_str: str | None) -> date | None:
        if not date_str:
            return None
        return datetime.strptime(date_str, DATE_FMT).date()

    def _invalidate_cache(self, key: str):
        self._cache.pop(key, None)
