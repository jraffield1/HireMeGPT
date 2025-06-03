from pydantic import BaseModel, Field


class JobPosting(BaseModel):
    job_title: str
    company_name: str | None = None
    job_location: str | None = None
    job_description: str
    required_qualifications: list[str]
    preferred_qualifications: list[str] = Field(default_factory=list)