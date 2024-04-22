from datetime import datetime
import re


# Extracting jobId from job URLs
def get_job_id(job_url: str, site: str) -> str:
    try:
        if site == 'indeed':
            job_id = re.search(r'(?<=jk=)[\w-]+', job_url).group()
        elif site == 'zip_recruiter':
            job_id = re.search(r'(?<=lvk=)[\w-]+', job_url).group()
        elif site == 'linkedin':
            job_id = re.search(r'(?<=view/)\d+', job_url).group()
        elif site == 'glassdoor':
            job_id = re.search(r'(?<=jl=)\d+', job_url).group()
        else:
            job_id = None
        return job_id
    except Exception as e:
        print(job_url)
        print(site)
        print(str(e))


# Function to get the current datetime
def current_datetime():
    return datetime.now()
