from pydantic import BaseModel
from typing import List, Optional
from datetime import date

class UserCreate(BaseModel):
    id: str
    email: str
    password: str
    role: str

class UserResponse(BaseModel):
    id: str
    email: str
    role: str

    class Config:
        orm_mode = True
        exclude = {"password"}

class JobCreate(BaseModel):
    id: str
    title: str
    description: str
    employer_id: str
    industry: str
    required_skills: str
    location: str
    salary_range: str
    deadline: str

class ApplicationCreate(BaseModel):
    id: str
    job_id: str
    seeker_id: str
    status: str
    application_date: str

class UserLogin(BaseModel):
    email: str
    password: str
