#Working code

import streamlit as st
from uipage1 import mainfunc
# import login, logout, register
from resume_analyser import resume_analyser
from job_recommendations import job_recommendations
from job_description import job_description
#from uipage1 import mainfunc, jobs_data  # Importing the mainfunc function and jobs_data list from uipage1.py



st.set_page_config(page_title="JobFit AI", page_icon="Icon.png")



def initialize_session_state():
    if "authentication_status" not in st.session_state:
        st.session_state["authentication_status"] = None
    if "logout" not in st.session_state:
        st.session_state["logout"] = True
    if "name" not in st.session_state:
        st.session_state["name"] = ""
    if "username" not in st.session_state:
        st.session_state["username"] = ""

def page_navigation():
    # if st.session_state.get("authentication_status", False):
    st.sidebar.title(f"Welcome {st.session_state.get('name')}")
    st.sidebar.image("Logo.png", width=200)
    page = st.sidebar.radio("", ("Resume Analyser", "Job Recommendations", "Upload Job Description"))

    if page == "Resume Analyser":
        resume_analyser()
    elif page == "Job Recommendations":
        job_recommendations()
    elif page == "Upload Job Description":
        job_description()
   

        # logout()
    # else:
    #     # auth_option = st.selectbox("JobFit", ("Login", "Signup"))
    #     _login, _register = st.tabs(["Login", "Signup"])

    #     with _login:
    #         login()
    #         if st.session_state.get("authentication_status"):
    #             st.rerun()
    #         elif st.session_state.get("authentication_status") is False:
    #             st.error('Username/password is incorrect')
    #         elif st.session_state.get("authentication_status") is None:
    #             st.warning('Please enter your username and password')
    #     with _register:
    #         register()

def main():
    
    initialize_session_state()
    page_navigation()

if __name__ == "__main__":
    main()
