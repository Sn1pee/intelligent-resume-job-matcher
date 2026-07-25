import re
from typing import List, Dict, Set, Any

# Predefined dictionary of technical skills with display names and search aliases
COMMON_SKILLS: Dict[str, List[str]] = {
    "Python": ["python", "py"],
    "Java": ["java"],
    "C++": ["c++", "cpp"],
    "C#": ["c#", "csharp"],
    "JavaScript": ["javascript", "js", "es6"],
    "TypeScript": ["typescript", "ts"],
    "SQL": ["sql", "mysql", "postgresql", "sqlite", "tsql", "plsql"],
    "HTML": ["html", "html5"],
    "CSS": ["css", "css3", "sass", "scss", "tailwind", "bootstrap"],
    "React": ["react", "reactjs", "react.js", "react native"],
    "Node.js": ["node.js", "nodejs", "node"],
    "FastAPI": ["fastapi", "fast api"],
    "Flask": ["flask"],
    "Django": ["django"],
    "Git": ["git"],
    "GitHub": ["github", "gitlab", "bitbucket"],
    "Docker": ["docker"],
    "Kubernetes": ["kubernetes", "k8s"],
    "AWS": ["aws", "amazon web services", "ec2", "s3", "lambda"],
    "Azure": ["azure", "microsoft azure"],
    "GCP": ["gcp", "google cloud", "google cloud platform"],
    "Machine Learning": ["machine learning", "ml"],
    "Deep Learning": ["deep learning", "dl"],
    "NLP": ["nlp", "natural language processing", "spacy", "nltk", "transformers"],
    "Computer Vision": ["computer vision", "cv", "opencv"],
    "Pandas": ["pandas"],
    "NumPy": ["numpy"],
    "Matplotlib": ["matplotlib", "seaborn", "plotly"],
    "Scikit-learn": ["scikit-learn", "sklearn"],
    "TensorFlow": ["tensorflow", "tf"],
    "PyTorch": ["pytorch"],
    "MongoDB": ["mongodb", "mongo"],
    "MySQL": ["mysql"],
    "PostgreSQL": ["postgresql", "postgres"],
    "Power BI": ["power bi", "powerbi"],
    "Tableau": ["tableau"],
    "Linux": ["linux", "ubuntu", "bash", "shell"],
    "REST API": ["rest api", "restful api", "rest", "api"],
    "GraphQL": ["graphql"],
    "Microservices": ["microservices", "microservice"],
    "CI/CD": ["ci/cd", "cicd", "jenkins", "github actions"],
    "Agile": ["agile", "scrum", "jira"],
    "Excel": ["excel", "microsoft excel"],
    "Data Analysis": ["data analysis", "data analytics"],
}

def extract_skills(text: str) -> List[str]:
    """
    Extracts known skills present in the given text using regex word boundary matching.
    """
    if not text:
        return []
    
    text_lower = text.lower()
    found_skills: List[str] = []

    for skill_name, aliases in COMMON_SKILLS.items():
        for alias in aliases:
            # Escaping special regex characters like c++, c#, .js
            escaped_alias = re.escape(alias)
            # Use boundary regex to avoid matching sub-words like 'java' inside 'javascript' unless alias is exact
            pattern = r'(?:^|[\s,.\/()\-:_])' + escaped_alias + r'(?:$|[\s,.\/()\-:_])'
            if re.search(pattern, text_lower):
                found_skills.append(skill_name)
                break

    return sorted(found_skills)


def analyze_skill_match(resume_text: str, job_text: str) -> Dict[str, Any]:
    """
    Compares resume skills vs job description skills.
    Returns matching, missing, additional skills, and skill match percentage.
    """
    resume_skills = set(extract_skills(resume_text))
    job_skills = set(extract_skills(job_text))

    matching_skills = sorted(list(resume_skills.intersection(job_skills)))
    missing_skills = sorted(list(job_skills.difference(resume_skills)))
    additional_skills = sorted(list(resume_skills.difference(job_skills)))

    if job_skills:
        skill_match_percentage = round((len(matching_skills) / len(job_skills)) * 100, 1)
    else:
        # Fallback if job description has no explicitly matched skills from dictionary
        skill_match_percentage = 50.0 if resume_skills else 0.0

    return {
        "resume_skills": sorted(list(resume_skills)),
        "job_skills": sorted(list(job_skills)),
        "matching_skills": matching_skills,
        "missing_skills": missing_skills,
        "additional_skills": additional_skills,
        "skill_match_percentage": skill_match_percentage,
    }
