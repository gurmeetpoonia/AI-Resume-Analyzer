import fitz
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity



def extract_text_from_pdf(pdf_file):
    """
    Extract text from an uploaded Pdf resume.
    Parameters 
    -----------
    pdf_file:uploadfile
        pdf file received from streamlit.

    Returns
    ------
    str 
        Complete extracted text.

    """

    document=fitz.open(stream=pdf_file.read(),filetype="pdf")
    text=""
    for page in document:
        text+= page.get_text()

    document.close()
    return text.strip()


def calculate_ATS_score(resume_text,job_description):
    """
    Calculate ATS similarity score between resume and job description.
    """
    documents=[
        resume_text,job_description
    ]

    tfidf=TfidfVectorizer(stop_words="english")
    tfidf_matrix=tfidf.fit_transform(documents)

    similarity=cosine_similarity(
        tfidf_matrix[0:1],
        tfidf_matrix[1:2]
    )[0][0]

    ats_score=round(similarity*100,2)
    return ats_score
    
def skill_analysis(resume_skills, jd_skills):

    resume_set = {skill.lower() for skill in resume_skills}
    jd_set = {skill.lower() for skill in jd_skills}

    matched = sorted(resume_set & jd_set)
    missing = sorted(jd_set - resume_set)

    return matched, missing