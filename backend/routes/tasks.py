"""Tasks API endpoints."""
from flask import Blueprint, jsonify, request

from models import Task
from services.sheets_service import SheetsRepository

repo = SheetsRepository()
tasks_bp = Blueprint("tasks", __name__)


@tasks_bp.get("/")
def list_tasks():
    return jsonify([t.__dict__ for t in repo.list_tasks()])


@tasks_bp.post("/")
def create_task():
    data = request.get_json(force=True)
    new_task = repo.create_task(
        title=data["title"],
        description=data.get("description", ""),
        due=data.get("due"),
    )
    return jsonify(new_task.__dict__), 201


@tasks_bp.patch("/<task_id>")
def patch_task(task_id: str):
    data = request.get_json(force=True)
    tasks = {t.id: t for t in repo.list_tasks()}
    if task_id not in tasks:
        return jsonify({"error": "not found"}), 404

    t: Task = tasks[task_id]
    t.title = data.get("title", t.title)
    t.description = data.get("description", t.description)
    t.completed = data.get("completed", t.completed)
    if "due" in data:
        t.due = repo._parse_date(data["due"])  # type: ignore
    repo.update_task(t)
    return jsonify(t.__dict__)


@tasks_bp.delete("/<task_id>")
def delete_task(task_id: str):
    repo.delete_task(task_id)
    return "", 204
