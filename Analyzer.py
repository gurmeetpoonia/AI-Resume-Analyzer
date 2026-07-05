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

