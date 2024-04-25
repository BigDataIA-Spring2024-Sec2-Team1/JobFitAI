import streamlit as st
import streamlit_authenticator as stauth
import yaml
from yaml.loader import SafeLoader
import os

print("current dir",  os.getcwd())
with open('/app/cred.yaml') as file:
    config = yaml.load(file, Loader=SafeLoader)

authenticator = stauth.Authenticate(
    config['credentials'],
    config['cookie']['name'],
    config['cookie']['key'],
    config['cookie']['expiry_days'],
    config['pre-authorized']
)

def login():
    authenticator.login()

def logout():
    authenticator.logout(location = "sidebar")
    if st.session_state.get("authentication_status") == None:
        st.rerun()

def register():
    try:
        email_of_registered_user, username_of_registered_user, name_of_registered_user = authenticator.register_user(pre_authorization=False)
        if email_of_registered_user:
            st.success('User registered successfully')
        writeConfig()
    except Exception as e:
        st.error(e)

def writeConfig():
    with open('/app/cred.yaml', 'w') as file:
        yaml.dump(config, file, default_flow_style=False)

# if st.session_state["authentication_status"]:
#     try:
#         if authenticator.reset_password(st.session_state["username"]):
#             st.success('Password modified successfully')
#     except Exception as e:
#         st.error(e)
