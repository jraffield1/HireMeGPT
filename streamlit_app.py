import base64
from datetime import datetime
import streamlit as st
from app.models.job_posting import JobPosting
from app.models.resume import JobEntry, Resume
import asyncio

from app.services.job_scaper import extract_job_posting
from app.services.resume_generator import get_resume_coverletter, get_resume_suggestions, parse_freeform_resume_to_model
from app.services.resume_renderer import generate_coverletter_pdf, generate_resume_pdf

from dotenv import load_dotenv
from openai import OpenAI
import os

from app.templates import resumes

load_dotenv()
api_key = os.getenv("OPENAI_API_KEY")
client = OpenAI(api_key=api_key)

st.set_page_config(page_title="HireMeGPT", layout="wide")
st.title("HireMeGPT")

# --- Initialize resume session state ---
if "resume" not in st.session_state:
    st.session_state.resume = resumes.originalResume.model_copy()
    st.session_state.edited_resume = resumes.originalResume.model_copy()

# --- Input: Job posting URL or description ---
job_url = st.text_input("Paste a job posting URL to tailor your resume:")
job_text = st.text_area("Or paste the full job description here:", height=200)

user_resume_text = st.text_area(
    "Tell us about your work experience (paste bullets, accomplishments, tech stack, etc.)",
    key="user_resume_text",
    height=150,
    help="This goes straight to the model to improve tailoring."
)

extra_commands = st.text_area("Additional commands to tweak resume", height=200)

if ((job_url or job_text) and user_resume_text) and st.button("Tailor Resume"):
    try:
        parsed_resume = asyncio.run(parse_freeform_resume_to_model(client, user_resume_text))

        st.session_state.resume = parsed_resume
        st.session_state.edited_resume = parsed_resume

        job_posting = asyncio.run(extract_job_posting(client, job_url, job_text))
        updated_resume = asyncio.run(get_resume_suggestions(client, job_posting, st.session_state.resume, extra_commands))
        st.session_state.edited_resume = updated_resume
        st.session_state.job_posting = job_posting

        cover_letter = asyncio.run(get_resume_coverletter(client, job_posting, updated_resume))
        st.session_state.cover_letter = cover_letter

        st.success("Resume tailored and PDFs generated!")

        # Generate PDFs
        resume_pdf = generate_resume_pdf(updated_resume)
        cover_pdf = generate_coverletter_pdf(cover_letter, updated_resume)

        today = datetime.now().strftime("%Y-%m-%d")
        company = job_posting.company_name.replace(" ", "_")
        st.session_state.resume_filename = f"{today}_{company}_resume.pdf"
        st.session_state.cover_filename = f"{today}_{company}_cover.pdf"
        st.session_state.resume_pdf = resume_pdf
        st.session_state.cover_pdf = cover_pdf

    except Exception as e:
        st.error(f"Error tailoring resume: {e}")

# --- Show editor and previews only if tailored ---
if "job_posting" in st.session_state and "edited_resume" in st.session_state:
    resume = st.session_state.edited_resume

    left, right = st.columns([3, 2])

    with left:
        st.subheader("Headline")
        headline = st.text_input("Headline", value=resume.headline)

        st.subheader("Summary")
        summary = st.text_area("Professional Summary", value=resume.summary, height=150)

        st.subheader("Technical Skills")
        technical_skills_input = st.text_area(
            "Comma-separated skills", value=", ".join(resume.technical_skills)
        )
        technical_skills = [s.strip() for s in technical_skills_input.split(",") if s.strip()]

        st.subheader("Core Competencies")
        core_competencies_input = st.text_area(
            "Comma-separated competencies", value=", ".join(resume.core_competencies)
        )
        core_competencies = [s.strip() for s in core_competencies_input.split(",") if s.strip()]

        st.subheader("Work Experience")
        updated_jobs = []
        for i, job in enumerate(resume.work_experience):
            with st.expander(f"{job.title} at {job.company}"):
                title = st.text_input("Title", value=job.title, key=f"title_{i}")
                company = st.text_input("Company", value=job.company, key=f"company_{i}")
                location = st.text_input("Location", value=job.location, key=f"loc_{i}")
                dates = st.text_input("Dates", value=job.dates, key=f"dates_{i}")
                description_input = st.text_area("Bullet points", value="\n".join(job.description), key=f"desc_{i}")
                description = [line.strip() for line in description_input.split("\n") if line.strip()]

                updated_jobs.append(
                    JobEntry(
                        title=title,
                        company=company,
                        location=location,
                        dates=dates,
                        description=description
                    )
                )

        st.subheader("Cover Letter")
        cover_letter_text = st.session_state.get("cover_letter", "")
        st.session_state.cover_letter = st.text_area(
            "Edit Cover Letter Below", value=cover_letter_text, height=300
        )

        # Update session state resume
        new_resume = Resume(
            full_name=resume.full_name,
            email=resume.email,
            phone=resume.phone,
            linkedin=resume.linkedin,
            location=resume.location,
            headline=headline,
            summary=summary,
            technical_skills=technical_skills,
            core_competencies=core_competencies,
            work_experience=updated_jobs,
            education=resume.education
        )

        # Compare and regenerate if needed
        if new_resume != st.session_state.edited_resume or st.session_state.cover_letter != st.session_state.get("last_cover_text", ""):
            st.session_state.edited_resume = new_resume
            st.session_state.resume_pdf = generate_resume_pdf(new_resume)

            current_cover = st.session_state.cover_letter
            st.session_state.cover_pdf = generate_coverletter_pdf(current_cover, new_resume)
            st.session_state.last_cover_text = current_cover

    with right:
        st.subheader("Resume Preview")
        if "resume_pdf" in st.session_state:
            st.download_button(
                label="Download Resume",
                data=st.session_state.resume_pdf,
                file_name=st.session_state.resume_filename,
                mime="application/pdf"
            )
            
            base64_pdf = base64.b64encode(st.session_state.resume_pdf).decode("utf-8")
            pdf_display = f"""
                <div style="width: 100%; height: 1000px;">
                    <embed src="data:application/pdf;base64,{base64_pdf}" type="application/pdf" width="100%" height="100%">
                </div>
            """
            st.markdown(pdf_display, unsafe_allow_html=True)

        st.subheader("Cover Letter Preview")
        if "cover_pdf" in st.session_state:
            st.download_button(
                label="Download Cover Letter",
                data=st.session_state.cover_pdf,
                file_name=st.session_state.cover_filename,
                mime="application/pdf"
            )
            #pdf_viewer(st.session_state.cover_pdf, width=700)
            base64_pdf = base64.b64encode(st.session_state.cover_pdf).decode("utf-8")
            pdf_display = f"""
                <div style="width: 100%; height: 1000px;">
                    <embed src="data:application/pdf;base64,{base64_pdf}" type="application/pdf" width="100%" height="100%">
                </div>
            """
            st.markdown(pdf_display, unsafe_allow_html=True)
