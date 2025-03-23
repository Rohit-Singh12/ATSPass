import streamlit as st
import requests
import os

from DocumentReader import DocumentReader

# Backend API URL (Replace with your actual API endpoint)
API_URL = "http://fastapi:8000/process_resume/"
FILE_PATH = ""

# Function to extract text from PDF
def write_to_location(uploaded_file):
    global FILE_PATH  # Use the global variable
    _, file_extension = os.path.splitext(uploaded_file.name)
    os.makedirs("/app/UploadedResumes", exist_ok=True)
    FILE_PATH = f'/app/UploadedResumes/resume{file_extension}'
    print(FILE_PATH)
    with open(FILE_PATH, "wb") as f:
        f.write(uploaded_file.getbuffer())

# Streamlit UI
st.title("📄 ATS Resume Scoring System")
st.markdown("Upload your resume and enter a job description to get an ATS score.")

# Upload resume
uploaded_file = st.file_uploader("Upload Resume (PDF/TXT)", type=["pdf", "doc", "txt"])

# Job description input
job_description = st.text_area("Enter Job Description", height=200)

# Submit button
if st.button("Analyze Resume"):
    if uploaded_file is None or not job_description.strip():
        st.warning("Please upload a resume and enter a job description.")
    else:
        with st.spinner("⏳ Please wait... Processing resume..."):
            # Extract text from file
            try:
                print("FILE PATH " + FILE_PATH)
                write_to_location(uploaded_file)
                resume_text = DocumentReader(FILE_PATH).read_document()

                # Prepare API request
                payload = {"resume": resume_text, "job_desc": job_description}
                response = requests.post(API_URL, json=payload)
                print("Processing resume....", response)

                # Display results
                if response.status_code == 200:
                    result = response.json()
                    st.success(f"✅ **ATS Score:** {result['ats_score']}%")
                    st.subheader("💡 Resume Feedback:")
                    st.markdown(result["feedback"])
                else:
                    st.error("❌ Error processing the request. Please try again.")
                if os.path.exists(FILE_PATH):
                    os.remove(FILE_PATH)
            except Exception as ex:
                print(ex)
                st.error(f"❌ {ex}")
                if os.path.exists(FILE_PATH):
                    os.remove(FILE_PATH)
