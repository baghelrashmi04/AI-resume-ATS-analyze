
from extract import extract_pdf , extract_docx
from preprocess import normalise_text, split_into_sections
import spacy
import re

nlp = spacy.load("en_core_web_sm")


STOPWORD_PHRASES= {
    "the ideal candidate","our team","year of experience","a plus ","this role","the company"
}
mini_key= 3
generic_junk={
    "knowlege","familiarity", "experience", "qualification",
    "willingness", "any graduate", "new technologies",
    "good communication", "basic understanding", "preferred skills",
    "required skills"
}

def clean_phrase(phrase:str) ->str:
    parts= re.split(r'[•\n]',phrase)
    cleaned=[]
    for part in parts:
        part=re.sub(r'\s+', ' ', part).strip(":.-")
        if len(part) >= mini_key and part not in generic_junk:
            cleaned.append(part)
    return cleaned
def extract_keywords(jd_text:str) ->list[str]:      
    doc= nlp(jd_text)
    keywords=set()
    
    for chunk in doc.noun_chunks:        #noun chunks
        phrase= chunk.text.strip().lower()
        if phrase not in STOPWORD_PHRASES:
            for cleaned in clean_phrase(phrase):
                
                    keywords.add(cleaned)
        #if len(phrase) > 2 and phrase not in STOPWORD_PHRASES:
          #  keywords.add(phrase)
    
    for ent in doc.ents:
        if ent.label_ in ("ORG","PRODUCT","LANGUAGE"):
            for cleaned in clean_phrase(ent.text.strip().lower()):
                keywords.add(cleaned)
            #keywords.add(ent.text.strip().lower())
            
    return sorted(keywords)    
if __name__=="__main__":
  with open("note.txt","r",encoding="utf-8") as f:
    jd_text=f.read()
    
  jd_keywords=extract_keywords(jd_text)
  print("----KEYWORD EXTRACTION ----------")
  print(jd_keywords)

  print("-----LENGTH:",len(jd_keywords),"keywords------")
  print("------------------------------")