from tasks.util import extractKeywordFromLightSkillAPI, getAccessToken

import openai
# import pinecone

from pinecone import Pinecone
from dotenv import load_dotenv
import os

load_dotenv()
# OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
# PINECONE_API_KEY = os.getenv("PINECONE_API_KEY")
OPENAI_API_KEY = "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"
PINECONE_API_KEY = "432efbce-a192-4eb1-bba7-6b46fb18f1b5"

client = openai.OpenAI(api_key=OPENAI_API_KEY)
pc = Pinecone(api_key=PINECONE_API_KEY)

# Define the list of skills
_skills = [
    'Detail Oriented', 'Oncology', 'Palliative Care', 'Profit And Loss (P&L) Management',
    'QuickBooks (Accounting Software)', 'Communication', 'Medical Science', 'Neurosurgery',
    'Electronic Documents', 'Paychex', 'Surgery', 'Pediatrics', 'Neurology', 'Accounts Payable',
    'Bookkeeping', 'Radiosurgery', 'Problem Solving', 'Management', 'Filing', 'Microsoft Excel'
]
EMBEDDING_MODEL = "text-embedding-3-small"


def create_embeddings(**kwargs):
    ti = kwargs['ti']
    job_posting_list = ti.xcom_pull(
        key="job_posting_list", task_ids="validate_scraped_data")
    print("job_posting_list")
    print(len(job_posting_list))
    if len(job_posting_list):
        print(job_posting_list[0])
        for job in job_posting_list:
            text = job["description"]
            token = getAccessToken()
            job_description_skills = extractKeywordFromLightSkillAPI(
                text, token)
            job_skills = job_description_skills
            job_id = job["job_id"]
            upsert(job_skills, job_id)


def upsert(job_skills, job_id):

    response = client.embeddings.create(
        input=_skills,
        model="text-embedding-ada-002"
    )
    for i, be in enumerate(response.data):
        assert i == be.index
    embedding_list = [e.embedding for e in response.data]
    # Extract the embeddings
    job_fit_index_name = 'job-fit'
    # Define metadata for each embedding
    _metadata = {"job_id": "3911514027", "skills": job_skills}
    # Upsert embeddings to Pinecone
    # Connect to Pinecone
    index = pc.Index(job_fit_index_name)
    # pc.create_index(job_fit_index_name, dimension=len(
    #     skills_embeddings[0]), metric="cosine")
    # index.upsert(vectors=skills_embeddings,
    #              namespace="live_job_skills", metadata=_metadata)
    # _skills_embeddings_df = pd.DataFrame(embedding_list)

    print(embedding_list[0])
    vectors_to_upsert = [(str(job_id), embedding_list[0], _metadata)]
    # embed(_skills_embeddings_df, index)
    try:
        print("upserting")
        res = index.upsert(
            vectors=vectors_to_upsert,
            namespace="live_job_skills"
        )
        print(res)
        print("upsert done")
    except Exception as e:
        print(str(e))
# create_embeddings(_skills)
