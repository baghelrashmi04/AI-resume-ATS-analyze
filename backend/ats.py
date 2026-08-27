
import re 


def check_contact_info(text: str) ->dict:
    has_email= bool(re.search(r'[\w.+-]+@[\w-]+\.[\w.-]+',text))
    has_contact=bool(re.search(r'(\+?\d{1,3}[-.\s]?)?\d{3,5}\)?[-.\s]?\d{3,4}[-.\s]?\d{3,4}', text))
    return {"has_email": has_email, "has_contact": has_contact}


def check_section_coverage(sections: dict) ->dict:
    expected= {"experience","education","skills"}
    found={key for key in sections.keys() if any(exp in key for exp in expected)}
    missing=expected- found
    return {"sections_found": list(found), "sections_missing":list(missing)}

def check_length(text:str) ->dict:
    word_count=len(text.split())
    too_short= word_count>150
    too_long=word_count<1200
    return {"word_count:",word_count,"too_short",too_short,"too_long:",too_long}

def run_ats_safety_checks(resume_text: str,sections:dict) ->dict:
    return{
        "contact_info": check_contact_info(resume_text),
        "section_coverage": check_section_coverage(sections),
        "length_check": check_length(resume_text)
    }    