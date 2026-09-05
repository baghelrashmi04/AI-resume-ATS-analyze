

# this file holds functions everything related to ai powered bullets , 
# the section of the product which is responisble for ai content



import re
import os 
from google import genai
from google.genai import types
from dotenv import load_dotenv
load_dotenv()

client = genai.Client(api_key=os.environ["GEMINI_API_KEY"])

REWRITE_PROMPT = """
You are an expert ATS (Applicant Tracking System) friendly resume writer.
YOUR GOAL:
Rewrite and improve the resume bullet points to naturally incorporate missing targeted keywords by
following Google's formula ("Accomplished [x], measured by [y], by doing [z]").

INPUT DATA:
- Target job keywords to include: {missing_keywords}
- Current resume experience/bullets:
{experience_text}

RULES & CONSTRAINTS:
- Preserve truthfulness; only include metrics/numbers if they are explicitly present in the original
  bullet or can be reasonably inferred from it — never invent numbers, percentages, or scale that
  aren't implied by the source text.
- Start every bullet point with a strong, specific action verb — vary the verb across bullets, never
  repeat the same one twice.
- AVOID generic filler words and phrases entirely: "ensuring," "driving," "leveraging," "facilitating,"
  "utilizing," "responsible for," "helped," "worked on." Name the actual tool, technology, or method
  instead of describing the action abstractly.
- Be maximally concrete: name specific technologies, data types, or processes from the original bullet
  rather than paraphrasing them generically. If the original says "Azure Data Factory," keep saying
  "Azure Data Factory" — don't abstract it into "cloud tools."
- If a bullet point is too vague or generic to honestly rewrite with specific achievements (e.g.,
  "responsible for various tasks"), do NOT invent scope, metrics, or specifics that aren't implied by
  the original text. Instead, improve only what can be honestly improved (stronger verb, clearer
  wording), and explicitly note in your response that this bullet lacks enough detail for a stronger
  rewrite — recommend the person add specifics themselves.
- Provide exactly 3-4 polished, ready-to-use replacement bullet points.
- Naturally incorporate relevant missing keywords ONLY if they genuinely fit the described work.
- Stay under 2 lines / ~30 words per bullet.
- Never invent skills, tools, or achievements not implied by the original bullet.

OUTPUT FORMAT:
Provide the response in clear, bulleted markdown format. After the bullets, add a brief 1-sentence note
explaining how the missing keywords were integrated.

Return only the rewritten points, nothing else.

"""

REWRITE_SUMMARY = """
You are an expert resume writer. Write a crisp, confident professional summary 
tailored specifically to the job description below, based on the candidate's 
actual experience.

JOB DESCRIPTION:
{jd_text}

CANDIDATE'S EXPERIENCE:
{experience_text}

RULES & CONSTRAINTS:
- Do NOT use generic filler phrases like "results-driven," "action-oriented," 
  "team player," "detail-oriented," or similar clichés.
- Do NOT invent facts, skills, tools, or achievements not present in the 
  candidate's experience — only characterize what's genuinely there.
- If the candidate's experience includes hands-on projects, reflect that with 
  concrete language (e.g., "hands-on experience building..." rather than vague claims).
- Keep it under 70 words, as a single paragraph.
- End with one sentence expressing genuine interest in or fit for the specific 
  type of role mentioned in the job description.

Return only the summary paragraph, nothing else.
"""


def profile_summary_fit(jd_text: str, experience_text: str) -> str:
    """
    Calls Gemini to generate a JD-tailored professional summary based on the
    candidate's actual resume experience.
    """
    formatted_prompt = REWRITE_SUMMARY.format(       # .formt() is ussed for interpolation is a string method
        jd_text=jd_text,
        experience_text=experience_text[:1500]
    )

    try:
        response = client.models.generate_content(
            model="gemini-3.6-flash",
            contents=formatted_prompt,
            config=types.GenerateContentConfig(temperature=0.3)
        )
        return response.text
    except Exception as e:
        return "The AI summary service is temporarily unavailable. Please try again in a moment."







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
    
def looks_like_header(line: str) -> bool:
    """Detects stray section-header fragments (e.g. 'TECHNICAL SKILLS') that
    shouldn't be treated as part of a bullet."""
    letters_only = re.sub(r'[^a-zA-Z]', '', line)
    if not letters_only:
        return False
    return letters_only.isupper() and len(letters_only) <= 30
            
def split_into_bullets(text:str) ->list[str]:   # it splits paragrapgh or multiple lines into single lines
    raw_lines = [line.strip() for line in text.splitlines() if line.strip()]
    lines = [line for line in raw_lines if not looks_like_header(line)]

    bullets = []
    for line in lines:
        starts_new_bullet = line[0] in ("•", "-", "*") or line[0].isupper()

        if starts_new_bullet or not bullets:
            bullets.append(line)
        else:
            bullets[-1] = bullets[-1] + " " + line

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
    