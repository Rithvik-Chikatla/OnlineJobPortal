import streamlit as st
import requests

API_URL = "http://127.0.0.1:8000"  # FastAPI backend URL

if "delete_message" not in st.session_state:
    st.session_state["delete_message"] = None

def display_dashboard(role, id):
    if role == "job_seeker":
        st.subheader("Job Seeker Dashboard")
        
        response = requests.get(f"{API_URL}/applications", params={"user_id": id})
        applications = response.json()
        if applications:
            for app in applications:
                # print(app['job_id'])
                job_response = requests.get(f"{API_URL}/jobs", params={"id": app['job_id']})
                job_data = job_response.json()
                job = job_data[0]
                if job:
                    st.write(f"Job: {job['title']} - Status: {app['status']}")
        else:
            st.write("No applications found.")
        
    elif role == "employer":
        if "delete_message" not in st.session_state:
            st.session_state["delete_message"] = None
        st.subheader("Employer Dashboard")
        st.write("Your posted jobs")
        response = requests.get(f"{API_URL}/jobs", params={"employer_id": id})
        jobs = response.json()
        if jobs:
            for job in jobs:

                applicants_response = requests.get(f"{API_URL}/applications", params={"job_id": job['id']})
                applicants = applicants_response.json()
                st.write(f"Job: {job['title']} Applicants: {len(applicants)}")
                # for applicant in applicants:
                #     st.write(applicant['email'])
                if st.button(f"Delete {job['title']}", key=f"delete_{job['id']}"):
                    delete_job(job['id'])
                    st.success(f"Job '{job['title']}' has been deleted.")
                    # response = requests.get(f"{API_URL}/jobs", params={"employer_id": id})
                    # jobs = response.json()
                    st.session_state["delete_message"] = f"Job '{job['title']}' has been deleted."
                    st.rerun()
                    # break  
        else:
            st.write("No posted jobs.")

    if st.session_state["delete_message"]:
        st.success(st.session_state["delete_message"])
        st.session_state["delete_message"] = None


def delete_job(job_id):
    try:
        response = requests.delete(f"{API_URL}/jobs/{job_id}")
        if response.status_code == 200:
            st.success("Job deleted successfully!")
        else:
            st.error(f"Failed to delete the job. Status code: {response.status_code}")
    except requests.exceptions.RequestException as e:
        st.error(f"An error occurred while deleting the job: {str(e)}")