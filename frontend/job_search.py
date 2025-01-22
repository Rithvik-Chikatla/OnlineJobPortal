import streamlit as st
import requests
import uuid
from datetime import datetime


API_URL = "http://127.0.0.1:8000"  

def job_search_form(seeker_id):
    st.subheader("Search Jobs")

    
    industry = st.selectbox("Industry", ["Technology", "Healthcare", "Finance"])
    skills = st.multiselect("Skills", ["Python", "Java", "Machine Learning", "Data Analysis"])
    location = st.text_input("Location")
    salary_range = st.slider("Salary Range", 30000, 200000, (50000, 100000))

    if st.button("Search"):
        st.session_state["job_filters"] = {
            "industry": industry,
            "skills": skills,
            "location": location,
            "salary_range": salary_range,
        }
        st.session_state["searched"] = True  

    if st.session_state.get("searched", False):
        job_filters = st.session_state.get("job_filters", {})
        try:
            response = requests.get(f"{API_URL}/jobs", params=job_filters)
            if response.status_code == 200:
                jobs = response.json()  

                if jobs:
                    for job in jobs:
                        st.write(f"**{job['title']}** - {job['description']}")
                        st.write(f"**Location:** {job['location']} | **Salary:** {job['salary_range']}")

                        apply_key = f"applied_{job['id']}"

                        if apply_key not in st.session_state:
                            st.session_state[apply_key] = False

                        if st.session_state[apply_key]:
                            st.success(f"You have already applied to {job['title']}!")
                        else:
                            if st.button(f"Apply to {job['title']}", key=f"apply_btn_{job['id']}"):
                                apply_to_job(job["id"], seeker_id)
                                st.session_state[apply_key] = True  
                else:
                    st.error("No jobs found.")
            else:
                st.error(f"Failed to retrieve jobs. Status code: {response.status_code}")
        except requests.exceptions.RequestException as e:
            st.error(f"An error occurred while making the request: {str(e)}")

def apply_to_job(job_id, seeker_id):
    
    id = str(uuid.uuid1())
    application_date = datetime.today().strftime('%Y-%m-%d')

    payload = {
        "id": id,
        "job_id": job_id,
        "seeker_id": seeker_id,
        "status": "Pending",
        "application_date": application_date
    }

    try:
        response = requests.post(f"{API_URL}/applications", json=payload)
        
        if response.status_code == 200:  # HTTP 201 Created
            st.success("You have successfully applied to the job!")
        elif response.status_code == 400:
            st.warning(response.json().get("detail", "Failed to apply to the job."))
        else:
            st.error(f"Failed to apply to the job. Status code: {response.status_code}")
    except requests.exceptions.RequestException as e:
        st.error(f"An error occurred while applying to the job: {str(e)}")
