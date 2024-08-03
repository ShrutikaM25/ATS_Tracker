from dotenv import load_dotenv
load_dotenv()
import streamlit as st
import os
import io
import base64
from PIL import Image
import pdf2image
import google.generativeai as genai

genai.configure(api_key = os.getenv("GOOGLE_API_KEY"))
poppler_path = r'C:\Program Files (x86)\poppler\Library\bin'

def get_gemini_response(input, pdf_content, prompt):
    model = genai.GenerativeModel('gemini-1.5-flash')
    response = model.generate_content([input, pdf_content[0], prompt])

    return response.text

def input_pdf_setup(uploaded_file):
    if uploaded_file is not None:
        ## convert pdf to image
        images = pdf2image.convert_from_bytes(uploaded_file.read(), poppler_path=poppler_path)

        first_page = images[0]

        img_byte_arr = io.BytesIO()
        first_page.save(img_byte_arr, format="JPEG")
        img_byte_arr = img_byte_arr.getvalue()

        pdf_part = [
            {
                "mime_type": "image/jpeg",
                "data": base64.b64encode(img_byte_arr).decode() ## convert to encode base64
            }
        ]

        return pdf_part
    else:
        raise FileNotFoundError("No files uploaded")


#STREAMLIT UI

st.set_page_config(page_title="ATS Resume Expert")
st.header("ATS Tracking system")
input_text = st.text_area("Job Description: ", key="input")
uploaded_file = st.file_uploader("Upload your Resume(PDF)...", type=["pdf"])

if uploaded_file is not None:
    st.write("File uploaded successfully")

submit1 = st.button("Tell me About the Resume")
submit3 = st.button("Percentage Match")

input_prompt1 = """
You are an experienced HR with Tech Experience in the field of any one job role from Data Science, Full stack Web development, Big Data Engineering,
DEVOPS, Data Analyst your task is to review the provided resume against the job description for these profiles.
Please share your professional evaluation on whether the candidate's profile aligns with the role.
Highlight the strengths and weaknesses of the applicant in relation to the specified job requirements.
"""

input_prompt3 = """
You are a skilled ATS (Application Tracking System) scanner with a deep understanding of any one job role from Data Science, Full stack Web development 
Big Data Engineering, DEVOPS, Data Analyst and deep ATS Functionality, your task is to evaluate the resume against the provided job description. Give me the percentage 
of match if the resume matches the job description. First the output should come as percentage and then keywords missing and last final thoughts.
"""

if submit1:
    if uploaded_file is not None:
        pdf_content = input_pdf_setup(uploaded_file)
        response = get_gemini_response(input_prompt1, pdf_content, input_text)
        st.subheader("The Response is: ")
        st.write(response)
    else:
        st.write("Please upload the resume")
elif submit3:
    if uploaded_file is not None:
        pdf_content = input_pdf_setup(uploaded_file)
        response= get_gemini_response(input_prompt3, pdf_content, input_text)
        st.subheader("The Response is: ")
        st.write(response)
    else:
        st.write("Please upload the resume")
