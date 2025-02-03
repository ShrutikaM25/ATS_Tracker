from dotenv import load_dotenv
load_dotenv()
import streamlit as st
import os
import io
import base64
from PIL import Image
import pdf2image
import google.generativeai as genai

genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))

def apply_custom_css():
    st.markdown("""
        <style>
            
            /* Header Styles */
            .main-header {
                background: linear-gradient(135deg, #2A4365, #1A365D);
                color: white;
                padding: 2rem;
                border-radius: 15px;
                margin-bottom: 2rem;
                box-shadow: 0 4px 20px rgba(0, 0, 0, 0.1);
                display: flex;
            }
            
            
            .feature-card {
                padding: 1.5rem;
                border-radius: 12px;
                box-shadow: 0 4px 15px rgba(0, 0, 0, 0.05);
                transition: transform 0.3s ease, box-shadow 0.3s ease;
                cursor: pointer;
                border: 1px solid rgba(0, 0, 0, 0.05);
            }
            
            .feature-card:hover {
                transform: translateY(-5px);
                box-shadow: 0 8px 25px rgba(0, 0, 0, 0.1);
            }
            
            /* Upload Section Styles */
            .upload-section {
                padding: 2rem;
                border-radius: 15px;
                box-shadow: 0 4px 15px rgba(0, 0, 0, 0.05);
                margin: 2rem 0;
            }
            
            /* Button Styles */
            .custom-button {
                background: linear-gradient(135deg, #4299E1, #2B6CB0);
                color: white;
                margin-top: 2.5rem;
                margin-left: 27rem;
                padding: 0.75rem 1.5rem;
                border-radius: 8px;
                border: none;
                box-shadow: 0 4px 15px rgba(66, 153, 225, 0.3);
                transition: all 0.3s ease;
            }
            .custom-button:hover {
                background: linear-gradient(135deg, #2B6CB0, #4299E1);
                transform: translateY(-2px);
                box-shadow: 0 6px 20px rgba(66, 153, 225, 0.4);
            }
            
            /* Response Section Styles */
            .response-section {
                background: white;
                padding: 2rem;
                border-radius: 15px;
                box-shadow: 0 4px 15px rgba(0, 0, 0, 0.05);
                margin-top: 2rem;
            }
            
            /* Success Message Styles */
            .success-message {
                background: linear-gradient(135deg, #48BB78, #38A169);
                color: white;
                padding: 1rem;
                border-radius: 8px;
                margin: 1rem 0;
            }
            
            /* Loading Spinner Styles */
            .stSpinner {
                border-color: #4299E1;
            }
        </style>
    """, unsafe_allow_html=True)

def get_gemini_response(input, pdf_content, prompt):
    model = genai.GenerativeModel('gemini-1.5-flash')
    response = model.generate_content([input, pdf_content[0], prompt])
    return response.text

def input_pdf_setup(uploaded_file):
    if uploaded_file is not None:
        images = pdf2image.convert_from_bytes(uploaded_file.read())
        first_page = images[0]

        img_byte_arr = io.BytesIO()
        first_page.save(img_byte_arr, format="JPEG")
        img_byte_arr = img_byte_arr.getvalue()

        pdf_part = [
            {
                "mime_type": "image/jpeg",
                "data": base64.b64encode(img_byte_arr).decode()
            }
        ]

        return pdf_part
    else:
        raise FileNotFoundError("No files uploaded")
    

# STREAMLIT UI
def main():
    # st.set_page_config(page_title="ATS Tracking System", page_icon="📄", layout="wide")

    apply_custom_css()

    st.markdown("""
            <div class="main-header">
            <div>
                <h1 style="font-size: 2.5rem; margin-bottom: 1rem;">ATS Tracking System</h1>
                <p style="font-size: 1.2rem; opacity: 0.9;">Optimize your resume with AI-powered insights</p>
            </div>
            <div>
                <button class="custom-button" onclick="window.location.reload();">🔙 Back to Dashboard</button>
            </div>
        </div>
    """, unsafe_allow_html=True)

    st.subheader("Optimize your resume for ATS and get personalized feedback")
    st.markdown("### 🔍 **Select a Feature to Get Started**")

    features = {
        "📄 Resume Analysis": "Get comprehensive feedback on your resume",
        "📊 Match Score": "See how well your resume matches the job",
        "🛠️ Skill Analysis": "Identify skill gaps and improvements",
        "📌 Job Fit": "Evaluate your fit for the role",
        "📂 ATS Format": "Optimize format for ATS systems",
        "🔑 Keywords": "Optimize resume keywords",
        "🎯 Role Suggestions": "Discover alternative career paths",
        "📉 Benchmarking": "Compare against other candidates",
        "😊 Tone Analysis": "Assess your resume's tone",
        "💬 Interview Prep": "Generate practice questions",
        "🔗 LinkedIn Import": "Import your LinkedIn profile",
        "📅 Application Tracker": "Track your job applications",
        "❓ Custom Analysis": "Ask specific questions"
    }

    # Display features in a 3-column grid
    # cols = st.columns(5)
    # for idx, feature in enumerate(features):
    #     with cols[idx % 5]:
    #         if st.button(feature, key=f"feature_{idx}"):
    #             st.session_state["selected_feature"] = feature

    # selected_feature = st.session_state.get("selected_feature", None)

    st.markdown("### Select a Feature")

    cols = st.columns(4)
    for idx, (feature, desc) in enumerate(features.items()):
        with cols[idx % 4]:
            if st.button(
                feature,
                key=f"feature_{idx}",
                help=desc,
                use_container_width=True
            ):
                st.session_state["selected_feature"] = feature

# Upload Section
    st.markdown("""
        <div class="upload-section">
            <h3>📤 Upload Your Documents</h3>
        </div>
    """, unsafe_allow_html=True)

    uploaded_file = st.file_uploader("Upload your Resume (PDF):", type=["pdf"], key="upload_file_main")
    input_text = st.text_area("Job Description:", key="input_text")

    if uploaded_file:
        st.markdown("""
            <div class="success-message">
                ✅ Resume uploaded successfully!
            </div>
        """, unsafe_allow_html=True)        
        pdf_content = input_pdf_setup(uploaded_file)

        prompts = {
            "📄 Tell me About the Resume": """
                You are an experienced HR with Tech Experience in Data Science, Full Stack Web Development, Big Data Engineering,
                DevOps, or Data Analysis. Review the resume against the job description and provide professional evaluation.
                Highlight strengths and weaknesses in relation to job requirements.
            """,
            "📊 Percentage Match": """
                As an ATS scanner, evaluate the resume against the job description. 
                Provide a match percentage, list missing keywords, and share final thoughts.
            """,
            "🛠️ Skill Gap Analysis": """
                Identify missing skills in the resume compared to the job description and suggest relevant courses or certifications.
            """,
            "📌 Job Fit Prediction": """
                Analyze the resume and job description to predict how well the candidate fits the role and company culture.
            """,
            "📂 ATS-optimized Formatting": """
                Evaluate the resume formatting and suggest improvements for better ATS compatibility.
            """,
            "🔑 Resume Keyword Optimization": """
                Analyze missing or weak keywords in the resume compared to the job description.
            """,
            "🎯 Job Role-based Suggestions": """
                Suggest alternative job roles that might be a better fit based on the resume.
            """,
            "📉 Benchmarking Against Competitors": """
                Compare the candidate's resume to other applicants and provide insights into skills and experience.
            """,
            "😊 Emotional Tone Assessment": """
                Analyze the resume's emotional tone and suggest ways to improve the conveyed personality.
            """,
            "💬 Generate Interview Questions": """
                Generate potential interview questions based on the resume and job description.
            """,
            "❓ Custom Query": """
                Provide a custom analysis based on the user’s query related to the uploaded PDF.
            """
        }

        selected_feature = st.session_state.get("selected_feature", None)

        if selected_feature and selected_feature in prompts:
            prompt = prompts[selected_feature]

            if st.button(f"Analyze with {selected_feature}", key="run_analysis", use_container_width=True):
                with st.spinner('Processing your request...'):
                    response = get_gemini_response(input_text, pdf_content, prompt)            
                st.subheader(f"{selected_feature} Result:")
                st.markdown(f"""
                    <div class="response-section">
                        <h3>{selected_feature} Results</h3>
                        <div style="margin-top: 1rem;">
                            {response}
                        </div>
                    </div>
                """, unsafe_allow_html=True)
        elif selected_feature == "❓ Custom Query":
            custom_query = st.text_area("Enter your custom query:", key="custom_query_input")
            if st.button("Submit Query", key="submit_custom_query"):
                with st.spinner('Processing...'):
                    response = get_gemini_response(input_text, pdf_content, custom_query)
                st.subheader("Response to Your Query:")
                st.markdown(f"""
                    <div class="response-section">
                        <h3>{selected_feature} Results</h3>
                        <div style="margin-top: 1rem;">
                            {response}
                        </div>
                    </div>
                """, unsafe_allow_html=True)
    else:
        st.info("Please upload a resume to get started.")



if __name__ == "__main__":
    main()
