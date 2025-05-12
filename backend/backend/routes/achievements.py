"""Achievements endpoint."""
from flask import Blueprint, jsonify

from services.sheets_service import SheetsRepository

repo = SheetsRepository()
achievements_bp = Blueprint("achievements", __name__)


@achievements_bp.get("/")
def list_achievements():
    return jsonify([a.__dict__ for a in repo.list_achievements()])
