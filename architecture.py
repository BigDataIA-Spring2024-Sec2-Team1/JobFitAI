from diagrams import Diagram, Cluster
from diagrams.programming.language import Python
from diagrams.custom import Custom
from diagrams.onprem.database import Mongodb

with Diagram("User Flow Diagram 1", show=False):
    with Cluster("User Flow 1"):
        streamlit = Custom("Upload Resume", "./assets/streamlit.png")
        user = Custom("Users", "./assets/user.png")

        with Cluster("Extraction"):
            extract_text = Python("Extract Text")
            keyword_extraction = Python("Keyword Extraction")

        with Cluster("Similarity search from Pinecone"):
            pinecone = Custom("Similarity search", "./assets/pinecone.png")
            resume_pinecone_search = Python("User Categorization")
            openai_user_categoition = Custom("If failed by pinecone", "./assets/openai.png")
            job_description_pinecone_search = Python("Match Job Description")
            database = Mongodb("Store data")

        with Cluster("Open AI Suggestion and Linkedin Job Extraction Based on Keyword"):
            openai = Custom("", "./assets/openai.png")
            current_job_extraction = Python("Based on User category and skills")
            linkedin = Custom("", "./assets/linkedin_logo.png")

        user  >> streamlit >> extract_text 
        keyword_extraction >> resume_pinecone_search
        resume_pinecone_search >> pinecone >> openai_user_categoition >> job_description_pinecone_search >> database >> openai >> current_job_extraction >> linkedin >> user

with Diagram("User Flow Diagram 2", show=False):
    with Cluster("User Flow 2"):
        streamlit_res = Custom("Upload Resume", "./assets/streamlit.png")
        streamlit_jd = Custom("Upload Job Description", "./assets/streamlit.png")
        user = Custom("Users", "./assets/user.png")

        with Cluster("Extraction"):
            extract_text = Python("Extract Text")
            keyword_extraction = Python("Keyword Extraction")

        with Cluster("Keyword matching"):
            openai_keywords = Custom("Keyword", "./assets/openai.png")
            keyword_matching = Python("Match Job Description")

        with Cluster("Open AI Suggestion"):
            openai = Custom("", "./assets/openai.png")

        user  >> streamlit_res >> extract_text
        user >> streamlit_jd >> extract_text
        extract_text >> keyword_extraction >> openai_keywords
        keyword_matching >> openai >> user

with Diagram("Pipeline 1", show=False):
    with Cluster("Knowledge Base Pipeline in Airflow"):
        cv_csv = Custom("Resume", "./assets/csv.jpeg")
        jd_csv = Custom("Job Description", "./assets/csv.jpeg")
        cv_jd_csv = Custom("User Uploaded Resume and JD", "./assets/csv.jpeg")
        extract_text_keyword = Python("Extract Text and Keywords")
        openai = Custom("Create Embedding", "./assets/openai.png")
        pinecone_script = Python("Store it in pinecone")
        pinecone = Custom("", "./assets/pinecone.png")

    cv_csv >> extract_text_keyword
    jd_csv >> extract_text_keyword
    cv_jd_csv >> extract_text_keyword

    extract_text_keyword >> openai >> pinecone_script >> pinecone

with Diagram("Pipeline 2", show=False):
    with Cluster("Current Job Extraction Pipeline in Airflow"):
        jd_from_linkedin = Custom("", "./assets/linkedin_logo.png")
        extract_text_keyword = Python("Extract Text and Keywords")
        openai = Custom("Create Embedding", "./assets/openai.png")
        pinecone_script = Python("Store it in pinecone")
        pinecone = Custom("", "./assets/pinecone.png")
        database = Mongodb("For User specific Job recommendation")

    jd_from_linkedin >> extract_text_keyword

    extract_text_keyword >> database

    extract_text_keyword >> openai >> pinecone_script >> pinecone
