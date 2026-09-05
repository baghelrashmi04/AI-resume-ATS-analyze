# this file is the orecestrator as its name main , owns the /anlayse FastApi endpoint 
# this file calls functions from every file in sequence , and assembles the final json response


from fastapi import FastAPI, UploadFile,File, Form
import shutil
import os
import uuid

from extract import extract_pdf,extract_docx
from  preprocess import normalise_text, split_into_sections
from  keywords import extract_keywords
from scoring import compute_ats_score
from rewrite import generated_improved_bullets , separate_vague_bullets, profile_summary_fit
from ats import run_ats_safety_checks


app=FastAPI()

@app.post("/analyze")
async def analyse_resume(resume: UploadFile=File(...), jd_text:str=Form(...)):
    file_ext= os.path.splitext(resume.filename)[1]
    temp_path=f"temp_{uuid.uuid4().hex}{file_ext}"
    with open(temp_path,"wb") as f:
        shutil.copyfileobj(resume.file, f)
        
    if resume.filename.endswith(".pdf"):
        resume_text=extract_pdf(temp_path)
        if not resume_text.strip():
          return {"error": "Couldn't extract because the file format is different that required."}
    elif resume.filename.endswith(".docx"):
        resume_text=extract_docx(temp_path)
    else: 
        os.remove(temp_path)
        return {"error": "OOPS!! Looks like you file format isn't .pdf or .docx , try again with these formats:-)"}
    os.remove(temp_path)
    
    
    jd_keywords= extract_keywords(jd_text)
    ats_result= compute_ats_score(jd_keywords, resume_text)
    
    sections= split_into_sections(resume_text)
    recheck=run_ats_safety_checks(resume_text,sections)
    experience_text= sections.get("work experience") or sections.get("professional experience") or sections.get("project experience")  or sections.get("experience",resume_text) ## experience_text is a whole blob of text that is sent to gemini
    good_bullets,vague_bullets= separate_vague_bullets(experience_text)
    good_bullets_text="\n".join(good_bullets)
    profile_summary = profile_summary_fit(jd_text, experience_text)
    improved_bullets= generated_improved_bullets(ats_result["missing_keywords"],good_bullets_text[:1500])
    return{
        "ats_score" : ats_result["score"],
        "matched_keywords": ats_result["matched_keywords"],
        "missing_keywords": ats_result["missing_keywords"],
        "profile_summary": profile_summary,
        "improved_bullets": improved_bullets,
        "vague_bullets": vague_bullets,
        "full_ats_check": recheck
    }
    
    
    


@app.get("/")
async def root():
    return {"message": "Resume analyzer API is running. Use POST /analyze."}