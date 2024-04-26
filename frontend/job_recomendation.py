import json
import streamlit as st
import requests


def get_job_recommendations():
    st.title("Job Recommendations")
    st.write("Here's your Job Recommendation")
    print("_username")
    print(st.session_state.get("username"))
    # Calculate the width of each column dynamically
    if st.button("Get Job Recommendations"):
        url = "http://backend:8000"
        _username = st.session_state.get("username")
        print(_username)
        print("username is", _username)
        response = requests.post(
            f"{url}/getJobSuggesions", json={"username": _username})
        print(response)
        if response.status_code == 200:
            jobs_data = response.json()
            job_descriptions_list = jobs_data["data"]["job_descriptions"]
            # data = json.loads(jobs_data)
            if job_descriptions_list:
                # Display jobs in expanders side by side
                for job in job_descriptions_list[:20]:
                    with st.expander(f"{job['title']}\n\n{job['company']}, {job['location']}"):
                        st.write("[Apply Here](" + job['apply_url'] + ")")
                        st.write("Posted on:", job['job_posted'])
                        st.write(job['description'])
                        st.write("---")
