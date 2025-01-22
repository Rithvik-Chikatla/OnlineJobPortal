import streamlit as st
import requests
import uuid

API_URL = "http://127.0.0.1:8000"  

def post_job_form(token):
    st.subheader("Post a Job")

    title = st.text_input("Job Title")
    description = st.text_area("Job Description")
    industry = st.selectbox("Industry", ["Technology", "Healthcare", "Finance"])
    required_skills = st.multiselect("Required Skills", ["Python", "Java", "Machine Learning", "Data Analysis"])
    location = st.text_input("Location")
    salary_range = st.slider("Salary Range", 30000, 200000, (50000, 100000))
    # salary_range = st.text_input("Salary Range")
    deadline = st.date_input("Application Deadline")
    # deadline = st.text_input("Enter date in text")
    id = uuid.uuid1()


    if st.button("Post Job"):
        # print(id, required_skills, salary_range, deadline, industry)
        # print(str(required_skills))
        deadline_str = deadline.strftime("%Y-%m-%d")

        job_data = {
            "id": id.hex,
            "title": title,
            "description": description,
            "employer_id": "",
            "industry": industry,
            "required_skills": str(required_skills),
            "location": location,
            "salary_range": str(salary_range),
            "deadline": deadline_str,
        }
        # headers = {
        # "Authorization": f"Bearer {token}",
        # }
        response = requests.post(f"{API_URL}/jobs/?token={token}", json=job_data)
        if response.status_code == 200:
            st.success("Job posted successfully!")
        else:
            st.error("Failed to post job.")
