from app.models.job_posting import JobPosting
from app.models.resume import JobEntry, Resume


def job_scrape_prompt(webdata: str) -> str: 
    return f"""Below is the full visible text of a job posting scraped from a website.
    Extract the following fields in **valid JSON format**:

    - job_title: string
    - company_name: string or null
    - job_description: string (a concise paragraph summarizing the role’s duties and responsibilities)
    - required_qualifications: list of strings
    - preferred_qualifications: list of strings

    ❗ All fields must be flat. Do not nest dictionaries inside fields.
    ❗ job_description must be a paragraph string, not a dictionary or list.

    Only return JSON. Do not include explanations or formatting outside the JSON.

    Job Posting Text:
    <<<
    {webdata}
    >>>
    """

def format_experience_for_prompt(jobs: list[JobEntry]) -> str:
    return "\n\n".join(
        f"{job.title} at {job.company} ({job.dates})\n" +
        "\n".join(f"- {b}" for b in job.description)
        for job in jobs
    )

def resume_finetuning_prompt(job: JobPosting, resume: Resume, extra_commands: str) -> str:
    return f"""
    Given a job description and a candidate's resume, revise the resume to align with the job while being truthful and emphasizing real strengths.
    Make this resume as strong as you can for this position.
    Don't be too wordy with the job experience descriptions but try to pepper them with meaningful metrics

    Extra overriding commands: {extra_commands}

    Here is the job description:
    <<<
    Title: {job.job_title}
    Company: {job.company_name or 'Unknown'}
    Location: {job.job_location or 'Unlisted'}

    Summary:
    {job.job_description}

    Required Qualifications:
    {', '.join(job.required_qualifications)}

    Preferred Qualifications:
    {', '.join(job.preferred_qualifications)}
    >>>

    Here is the candidate's current resume:
    <<<
    Summary:
    {resume.summary}

    Technical Skills:
    {', '.join(resume.technical_skills)}

    Core Competencies:
    {', '.join(resume.core_competencies)}

    Work Experience:
    {format_experience_for_prompt(resume.work_experience)}
    >>>

    Return updated fields in valid JSON format with these keys:
    - summary: str 4–5 sentence version rewritten for this job
    - technical_skills: list[str] revised list of real skills most relevant to this job
    - core_competencies: list[str] updated strengths that match the job needs
    - work_experience: 4-5 updated bullet points per job that highlight relevant value: list of dictionaries, where each dictionary has:
        - title: str
        - company: str
        - location: str
        - dates: str
        - description: list[str]
    """

def coverletter_prompt(job: JobPosting, resume: Resume) -> str:
    return f"""
    You are an expert job application assistant. Write a tailored cover letter for the following job.

    --- Job Title ---
    {job.job_title}

    --- Job Description ---
    {job.job_description}

    --- Resume Summary ---
    Name: {resume.full_name}
    Headline: {resume.headline}
    Summary: {resume.summary}
    Most Recent Job: {resume.work_experience[0].title} at {resume.work_experience[0].company}
    Technical Skills: {', '.join(resume.technical_skills)}
    Core Competencies: {', '.join(resume.core_competencies)}

    The tone should be professional, enthusiastic, and specific. The letter should reference details from the job and align with the candidate's strengths.
    Follow this structure:
    1. Introduce yourself and greet the reader
    In the first sentence of your cover letter, you can clarify your reason for writing by specifying the position for which you're applying. You can detail who you are by explaining your role and how much experience you have in it. This paragraph can include information about your specializations or interests within software engineering and how they apply to the role you want.Related: How To Write a Cover Letter: Top 3 Tips, Format & Examples [Video + Transcript]
    2. Detail your software background
    Provide information about the experiences you have that helped you gain software and technology skills. This can include internships, entry-level positions and personal projects. Be specific about the tasks you managed and the skills you gained in each experience.Related: How To Write the Best Cover Letter (With Template and Sample)
    3. Describe your most relevant skills
    While detailing your experience, you can highlight your technical and interpersonal skills. Focus on hard skills, such as coding languages and Agile understanding, as well as soft skills like communication and teamwork. This approach demonstrates how you provide value to your team and the workplace.
    4. Include a call to action for the reader
    The final paragraph of your cover letter can thank the reader for their time and prompt them to contact you with a call to action. For example, you may express your interest in scheduling an interview or answering further questions about your candidacy. You can also include a sentence about how you can bring value to the company.
    5. Finish and sign the cover letter
    To finish your cover letter, include a sign-off and your signature.

    ❗ Generate only the body of the cover letter, starting from the salutation ("Dear [Hiring Manager],"). Do NOT include any placeholders like [Your Name], [Address], [Date], or any heading or contact information. Return only the letter text.
    ❗ “Do not include any sign-off or closing.
    
    """

def resume_parse_prompt(resume_text: str) -> str:
    return f"""
    You are a strict JSON data extractor.

    Goal: Take a freeform resume text and return valid JSON that exactly matches this schema:

    class JobEntry(BaseModel):
        company: str
        location: str
        dates: str
        title: str
        description: list[str]

    class EducationEntry(BaseModel):
        degree: str
        school: str

    class Resume(BaseModel):
        full_name: str
        email: str
        phone: str
        linkedin: str
        headline: str
        location: str
        summary: str
        technical_skills: list[str]
        core_competencies: list[str]
        work_experience: list[JobEntry]
        education: list[EducationEntry]

        class Config:
            extra = "forbid"

    Rules:
    1) Always include all fields in the output, even if empty ("" for strings, [] for lists).
    2) Output ONLY valid JSON. No explanations, no commentary.
    3) For description in each JobEntry, return a list of short bullet-style strings (no dashes or numbering).
    4) If a field is missing in the input, use "" or [] accordingly.

    Few-shot example:

    Input:
    \"\"\"
    John Smith is a software engineer with 5 years of experience in backend development using Python and AWS.
    Worked at TechCorp in New York from Jan 2020 to May 2023 as Senior Backend Engineer, leading a team of 5 to build microservices, optimize databases, and improve deployment pipelines.
    Prior to that, worked at DataSys in Boston from Jun 2018 to Dec 2019 as Software Engineer, focusing on data processing scripts and API integrations.
    BS in Computer Science from MIT.
    \"\"\"

    Output:
    {{
    "full_name": "John Smith",
    "email": "",
    "phone": "",
    "linkedin": "",
    "headline": "Software Engineer",
    "location": "",
    "summary": "Software engineer with 5 years of backend experience using Python and AWS.",
    "technical_skills": ["Python", "AWS", "microservices", "databases", "deployment pipelines", "API integrations"],
    "core_competencies": ["Backend Development", "Team Leadership", "Database Optimization", "API Integration"],
    "work_experience": [
        {{
        "company": "TechCorp",
        "location": "New York",
        "dates": "Jan 2020 - May 2023",
        "title": "Senior Backend Engineer",
        "description": [
            "Led a team of 5 to build microservices",
            "Optimized databases",
            "Improved deployment pipelines"
        ]
        }},
        {{
        "company": "DataSys",
        "location": "Boston",
        "dates": "Jun 2018 - Dec 2019",
        "title": "Software Engineer",
        "description": [
            "Developed data processing scripts",
            "Integrated APIs"
        ]
        }}
    ],
    "education": [
        {{
        "degree": "BS in Computer Science",
        "school": "MIT"
        }}
    ]
    }}

    Now parse this resume text and return ONLY the JSON:

    \"\"\"
    {resume_text}
    \"\"\"
    """