
from extract import extract_pdf , extract_docx
from preprocess import normalise_text, split_into_sections

resume_text= extract_pdf("Rashmiii_s__ML_Resume.pdf")


normalised = normalise_text(resume_text)
print("-----NORMALISED-----")
print(normalised[:500])  # just taking 500 words m not dumping all 


sections= split_into_sections(resume_text)
print("-----SECTIONS-----")
for section, content in sections.items():
    print(f"Section: {section}")
    print(f"Content: {content[:200]}")  # just taking 200 words m not dumping all 
    print("--------------------------------------------------")
