from sqlalchemy.orm import Session
import models, schemas
from fastapi import HTTPException, status
# from models import User
import bcrypt

def create_user(db: Session, user: schemas.UserCreate):
    existing_user = db.query(models.User).filter(models.User.email == user.email).first()
    if existing_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Email already exists."
        )
    
    db_user = models.User(id=user.id, email=user.email, password=user.password, role=user.role)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    # return db_user
    return schemas.UserResponse(id=db_user.id, email=db_user.email, role=db_user.role)

def authenticate_user(db: Session, email: str, password: str):
    db_user = db.query(models.User).filter(models.User.email == email).first()
    
    # Check if the user exists and if the password matches
    if db_user and bcrypt.checkpw(password.encode('utf-8'), db_user.password.encode('utf-8')):
        return db_user
    return None
    # return db.query(models.User).filter(models.User.email == email, models.User.password == password).first()

def create_job(db: Session, job: schemas.JobCreate, employer_id: str):
    # db_job = models.Job(**job.model_dump(), employer_id=employer_id)
    db_job = models.Job(id=job.id, title=job.title, description=job.description, employer_id=employer_id, industry=job.industry, required_skills=job.required_skills, location=job.location, salary_range=job.salary_range, deadline=job.deadline)
    db.add(db_job)
    db.commit()
    db.refresh(db_job)
    return db_job

def get_jobs(db: Session, filters: dict):
    query = db.query(models.Job)
    if filters:
        if filters.get("industry"):
            query = query.filter(models.Job.industry == filters["industry"])
        if filters.get("location"):
            query = query.filter(models.Job.location == filters["location"])
        if filters.get("employer_id"):
            query = query.filter(models.Job.employer_id == filters["employer_id"])
        if filters.get("id"):
            query = query.filter(models.Job.id == filters["id"])  
    return query.all()

def delete_job(db: Session, id: str):
    db_job = db.query(models.Job).filter(models.Job.id == id).first()
    if db_job:
        db.delete(db_job)
        db.commit()
        return db_job
    return None

def apply_for_job(db: Session, application: schemas.ApplicationCreate):
    db_application = models.Application(**application.dict())
    db.add(db_application)
    db.commit()
    db.refresh(db_application)
    return db_application

def get_user_applications(db: Session, user_id: str, job_id: str):
    query = db.query(models.Application)
    if user_id: 
        query = db.query(models.Application).filter(models.Application.seeker_id == user_id).all()
    if job_id:
        query = db.query(models.Application).filter(models.Application.job_id == job_id).all()
    return query


def get_user_by_id(db: Session, user_id: str):
    return db.query(models.User).filter(models.User.id == user_id).first()