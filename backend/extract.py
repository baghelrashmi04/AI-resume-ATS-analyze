
import pdfplumber 
from docx import Document

def extract_pdf(filepath: str) ->str:
    text=""
    with pdfplumber.open(filepath) as pdf:
        for page in pdf.pages:
            page_text=page.extract_text()
            if page_text:
                text += page_text + "\n"
    return text


def extract_docx(filepath: str) ->str:
    doc=Document(filepath)
    return "\n".join(para.text for para in doc.paragraphs)

if __name__=="__main__":
    pdf_text = extract_pdf("vijay_resume.pdf")
    print("--PDF--EXTRACTION--")
    print(pdf_text)
    print("--LENGTH:", len(pdf_text),"chars ----")
    print("----------------------------------------------------------------------")
    docx_test= extract_docx("resume.docx")
    print("--DOCX--EXTRACTION--")
    print(docx_test)
    print("--LENGTH:", len(docx_test))
    