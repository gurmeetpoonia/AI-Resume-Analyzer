from google import genai
from google.genai import types
import time
from google.genai.errors import APIError 
from dotenv import load_dotenv
import os
import json 

load_dotenv()

# Client Initialization
client = genai.Client(
    api_key=os.getenv("API_KEY")
)



def analyze_resume(resume_text, job_description):
    prompt = f"""
You are an expert ATS Resume Analyzer.

Your task is to compare the resume ONLY with the provided job description.

Do NOT use any assumptions.

Rules:
1. ATS score must depend on similarity between resume and job description.
2. Matching skills = only skills present in BOTH.
3. Missing skills = skills in JD but absent in resume.
4. Strengths must come ONLY from resume.
5. Weaknesses must come ONLY from missing skills.
6. Suggestions must directly improve missing skills.
7. Final verdict must depend on ATS score.

Scoring:

90-100 = Excellent Match
75-89 = Good Match
50-74 = Average Match
Below 50 = Poor Match

Resume:
----------------
{resume_text}

Job Description:
----------------
{job_description}

Return JSON only.
"""

    max_retries = 3
    retry_delay = 2  # Start with a 2-second delay

    for attempt in range(max_retries):
        try:
            response = client.models.generate_content(
                model="gemini-2.5-flash",
                contents=prompt,
                config=types.GenerateContentConfig(
                    temperature=0.7,
                    top_p=0.95,    
                    response_mime_type="application/json",
                    system_instruction=(
                        "Extract technical skills, ignore soft skills, ensure unique entries, proper capitalization, "
                        "keep strengths/weaknesses/suggestions concise, and return an integer ats_score between 0 and 100."
                    ),
                    response_schema={
                        "type": "OBJECT",
                        "properties": {
                            "ats_score": {"type": "INTEGER"},
                            "resume_skills": {"type": "ARRAY", "items": {"type": "STRING"}},
                            "job_skills": {"type": "ARRAY", "items": {"type": "STRING"}},
                            "matched_skills": {"type": "ARRAY", "items": {"type": "STRING"}},
                            "missing_skills": {"type": "ARRAY", "items": {"type": "STRING"}},
                            "strengths": {"type": "ARRAY", "items": {"type": "STRING"}},
                            "weaknesses": {"type": "ARRAY", "items": {"type": "STRING"}},
                            "suggestions": {"type": "ARRAY", "items": {"type": "STRING"}},
                            "final_verdict": {"type": "STRING"}
                        },
                        "required": [
                            "ats_score", "resume_skills", "job_skills", "matched_skills", 
                            "missing_skills", "strengths", "weaknesses", "suggestions", "final_verdict"
                        ]
                    }
                )
            )

            # If successful, parse and return data
            data = json.loads(response.text.strip())
            data.setdefault("status", "success")
            return data

        except Exception as e:
            error = str(e)
            # If it's a quota error and we have retries left, wait and try again
            if ("429" in error or "RESOURCE_EXHAUSTED" in error) and attempt < max_retries - 1:
                time.sleep(retry_delay)
                retry_delay *= 2  # Double the wait time for the next attempt (Exponential Backoff)
                continue
            
            # If all retries fail or it's a quota error on the final attempt
            if "429" in error or "RESOURCE_EXHAUSTED" in error:
                return {"status": "quota_exceeded", "final_verdict": "Quota exceeded after retries."}
            
            # General system error handling
            return {
    "status":"error",
    "ats_score":0,
    "resume_skills":[],
    "job_skills":[],
    "matched_skills":[],
    "missing_skills":[],
    "strengths":[],
    "weaknesses":[],
    "suggestions":[],
    "final_verdict":error
}