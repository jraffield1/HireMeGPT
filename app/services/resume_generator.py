import json
import re
from openai import OpenAI
from app.models.job_posting import JobPosting
from app.models.resume import JobEntry, Resume
from app.prompts import coverletter_prompt, resume_finetuning_prompt, resume_parse_prompt

GPT_MODEL = "gpt-4o-mini"

async def get_resume_suggestions(client: OpenAI, jobPosting: JobPosting, resume: Resume, extra_commands: str) -> Resume:
    suggestion_prompt = resume_finetuning_prompt(jobPosting, resume, extra_commands)

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

def _extract_json_text(response) -> str | None:
    """
    Your Responses API returns text at response.output[0].content[0].text in your current usage.
    This helper pulls that out and also attempts to grab the largest {...} block if needed.
    """
    try:
        text = response.output[0].content[0].text
    except Exception:
        return None

    # If the model already returned clean JSON, great. Otherwise, extract the biggest JSON object.
    text_stripped = text.strip()
    if text_stripped.startswith("{") and text_stripped.endswith("}"):
        return text_stripped

    match = re.search(r"\{(?:[^{}]|(?R))*\}", text_stripped, re.DOTALL)  # recursive-ish best effort
    if match:
        return match.group(0)
    return None

async def parse_freeform_resume_to_model(client: OpenAI, resume_text: str) -> Resume:
    """
    Calls the model with a strict JSON prompt and validates with Pydantic.
    Returns a fully-typed Resume (extra='forbid' will raise on unexpected keys).
    """
    prompt = resume_parse_prompt(resume_text)

    # Try JSON mode if available; if not, we still validate via Pydantic
    try:
        response = client.responses.create(
            model=GPT_MODEL,
            instructions="You are a strict JSON data extractor. Output ONLY valid JSON for the schema.",
            input=prompt
        )
    except Exception:
        # Fallback without response_format
        response = client.responses.create(
            model=GPT_MODEL,
            instructions="You are a strict JSON data extractor. Output ONLY valid JSON for the schema.",
            input=prompt,
        )

    json_text = _extract_json_text(response)
    if not json_text:
        raise ValueError("Failed to extract JSON from model response.")

    # Pydantic v2 convenience: validate from raw JSON string
    try:
        return Resume.model_validate_json(json_text)
    except Exception as e:
        # As a fallback, load then validate—also lets you inspect/clean if necessary
        try:
            data = json.loads(json_text)
        except Exception:
            raise ValueError(f"Model returned invalid JSON: {json_text[:400]}...") from e
        return Resume.model_validate(data)