import streamlit as st
import docx
from PyPDF2 import PdfReader

def read_docx(file):
    doc = docx.Document(file)
    full_text = []
    for para in doc.paragraphs:
        full_text.append(para.text)
    return '\n'.join(full_text)

def read_pdf(file):
    pdf_reader = PdfReader(file)
    num_pages = len(pdf_reader.pages)
    full_text = []
    for page_num in range(num_pages):
        page = pdf_reader.pages[page_num]
        full_text.append(page.extract_text())
    return '\n'.join(full_text)

def main():
    st.title("Resume Upload and Job Position Selection")

    # File Upload
    uploaded_file = st.file_uploader("Upload a file", type=['docx', 'pdf'])

    # Select multiple chiplets
    chiplet_names = st.multiselect("Select the position you are targeting to apply", options=['Software Engineering', 'Data Scientist', 'Data Analyst', 'Data Engineer', 'Business Analyst', 'Other'])

    # Text Input
    user_text = st.text_area("If targeting position is not in the list, type below.")

    # Display uploaded file
    if uploaded_file is not None:
        st.write("Uploaded file contents:")
        if uploaded_file.type == "application/vnd.openxmlformats-officedocument.wordprocessingml.document":
            text = read_docx(uploaded_file)
            st.write(text)
        elif uploaded_file.type == "application/pdf":
            text = read_pdf(uploaded_file)
            st.write(text)
        else:
            st.write("Unsupported file type")

    # Display selected chiplet names
    if chiplet_names:
        st.write("You are targeting to position:")
        for chiplet in chiplet_names:
            st.write(chiplet)

    # Display user entered text
    if user_text:
        st.write("Entered Text:")
        st.write(user_text)

   
if __name__ == "__main__":
    main()
