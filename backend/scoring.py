
from preprocess import normalise_text
#from  test_preprocess import resume_text 


def compute_ats_score(jd_keywords: list[str],resume_text: str) ->dict:
    normalised_resume = normalise_text(resume_text)
    matched=[]
    missing=[]
    for keywords in jd_keywords:
        if keywords in normalised_resume:
            matched.append(keywords)
        else:
            missing.append(keywords)
            
    total = len(jd_keywords)
    total_matched=len(matched)
    score= round((len(matched)/total)*100,1) if total>0 else 0.0
    return{
        "score": score,
        "matched_keywords": matched,
        "missing_keywords": missing,
        "total_keywords":total,
        "total_matched_keywords":total_matched
    }
    
if __name__=="__main__":
    from keywords import jd_keywords
    from test_preprocess import resume_text
    ats_result= compute_ats_score(jd_keywords,resume_text)
    print("----ATS SCORE-----")
    print("Score:", ats_result["score"])
    print("Matched Keywords:", ats_result["matched_keywords"])
    print("Missing Keywords:", ats_result["missing_keywords"])
    print("Total Keywords:", ats_result["total_keywords"])
    print("Total Matched Keywords:", ats_result["total_matched_keywords"])