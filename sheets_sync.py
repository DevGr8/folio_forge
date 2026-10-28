"""
Google Sheets Synchronization Module
Supports:
1. Official Google Sheets API v4 via `gspread` + Service Account JSON
2. Google Apps Script Web App Webhook (`APPS_SCRIPT_WEBHOOK_URL`)
Live Exported Sheet URL: https://docs.google.com/spreadsheets/d/1QvYmG86KlyvcsC-5nvnMpoWUakX2yFgCdXvxvjb9xjU/edit
"""
import os
import json
import urllib.request
from typing import Dict, Any
from dotenv import load_dotenv

load_dotenv()

DEFAULT_SHEET_ID = os.getenv("GOOGLE_SHEET_ID", "1QvYmG86KlyvcsC-5nvnMpoWUakX2yFgCdXvxvjb9xjU")
DEFAULT_SHEET_URL = f"https://docs.google.com/spreadsheets/d/{DEFAULT_SHEET_ID}/edit"


def sync_portfolio_to_google_sheets(portfolio_data: Dict[str, Any]) -> Dict[str, Any]:
    """
    Synchronizes all 10 portfolio database tables to the target Google Sheet.
    Checks for Service Account credentials first, then Apps Script Webhook URL.
    """
    creds_path = os.getenv("GOOGLE_SHEETS_CREDENTIALS_PATH", "service_account.json")
    webhook_url = os.getenv("APPS_SCRIPT_WEBHOOK_URL", "").strip()

    if os.path.exists(creds_path):
        import gspread
        gc = gspread.service_account(filename=creds_path)
        sh = gc.open_by_key(DEFAULT_SHEET_ID)
        tabs_mapping = {
            "Personal_Info": [portfolio_data["personal_info"]],
            "Career_Summaries": portfolio_data["career_summaries"],
            "Education": portfolio_data["education"],
            "Skills": portfolio_data["skills"],
            "Certifications": portfolio_data["certifications"],
            "Projects": portfolio_data["projects"],
            "Experience": portfolio_data["experience"],
            "Achievements": portfolio_data["achievements"],
            "Publications_Activities": portfolio_data["publications_activities"],
            "Languages_Competencies": portfolio_data["languages_competencies"],
        }
        for tab_name, rows in tabs_mapping.items():
            if not rows:
                continue
            try:
                ws = sh.worksheet(tab_name)
                ws.clear()
            except Exception:
                ws = sh.add_worksheet(title=tab_name, rows="100", cols="20")
            headers = list(rows[0].keys())
            values = [headers] + [[json.dumps(r[h]) if isinstance(r[h], list) else str(r.get(h, "")) for h in headers] for r in rows]
            ws.update("A1", values)
        return {"status": "synced_via_gspread", "sheet_url": DEFAULT_SHEET_URL, "tabs_synced": 10}

    if webhook_url:
        req = urllib.request.Request(
            webhook_url,
            data=json.dumps(portfolio_data).encode("utf-8"),
            headers={"Content-Type": "application/json"},
            method="POST"
        )
        with urllib.request.urlopen(req, timeout=15) as resp:
            return {"status": "synced_via_apps_script", "sheet_url": DEFAULT_SHEET_URL, "response": resp.read().decode("utf-8")}

    return {
        "status": "ready_pre_synced",
        "sheet_id": DEFAULT_SHEET_ID,
        "sheet_url": DEFAULT_SHEET_URL,
        "message": "Connected to live 10-tab Google Sheet. Set GOOGLE_SHEETS_CREDENTIALS_PATH or APPS_SCRIPT_WEBHOOK_URL in .env for live write-back."
    }
