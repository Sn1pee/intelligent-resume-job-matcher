import fitz

def generate_sample_pdf(output_path="sample_data/sample_resume.pdf"):
    doc = fitz.open()
    page = doc.new_page(width=595, height=842) # A4 dimensions
    
    resume_text = """
ALEX MORGAN
Computer Science Graduate & Software Developer
Email: alex.morgan@example.com | GitHub: github.com/alexmorgan | Phone: +1 555-0199

PROFESSIONAL SUMMARY
Motivated Software Developer with expertise in Python, SQL, and data analysis. Experienced in building machine learning models, REST APIs, and automated data processing tools. Proficient with Git version control and statistical analysis libraries.

EDUCATION
Bachelor of Technology in Computer Science & Engineering
State University | Graduated: May 2025 | GPA: 3.8/4.0

TECHNICAL SKILLS
- Programming Languages: Python, JavaScript, C++, SQL
- Data Science & ML: Pandas, NumPy, Scikit-learn, Machine Learning, Matplotlib
- Web Frameworks & Tools: FastAPI, Flask, HTML, CSS, Git, GitHub
- Databases: PostgreSQL, MySQL, SQLite

PROJECTS
1. Intelligent Customer Churn Prediction Model
   - Built a supervised Machine Learning pipeline using Python, Pandas, and Scikit-learn to predict customer retention with 89% accuracy.
   - Deployed a REST API backend using FastAPI to serve model predictions in real time.
   - Used Git & GitHub for version control and issue tracking.

2. Automated SQL Query & Reporting Tool
   - Created Python scripts to parse, query, and process large relational datasets from PostgreSQL databases.
   - Optimized database query performance and exported structured reports.

EXPERIENCE
Software Development Intern | Tech Solutions Inc.
June 2024 - August 2024
- Assisted in developing backend services using Python and Flask.
- Wrote automated data validation tests using PyTest and managed SQL schemas.
- Collaborated in an Agile software development team.

CERTIFICATIONS
- Python for Data Science & Machine Learning Certificate
- SQL Database Administration Basics
"""

    # Add text to page
    rect = fitz.Rect(40, 40, 555, 802)
    page.insert_textbox(rect, resume_text, fontsize=10, fontname="helv")
    
    doc.save(output_path)
    doc.close()
    print(f"Sample PDF resume generated successfully at {output_path}")

if __name__ == "__main__":
    generate_sample_pdf()
