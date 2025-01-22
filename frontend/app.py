import streamlit as st
from authentication import authenticate_user, display_login, display_signup
from job_posting import post_job_form
from job_search import job_search_form
from dashboard import display_dashboard

def main():
    st.title("Job Portal")
    
    if "user" not in st.session_state:
        st.session_state.user = None
    if "role" not in st.session_state:
        st.session_state.role = None

    choice = st.sidebar.selectbox("Select an option", ["Login", "Sign Up"])
    
    if choice == "Login":
        user = display_login() 
    # if user:  
    #     st.session_state.user = user
    #     st.session_state.role = user.get("role")
    #     st.session_state.token = user.get("token")
    elif choice == "Sign Up":
        user = display_signup() 
    if user:  
        st.session_state.user = user
        st.session_state.role = user.get("role")
        st.session_state.token = user.get("token")
        st.session_state.id = user.get("id")

    if st.session_state.user:
    #     st.write(f"Welcome, {st.session_state.user.get('name')}!")
        role = st.session_state.role
        token = st.session_state.token
        id = st.session_state.id

        if role == "Employer":
            post_job_form(token)  
            display_dashboard("employer", id)

        elif role == "Job Seeker":
            job_search_form(id)  
            display_dashboard("job_seeker", id)
    else:
        st.write("Please log in or sign up to continue.")

    # if choice == "Login":
    #     user = display_login()
    # elif choice == "Sign Up":
    #     user = display_signup()
    
    # if user:
    #     role = user.get("role")
        
    #     
    #     if role == "Employer":
    #         post_job_form()
    #         # display_dashboard("employer")
    #     elif role == "Job Seeker":
    #         job_search_form()
    #         # display_dashboard("job_seeker")

if __name__ == "__main__":
    main()
