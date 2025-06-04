import json
import re
from openai import OpenAI
from app.models.job_posting import JobPosting
from app.models.resume import JobEntry, Resume
from app.prompts import coverletter_prompt, resume_finetuning_prompt

GPT_MODEL = "gpt-4o-mini"

async def get_resume_suggestions(client: OpenAI, jobPosting: JobPosting, resume: Resume) -> Resume:
    suggestion_prompt = resume_finetuning_prompt(jobPosting, resume)

    response = client.responses.create(
        model=GPT_MODEL,
        instructions="You are an applicant tracking system and an expert resume analyst",
        input=suggestion_prompt
        )

    parsed = None
    match = re.search(r"\{.*\}", response.output[0].content[0].text, re.DOTALL)
    if match:
        parsed = json.loads(match.group(0))

    print(f"created new resume for {jobPosting.job_title}")

    return Resume(
        full_name=resume.full_name,
        email=resume.email,
        phone=resume.phone,
        linkedin=resume.linkedin,
        location=resume.location,
        headline=jobPosting.job_title,
        summary=parsed["summary"],
        technical_skills=parsed["technical_skills"],
        core_competencies=parsed["core_competencies"],
        work_experience=[
            JobEntry(
                title=original.title,
                company=original.company,
                location=original.location,
                dates=original.dates,
                description=j.get("description"),
            )
            for j, original in zip(parsed["work_experience"], resume.work_experience)
        ],
        education=resume.education,
    )

async def get_resume_coverletter(client: OpenAI, jobPosting: JobPosting, resume: Resume) -> str:
    suggestion_prompt = coverletter_prompt(jobPosting, resume)

    response = client.responses.create(
        model=GPT_MODEL,
        instructions="You are an applicant tracking system and an expert resume analyst",
        input=suggestion_prompt
        )
    
    return response.output[0].content[0].text