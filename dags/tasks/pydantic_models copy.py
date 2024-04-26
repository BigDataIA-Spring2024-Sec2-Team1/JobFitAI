from pydantic import BaseModel, Field
from typing import List, Optional, Dict, Union, Any
from datetime import datetime


class Job(BaseModel):
    jobId: str
    title: str
    location: Any
    company: str
    link: str
    jobDescription: Optional[str]
    scapetime: datetime
    jobPosted: datetime


class LogoImage(BaseModel):
    width: int
    fileIdentifyingUrlPathSegment: str
    expiresAt: int
    height: int
    rootUrl: str


class Logo(BaseModel):
    image: LogoImage


class WebCompactJobPostingCompany(BaseModel):
    companyResolutionResult: Dict[str, Union[str, Logo]]
    company: str
    universalName: str
    url: str


class WebCompactJobPostingDescriptionAttributes(BaseModel):
    start: int
    length: int


class WebCompactJobPostingDescription(BaseModel):
    attributes: List[WebCompactJobPostingDescriptionAttributes]
    text: str


class OffsiteApply(BaseModel):
    applyStartersPreferenceVoid: bool
    companyApplyUrl: str
    inPageOffsiteApply: bool


class JobPosting(BaseModel):
    title: str
    company: str
    location: str
    description: str
    apply_url: str
    listed_at: int
    job_id: int
    job_posted: datetime

    @classmethod
    def parse_obj(cls, obj):
        # Validate and parse the dictionary into the Pydantic model
        return cls(**obj)
