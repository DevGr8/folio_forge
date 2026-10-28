-- Normalized SQLite Schema for AI-Powered Portfolio Database (10 Core Categories)
PRAGMA foreign_keys = ON;

CREATE TABLE IF NOT EXISTS personal_info (
    id TEXT PRIMARY KEY,
    full_name TEXT NOT NULL,
    email TEXT NOT NULL,
    phone TEXT,
    location TEXT,
    linkedin_url TEXT,
    github_url TEXT,
    portfolio_url TEXT,
    base_title TEXT
);

CREATE TABLE IF NOT EXISTS career_summaries (
    id TEXT PRIMARY KEY,
    user_id TEXT NOT NULL REFERENCES personal_info(id) ON DELETE CASCADE,
    title_variant TEXT NOT NULL,
    is_default BOOLEAN DEFAULT 0,
    summary_text TEXT NOT NULL
);

CREATE TABLE IF NOT EXISTS education (
    id TEXT PRIMARY KEY,
    user_id TEXT NOT NULL REFERENCES personal_info(id) ON DELETE CASCADE,
    institution TEXT NOT NULL,
    degree TEXT NOT NULL,
    field_of_study TEXT,
    start_date TEXT,
    end_date TEXT,
    gpa_or_grade TEXT,
    highlights TEXT
);

CREATE TABLE IF NOT EXISTS skills (
    id TEXT PRIMARY KEY,
    user_id TEXT NOT NULL REFERENCES personal_info(id) ON DELETE CASCADE,
    category TEXT NOT NULL,
    skill_name TEXT NOT NULL,
    proficiency_level TEXT,
    years_experience REAL,
    jd_tags TEXT
);

CREATE TABLE IF NOT EXISTS certifications (
    id TEXT PRIMARY KEY,
    user_id TEXT NOT NULL REFERENCES personal_info(id) ON DELETE CASCADE,
    name TEXT NOT NULL,
    issuing_organization TEXT NOT NULL,
    issue_date TEXT,
    expiry_date TEXT,
    credential_id TEXT,
    credential_url TEXT,
    focus_area TEXT
);

CREATE TABLE IF NOT EXISTS projects (
    id TEXT PRIMARY KEY,
    user_id TEXT NOT NULL REFERENCES personal_info(id) ON DELETE CASCADE,
    title TEXT NOT NULL,
    role TEXT,
    tech_stack TEXT,
    start_date TEXT,
    end_date TEXT,
    description_bullets TEXT NOT NULL, -- JSON array
    repo_url TEXT,
    live_url TEXT,
    key_metrics TEXT,
    domain_tag TEXT
);

CREATE TABLE IF NOT EXISTS experience (
    id TEXT PRIMARY KEY,
    user_id TEXT NOT NULL REFERENCES personal_info(id) ON DELETE CASCADE,
    role_title TEXT NOT NULL,
    company TEXT NOT NULL,
    employment_type TEXT,
    location TEXT,
    start_date TEXT,
    end_date TEXT,
    achievements_bullets TEXT NOT NULL, -- JSON array
    technologies_used TEXT,
    domain_tag TEXT
);

CREATE TABLE IF NOT EXISTS achievements (
    id TEXT PRIMARY KEY,
    user_id TEXT NOT NULL REFERENCES personal_info(id) ON DELETE CASCADE,
    title TEXT NOT NULL,
    issuer_or_event TEXT,
    date_awarded TEXT,
    description TEXT
);

CREATE TABLE IF NOT EXISTS publications_activities (
    id TEXT PRIMARY KEY,
    user_id TEXT NOT NULL REFERENCES personal_info(id) ON DELETE CASCADE,
    item_type TEXT NOT NULL,
    title TEXT NOT NULL,
    venue_or_publisher TEXT,
    publication_date TEXT,
    url TEXT,
    summary TEXT
);

CREATE TABLE IF NOT EXISTS languages_competencies (
    id TEXT PRIMARY KEY,
    user_id TEXT NOT NULL REFERENCES personal_info(id) ON DELETE CASCADE,
    category TEXT NOT NULL,
    name TEXT NOT NULL,
    proficiency TEXT
);
