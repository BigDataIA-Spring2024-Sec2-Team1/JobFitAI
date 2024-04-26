# JobFit AI

## Live application Links :octopus:

- Please use this application responsibly, as we have limited free credits remaining.

[![Streamlit](<ADDLINK>)

[![FastAPI](<ADDLINK>)

[![Apache Airflow](<ADDLINK>)

[![codelabs](https://codelabs-preview.appspot.com/?file_id=1vgMyIUyW9-KYcdxPMUs-lFjF9gVwKMT2BpwPWluPthc/edit#0)

[![Demo Link](<ADDLINK>)



## Abstract :memo: 

The "JobFit AI" project introduces an innovative AI-driven Applicant Tracking System (ATS) aimed at optimizing the resume tailoring process. It facilitates seamless communication between users and the application through a Streamlit frontend and FastAPI backend. By leveraging cutting-edge technologies such as OpenAI's GPT, the system offers personalized suggestions for resume enhancement, empowering users to tailor their resumes to specific job requirements effectively.

## Problem Statement :Construction:
### Current Challenges
Many students face significant challenges in efficiently screening job descriptions, analyzing the skills required, comparing with their resumes and updating their resumes and gaining expertise in skills they are lagging behind during the application process. Some common challenges include:
1. Limited Guidance: Many students or applicants lack guidance on how to optimize their resumes for specific job roles or industries, leading to missed opportunities in the job market.
2. Time-Consuming Process: Manual resume optimization can be time-consuming and labor-intensive, especially for individuals with limited experience or resources.
3. Competitive Job Market: In a competitive job market, it's essential for resumes to stand out and effectively showcase candidates' qualifications and skills.
4. Lack of Personalization: Generic resume templates and advice may not adequately address individual strengths, experiences, and career goals.

## Project Goals :dart:

1. Leverage Pydantic or NLP to extract key skills and experience from resumes.
2. Compare extracted data with job requirements and provide personalized improvement suggestions.
3. Utilize user data and APIs to recommend relevant job openings.
4. Tailor resumes to match job descriptions through keyword analysis and suggestion generation.
5. Integrate Chat GPT (or similar) for enhanced and refined resume improvement recommendations.
6. Develop a user-friendly Streamlit application for a seamless user experience.

## Use case :bookmark_tabs:

Job seekers struggling to tailor their resumes for specific job roles can leverage JobFit AI. By uploading their resume and a desired job description, JobFit AI analyzes both documents. It  identifies missing skills, suggests targeted improvements, and recommends relevant job openings based on the user's experience. This empowers job seekers to present strong resumes and increase their chances of landing their dream job.

## Technologies Used :computer:

[![Streamlit](https://img.shields.io/badge/Streamlit-FF4B4B?style=for-the-badge&logo=Streamlit&logoColor=white)](https://streamlit.io/)
[![GitHub](https://img.shields.io/badge/GitHub-100000?style=for-the-badge&logo=github&logoColor=white)](https://github.com/)
[![FastAPI](https://img.shields.io/badge/fastapi-109989?style=for-the-badge&logo=FASTAPI&logoColor=white)](https://fastapi.tiangolo.com/)
[![Amazon AWS](https://img.shields.io/badge/Amazon_AWS-FF9900?style=for-the-badge&logo=amazonaws&logoColor=white)](https://aws.amazon.com/)
[![Python](https://img.shields.io/badge/Python-FFD43B?style=for-the-badge&logo=python&logoColor=blue)](https://www.python.org/)
[![HTML5](https://img.shields.io/badge/HTML5-E34F26?style=for-the-badge&logo=html5&logoColor=white)](https://developer.mozilla.org/en-US/docs/Web/Guide/HTML/HTML5)
[![Pandas](https://img.shields.io/badge/Pandas-2C2D72?style=for-the-badge&logo=pandas&logoColor=white)](https://pandas.pydata.org/)
[![NumPy](https://img.shields.io/badge/Numpy-777BB4?style=for-the-badge&logo=numpy&logoColor=white)](https://numpy.org/)
[![Apache Airflow](https://img.shields.io/badge/Airflow-017CEE?style=for-the-badge&logo=Apache%20Airflow&logoColor=white)](https://airflow.apache.org/)
[![GitHub Actions](https://img.shields.io/badge/Github%20Actions-282a2e?style=for-the-badge&logo=githubactions&logoColor=367cfe)](https://github.com/features/actions)

## Data Source :flashlight:

Dataset consisting of job descriptions and resumes obtained from various sources are used as data sources.

## Process Outline :Counterclockwise Arrows:
**1. Data Acquisition:** Users upload their resumes and desired job descriptions through a user-friendly interface.
**2. Data Processing:** Utilize Pydantic or NLP techniques to extract key skills and experience from resumes.
**3. Analysis and Recommendations:**
- Compare extracted data with pre-defined skills or job requirements.
- Recommend improvements to the resume based on the job description and missing skills.
- Leverage APIs (e.g., LinkedIn) to suggest relevant job postings.
**4. AI-powered Enhancement:** Integrate Chat GPT (or similar) to generate insightful and personalized suggestions for further resume optimization.
**5. User Interface:** Develop a user-friendly Streamlit application to display extracted skills, recommended improvements, job recommendations, and AI-powered suggestions.

## Project Setup

<img width="607" alt="image" src="https://user-images.githubusercontent.com/114537365/234988315-a9f89c76-b0ac-413c-9f4b-977eb7c5eab9.png">


## Requirements :Briefcase:
```
fastapi==0.92.0

pydantic==1.10.4

openai==0.27.0

🖼streamlit==1.18.1
```

## Project Folder Structure :Folder:

```
📦 Final-Project-Playground
├─ .github
│  └─ workflows
│     └─ pytest.yml
├─ .gitignore
├─ Airflow
│  └─ Dags
│     ├─ README.md
│     ├─ db_update.py
│     ├─ ge_report.py
│     └─ issue_embedding_and_storing.py
├─ Dockerfile
├─ README.md
├─ __init__.py
├─ backend
│  ├─ .DS_Store
│  ├─ Dockerfile
│  ├─ __init__.py
│  ├─ database.py
│  ├─ hashing.py
│  ├─ main.py
│  ├─ models.py
│  ├─ requirements.txt
│  └─ schema.py
├─ bert_download.py
├─ docker-compose.yml
├─ great_expectations
│  ├─ .gitignore
│  ├─ README.md
│  ├─ checkpoints
│  │  ├─ github_issues_checkpoint_v0.yml
│  │  └─ github_issues_checkpoint_v1.yml
│  ├─ expectations
│  │  ├─ .ge_store_backend_id
│  │  └─ github_issues_suite.json
│  ├─ great_expectations.yml
│  └─ plugins
│     └─ custom_data_docs
│        └─ styles
│           └─ data_docs_custom_styles.css
├─ navigation
│  ├─ __init__.py
│  ├─ adminworkarea.py
│  ├─ analytics.py
│  ├─ errorsearch.py
│  └─ issuesearch.py
├─ pyrequirements.txt
├─ requirements.txt
├─ unit_testing.py
├─ userinterface.py
└─ utils
   ├─ __init__.py
   └─ core_helpers.py
```
©generated by [Project Tree Generator](https://woochanleee.github.io/project-tree-generator)


## How to run Application locally :Rocket:

To run the application locally, follow these steps:

1. Clone the repository to get all the source code on your machine.

2. Create a virtual environment and install all requirements from the requirements.txt file present.

3. Create a .env file in the root directory with the following variables:

    GITHUB_API_TOKEN: your GitHub API token.

    SNOWFLAKE_USER: your Snowflake username.

    SNOWFLAKE_PASSWORD: your Snowflake password.

    SNOWFLAKE_ACCOUNT: your Snowflake account name.

    SNOWFLAKE_DATABASE: the name of the Snowflake database to use.

    SNOWFLAKE_SCHEMA: the name of the Snowflake schema to use.

    ACESS_TOKEN: Your Github Acess token

    SECRET_KEY: "09d25e094faa6ca2556c818166b7a9563b93f7099f6f0f4caa6cf63b88e8d3e7" - for JWT Hashing

    ALGORITHM: "HS256" - - for JWT Hashing

    ACCESS_TOKEN_EXPIRE_MINUTES: The expiration time of the access token in minutes

    OPENAI_API_KEY: Your OpenAI API key for accessing the GPT model.

4. Once you have set up your environment variables, start Airflow by running the following command from the root directory:

docker-compose up airflow-init && docker-compose up -d

5. Access the Airflow UI by navigating to http://localhost:8080/ in your web browser.

6. To run the DAG in Airflow, click on the dag link on the Airflow UI and toggle the switch to enable the DAGs.

7. Once the DAGs have run successfully, start the Streamlit application by running the following command from the streamlit-app directory:

docker-compose up

8. Access the Streamlit UI by navigating to http://localhost:8501/ in your web browser.

## Github Actions - Testing

<img width="1512" alt="image" src="https://user-images.githubusercontent.com/114537365/235001553-2dc11cd4-9131-48d2-a57b-75b302aeb372.png">

## References :Books:
- https://code.visualstudio.com/docs/python/tutorial-fastapiLinks
- https://aws.amazon.com/s3/
- https://github.com/Coding-Crashkurse/Pydantic-v2-crashcourseLinks to an external site.
- https://docs.pinecone.io/guides/getting-started/quickstart/Using_Pinecone_for_embeddings_search.ipynb
- https://github.com/openai/openai-cookbook/blob/main/examples/vector_databases/pinecone/
- https://github.com/openai/openai-cookbook/blob/main/examples/vector_databases/pinecone/GPT4_Retrieval_Augmentation.ipynb


## Learning Outcomes :Graduation Cap:
List the learning outcomes from the assignment/project
### Technical skills:
1. Proficiency in Natural Language Processing (NLP): Gain proficiency in leveraging OpenAI's GPT API for analyzing and processing text data from resumes and job descriptions.
2. Experience with Streamlit and FastAPI: Acquire familiarity with building interactive web applications using Streamlit for the frontend and FastAPI for the backend, including handling user input, authentication, and data communication.
3. Understanding of AI-driven Systems: Develop an understanding of how AI-driven systems can be integrated into applications to provide personalized recommendations and enhance user experiences.
4. Knowledge of API Integration: Learn how to integrate external APIs, such as the LinkedIn API, for fetching real-time job descriptions and enhancing the system's recommendation capabilities.
5. Data Management and Storage: Gain experience in managing and storing large datasets, including resumes and job descriptions, using technologies like Amazon S3 for data storage and retrieval.
### Softskills
1. Problem-Solving Abilities: Discuss how the project challenged participants to think critically, solve problems, and overcome obstacles.
2. Project Management Skills: Highlight any experience gained in project planning, organization, task management, and collaboration within a team.
3. Communication and Collaboration: Reflect on the effectiveness of communication and collaboration within the team, including teamwork, leadership, and interpersonal skills.


## Team Information and Contribution :Handshake:

Name            | Contribution % | Contribution                         |
---             | ---            | ---                                  |
Aniket Giram    | 33.33%         |Text, keywords extraction, Embeddings |
Sudarshan Dudhe | 33.33%         |Backend, pytest, testing              |
Rasika Kole     | 33.33%         |Frontend, Backend, Documentation      |


