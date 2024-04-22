from pydantic import BaseModel
from datetime import datetime
from typing import Optional
from typing import Any

class Job(BaseModel):
    jobId: str
    title: str
    location: Any
    company: str
    link: str
    jobDescription: Optional[str]
    scapetime: datetime
    jobPosted: datetime