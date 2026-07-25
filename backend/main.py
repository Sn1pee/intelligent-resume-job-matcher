import os
import sys
from pathlib import Path

# Add backend directory to sys.path
backend_dir = Path(__file__).resolve().parent
if str(backend_dir) not in sys.path:
    sys.path.insert(0, str(backend_dir))

from fastapi import FastAPI, UploadFile, File, Form, HTTPException, status
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse, JSONResponse
from dotenv import load_dotenv

from services.pdf_parser import extract_text_from_pdf_bytes
from services.skill_matcher import analyze_skill_match, COMMON_SKILLS
from services.similarity import calculate_semantic_similarity
from services.analyzer import analyze_resume_and_job

load_dotenv()

app = FastAPI(
    title="Intelligent Resume & Job Matching System",
    description="Student Portfolio Project for NLP-based Resume and Job Description Matching",
    version="1.0.0"
)

# Enable CORS for local development
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/api/health")
async def health_check():
    return {
        "status": "online",
        "service": "Intelligent Resume & Job Matching API",
        "version": "1.0.0"
    }


@app.get("/api/skills")
async def get_available_skills():
    return {
        "skills": sorted(list(COMMON_SKILLS.keys())),
        "total_skills": len(COMMON_SKILLS)
    }


@app.post("/api/analyze")
async def analyze_matching(
    resume_file: UploadFile = File(...),
    job_description: str = Form(...)
):
    # Validate job description input
    if not job_description or not job_description.strip():
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Job description text cannot be empty."
        )

    # Validate file type
    if not resume_file.filename.lower().endswith(".pdf"):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Invalid file format. Please upload a PDF resume file (.pdf)."
        )

    try:
        # Read file contents
        pdf_bytes = await resume_file.read()
        
        # 1. PDF Text Extraction
        resume_text, page_count = extract_text_from_pdf_bytes(pdf_bytes)

        # 2. Skill Extraction & Matching
        skill_analysis = analyze_skill_match(resume_text, job_description)

        # 3. Semantic Similarity via Embeddings / TF-IDF
        similarity_analysis = calculate_semantic_similarity(resume_text, job_description)

        # 4. Overall Scoring & Insights Generation
        result = analyze_resume_and_job(
            resume_text=resume_text,
            job_text=job_description,
            skill_analysis=skill_analysis,
            similarity_analysis=similarity_analysis
        )

        # Include metadata
        result["metadata"] = {
            "resume_filename": resume_file.filename,
            "page_count": page_count,
            "resume_character_count": len(resume_text),
            "job_character_count": len(job_description)
        }

        return JSONResponse(content=result)

    except ValueError as ve:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(ve))
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"An unexpected error occurred during analysis: {str(e)}"
        )


# Serve Static Frontend Files
frontend_path = backend_dir.parent / "frontend"

if frontend_path.exists():
    app.mount("/static", StaticFiles(directory=str(frontend_path)), name="static")

    @app.get("/")
    async def serve_index():
        return FileResponse(str(frontend_path / "index.html"))
