import streamlit as st
import requests
import uuid

API_URL = "http://127.0.0.1:8000"  

def authenticate_user(email, password):
    response = requests.post(f"{API_URL}/login", json={"email": email, "password": password})
    return response.json() if response.status_code == 200 else None

def display_login():
    email = st.text_input("Email")
    password = st.text_input("Password", type="password")
    
    if st.button("Login"):
        user = authenticate_user(email, password)
        if user:
            st.session_state["user"] = user
            st.success("Login successful!")
            return user
        else:
            st.error("Invalid credentials.")
    return None

def display_signup():
    email = st.text_input("Email")
    password = st.text_input("Password", type="password")
    role = st.selectbox("Role", ["Job Seeker", "Employer"])
    id = uuid.uuid1()

    if st.button("Sign Up"):
        response = requests.post(f"{API_URL}/signup", json={"id": id.hex, "email": email, "password": password, "role": role})
        if response.status_code == 200:
            st.success("Account created successfully!")
        else:
            st.error("Error in account creation.")
