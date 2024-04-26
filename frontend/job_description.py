import streamlit as st
def job_description():
    st.title("Job Description")
    st.image("Job_Description.jpg", width=300, use_column_width=True)
      
    # Multiline text input for job description
    job_description = st.text_area("Enter your job description:", height=200)

    # Button to submit the job description
    if st.button("Submit"):
        # Process the job description
        if job_description:
            st.success("Job description submitted successfully!")
            # Add your processing logic here
            st.write("You submitted the following job description:")
            st.write(job_description)
        else:
            st.warning("Please enter a job description.")

    st.write("Upload another resume?")
    uploaded_file = st.file_uploader("Upload a file", type=['docx', 'pdf'])