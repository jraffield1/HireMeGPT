from datetime import datetime
from pathlib import Path
import streamlit as st
from app.models.resume import JobEntry, Resume
import asyncio

from app.services.job_scaper import extract_job_posting
from app.services.resume_generator import get_resume_coverletter, get_resume_suggestions
from app.services.resume_renderer import generate_coverletter_pdf, generate_resume_pdf

from dotenv import load_dotenv
from openai import OpenAI
import os

from app.templates import resumes

load_dotenv()
api_key = os.getenv("OPENAI_API_KEY")
client = OpenAI(api_key=api_key)

st.set_page_config(page_title="HireMeGPT", layout="centered")
st.title("🧠 HireMeGPT")

# --- Upload resume or load dummy ---
if "resume" not in st.session_state:
    st.session_state.resume = resumes.originalResume.model_copy()
    st.session_state.edited_resume = resumes.originalResume.model_copy()

resume = st.session_state.edited_resume

# --- Input: Job posting URL ---
job_url = st.text_input("Paste a job posting URL to tailor your resume:")
job_text = st.text_area("Or paste the full job description here:", height=200)

if (job_url or job_text) and st.button("Tailor Resume"):
    job_posting = asyncio.run(extract_job_posting(client, job_url, job_text))
    updated_resume = asyncio.run(get_resume_suggestions(client, job_posting, st.session_state.resume))
    st.session_state.edited_resume = updated_resume
    st.session_state.job_posting = job_posting

    cover_letter = asyncio.run(get_resume_coverletter(client, job_posting, updated_resume))
    st.session_state.cover_letter = cover_letter

    st.success("Resume updated!")

resume = st.session_state.edited_resume

# --- Edit Sections ---
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

# --- Work Experience ---
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

# --- Cover Letter Section ---
st.subheader("📄 Cover Letter")

cover_letter_text = st.session_state.get("cover_letter", "")
st.session_state.cover_letter = st.text_area(
    "Edit Cover Letter Below", value=cover_letter_text, height=300
)

# --- Update Resume in session state ---
st.session_state.edited_resume = Resume(
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

# --- Generate PDF ---
if st.button("📄 Generate & Save"):
    with st.spinner("Generating documents..."):
        resume_pdf = generate_resume_pdf(st.session_state.edited_resume)
        cover_pdf = generate_coverletter_pdf(st.session_state.cover_letter, st.session_state.edited_resume)

        today = datetime.now().strftime("%Y-%m-%d")
        company = st.session_state.job_posting.company_name.replace(" ", "_")

        base_dir = "/mnt/c/Users/jhraf/OneDrive/Desktop/Job Search/"

        resume_path = base_dir + f"Raffield_resume_{company}_{today}.pdf"
        cover_path = base_dir + f"Raffield_coverletter_{company}_{today}.pdf"

        with open(resume_path, "wb") as f:
            f.write(resume_pdf)

        with open(cover_path, "wb") as f:
            f.write(cover_pdf)

    st.success("Saved!")
