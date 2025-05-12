import os, gspread, json
from oauth2client.service_account import ServiceAccountCredentials

sheet_id = os.getenv('GOOGLE_SHEETS_ID')
creds_json = os.getenv('GOOGLE_SHEETS_CREDENTIALS')
if creds_json:
    creds_dict = json.loads(creds_json)
    scope = ['https://spreadsheets.google.com/feeds','https://www.googleapis.com/auth/drive']
    creds = ServiceAccountCredentials.from_json_keyfile_dict(creds_dict, scope)
    gc = gspread.authorize(creds)
    sheet = gc.open_by_key(sheet_id)
else:
    sheet = None

def load_tasks():
    if not sheet: return []
    ws = sheet.worksheet('Tasks')
    return ws.get_all_records()

def append_task(task):
    if not sheet: return
    ws = sheet.worksheet('Tasks')
    ws.append_row([task['id'],task['title'],task['description'],task['dueDate'],False,False])

def load_achievements():
    if not sheet: return []
    return sheet.worksheet('Achievements').get_all_records()
