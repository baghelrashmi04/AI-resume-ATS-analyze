
# so this file is about rule-based resume "health" check unrealted to keywords


import re 

# this function chekcs if resume has contact or email or not 
def check_contact_info(text: str) ->dict:
    has_email= bool(re.search(r'[\w.+-]+@[\w-]+\.[\w.-]+',text))
    has_contact=bool(re.search(r'(\+?\d{1,3}[-.\s]?)?\d{3,5}\)?[-.\s]?\d{3,4}[-.\s]?\d{3,4}', text))
    return {"has_email": has_email, "has_contact": has_contact}

# function checks which expected sections are present and which are present 
def check_section_coverage(sections: dict) -> dict:
    section_synonyms = {
        "experience": ["experience", "work experience", "professional experience", "project experience"],
        "education": ["education"],
        "skills": ["skills", "technical skills", "languages", "tech stack", "core competencies"]
    }

    found = set()
    for standard_name, synonyms in section_synonyms.items():
        if any(any(syn in key for syn in synonyms) for key in sections.keys()):
            found.add(standard_name)

    expected = set(section_synonyms.keys())
    missing = expected - found
    return {"sections_found": list(found), "sections_missing": list(missing)}

# checks word count if resume is too long or too short
def check_length(text:str) ->dict:
    word_count=len(text.split())
    too_short= word_count<150
    too_long=word_count>1200
    return {"word_count":word_count,"too_short":too_short,"too_long":too_long}


# this functions bundles above all three functions check_contact , check_section , check_length and 
# runs a safety resume chedk function

def run_ats_safety_checks(resume_text: str,sections:dict) ->dict:
    return{
        "contact_info": check_contact_info(resume_text),
        "section_coverage": check_section_coverage(sections),
        "length_check": check_length(resume_text)
    }    