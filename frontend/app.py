
import streamlit as st 
import requests
import os

BACKEND_URL = os.environ.get("BACKEND_URL", "http://127.0.0.1:8000")
st.title("YOUR RESUME ANALYSER")
st.write("Upload your resume and JD to get a ATS score & improved bullet points.")
resume_file= st.file_uploader("Uplaod your resume", type=["pdf","docx"])
jd_text = st.text_area("Paste your JD here ", height=250)

if st.button("Analyzer"):
    if resume_file is None or not jd_text.strip():
        st.error("Please upload a resume and a JD")
    else:
        with st.spinner("Anlaysing... your resume"):
            files={"resume":(resume_file.name,resume_file.getvalue())}
            data={"jd_text": jd_text}
            
            response= requests.post(f"{BACKEND_URL}/analyze",files=files,data=data)
            
            
            if response.status_code==200:
                result= response.json()
                st.success("Analysis complete!")
                
                if "error" in result:
                    st.error(result["error"])
                else: 
                    st.subheader("ATS Score")
                    st.write(f"Score: {result['ats_score']}%")
                    st.progress(result["ats_score"]/100)
                    col1, col2 = st.columns(2)
                    with col1:
                        st.write("**Matched keywords**")
                        st.write(result["matched_keywords"])
                    with col2:
                        st.write("**Missing Keywords**")
                        st.write(result["missing_keywords"])
                        
                    st.subheader("AI-Improved bullet points")
                    st.markdown(result["improved_bullets"])
            else:
                st.error(f"something went wrong: {response.status_code}")
                    
                    
                    