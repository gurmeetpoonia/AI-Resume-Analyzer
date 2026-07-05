import re

def calculate_ats_score(resume_text, job_skills, matched_skills):

    resume = resume_text.lower()
    score = 0

    # =====================================
    # 1. Skill Match (50 Marks)
    # =====================================

    if job_skills:
        skill_score = (len(matched_skills) / len(job_skills)) * 50
        score += skill_score

    # =====================================
    # 2. Resume Length (10 Marks)
    # =====================================

    words = len(resume_text.split())

    if words >= 500:
        score += 10
    elif words >= 350:
        score += 8
    elif words >= 250:
        score += 6
    elif words >= 150:
        score += 4

    # =====================================
    # 3. Contact Information (10 Marks)
    # =====================================

    if re.search(r"\b\d{10}\b", resume_text):
        score += 5

    if re.search(r"[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}", resume_text):
        score += 5

    # =====================================
    # 4. Professional Links (10 Marks)
    # =====================================

    if "linkedin.com" in resume:
        score += 5

    if "github.com" in resume:
        score += 5

    # =====================================
    # 5. Resume Sections (15 Marks)
    # =====================================

    sections = [
        "summary",
        "education",
        "skills",
        "projects",
        "experience",
        "internship",
        "certification",
        "achievements"
    ]

    found = 0

    for section in sections:
        if section in resume:
            found += 1

    score += (found / len(sections)) * 15

    # =====================================
    # 6. Project Bonus (5 Marks)
    # =====================================

    project_words = [
        "machine learning",
        "deep learning",
        "streamlit",
        "docker",
        "python",
        "flask",
        "fastapi",
        "sql",
        "tensorflow",
        "pytorch",
        "power bi",
        "tableau"
    ]

    project_count = 0

    for word in project_words:
        if word in resume:
            project_count += 1

    score += min(project_count, 5)

    # =====================================
    # Final Score
    # =====================================

    score = min(round(score), 100)

    return score