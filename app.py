from dotenv import load_dotenv
import streamlit as st
import os
import io
import base64
import fitz
import google.generativeai as genai

load_dotenv()

genai.configure(api_key = os.getenv("GOOGLE_API_KEY"))

def get_gemini_response(input , pdf_content, prompt) -> None:
    model = genai.GenerativeModel('gemini-1.5-flash')
    response = model.generate_content([input , pdf_content[0], prompt])
    return response.text

def input_pdf_setup(uploaded_file) -> None:
    if uploaded_file is not None:
        ## open the pdf with pymupdf
        pdf_document = fitz.open(stream = uploaded_file.read(), filetype= "pdf")

        #extract the first page
        first_page = pdf_document.load_page(0)

        ## convert the page into images
        pix = first_page.get_pixmap()
        img_byte_arr = pix.tobytes()

        #encode to base64

        pdf_parts =[
        {"mime_type": "image/jpeg",
         "data":base64.b64encode(img_byte_arr).decode()}
        ]   
        return pdf_parts
    
    else:
        raise FileNotFoundError("No file Uploaded")

## using Stramlit we will make ui
st.set_page_config(page_title="My intelligent ATS Resume Expert")
st.header("My Intelligent ATS Expert")
input_text = st.text_area("Job Descriptor: ", key = "input")
uploaded_file = st.file_uploader("Upload Resume(PDF)", type=["pdf"])

if uploaded_file is not None:
    st.write("PDF uploaded Successfully....")

submit1 = st.button("Tell me About the Resume")
submit2 = st.button("Percentage Match")

input_prompt_1 = """
You are an experienced HR with Tech Experience in the filed of any one job role from data science, Full Stack, Web Development, Big Data Engoneering, Devops, Data Analyst. 
Your task is to review the provided resume against the job description for these profiles.
Please share the professional evaluation on whether the candidate's profile align with the Highlight the strengths and weakness of the applicant in the relation to the specified job role.
"""


input_prompt_2 = """
You are an experienced HR with Tech Experience in the filed of any one job role from data science, 
Full Stack, Web Development, Big Data Engoneering, Devops, Data Analyst. 
Your task is to review the provided resume against the job description for these profiles.
your task is to evaluate the resume against the provided job description.
Give me the percentage of match if the resume matches the job description.
first the output should come as percentage, then keywords missing and last final.
"""

if submit1:
    if uploaded_file is not None:
        pdf_content = input_pdf_setup(uploaded_file)
        response = get_gemini_response(input_prompt_1, pdf_content, input_text)
        st.subheader("The Response is: ")
        st.write(response)

    else: 
        st.write("Please Upload the Resume")

if submit2:
    if uploaded_file is not None:
        pdf_content = input_pdf_setup(uploaded_file)
        response = get_gemini_response(input_prompt_2, pdf_content, input_text)
        st.subheader("The Response is: ")
        st.write(response)

    else: 
        st.write("Please Upload the Resume")