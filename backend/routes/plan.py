"""Day plan endpoint."""
from flask import Blueprint, jsonify

from services.openai_service import OpenAIService
from services.sheets_service import SheetsRepository

repo = SheetsRepository()
ai = OpenAIService()
plan_bp = Blueprint("plan", __name__)


@plan_bp.get("/plan")
def get_day_plan():
    plan_text = ai.generate_day_plan(repo.list_tasks())
    return jsonify({"plan": plan_text})
