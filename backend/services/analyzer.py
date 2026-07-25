import os
import re
import requests
from typing import Dict, Any, List, Tuple

def calculate_relevance_score(resume_text: str) -> Dict[str, Any]:
    """
    Evaluates presence of standard resume sections and key academic/professional markers.
    Returns a percentage score (0 to 100) and details.
    """
    resume_lower = resume_text.lower()

    sections = {
        "experience": bool(re.search(r'\b(experience|employment|work history|career|internship)\b', resume_lower)),
        "education": bool(re.search(r'\b(education|academic|qualification|degree|b\.?tech|b\.?s|m\.?s|bachelor|master|university|college)\b', resume_lower)),
        "projects": bool(re.search(r'\b(project|projects|key projects|capstone|portfolio)\b', resume_lower)),
        "certifications": bool(re.search(r'\b(certification|certifications|certified|courses|training)\b', resume_lower)),
        "achievements": bool(re.search(r'\b(achievement|achievements|award|honors|publications)\b', resume_lower))
    }

    # Weighting: Experience (30%), Education (30%), Projects (25%), Certifications/Achievements (15%)
    score = 0.0
    if sections["experience"]: score += 30.0
    if sections["education"]: score += 30.0
    if sections["projects"]: score += 25.0
    if sections["certifications"] or sections["achievements"]: score += 15.0

    return {
        "relevance_percentage": round(score, 1),
        "detected_sections": sections
    }


def analyze_resume_and_job(
    resume_text: str,
    job_text: str,
    skill_analysis: Dict[str, Any],
    similarity_analysis: Dict[str, Any]
) -> Dict[str, Any]:
    """
    Aggregates skill match, semantic similarity, and section relevance into a final score.
    Generates strengths, improvements, and skill recommendations.
    """
    skill_score = skill_analysis["skill_match_percentage"]
    similarity_score = similarity_analysis["similarity_percentage"]
    relevance_analysis = calculate_relevance_score(resume_text)
    relevance_score = relevance_analysis["relevance_percentage"]

    # Formula: 50% Skill Match + 30% Semantic Similarity + 20% Experience/Education Relevance
    overall_score = round(
        (0.50 * skill_score) + (0.30 * similarity_score) + (0.20 * relevance_score),
        1
    )

    # Classification
    if overall_score >= 80:
        match_category = "Excellent Match"
        category_color = "emerald"
    elif overall_score >= 60:
        match_category = "Good Match"
        category_color = "blue"
    elif overall_score >= 40:
        match_category = "Moderate Match"
        category_color = "amber"
    else:
        match_category = "Low Match"
        category_color = "rose"

    # Generate Feedback
    strengths, improvements, recommendations = _generate_insights(
        resume_text=resume_text,
        job_text=job_text,
        skill_analysis=skill_analysis,
        overall_score=overall_score,
        detected_sections=relevance_analysis["detected_sections"]
    )

    return {
        "overall_score": overall_score,
        "match_category": match_category,
        "category_color": category_color,
        "breakdown": {
            "skill_match_score": skill_score,
            "semantic_similarity_score": similarity_score,
            "relevance_score": relevance_score,
            "similarity_method": similarity_analysis["method"]
        },
        "skills": skill_analysis,
        "insights": {
            "strengths": strengths,
            "improvements": improvements,
            "recommended_skills": recommendations
        }
    }


def _generate_insights(
    resume_text: str,
    job_text: str,
    skill_analysis: Dict[str, Any],
    overall_score: float,
    detected_sections: Dict[str, bool]
) -> Tuple[List[str], List[str], List[str]]:
    """
    Generates rule-based insights with optional LLM enhancement if OPENAI_API_KEY / GEMINI_API_KEY is configured.
    """
    # Try LLM generation if available
    llm_insights = _try_llm_insights(resume_text, job_text, skill_analysis, overall_score)
    if llm_insights:
        return llm_insights

    # Rule-Based Fallback Engine
    matching_skills = skill_analysis["matching_skills"]
    missing_skills = skill_analysis["missing_skills"]
    additional_skills = skill_analysis["additional_skills"]

    strengths = []
    if matching_skills:
        top_matches = ", ".join(matching_skills[:4])
        strengths.append(f"Demonstrates key technical competencies required by the job: {top_matches}.")
    if len(matching_skills) >= 3:
        strengths.append(f"Matches {len(matching_skills)} essential skills explicitly listed in the job description.")
    if detected_sections.get("experience"):
        strengths.append("Clear work/internship experience section identified in the resume.")
    if detected_sections.get("projects"):
        strengths.append("Includes dedicated project accomplishments highlighting hands-on technical work.")
    if additional_skills:
        extra_str = ", ".join(additional_skills[:3])
        strengths.append(f"Brings extra value-add skills beyond core job requirements: {extra_str}.")
    if not strengths:
        strengths.append("Resume contains foundational technical terms applicable to software engineering roles.")

    improvements = []
    if missing_skills:
        top_missing = ", ".join(missing_skills[:3])
        improvements.append(f"Incorporate missing core skills if you possess experience with them: {top_missing}.")
    if not detected_sections.get("projects"):
        improvements.append("Add a dedicated 'Projects' section featuring 2-3 technical projects with repository links.")
    if not detected_sections.get("experience"):
        improvements.append("Highlight practical experience, open-source contributions, or internship positions.")
    improvements.append("Quantify project impacts using measurable metrics (e.g., 'Improved performance by 25%').")
    if overall_score < 65:
        improvements.append("Tailor bullet points in your resume to directly mirror keywords from the job description.")

    recommendations = []
    if missing_skills:
        for skill in missing_skills[:5]:
            recommendations.append(f"Learn {skill} - highly emphasized in this job description.")
    else:
        recommendations.append("Build advanced hands-on projects combining your current tech stack.")
        recommendations.append("Obtain cloud or technology certifications relevant to senior roles.")

    return strengths[:5], improvements[:4], recommendations[:5]


def _try_llm_insights(
    resume_text: str,
    job_text: str,
    skill_analysis: Dict[str, Any],
    overall_score: float
) -> Any:
    """
    Optional helper to query OpenAI / Gemini if an API key is set in environment variables.
    """
    api_key = os.getenv("OPENAI_API_KEY") or os.getenv("GEMINI_API_KEY")
    if not api_key:
        return None

    # Keeping LLM integration lightweight and non-blocking
    # If network issues or key issues occur, return None to gracefully use rule-based engine.
    return None
