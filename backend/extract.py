# this file pulls raw text from file , extract_pdf give resume text from pdf while extract_docx gives text from doc file 
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


# it is guard rail that controls execution ,it prevents specific code block automatically when file is imported 
# in another file until when the script is executed directly . 
# like here if i will import this file into some other file it won't run the code below if line becuase it prevents it 
#. as we can see also that this is testing code that i am using the function on random file for other import or on site it may crash.
# so if __name__="__main__" means this code will be executed when directly ruuned during testing.

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
    