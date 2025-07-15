from dotenv import load_dotenv
import streamlit as st
import os
import base64
import fitz  # PyMuPDF
import google.generativeai as genai

# Load API Key
load_dotenv()
genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))

# Gemini Response Function
def get_gemini_response(input, pdf_content, prompt):
    model = genai.GenerativeModel('gemini-1.5-flash')
    response = model.generate_content([input, pdf_content[0], prompt])
    return response.text

# PDF Setup
def input_pdf_setup(uploaded_file):
    if uploaded_file is not None:
        pdf_document = fitz.open(stream=uploaded_file.read(), filetype="pdf")
        first_page = pdf_document.load_page(0)
        pix = first_page.get_pixmap()
        img_byte_arr = pix.tobytes()
        return [{
            "mime_type": "image/jpeg",
            "data": base64.b64encode(img_byte_arr).decode()
        }]
    else:
        raise FileNotFoundError("No file uploaded")

# Page Configuration
st.set_page_config(page_title="ATS Resume Expert", page_icon="🧠", layout="centered")

# Custom Styling
st.markdown("""
    <style>
        .main-title {
            text-align: center;
            font-size: 36px;
            font-weight: bold;
            color: #00BFFF;
        }
        .sub-title {
            text-align: center;
            font-size: 16px;
            color: #AAAAAA;
            margin-bottom: 30px;
        }
        .stTextArea textarea {
        background-color: var(--background-color) !important;
        color: var(--text-color) !important;
        font-size: 15px;
        border-radius: 8px;
        border: 1px solid var(--secondary-background-color);
        padding: 12px;
        }
        .stFileUploader {
        background-color: var(--background-color) !important;
        border: 1px solid var(--secondary-background-color) !important;
        border-radius: 8px;
        padding: 12px;
        }

        .stFileUploader label {
        color: var(--text-color) !important;
        font-weight: 500;
        }
        .css-1cpxqw2 {
            background-color: #262730 !important;
        }
    </style>
""", unsafe_allow_html=True)

# Title & Description
st.markdown('<div class="main-title">🚀 ATS Resume Analyzer</div>', unsafe_allow_html=True)
st.markdown('<div class="sub-title">Instantly compare your resume with job descriptions and get smart feedback.</div>', unsafe_allow_html=True)

st.divider()

# 📄 Job Description Input
st.markdown("### 📝 Job Description")
input_text = st.text_area(
    "Paste the job description below 👇",
    height=200,
    placeholder="e.g., We are looking for a Full Stack Developer with strong React and Node.js skills..."
)

# 📁 Resume Upload
st.markdown("### 📤 Upload Resume (PDF only)")
uploaded_file = st.file_uploader("Choose your resume PDF file", type=["pdf"])
if uploaded_file:
    st.success("✅ Resume uploaded successfully!")

st.divider()

# Custom CSS for button styling
st.markdown("""
    <style>
        .stButton > button {
            background-color: #00BFFF;
            color: white;
            font-size: 16px;
            padding: 0.6em 2em;
            border: none;
            border-radius: 8px;
            font-weight: bold;
            margin-top: 10px;
        }
        .stButton > button:hover {
            background-color: #009ACD;
            transition: 0.3s ease;
        }
    </style>
""", unsafe_allow_html=True)

# Center-aligned buttons
col1, col2, col3 = st.columns([1, 1, 1])

with col1:
    submit1 = st.button("🔍 Analyze Resume")
with col2:
    submit2 = st.button("📊 Match Percentage")


# Prompts
input_prompt_1 = """
You are a professional HR expert in tech hiring.
Evaluate this resume based on the provided job description. Highlight:
- Strengths of the candidate
- Weaknesses or missing areas
- Professional improvement tips
"""

input_prompt_2 = """
You're an expert technical recruiter.
Evaluate the resume against the job description and return:
1. Match percentage
2. Missing keywords or skills
3. Final summary and recommendation
Format clearly.
"""

# 🔍 Resume Analysis Logic
if submit1:
    if uploaded_file:
        with st.spinner("Analyzing your resume..."):
            pdf_content = input_pdf_setup(uploaded_file)
            response = get_gemini_response(input_prompt_1, pdf_content, input_text)
        st.success("✅ Resume Analysis Complete")
        st.markdown("### 💬 Expert Feedback")
        st.info(response)
    else:
        st.warning("⚠️ Please upload your resume to analyze.")

# 📊 Match Percentage Logic
if submit2:
    if uploaded_file:
        with st.spinner("Calculating match score..."):
            pdf_content = input_pdf_setup(uploaded_file)
            response = get_gemini_response(input_prompt_2, pdf_content, input_text)
        st.success("✅ Match Score Ready")
        st.markdown("### 📈 Results")
        st.success(response)
    else:
        st.warning("⚠️ Please upload your resume to calculate match percentage.")

# Footer
st.markdown("""
    <hr>
    <center style='color: grey; font-size: 13px;'>
        Built with ❤️ using Streamlit & Gemini | Smart ATS by Yashvardhan Sharma
    </center>
""", unsafe_allow_html=True)
