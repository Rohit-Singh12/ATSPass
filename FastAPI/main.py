from fastapi import FastAPI
from pydantic import BaseModel
from Resume import Resume

app = FastAPI()
resume = Resume('http://ollama:11434')
class ResumeJobPayload(BaseModel):
    resume: str
    job_desc: str

@app.post("/process_resume/")
def process_resume(payload: ResumeJobPayload):
    """
    Endpoint to process resume and job description.
    """
    if not payload:
        return None
    return resume.ats_system(payload.resume, payload.job_desc)
    