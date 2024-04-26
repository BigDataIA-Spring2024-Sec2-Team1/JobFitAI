'''import streamlit as st
from datetime import datetime

def job_recommendations():
    st.title("Job Recommendations")
    st.write("Recommendations from LinkedIn")
    data = [{'title': 'Software Quality Assurance Engineer',
        'company': 'Insight Global',
        'location': 'Beaverton, OR',
        'description': 'Position: Software Quality Assurance EngineerLocation: Beaverton, OR 5 Days onsiteContract: 3 Month Contract - Conversion/Extensions highly likelyLocal candidates ONLY as the role is fully onsite\nDesired Skills 3-5 years of experience in a Software Quality Assurance roleExperience with both manual and automated testingUnderstanding of network/WIFI/Bluetooth connectivityAbility to validate software quality on hardware productsJira experience for tracking bug defects\nPlusses Python programming for test automation\nDay-to-Day A client in the Beaverton, OR area is looking for a Software Quality Assurance professional to join their team. This person will be responsible for manually testing software on physical products and writing some automated test cases with Python. They will need to have experience with product validation and tracking bugs and defects using Jira. This SQA will be responsible for functional testing of the software on hardware products and needs to be well-versed in embedded firmware quality.',
        'apply_url': 'https://www.linkedin.com/job-apply/3905591997',
        'listed_at': 1713999481000,
        'job_id': 3905591997,
        'job_posted': datetime(2024, 4, 25, 15, 24, 59)}]

    # Display three boxes side by side
    col1, _, _ = st.columns(3)

    # Parse and display selected keys of JSON data
    try:
        # Assuming you want to display data from the 'data' list
        job_data = data[0]
        if job_data:
            with col1.expander("Show Details"):
                if st.button("Click to Expand"):
                    for key, value in job_data.items():
                        st.write(f"**{key.capitalize()}:** {value}")
    except ValueError:
        st.error("Invalid JSON format. Please enter valid JSON data.")

if __name__ == "__main__":
    job_recommendations()
'''
import streamlit as st

# Define the job data
jobs_data = [
    {
        'title': 'Software Quality Assurance Engineer',
        'company': 'Insight Global',
        'location': 'Beaverton, OR',
        'description': 'Position: Software Quality Assurance EngineerLocation: Beaverton, OR 5 Days onsiteContract: 3 Month Contract - Conversion/Extensions highly likelyLocal candidates ONLY as the role is fully onsite\nDesired Skills 3-5 years of experience in a Software Quality Assurance roleExperience with both manual and automated testingUnderstanding of network/WIFI/Bluetooth connectivityAbility to validate software quality on hardware productsJira experience for tracking bug defects\nPlusses Python programming for test automation\nDay-To-Day A client in the Beaverton, OR area is looking for a Software Quality Assurance professional to join their team. This person will be responsible for manually testing software on physical products and writing some automated test cases with Python. They will need to have experience with product validation and tracking bugs and defects using Jira. This SQA will be responsible for functional testing of the software on hardware products and needs to be well-versed in embedded firmware quality.',
        'apply_url': 'https://www.linkedin.com/job-apply/3905591997',
        'listed_at': 1713999481000,
        'job_id': 3905591997,
        'job_posted': '2024-04-25 15:24:59'
    },
    {
        'title': 'Senior Python Developer',
        'company': 'Hyqoo',
        'location': 'New York, United States',
        'description': "Job Title: Senior Python DeveloperLocation: Hybrid (3 days onsite/Week)Address: BAC location in NJ/NY area. The role is 100% remote for now but when HR sends to call all to the office will go to hybrid 3 days per week.\n\nAbout the Role:We are seeking a highly skilled and experienced Senior Python Developer to join our dynamic team. The successful candidate will play a pivotal role in developing sophisticated front-office applications within the banking services sector. With a strong background in object-oriented programming, particularly Python, the Senior Python Developer will contribute to quantitative research and analysis, risk and pricing application development, and various full-stack projects. Our ideal candidate is someone who thrives in a fast-paced environment and is comfortable working with complex systems and platforms, including Quartz.\nResponsibilities:- Design, develop, and implement front office applications for banking services, ensuring high performance and integration with various systems.- Lead quantitative research efforts and analyze data to support business decisions and strategies.- Build and maintain risk and pricing applications that meet the needs of the business and adhere to regulatory standards.- Collaborate with cross-functional teams to work on RESTful services, ReactJS, and Full Stack development projects.- Manage both object and relational databases to ensure data integrity, performance, and scalability.- Address trade surveillance and market misconduct issues within the global market, ensuring compliance with industry regulations.- Apply your subject matter expertise to leverage the capabilities of the Quartz platform for strategic projects.\nEducation Qualification:- Bachelor's degree in Computer Science, Engineering, or a related field is required.\nRequired Skills:- At least 5 years of hands-on programming experience in an object-oriented language, with a strong preference for Python expertise.- Minimum of 3 years of experience as a senior developer with a focus on front-office applications in the banking industry.- Proven track record with at least 2 years in quantitative research and development.- At least 2 years of experience in creating and managing risk and pricing applications.- Practical experience in REST, ReactJS, or FullStack development.\nDesired Skills and Knowledge:- A deep understanding of trade surveillance and market misconduct within the global market.- Experience with object databases and relational databases.- Familiarity with agile development methodologies and version control systems, such as Git.- Excellent problem-solving skills and the ability to work in a team-oriented, collaborative environment.- Strong communication and interpersonal skills.\nTools:- Proficiency with Python programming and its relevant frameworks and libraries.- Experience using RESTful API design and development.- Familiarity with ReactJS or other modern JavaScript frameworks.- Experience with the Quartz platform is highly desirable.- Knowledge of database technologies like SQL, NoSQL, and object-oriented databases.\nThis is a fantastic opportunity for a Senior Python Developer who is looking to take their career to the next level by working on challenging projects with a team of dedicated professionals. If you meet the qualifications and are eager to contribute to a forward-thinking company, we encourage you to apply.",
        'apply_url': 'https://www.linkedin.com/job-apply/3905906121',
        'listed_at': 1714000098000,
        'job_id': 3905906121,
        'job_posted': '2024-04-25 15:25:02'
    },
    {
        'title': 'Python Developer Pandas/NumPy/SQL/RDBMS',
        'company': 'Zeektek',
        'location': 'California, United States',
        'description': 'We have a contract position that goes to December 31st 2024. The position could be extended, or converted to a FTE. The position is for a Python / Pandas Automation Developer with strong experience in SQL programming. Experience with relational databases (Oracle, Teradata etc.), experience working with flat files (different delimiter, escape characters, common flat file issues)\nNice to have - Power BI, Power automate (MS environment), experience with APIs, experience with SFTP jobs, Snowflake\nPreferred candidates will sit in CA. The position is 100% remote and must work in Pacific hours.  Day-to-day responsibilities:Create and maintain complex data extracts in agreed-upon file layouts and send to internal/external teams at specific frequencies using Python, SQL, Excel, flat files (csv etc).Ingest data from different internal teams / external vendors in our databases.Automate data extract jobs/reports using Python scripts.Supporting ad hoc requests from management to run data analysis and provide requested information.Creating dashboards/reports using Power BICreate Scorecards for Health Information Exchanges and present them to HIEs.Work with different teams across the organization to get the answers to chase data needs.Re-engineered data processes in the department.Describe the performance expectations/metrics for this individual and their team:Expert in Python / Pandas coding, Coding in SQL, create/ingest data extract from databases in agreed upon file layouts and send to internal / external teams at specific frequency.Lead / Own a project and communicate with internal teams and external vendors.Ability to multitask on multiple projectsInternal/External Groups with which the Candidate will interface: Required Skills/Experience: Expert in Python / Pandas, automation and Advanced SQL Operations – Coding in Python and SQL. Run, monitor, automate, oversee data processing jobs Data File / Flat file parsing. Ingesting data from flat files in database. Sending data extract in agreed file format to internal / external vendors. Working with flat files using different delimiters. Data Analysis using Python/SQL on data stored in RDBMS like Oracle, Snowflake, Teradata, SQL Server. Research data needs, location, completeness, accuracy of data. Interface with business customers. Automate jobs using Python and Re-engineer data processes in department Internal Customer facing lead / contributor Ability to navigate and identify organization resources / subject matter experts to obtain knowledge in a decentralized organization Ability to multitask on multiple projects in parallel Education Requirement: Computer Science or equivalent Software Skills Required: Expert in Python, Advanced SQL, Automation, Running data analysis on RDBMS databases like Oracle, Teradata, Snowflake etc.',
        'apply_url': 'https://www.linkedin.com/job-apply/3905910594',
        'listed_at': 1714006028000,
        'job_id': 3905910594,
        'job_posted': '2024-04-25 15:25:08'
    },
]

# Streamlit app
def job_recommendations():
    
    st.title("Job Recommendations")
    st.image("Job_Recommendation.jpg", width=300, use_column_width=True)
    # Calculate the width of each column dynamically
    num_columns = len(jobs_data)
    col_width = int(12 / num_columns)

    # Display jobs in expanders side by side
    for job in jobs_data:
        with st.expander(f"{job['title']}\n\n{job['company']}, {job['location']}"):
            st.write("[Apply Here](" + job['apply_url'] + ")")
            st.write(job['description'])
            st.write("---")
