import json
import os
import sqlite3

DB_PATH = os.getenv("DATABASE_PATH", "portfolio.db")
PORTFOLIO_DATA = {
    "personal_info": {
        "id": "USR-001",
        "full_name": "Aarav Mehta",
        "email": "aarav.mehta.dev@example.com",
        "phone": "+91 98201 54321",
        "location": "Mumbai / Navi Mumbai, Maharashtra, India",
        "linkedin_url": "https://linkedin.com/in/aaravmehta-ai",
        "github_url": "https://github.com/aaravmehta-dev",
        "portfolio_url": "https://aaravmehta.dev",
        "base_title": "Full-Stack & AI/ML Software Engineer"
    },
    "career_summaries": [
        {
            "id": "SUM-01",
            "user_id": "USR-001",
            "title_variant": "General Full-Stack & AI Engineer",
            "is_default": True,
            "summary_text": "Software and AI Engineer with 3+ years of experience (including full-time and intensive industry internships) building production LLM pipelines, RAG architectures, and cloud-native React/FastAPI web applications. Proven track record of reducing inference latency by 42% and scaling microservices to 150K+ monthly active users."
        },
        {
            "id": "SUM-02",
            "user_id": "USR-001",
            "title_variant": "AI / Machine Learning Engineer (NLP & GenAI Systems)",
            "is_default": False,
            "summary_text": "AI/ML Engineer specializing in Retrieval-Augmented Generation (RAG), Google Gemini & Transformer fine-tuning, and low-latency vector search pipelines. Experienced in deploying deterministic, citation-grounded LLM workflows with Python, PyTorch, LangChain, ChromaDB, and FastAPI, achieving 91.4% retrieval precision and 63% latency reduction on enterprise knowledge bases."
        },
        {
            "id": "SUM-03",
            "user_id": "USR-001",
            "title_variant": "Full-Stack Cloud & Distributed Systems Engineer",
            "is_default": False,
            "summary_text": "Full-Stack Software Engineer skilled in architecting scalable multi-tenant web platforms using React 18, Next.js, TypeScript, Python (FastAPI), Node.js, PostgreSQL, and Docker on AWS and Google Cloud. Delivered high-throughput REST/WebSocket APIs handling 12,000+ req/min at 99.96% uptime with automated CI/CD and bi-directional Google Sheets synchronization."
        }
    ],
    "education": [
        {
            "id": "EDU-01",
            "user_id": "USR-001",
            "institution": "Veermata Jijabai Technological Institute (VJTI), Mumbai",
            "degree": "Bachelor of Technology (B.Tech)",
            "field_of_study": "Computer Engineering (Honors Minor in Artificial Intelligence)",
            "start_date": "Aug 2020",
            "end_date": "May 2024",
            "gpa_or_grade": "9.32 / 10.0 CGPA",
            "highlights": "Dean's Merit List (All 8 Semesters); Lead of AI & Robotics Society; Coursework: Deep Learning, NLP, Distributed Systems, DBMS, Algorithms"
        },
        {
            "id": "EDU-02",
            "user_id": "USR-001",
            "institution": "DAV Public School, New Panvel",
            "degree": "Higher Secondary Certificate (CBSE Class XII)",
            "field_of_study": "Physics, Chemistry, Mathematics & Computer Science",
            "start_date": "Jun 2018",
            "end_date": "May 2020",
            "gpa_or_grade": "96.4%",
            "highlights": "School Topper in Computer Science (99/100); National Science Olympiad Gold Medalist"
        }
    ],
    "skills": [
        {
            "id": "SKL-01",
            "category": "Programming Languages",
            "skill_name": "Python",
            "proficiency_level": "Expert",
            "years_experience": 4.5,
            "jd_tags": [
                "AI",
                "ML",
                "Backend",
                "FullStack"
            ]
        },
        {
            "id": "SKL-02",
            "category": "Programming Languages",
            "skill_name": "TypeScript & JavaScript (ES6+)",
            "proficiency_level": "Advanced",
            "years_experience": 3.5,
            "jd_tags": [
                "FullStack",
                "Frontend",
                "Web",
                "Backend"
            ]
        },
        {
            "id": "SKL-03",
            "category": "Programming Languages",
            "skill_name": "SQL (PostgreSQL, SQLite)",
            "proficiency_level": "Advanced",
            "years_experience": 3.5,
            "jd_tags": [
                "Backend",
                "FullStack",
                "Data",
                "AI"
            ]
        },
        {
            "id": "SKL-04",
            "category": "Programming Languages",
            "skill_name": "C++ & Go",
            "proficiency_level": "Intermediate",
            "years_experience": 2.0,
            "jd_tags": [
                "Backend",
                "Systems"
            ]
        },
        {
            "id": "SKL-05",
            "category": "AI & Machine Learning",
            "skill_name": "Google Gemini API & Vertex AI (Structured Outputs)",
            "proficiency_level": "Expert",
            "years_experience": 2.0,
            "jd_tags": [
                "AI",
                "ML",
                "LLM",
                "GenAI"
            ]
        },
        {
            "id": "SKL-06",
            "category": "AI & Machine Learning",
            "skill_name": "PyTorch & Hugging Face Transformers",
            "proficiency_level": "Advanced",
            "years_experience": 2.5,
            "jd_tags": [
                "AI",
                "ML",
                "NLP",
                "DeepLearning"
            ]
        },
        {
            "id": "SKL-07",
            "category": "AI & Machine Learning",
            "skill_name": "RAG Pipelines (LangChain, LlamaIndex, FAISS, ChromaDB)",
            "proficiency_level": "Expert",
            "years_experience": 2.0,
            "jd_tags": [
                "AI",
                "ML",
                "LLM",
                "NLP"
            ]
        },
        {
            "id": "SKL-08",
            "category": "AI & Machine Learning",
            "skill_name": "Scikit-Learn, Pandas, NumPy & OpenCV",
            "proficiency_level": "Advanced",
            "years_experience": 3.5,
            "jd_tags": [
                "AI",
                "ML",
                "Data"
            ]
        },
        {
            "id": "SKL-09",
            "category": "Web & Backend Frameworks",
            "skill_name": "FastAPI & Flask (Async Microservices)",
            "proficiency_level": "Expert",
            "years_experience": 3.5,
            "jd_tags": [
                "Backend",
                "FullStack",
                "AI",
                "API"
            ]
        },
        {
            "id": "SKL-10",
            "category": "Web & Backend Frameworks",
            "skill_name": "React.js 18, Next.js 14 & Tailwind CSS",
            "proficiency_level": "Advanced",
            "years_experience": 3.0,
            "jd_tags": [
                "Frontend",
                "FullStack",
                "Web"
            ]
        },
        {
            "id": "SKL-11",
            "category": "Web & Backend Frameworks",
            "skill_name": "Node.js, Express & REST/WebSocket APIs",
            "proficiency_level": "Advanced",
            "years_experience": 2.5,
            "jd_tags": [
                "Backend",
                "FullStack",
                "Web"
            ]
        },
        {
            "id": "SKL-12",
            "category": "Cloud & DevOps",
            "skill_name": "Docker, Kubernetes & GitHub Actions CI/CD",
            "proficiency_level": "Advanced",
            "years_experience": 2.5,
            "jd_tags": [
                "Cloud",
                "DevOps",
                "FullStack",
                "AI"
            ]
        },
        {
            "id": "SKL-13",
            "category": "Cloud & DevOps",
            "skill_name": "AWS (ECS, EC2, S3, RDS) & Google Cloud Run",
            "proficiency_level": "Advanced",
            "years_experience": 2.5,
            "jd_tags": [
                "Cloud",
                "FullStack",
                "Backend",
                "AI"
            ]
        },
        {
            "id": "SKL-14",
            "category": "Cloud & DevOps",
            "skill_name": "Redis Caching & Celery Distributed Queues",
            "proficiency_level": "Advanced",
            "years_experience": 2.0,
            "jd_tags": [
                "Backend",
                "FullStack",
                "AI"
            ]
        },
        {
            "id": "SKL-15",
            "category": "Soft Skills",
            "skill_name": "Cross-Functional Technical Communication",
            "proficiency_level": "Expert",
            "years_experience": 3.5,
            "jd_tags": [
                "SoftSkill",
                "Leadership"
            ]
        },
        {
            "id": "SKL-16",
            "category": "Soft Skills",
            "skill_name": "Agile Sprint Planning & Code Review Mentorship",
            "proficiency_level": "Advanced",
            "years_experience": 2.5,
            "jd_tags": [
                "SoftSkill",
                "Leadership"
            ]
        }
    ],
    "certifications": [
        {
            "id": "CRT-01",
            "name": "Google Cloud Certified \u2014 Professional Machine Learning Engineer",
            "issuing_organization": "Google Cloud",
            "issue_date": "Apr 2025",
            "expiry_date": "Apr 2027",
            "credential_id": "GCP-PMLE-884120",
            "credential_url": "https://cloud.google.com/certification/machine-learning-engineer",
            "focus_area": "AI/ML"
        },
        {
            "id": "CRT-02",
            "name": "AWS Certified Developer \u2014 Associate",
            "issuing_organization": "Amazon Web Services (AWS)",
            "issue_date": "Nov 2024",
            "expiry_date": "Nov 2027",
            "credential_id": "AWS-DVA-552910",
            "credential_url": "https://aws.amazon.com/certification/certified-developer-associate/",
            "focus_area": "Full-Stack"
        },
        {
            "id": "CRT-03",
            "name": "Generative AI with Large Language Models Specialization",
            "issuing_organization": "DeepLearning.AI & AWS",
            "issue_date": "Jun 2024",
            "expiry_date": "No Expiry",
            "credential_id": "DLAI-LLM-339104",
            "credential_url": "https://www.deeplearning.ai/courses/generative-ai-with-llms/",
            "focus_area": "AI/ML"
        },
        {
            "id": "CRT-04",
            "name": "Meta Front-End & Full-Stack Developer Professional Certificate",
            "issuing_organization": "Meta (Coursera)",
            "issue_date": "Sep 2023",
            "expiry_date": "No Expiry",
            "credential_id": "META-FS-771209",
            "credential_url": "https://www.coursera.org/professional-certificates/meta-front-end-developer",
            "focus_area": "Full-Stack"
        }
    ],
    "projects": [
        {
            "id": "PRJ-01",
            "title": "DocuPulse AI \u2014 Multi-Modal Enterprise RAG & Citation Engine",
            "role": "Lead AI Architect",
            "tech_stack": "Python, Gemini 2.5 API, FastAPI, ChromaDB, PyTorch, React, Docker",
            "start_date": "Aug 2025",
            "end_date": "Feb 2026",
            "description_bullets": [
                "Architected a zero-hallucination Retrieval-Augmented Generation (RAG) engine indexing 50,000+ technical PDFs with hybrid BM25 + dense vector embeddings.",
                "Implemented strict primary-key citation verification using Gemini Structured Outputs, reducing unsupported claims from 14.0% to under 0.8%.",
                "Optimized async FastAPI inference endpoints with Redis semantic caching, cutting p95 query latency from 3.8s to 1.4s (63% reduction)."
            ],
            "repo_url": "https://github.com/aaravmehta-dev/docupulse-rag",
            "live_url": "https://docupulse-demo.aaravmehta.dev",
            "key_metrics": "91.4% retrieval accuracy; 63% latency reduction",
            "domain_tag": "AI/ML"
        },
        {
            "id": "PRJ-02",
            "title": "FinScale Cloud \u2014 Real-Time Multi-Tenant Expense & Analytics SaaS",
            "role": "Full-Stack Lead",
            "tech_stack": "React 18, TypeScript, Next.js, Python FastAPI, PostgreSQL, Redis, Docker, AWS ECS",
            "start_date": "Jan 2025",
            "end_date": "Jul 2025",
            "description_bullets": [
                "Built a multi-tenant financial analytics SaaS supporting role-based access control (RBAC), real-time WebSocket dashboard updates, and automated CSV/Google Sheets reconciliation.",
                "Designed a normalized PostgreSQL schema with composite indexing and SQLAlchemy async sessions, handling 12,000+ requests/min at 99.96% uptime.",
                "Automated CI/CD deployment pipelines via GitHub Actions and Docker multi-stage builds deployed on AWS ECS Fargate."
            ],
            "repo_url": "https://github.com/aaravmehta-dev/finscale-cloud",
            "live_url": "https://finscale.aaravmehta.dev",
            "key_metrics": "12K req/min throughput; 99.96% uptime",
            "domain_tag": "Full-Stack"
        },
        {
            "id": "PRJ-03",
            "title": "MedVision Triage \u2014 Chest X-Ray Anomaly Detection & Clinical Report Generator",
            "role": "ML Researcher",
            "tech_stack": "PyTorch, Hugging Face, Vision-Language Models, FastAPI, OpenCV, SQLite",
            "start_date": "Jan 2024",
            "end_date": "Jun 2024",
            "description_bullets": [
                "Trained an ensemble DenseNet-121 and Vision-Language pipeline on 112,000+ NIH ChestX-ray images achieving 0.894 macro AUROC across 14 thoracic pathologies.",
                "Built a clinician-in-the-loop FastAPI web interface that generates structured radiology draft reports with Grad-CAM visual explainability heatmaps."
            ],
            "repo_url": "https://github.com/aaravmehta-dev/medvision-triage",
            "live_url": "https://medvision.aaravmehta.dev",
            "key_metrics": "0.894 AUROC across 14 pathologies",
            "domain_tag": "AI/ML"
        },
        {
            "id": "PRJ-04",
            "title": "SyncFlow \u2014 Collaborative Kanban & Automated Google Sheets Workflow Bridge",
            "role": "Full-Stack Developer",
            "tech_stack": "TypeScript, Node.js, Express, React, Tailwind CSS, Google Sheets API v4, WebSockets",
            "start_date": "Jul 2023",
            "end_date": "Dec 2023",
            "description_bullets": [
                "Developed a real-time project management board with bi-directional Google Sheets API v4 webhook synchronization for non-technical operations teams.",
                "Implemented optimistic UI updates, drag-and-drop state persistence, and OAuth2 token rotation supporting 1,800+ active student and startup users."
            ],
            "repo_url": "https://github.com/aaravmehta-dev/syncflow-sheets",
            "live_url": "https://syncflow.aaravmehta.dev",
            "key_metrics": "1,800+ active users; <120ms sync latency",
            "domain_tag": "Full-Stack"
        }
    ],
    "experience": [
        {
            "id": "EXP-01",
            "role_title": "Software & AI Systems Engineer",
            "company": "NexaCloud Technologies Pvt. Ltd.",
            "employment_type": "Full-Time",
            "location": "Mumbai, India",
            "start_date": "Jul 2024",
            "end_date": "Present",
            "achievements_bullets": [
                "Engineered production LLM microservice pipelines using Google Gemini API, Python, and FastAPI to automate customer ticket triage and contract extraction for 85+ enterprise clients.",
                "Reduced average ticket resolution time by 48% and saved 1,200+ manual review hours per month through schema-enforced AI extraction workflows.",
                "Built interactive React + TypeScript analytics dashboards and PostgreSQL audit logs with automated Google Sheets reporting exports.",
                "Mentored 4 junior developers on async Python patterns, unit testing (Pytest), and Docker containerization."
            ],
            "technologies_used": "Python, FastAPI, Gemini API, React, TypeScript, PostgreSQL, Docker, Redis, AWS",
            "domain_tag": "Both"
        },
        {
            "id": "EXP-02",
            "role_title": "Machine Learning Engineering Intern",
            "company": "Quantiphi Analytics",
            "employment_type": "Internship",
            "location": "Mumbai, India",
            "start_date": "Jan 2024",
            "end_date": "Jun 2024",
            "achievements_bullets": [
                "Developed domain-specific Named Entity Recognition (NER) and document classification models using PyTorch and Hugging Face Transformers with 93.2% F1-score.",
                "Built automated data ingestion and evaluation pipelines processing 250GB+ of unstructured financial PDFs and earnings transcripts.",
                "Collaborated with MLOps engineers to containerize inference services on Google Cloud Run, cutting cloud compute costs by 27%."
            ],
            "technologies_used": "Python, PyTorch, Hugging Face, GCP Cloud Run, Docker, SQL",
            "domain_tag": "AI/ML"
        },
        {
            "id": "EXP-03",
            "role_title": "Full-Stack Software Engineering Intern",
            "company": "RazorpayX Partner Labs (FinTech Cohort)",
            "employment_type": "Internship",
            "location": "Bengaluru, India (Hybrid)",
            "start_date": "May 2023",
            "end_date": "Aug 2023",
            "achievements_bullets": [
                "Implemented responsive React + Tailwind CSS merchant onboarding flows and RESTful Node.js/FastAPI backend endpoints serving 40,000+ daily sessions.",
                "Optimized slow SQL reporting queries by introducing read replicas and Redis caching, decreasing API response time from 620ms to 145ms (76% faster).",
                "Wrote comprehensive Jest and Pytest integration suites, raising automated test coverage from 64% to 91%."
            ],
            "technologies_used": "React, TypeScript, Node.js, FastAPI, PostgreSQL, Redis, Jest",
            "domain_tag": "Full-Stack"
        }
    ],
    "achievements": [
        {
            "id": "ACH-01",
            "title": "National Winner (1st Place) \u2014 Smart India Hackathon (AI & FinTech Track)",
            "issuer_or_event": "Ministry of Education & AICTE, Government of India",
            "date_awarded": "Dec 2023",
            "description": "Led a 6-member team to build an AI-powered multilingual grievance redressal and document verification platform in 36 hours out of 1,400+ competing teams."
        },
        {
            "id": "ACH-02",
            "title": "Top 15 Global Finalist \u2014 Google GenAI Exchange Hackathon",
            "issuer_or_event": "Google Developer Groups & Startup India",
            "date_awarded": "Sep 2025",
            "description": "Awarded Best Grounded Enterprise RAG Implementation for DocuPulse AI among 4,500+ participants nationwide."
        },
        {
            "id": "ACH-03",
            "title": "Institute Academic Excellence Award (Top 2% of Graduating Batch)",
            "issuer_or_event": "VJTI Mumbai",
            "date_awarded": "May 2024",
            "description": "Recognized for graduating with a 9.32 CGPA and publishing peer-reviewed AI research during undergraduate studies."
        }
    ],
    "publications_activities": [
        {
            "id": "PUB-01",
            "item_type": "Research Paper",
            "title": "Citation-Grounded Retrieval-Augmented Generation for Low-Resource Indian Legal & Financial Documents",
            "venue_or_publisher": "IEEE International Conference on Data Science and Advanced Analytics (ICDSAA)",
            "publication_date": "Apr 2024",
            "url": "https://doi.org/10.1109/ICDSAA.2024.104921",
            "summary": "Proposed a hybrid lexical-semantic chunking and primary-key verification method that reduces LLM hallucination rates by 38% on domain-specific PDFs."
        },
        {
            "id": "PUB-02",
            "item_type": "Technical Speaker & Open-Source Maintainer",
            "title": "Building Deterministic AI Workflows with Gemini Structured Outputs and FastAPI",
            "venue_or_publisher": "Google Developer Group (GDG) Mumbai DevFest",
            "publication_date": "Nov 2025",
            "url": "https://gdgmumbai.dev/talks/gemini-structured-outputs",
            "summary": "Delivered a hands-on workshop to 350+ developers on schema-guided generation, SQLite/Sheets synchronization, and zero-hallucination guardrails."
        }
    ],
    "languages_competencies": [
        {
            "id": "LNG-01",
            "category": "Language",
            "name": "English",
            "proficiency": "Native / Bilingual (TOEFL 114/120)"
        },
        {
            "id": "LNG-02",
            "category": "Language",
            "name": "Hindi",
            "proficiency": "Native / Bilingual"
        },
        {
            "id": "LNG-03",
            "category": "Language",
            "name": "Marathi",
            "proficiency": "Native / Bilingual"
        },
        {
            "id": "LNG-04",
            "category": "Core Competency",
            "name": "System Design & Scalable Microservices",
            "proficiency": "Advanced (REST, WebSockets, Rate Limiting)"
        },
        {
            "id": "LNG-05",
            "category": "Core Competency",
            "name": "AI Safety & Grounded RAG Evaluation",
            "proficiency": "Expert (Zero-Hallucination Prompting, Schema Validation)"
        }
    ]
}
SAMPLE_JDS = {
    "jd_1_ai_ml": {
        "id": "JD-001",
        "title": "AI / Machine Learning Engineer (LLM & RAG Systems)",
        "company": "VertexScale AI Labs",
        "location": "Mumbai / Bengaluru (Hybrid)",
        "jd_text": "Role: AI / Machine Learning Engineer (LLM & RAG Systems)\nCompany: VertexScale AI Labs | Location: Mumbai / Bengaluru (Hybrid)\n\nAbout the Role:\nWe are seeking an AI / Machine Learning Engineer to design, build, and scale enterprise Retrieval-Augmented Generation (RAG) pipelines, multi-modal document understanding workflows, and low-latency LLM inference microservices.\n\nKey Responsibilities:\n- Architect and deploy production LLM applications using Google Gemini API / Vertex AI, LangChain, and vector databases (ChromaDB / FAISS).\n- Enforce strict JSON schema validation and citation grounding to eliminate hallucinations across enterprise financial and legal document corpora.\n- Fine-tune and evaluate PyTorch and Hugging Face Transformer models for Named Entity Recognition (NER) and classification.\n- Build high-performance async Python (FastAPI) inference APIs with Redis caching and containerize services using Docker on Google Cloud Run or AWS.\n\nRequired Qualifications:\n- B.Tech/B.E. in Computer Science, AI, or equivalent with strong academic foundation.\n- Hands-on experience with Python, PyTorch, Hugging Face Transformers, Google Gemini API, and RAG architectures.\n- Proven track record of optimizing inference latency and publishing or building verifiable AI/ML systems.\n- Cloud ML certification (Google Cloud MLE or DeepLearning.AI LLM specialization) is a strong plus.",
        "match_score": 96,
        "matched_keywords": [
            "Python",
            "Google Gemini API",
            "Vertex AI",
            "RAG Architectures",
            "LangChain",
            "ChromaDB",
            "PyTorch",
            "Hugging Face Transformers",
            "NER",
            "FastAPI",
            "Redis Caching",
            "Docker",
            "Google Cloud Run",
            "Citation Grounding",
            "JSON Schema Validation"
        ],
        "missing_keywords": [
            "Rust Tokenizers (Optional)",
            "vLLM Multi-GPU Sharding"
        ],
        "selected_ids": {
            "summary_id": "SUM-02",
            "skill_ids": [
                "SKL-01",
                "SKL-05",
                "SKL-06",
                "SKL-07",
                "SKL-08",
                "SKL-09",
                "SKL-03",
                "SKL-12",
                "SKL-13",
                "SKL-14",
                "SKL-15"
            ],
            "experience_ids": [
                "EXP-01",
                "EXP-02"
            ],
            "project_ids": [
                "PRJ-01",
                "PRJ-03"
            ],
            "certification_ids": [
                "CRT-01",
                "CRT-03"
            ],
            "achievement_ids": [
                "ACH-02",
                "ACH-01",
                "ACH-03"
            ],
            "publication_ids": [
                "PUB-01",
                "PUB-02"
            ],
            "education_ids": [
                "EDU-01"
            ],
            "language_ids": [
                "LNG-01",
                "LNG-02",
                "LNG-05"
            ]
        },
        "improvement_suggestions": [
            "Highlighted DocuPulse AI (PRJ-01) and IEEE ICDSAA Research Paper (PUB-01) at the top of Projects/Publications as they directly prove citation-grounded RAG and 63% latency reduction.",
            "Prioritized Quantiphi ML Internship (EXP-02) alongside NexaCloud (EXP-01) to showcase 93.2% F1-score NER models with PyTorch and Hugging Face.",
            "Deselected purely frontend/Kanban items (PRJ-04, CRT-04) to keep the resume 100% focused on AI/ML and LLM engineering."
        ]
    },
    "jd_2_fullstack": {
        "id": "JD-002",
        "title": "Full-Stack Cloud & Distributed Systems Engineer",
        "company": "FinNova Cloud Pay",
        "location": "Mumbai / Navi Mumbai, India",
        "jd_text": "Role: Full-Stack Cloud & Distributed Systems Engineer\nCompany: FinNova Cloud Pay | Location: Mumbai / Navi Mumbai\n\nAbout the Role:\nFinNova Cloud Pay is hiring a Full-Stack Software Engineer to architect high-throughput merchant dashboards, multi-tenant SaaS backends, and automated spreadsheet/ERP data synchronization bridges.\n\nKey Responsibilities:\n- Build responsive, accessible frontend applications using React 18, Next.js, TypeScript, and Tailwind CSS.\n- Design scalable REST and WebSocket backend microservices using Python (FastAPI) and Node.js/Express backed by PostgreSQL and Redis.\n- Optimize database query performance, implement role-based access control (RBAC), and maintain 99.9%+ production uptime on AWS (ECS/EC2/RDS).\n- Build bi-directional Google Sheets API integrations and automated CI/CD pipelines with Docker, GitHub Actions, Pytest, and Jest.\n\nRequired Qualifications:\n- B.Tech in Computer Engineering or related field.\n- Strong proficiency in TypeScript, JavaScript, Python, React, Next.js, FastAPI, Node.js, and SQL (PostgreSQL).\n- Experience with AWS cloud deployment, Docker containerization, Redis caching, and automated testing.\n- AWS Developer Associate or Full-Stack professional certification preferred.",
        "match_score": 95,
        "matched_keywords": [
            "React 18",
            "Next.js",
            "TypeScript",
            "Tailwind CSS",
            "Python (FastAPI)",
            "Node.js / Express",
            "PostgreSQL",
            "Redis",
            "WebSockets",
            "RBAC",
            "Google Sheets API v4",
            "Docker",
            "AWS ECS",
            "GitHub Actions CI/CD",
            "Jest & Pytest"
        ],
        "missing_keywords": [
            "GraphQL Federation",
            "Terraform IaC"
        ],
        "selected_ids": {
            "summary_id": "SUM-03",
            "skill_ids": [
                "SKL-02",
                "SKL-01",
                "SKL-03",
                "SKL-09",
                "SKL-10",
                "SKL-11",
                "SKL-12",
                "SKL-13",
                "SKL-14",
                "SKL-04",
                "SKL-16"
            ],
            "experience_ids": [
                "EXP-01",
                "EXP-03"
            ],
            "project_ids": [
                "PRJ-02",
                "PRJ-04"
            ],
            "certification_ids": [
                "CRT-02",
                "CRT-04"
            ],
            "achievement_ids": [
                "ACH-01",
                "ACH-03"
            ],
            "publication_ids": [
                "PUB-02"
            ],
            "education_ids": [
                "EDU-01"
            ],
            "language_ids": [
                "LNG-01",
                "LNG-02",
                "LNG-04"
            ]
        },
        "improvement_suggestions": [
            "Selected FinScale Cloud SaaS (PRJ-02) and SyncFlow Google Sheets Bridge (PRJ-04) to directly demonstrate 12,000+ req/min PostgreSQL scale, RBAC, WebSockets, and bi-directional Google Sheets API v4 sync.",
            "Included RazorpayX Partner Labs FinTech Internship (EXP-03) to highlight 40,000+ daily sessions, SQL + Redis query optimization (620ms to 145ms), and 91% Jest/Pytest coverage.",
            "Omitted medical imaging project (PRJ-03) to maintain sharp alignment with FinTech Full-Stack & Cloud engineering."
        ]
    }
}

def init_and_seed_db():
    conn = sqlite3.connect(DB_PATH)
    with open("schema.sql", "r") as f:
        conn.executescript(f.read())
    cur = conn.cursor()

    p = PORTFOLIO_DATA["personal_info"]
    cur.execute(
        "INSERT OR REPLACE INTO personal_info VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)",
        (p["id"], p["full_name"], p["email"], p["phone"], p["location"],
         p["linkedin_url"], p["github_url"], p["portfolio_url"], p["base_title"])
    )

    for s in PORTFOLIO_DATA["career_summaries"]:
        cur.execute(
            "INSERT OR REPLACE INTO career_summaries VALUES (?, ?, ?, ?, ?)",
            (s["id"], s["user_id"], s["title_variant"], int(s["is_default"]), s["summary_text"])
        )

    for e in PORTFOLIO_DATA["education"]:
        cur.execute(
            "INSERT OR REPLACE INTO education VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)",
            (e["id"], e["user_id"], e["institution"], e["degree"], e["field_of_study"],
             e["start_date"], e["end_date"], e["gpa_or_grade"], e["highlights"])
        )

    for sk in PORTFOLIO_DATA["skills"]:
        cur.execute(
            "INSERT OR REPLACE INTO skills VALUES (?, ?, ?, ?, ?, ?, ?)",
            (sk["id"], "USR-001", sk["category"], sk["skill_name"],
             sk["proficiency_level"], sk["years_experience"], ",".join(sk["jd_tags"]))
        )

    for c in PORTFOLIO_DATA["certifications"]:
        cur.execute(
            "INSERT OR REPLACE INTO certifications VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)",
            (c["id"], "USR-001", c["name"], c["issuing_organization"], c["issue_date"],
             c["expiry_date"], c["credential_id"], c["credential_url"], c["focus_area"])
        )

    for prj in PORTFOLIO_DATA["projects"]:
        cur.execute(
            "INSERT OR REPLACE INTO projects VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)",
            (prj["id"], "USR-001", prj["title"], prj["role"], prj["tech_stack"],
             prj["start_date"], prj["end_date"], json.dumps(prj["description_bullets"]),
             prj["repo_url"], prj["live_url"], prj["key_metrics"], prj["domain_tag"])
        )

    for exp in PORTFOLIO_DATA["experience"]:
        cur.execute(
            "INSERT OR REPLACE INTO experience VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)",
            (exp["id"], "USR-001", exp["role_title"], exp["company"], exp["employment_type"],
             exp["location"], exp["start_date"], exp["end_date"],
             json.dumps(exp["achievements_bullets"]), exp["technologies_used"], exp["domain_tag"])
        )

    for ach in PORTFOLIO_DATA["achievements"]:
        cur.execute(
            "INSERT OR REPLACE INTO achievements VALUES (?, ?, ?, ?, ?, ?)",
            (ach["id"], "USR-001", ach["title"], ach["issuer_or_event"], ach["date_awarded"], ach["description"])
        )

    for pub in PORTFOLIO_DATA["publications_activities"]:
        cur.execute(
            "INSERT OR REPLACE INTO publications_activities VALUES (?, ?, ?, ?, ?, ?, ?, ?)",
            (pub["id"], "USR-001", pub["item_type"], pub["title"], pub["venue_or_publisher"],
             pub["publication_date"], pub["url"], pub["summary"])
        )

    for lng in PORTFOLIO_DATA["languages_competencies"]:
        cur.execute(
            "INSERT OR REPLACE INTO languages_competencies VALUES (?, ?, ?, ?, ?)",
            (lng["id"], "USR-001", lng["category"], lng["name"], lng["proficiency"])
        )

    conn.commit()
    conn.close()
    print(f"Database '{DB_PATH}' initialized and seeded with 10 categories for Aarav Mehta.")

if __name__ == "__main__":
    init_and_seed_db()
