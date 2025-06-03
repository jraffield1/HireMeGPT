from pydantic import BaseModel

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
