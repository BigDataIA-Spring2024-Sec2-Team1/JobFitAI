import streamlit as st
from auth import login, logout, register

def page_navigation():
    if st.session_state.get("authentication_status", False):
        st.sidebar.title(f"Hello {st.session_state.get('name')}")
        page = st.sidebar.radio("", ("Home", "Page 1", "Page 2"))

        if page == "Home":
            st.title("Home Page")
            st.write("Welcome to the Home Page!")

        elif page == "Page 1":
            st.title("Page 1")
            st.write("This is Page 1.")

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
    st.title(f"Job Fit")
    page_navigation()

if __name__ == "__main__":
    main()
