import streamlit as st
import requests
import json

def job_fit_score():
    if "score" not in st.session_state:
        st.session_state["score"] = ""

    url = "http://backend:8000"

    if st.session_state["resume_file_name"]:
        st.write(f"Matching Job Description with - {st.session_state.get('resume_file_name')}")
        job_description = st.text_area("Enter Job Description", height=40)
        if st.button("Get Job Match Score"):
            score = requests.post(f"{url}/get-job-match-score", json={"username": st.session_state.get("username"), "skills": [], "job_description": job_description})

            if score.status_code == 200:
                st.session_state["score"] = score.json()
                
                st.write("JobFit Score: ", score.json().get("match_percentage"))
                st.write("Matched Skills from your resume")

                num_of_columns = 3
                _presentcolumns = st.columns(num_of_columns)

                for i, skill in enumerate(score.json().get("matched_skills")):
                    with _presentcolumns[i % num_of_columns]:
                        st.button(skill, key=f"{i}{skill}")

                st.write("Missing Skills from your resume")

                num_of_columns = 3
                columns = st.columns(num_of_columns)

                for i, skill in enumerate(score.json().get("missing_skills")):
                    with columns[i % num_of_columns]:
                        st.button(skill, key=f"{i}{skill}")
                # st.write(score.json())
        
        if st.button("Get Recommandation"):
            bullet_points = requests.post(f"{url}/get-experience-bullet-points", json={"username": st.session_state.get("username"), "job_description": job_description, "skills":st.session_state["score"].get("missing_skills"), "resume_text": st.session_state.get("resume_text")})
            for i in bullet_points.json():
                st.write("Some Suggested Bullet Points for Resume: Experience - ", i.get("name"))
                st.write(i.get("bullet_point"))
    else:
        st.write(f"No resume attached to profile, please upload a resume inn Job Analyser")
