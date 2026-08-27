import re 
SECTION_HEADERS = ["experience","work experience","professional experience","objectives","certifications","summary","technical skills",
                   "skills","education","projects","achievements","publications","awards","interests","languages","references"]


def normalise_text(text: str)  ->str:
    text = text.lower()
    text=re.sub(r'\s+','',text)
    return text.strip()


def split_into_sections(text: str) ->dict:
    lines= text.split("\n")
    sections={}
    current_section = "header"
    buffer=[]
    
    for line in lines:
        clean_line=line.strip().lower()
        matched_header=None
        for header in SECTION_HEADERS:
            if clean_line == header or clean_line.startswith(header):
                matched_header=header
                break
        if matched_header:
            sections[current_section] ="\n".join(buffer).strip()
            current_section=matched_header
            buffer=[]
        else:
            buffer.append(line)
    sections[current_section] ="\n".join(buffer).strip()
    return sections    