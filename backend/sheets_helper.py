import os, json, gspread
from gspread.exceptions import WorksheetNotFound
from oauth2client.service_account import ServiceAccountCredentials

sheet_id = os.getenv("GOOGLE_SHEETS_ID")
creds_json = os.getenv("GOOGLE_SHEETS_CREDENTIALS")

if creds_json and sheet_id:
    scope = [
        "https://spreadsheets.google.com/feeds",
        "https://www.googleapis.com/auth/drive",
    ]
    creds = ServiceAccountCredentials.from_json_keyfile_dict(
        json.loads(creds_json), scope
    )
    gc = gspread.authorize(creds)
    sheet = gc.open_by_key(sheet_id)
else:
    sheet = None


def _ensure_tasks_ws():
    """Возвращает worksheet Tasks, создаёт при отсутствии."""
    if not sheet:
        return None
    try:
        return sheet.worksheet("Tasks")
    except WorksheetNotFound:
        ws = sheet.add_worksheet(title="Tasks", rows=200, cols=6)
        ws.append_row(
            ["ID", "Title", "Description", "DueDate", "Completed", "Frozen"]
        )
        print("Worksheet 'Tasks' auto-created.")
        return ws


def load_tasks():
    ws = _ensure_tasks_ws()
    return ws.get_all_records() if ws else []


def append_task(task: dict):
    ws = _ensure_tasks_ws()
    if ws:
        ws.append_row(
            [
                task["id"],
                task["title"],
                task["description"],
                task["dueDate"],
                False,
                False,
            ]
        )
