import streamlit as st
import streamlit_authenticator as stauth
import yaml
from yaml.loader import SafeLoader
import os
from pymongo import MongoClient
from pymongo.errors import ConnectionFailure, ServerSelectionTimeoutError

path = "/app/cred.yaml" # when you are using docker uncomment this and commont belows path
# path = "cred.yaml"
with open(path) as file:
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
            saveUserToDb(email_of_registered_user, username_of_registered_user, name_of_registered_user)
            st.success('User registered successfully')
        writeConfig()
    except Exception as e:
        st.error(e)

def writeConfig():
    with open(path, 'w') as file:
        yaml.dump(config, file, default_flow_style=False)


def saveUserToDb(email, username, name):
    try:
        user = {
            "name": name,
            "username": username,
            "email": email
        }
        collection = connect_to_mongodb('User')
        result = collection.insert_one(user)
        print("user inserted to db")
    except Exception as e:
        print("Error in Storing user to DB", e)

# if st.session_state["authentication_status"]:
#     try:
#         if authenticator.reset_password(st.session_state["username"]):
#             st.success('Password modified successfully')
#     except Exception as e:
#         st.error(e)


def connect_to_mongodb(collection_name):
    username = 'sudarshandudhemasters'
    password = 'NRGu4wKCkJDvG9ih'
    cluster_url = 'clustersd.2b003uq.mongodb.net'
    database_name = 'jobfit'
    collection_name = collection_name
    connection_string = f"mongodb+srv://{username}:{password}@{cluster_url}/{database_name}?retryWrites=true&w=majority&appName=clusterSD"
    try:
        client = MongoClient(connection_string)
        client.admin.command('ping')
        print("Connection established to MongoDB")
        db = client[database_name]
        collection = db[collection_name]
        return collection
    except ServerSelectionTimeoutError:
        print("Server selection timeout. Could not connect to MongoDB.")
        return None
    except ConnectionFailure:
        print("Failed to connect to MongoDB. Check your connection settings.")
        return None
    except Exception as e:
        print(f"An error occurred: {e}")
        return None
