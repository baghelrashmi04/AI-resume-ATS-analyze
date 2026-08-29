

# this file holds functions everything related to ai powered bullets , 
# the section of the product which is responisble for ai content




import os 
from google import genai
from google.genai import types
from dotenv import load_dotenv
load_dotenv()

client = genai.Client(api_key=os.environ["GEMINI_API_KEY"])

REWRITE_PROMPT = """
You are an expert ATS (Application Tracking system) friendly resume writer.
YOUR GOAL:
Rewrite and improve the resume bullet points to naturally incorporate missing targeted keywords by 
following Google's formula ("Accomplished[x], measured by [y], by doing [z]").

INPUT DATA:
-target job keywords to include : {missing_keywords}
-current resume experience/bullets:
{experience_text}

RULES & CONSTRAINTS:
-preserve truthfullness ; Only include metrics/numbers if they are explicitly present in the original 
bullet or can be reasonably inferred from it — never invent numbers, percentages, or scale that aren't 
implied by the source text

- start every bullet point with a strong action verb(e.g, "Architectured","Optimised","Engineered").
-If a bullet point is too vague or generic to honestly rewrite with specific 
 achievements (e.g., "responsible for various tasks"), do NOT invent scope, 
   metrics, or specifics that aren't implied by the original text. Instead, 
   improve only what can be honestly improved (stronger verb, clearer wording), 
   and explicitly note in your response that this bullet lacks enough detail 
   for a stronger rewrite — recommend the person add specifics themselves.
-Provide exactly 3-4 points polished,, ready to use replacement bullet points.
-Naturally incorporate relevant missing keywords ONLY if they genuinely fit the described work
- Stay under 2 lines / ~30 words
- Never invent skills, tools, or achievements not implied by the original bullet

OUTPUT FORMAT:
provide the response in clear , bulleted markdwon format. After the bullets, add a brief 1-sentence note 
explaining how the missing keywords were integrated
 
Return only rewritten points nothing else
"""


def generated_improved_bullets(missing_keywords: list[str],experience_text: str) ->str:
    """
       calls gemini api to rewrite resume bullets with missing ats keywords.
    """
    if not missing_keywords:
        return "No missing keywords your resume experience covers the required terms."
    
    formatted_prompt= REWRITE_PROMPT.format(
        missing_keywords=','.join(missing_keywords),
        experience_text=experience_text
    )
    
    #making the api call 
    try:
        response=client.models.generate_content(
            model="gemini-3.6-flash",
            contents= formatted_prompt,
            config=types.GenerateContentConfig(temperature=0.3)
        )
        return response.text
    except Exception as e:
        return "The AI rewriting service is temporarily unavailable. Please try again in a moment."
    
    
def is_bullet_too_vague(bullet: str) ->bool:
    """
       checks if a bullet point is too vague to rewrite with specifics.
    """
    vague_phrases=[
        "responsible for","various tasks","assisted with","helped with",
        "worked on","involved in","participated in"
    ]
    bullet_lower=bullet.lower()
    words=bullet.split()
    word_count= len(words)
    
    if word_count <=10 or any(phrase in bullet_lower for phrase in vague_phrases):
        return True
        
        
    else:
        return False
            
def split_into_bullets(text:str) ->list[str]:   # it splits paragrapgh or multiple lines into single lines
    bullets=[line.strip() for line in text.splitlines() if line.strip()]
    return bullets

#this function separte the vague bullets from good bullets , vague bullets are flagged for user while 
# good bullets goes to ai prompting

def separate_vague_bullets(text: str) ->tuple:
    bullets= split_into_bullets(text)
    vague_bullets=[]
    good_bullets=[]
    for bullet in bullets:
        if is_bullet_too_vague(bullet):
            vague_bullets.append(bullet)
        else:
            good_bullets.append(bullet)
    return vague_bullets,good_bullets
    
    


    
    
    
    
    # for my knwledge just , this if dunder method is used to tell the interpreter that this 
    # block of code must be used when it is called or imported 
    
if __name__=="__main__":
    from scoring import compute_ats_score
    from keywords import jd_keywords
    from test_preprocess import resume_text
    from preprocess import split_into_sections
    
    ats_result= compute_ats_score(jd_keywords,resume_text)
    missing_keywords= ats_result["missing_keywords"]
    
    sections=split_into_sections(resume_text)
    experience_text=sections.get("experience",sections.get("work experience",resume_text))
    
    print(f"----MISSING KEYWORDS ({(len(missing_keywords))})-----")
    #print(missing)
    print(missing_keywords)
    
    #experience_text=resume_text
    improved_bullets=generated_improved_bullets(missing_keywords,experience_text)
    
    print("----IMPROVED BULLETS-----")
    print(improved_bullets)
    