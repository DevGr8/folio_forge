"""
FastAPI Backend Server for AI-Powered Portfolio Database & Dynamic Resume Generator
Run locally with:
    pip install -r requirements.txt
    python seed_data.py
    uvicorn app:app --reload --port 8000
"""
import os
import json
import sqlite3
from typing import Dict, Any, List, Optional
from fastapi import FastAPI, HTTPException
from fastapi.responses import FileResponse, HTMLResponse
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

from seed_data import PORTFOLIO_DATA, SAMPLE_JDS, init_and_seed_db, DB_PATH
from gemini_service import analyze_jd_with_gemini
from sheets_sync import sync_portfolio_to_google_sheets, DEFAULT_SHEET_URL
from resume_builder import build_tailored_docx

app = FastAPI(
    title="AI-Powered Portfolio Database & Dynamic Resume Generator",
    version="1.0.0",
    description="Centralized SQLite + Google Sheets Portfolio Database with Gemini 2.5 Flash JD Analysis and Dynamic PDF/DOCX Resume Generation."
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)


class JDAnalyzeRequest(BaseModel):
    jd_text: str


class ResumeGenerateRequest(BaseModel):
    target_role_title: str
    custom_summary: str
    selected_ids: Dict[str, List[str]]
    format: str = "docx"


@app.on_event("startup")
def on_startup():
    if not os.path.exists(DB_PATH):
        init_and_seed_db()



@app.get("/", response_class=HTMLResponse)
def serve_dashboard():
    """Serves the interactive Portfolio Database & Dynamic Resume Generator UI at http://localhost:8000"""
    index_path = os.path.join(os.path.dirname(__file__), "static", "index.html")
    with open(index_path, "r", encoding="utf-8") as f:
        return f.read()


@app.get("/api/portfolio")
def get_full_portfolio():
    """Returns all 10 categories of portfolio records and live Google Sheet metadata."""
    return {
        "portfolio": PORTFOLIO_DATA,
        "sample_jds": SAMPLE_JDS,
        "google_sheet_url": DEFAULT_SHEET_URL
    }


@app.post("/api/analyze-jd")
def analyze_job_description(req: JDAnalyzeRequest):
    """Analyzes a Job Description using Gemini API and matches verified portfolio IDs."""
    if not req.jd_text.strip():
        raise HTTPException(status_code=400, detail="Job description text cannot be empty.")
    return analyze_jd_with_gemini(PORTFOLIO_DATA, req.jd_text)


@app.post("/api/sync-sheets")
def trigger_sheets_sync():
    """Synchronizes all 10 SQLite tables to the 10-tab Google Sheet."""
    return sync_portfolio_to_google_sheets(PORTFOLIO_DATA)


@app.post("/api/export-resume")
def export_tailored_resume(req: ResumeGenerateRequest):
    """Generates and returns a tailored DOCX resume from the user's selected record IDs."""
    out_file = os.path.join("exports", "Tailored_Resume_Aarav_Mehta.docx")
    os.makedirs("exports", exist_ok=True)
    build_tailored_docx(
        portfolio=PORTFOLIO_DATA,
        selected_ids=req.selected_ids,
        target_role_title=req.target_role_title,
        custom_summary=req.custom_summary,
        output_path=out_file
    )
    return FileResponse(
        out_file,
        media_type="application/vnd.openxmlformats-officedocument.wordprocessingml.document",
        filename="Tailored_Resume_Aarav_Mehta.docx"
    )
