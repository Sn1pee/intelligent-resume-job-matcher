# Intelligent Resume & Job Matching System

A full-stack web application designed to evaluate candidate resume suitability against job descriptions using Natural Language Processing (NLP), skill pattern matching, and sentence embeddings.

---

## 📌 Project Overview

The **Intelligent Resume & Job Matching System** is a student portfolio application created to demonstrate practical NLP concepts without unnecessary enterprise complexity. Users can upload a PDF resume, paste a target job description, and receive an instant analysis breakdown, match score, skill overlap report, and actionable resume optimization suggestions.

---

## ✨ Features

- 📄 **PDF Text Extraction**: Parses raw resume text cleanly from uploaded `.pdf` documents using PyMuPDF (`fitz`).
- 🎯 **Technical Skill Extractor**: Identifies skills from a predefined dictionary of 35+ common technologies using word-boundary pattern matching.
- 🧮 **Multi-Factor Scoring Engine**:
  - **Skill Match (50%)**: Direct comparison of candidate skills vs required job skills.
  - **Semantic Similarity (30%)**: Embedding vector cosine similarity using `SentenceTransformer('all-MiniLM-L6-v2')` (with TF-IDF cosine similarity fallback).
  - **Relevance & Structure (20%)**: Section presence checks (Experience, Education, Projects, Certifications).
- 📊 **Interactive Visual Dashboard**:
  - Animated SVG circular match score ring with score classification badges.
  - Color-coded skill tags (Matching, Missing, Additional).
  - Categorized insights: Strengths, Areas for Improvement, and Recommended Skills to Learn.
- ⚡ **One-Click Demo**: Built-in sample dataset loader for instant testing.

---

## 🛠️ Tech Stack

### Backend
- **Framework**: Python 3.12 + [FastAPI](https://fastapi.tiangolo.com/)
- **ASGI Server**: Uvicorn
- **PDF Parser**: PyMuPDF (`fitz`)
- **NLP / Embeddings**: `sentence-transformers` (`all-MiniLM-L6-v2`), `scikit-learn` (TF-IDF Cosine Similarity)

### Frontend
- **Structure**: HTML5 + Vanilla JavaScript
- **Styling**: Tailwind CSS (CDN) + Custom Glassmorphism CSS
- **Icons**: FontAwesome 6

---

## ⚙️ How It Works & Matching Algorithm

The matching system evaluates alignment through a weighted algorithm designed to simulate initial ATS (Applicant Tracking System) screening heuristics:

$$\text{Overall Score} = (0.50 \times \text{Skill Match}) + (0.30 \times \text{Semantic Similarity}) + (0.20 \times \text{Relevance Score})$$

### Score Breakdown
1. **Skill Match Score (50%)**:
   $$\text{Skill Match \%} = \frac{\text{Matching Skills Count}}{\text{Total Job Required Skills Count}} \times 100$$
2. **Semantic Similarity Score (30%)**:
   Computes dense vector representations of both texts using `all-MiniLM-L6-v2` embeddings and measures the cosine distance between them.
3. **Relevance & Experience Score (20%)**:
   Detects structural standard sections (Work Experience, Education, Projects, Certifications) and checks for domain academic credentials.

### Score Classification
- **80% – 100%**: Excellent Match
- **60% – 79%**: Good Match
- **40% – 59%**: Moderate Match
- **Below 40%**: Low Match

---

## 📂 Project Architecture

```
resume-matcher/
├── backend/
│   ├── main.py                 # FastAPI endpoints & static file hosting
│   ├── services/
│   │   ├── pdf_parser.py       # PyMuPDF PDF text extraction
│   │   ├── skill_matcher.py    # Skill extraction & dictionary matching
│   │   ├── similarity.py       # SentenceTransformers / TF-IDF similarity
│   │   └── analyzer.py         # Multi-factor score calculator & insights engine
│   └── requirements.txt        # Python backend dependencies
├── frontend/
│   ├── index.html              # Modern dashboard UI
│   ├── css/
│   │   └── style.css           # Glassmorphism & animation styles
│   └── js/
│       └── app.js              # Drag-drop PDF uploader, API fetch & score ring
├── sample_data/
│   ├── create_sample_pdf.py    # Script to generate sample resume PDF
│   ├── sample_resume.pdf       # Pre-generated sample PDF resume
│   └── sample_job_description.txt # Sample job description
├── .env.example                # Environment configuration template
├── .gitignore                  # Git ignore rules
└── README.md                   # Project documentation
```

---

## 🚀 Installation & How to Run

### Prerequisites
- Python 3.9+ (Python 3.12 recommended)

### 1. Clone / Navigate to Project Directory
```bash
cd resume-matcher
```

### 2. Install Dependencies
```bash
pip install -r backend/requirements.txt
```

### 3. Generate Sample PDF Data
```bash
python sample_data/create_sample_pdf.py
```

### 4. Start the Application Server
```bash
python -m uvicorn backend.main:app --reload --port 8000
```

### 5. Open Web Application
Navigate to `http://127.0.0.1:8000` in your web browser.

---

## 🔐 Environment Variables

Rename `.env.example` to `.env` if you wish to configure custom environment settings:

```env
# Optional AI LLM API Key (Leave blank to use built-in rule-based insight engine)
OPENAI_API_KEY=
GEMINI_API_KEY=

HOST=127.0.0.1
PORT=8000
```

---

## ⚠️ Limitations & Educational Note

This application is built as an **educational student portfolio project**. 

- **Approximate Matching**: The match score is a heuristic analysis combining skill presence and vector text similarity. It does not replace human recruiters or proprietary enterprise ATS algorithms.
- **Scanned PDFs**: Scanned image-only PDFs require OCR (Optical Character Recognition) which is outside the scope of this lightweight student stack; standard text-based PDFs are supported.
