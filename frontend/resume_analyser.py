import streamlit as st
import requests
import json

def resume_analyser():

    url = "http://backend:8000"

    if 'user_resume_keywords' not in st.session_state:
        st.session_state.user_resume_keywords = []

    if 'similar_user_keywords' not in st.session_state:
        st.session_state.similar_user_keywords = []

    if 'user_designations' not in st.session_state:
        st.session_state.user_designations = []

    if 'jd_match_skills' not in st.session_state:
        st.session_state.jd_match_skills = []

    if 'resume_text' not in st.session_state:
        st.session_state.resume_text = ''

    uploaded_file = st.file_uploader("Upload a file", type=['docx', 'pdf'])

    if uploaded_file:
        progress_bar = st.progress(0)
        if st.button("Upload to S3"):
            files = {"file": (uploaded_file.name, uploaded_file.getvalue())}
            st.session_state["resume_file_name"] = uploaded_file.name
            print("file name is", uploaded_file.name)
            response = requests.post(f"{url}/upload", files=files)
            if response.status_code == 200:
                st.toast("File uploaded successfully to S3! We are currently parsing your resume")
                parse_resume_res = requests.post(f"{url}/parse-resume", files=files)
                if parse_resume_res.status_code == 200:
                    print("resume successfully parsed")
                    st.session_state.resume_text =  parse_resume_res.json().get("text")
                    st.session_state.user_resume_keywords.append(parse_resume_res.json().get("skills"))
                    add_user_skills_db = requests.post(f"{url}/add-user-skills-to-db", json={"skills": parse_resume_res.json().get("skills"), "username": st.session_state.get("username")})
                    if add_user_skills_db.status_code == 200:
                        user_categorization_res = requests.post(f"{url}/user-categorization", json={"skills": parse_resume_res.json().get("skills"), "namespace": "resume_skills", "resume_text": parse_resume_res.json().get("text")})
                        if user_categorization_res.status_code == 200:
                            st.session_state.similar_user_keywords.append(user_categorization_res.json().get("similar_profile_skills"))
                            st.session_state.jd_match_skills.append(user_categorization_res.json().get("jd_skills"))
                            st.toast("Resume Parsing and User Categorization Successfull")
                            st.session_state.user_designations = user_categorization_res.json().get("designations")
                            st.session_state.user_designations.append("Other")
                        else:
                            st.error("Failed in User Categorization")
                    else:
                        st.error("Error in Storing users skills")
                else:
                    st.error("Failed in Parsing resume")
            else:
                st.error("Failed to upload file. Error: {}".format(response.text))

        if 'selected_designation' not in st.session_state:
            st.session_state.selected_designation = ''

        st.session_state.selected_designation = st.selectbox("Select the position you are targeting to apply", st.session_state.user_designations, key='selected_designation_key')

        if st.session_state.selected_designation == "Other":
            user_input = st.text_input("If targeting position is not in the list, type below.")
            st.write(user_input)
            st.session_state.selected_designation = user_input

        if st.session_state.selected_designation:
            if st.button("Suggest Keywords"):
                getSkillsSuggestion(url, st.session_state.user_resume_keywords, st.session_state.similar_user_keywords, st.session_state.jd_match_skills)


        # st.write(f"Intersection - {set_b.union(set_a)}")
        # st.write("Already present", set_a.intersection())


def getSkillsSuggestion(url, user_resume_keywords, similar_user_keywords, jd_skills):

    if user_resume_keywords and similar_user_keywords:
        flat_a = [item.lower() for sublist in user_resume_keywords for item in sublist]
        flat_b = [item.lower() for sublist in similar_user_keywords for subsublist in sublist for item in subsublist]
        jd_skills = [item.lower() for sublist in jd_skills for subsublist in sublist for item in subsublist.split(",")]
        set_a = set(flat_a)
        set_b = set(flat_b)
        set_jd_skills = set(jd_skills)
        low_priority_skills = list(set_a.union(set_b) - set_a.intersection(set_b))
        intersection_result = set_a.intersection(set_b)
        only_set_b = set_b.difference(set_a)
        combined_result = only_set_b.union(intersection_result)

        # if you want totally new keywords which are not in resume then pass only_set_b in similar_skills or else combined one will also set some of the relevent skills which might be present in resume
        suggested_skills = requests.post(f"{url}/suggest-keyword", json={"similar_skills": list(combined_result), "resume_text": st.session_state.resume_text, "designation": st.session_state.selected_designation, "num_of_skills": 20})

        if suggested_skills.status_code == 200:
            ai_suggested_skills = [item.lower() for item in eval(suggested_skills.json().get("response")).get("Skills")]
            top_k_skills = [item.lower() for item in eval(suggested_skills.json().get("top_k")).get("Skills")]

            if len(low_priority_skills) < 2:
                st.write(ai_suggested_skills)

            st.write("Top skills")

            num_of_columns = 3

            # Create a list of columns
            columns = st.columns(num_of_columns)

            # Iterate over the list of skills and create a button in each column
            for i, skill in enumerate(top_k_skills):
                with columns[i % num_of_columns]:
                    st.button(skill, key=f"{i}{skill}")


            st.write(f"Skills we found in Job Posting posted for title: {st.session_state.selected_designation} ")

            jd_columns = st.columns(num_of_columns)

            # Iterate over the list of skills and create a button in each column
            for i, skill in enumerate(set_jd_skills):
                with jd_columns[i % num_of_columns]:
                    st.button(skill, key=f"{i}{skill}")

            unique = [item for item in low_priority_skills if item not in top_k_skills][1:15]
            st.write("We found these skills that might be applicable to your resume")
            columns_for_unique = st.columns(num_of_columns)
            for i, skill in enumerate(unique):
                with columns_for_unique[i % num_of_columns]:
                    st.button(skill, key=f"{i}{skill}")

    else:
        st.toast("Sommething went wrong")
