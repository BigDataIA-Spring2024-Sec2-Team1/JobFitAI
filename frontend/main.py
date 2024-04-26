import streamlit as st
from auth import login, logout, register
from resume_analyser import resume_analyser
from job_fit_score import job_fit_score

def initialize_session_state():
    if "authentication_status" not in st.session_state:
        st.session_state["authentication_status"] = None
    if "logout" not in st.session_state:
        st.session_state["logout"] = True
    if "name" not in st.session_state:
        st.session_state["name"] = ""
    if "username" not in st.session_state:
        st.session_state["username"] = ""
    if "resume_file_name" not in st.session_state:
        st.session_state["resume_file_name"] = ""

def page_navigation():
    if st.session_state.get("authentication_status", False):
        st.sidebar.title(f"Hello {st.session_state.get('name')}")
        page = st.sidebar.radio("", ("Resume Analyser", "Job Fit Score", "Page 2"))

        if page == "Resume Analyser":
            resume_analyser()
        elif page == "Job Fit Score":
            job_fit_score()
        elif page == "Page 2":
            st.title("Page 2")
            st.write("This is Page 2.")

        logout()
    else:
        # auth_option = st.selectbox("JobFit", ("Login", "Signup"))
        _login, _register = st.tabs(["Login", "Signup"])

        with _login:
            login()
            if st.session_state.get("authentication_status"):
                st.rerun()
            elif st.session_state.get("authentication_status") is False:
                st.error('Username/password is incorrect')
            elif st.session_state.get("authentication_status") is None:
                st.warning('Please enter your username and password')
        with _register:
            register()

def main():
    initialize_session_state()
    page_navigation()

if __name__ == "__main__":
    main()
