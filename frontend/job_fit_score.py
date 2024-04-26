import streamlit as st
import requests
import json

def job_fit_score():

    url = "http://localhost:8000"

    if st.session_state["resume_file_name"]:
        st.write(f"Matching Job Description with - {st.session_state.get('resume_file_name')}")
        job_description = st.text_area("Enter Job Description", height=40)
        if st.button("Get Job Match Score"):
            score = requests.post(f"{url}/get-job-match-score", json={"username": st.session_state.get("username"), "skills": [], "job_description": job_description})

            if score.status_code == 200:
                st.write(score.json())
    else:
        st.write(f"No resume attached to profile, please upload a resume inn Job Analyser")
