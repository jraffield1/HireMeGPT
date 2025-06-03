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

def resume_finetuning_prompt(job: JobPosting, resume: Resume) -> str:
    return f"""
    Given a job description and a candidate's resume, revise the resume to align with the job while being truthful and emphasizing real strengths.
    Make this resume as strong as you can for this position.
    Don't be too wordy with the job experience descriptions but try to pepper them with meaningful metrics

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