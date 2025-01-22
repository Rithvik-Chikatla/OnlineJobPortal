from fastapi import FastAPI, Depends, HTTPException, Request
from sqlalchemy.orm import Session
import crud, models, schemas, database, auth
from database import engine, SessionLocal
import json
from typing import List, Optional
import bcrypt

app = FastAPI()
models.Base.metadata.create_all(bind=engine)



def get_db():
    db = database.SessionLocal()
    try:
        yield db
    finally:
        db.close()

def hash_password(password: str) -> str:
    salt = bcrypt.gensalt()
    hashed_password = bcrypt.hashpw(password.encode('utf-8'), salt)
    return hashed_password.decode('utf-8')

@app.post("/signup")
def signup(user: schemas.UserCreate, db: Session = Depends(get_db)):
    user.password = hash_password(user.password)
    return crud.create_user(db=db, user=user)

@app.post("/login")
def login(user: schemas.UserLogin, db: Session = Depends(get_db)):
    db_user = crud.authenticate_user(db=db, email=user.email, password=user.password)
    if not db_user:
        raise HTTPException(status_code=400, detail="Invalid credentials")
    # curr_user = db_user
    # print(curr_user.email)
    # return db_user
    return {"token": auth.create_access_token(user={"email": db_user.email, "role": db_user.role, "id": db_user.id}), "role": db_user.role, "id": db_user.id}


@app.post("/jobs")
def create_job(job: schemas.JobCreate, db: Session = Depends(get_db), current_user: models.User = Depends(auth.get_current_user)):
    # print(curr_user.email)
    # print(job)
    if current_user.role != "Employer":
        raise HTTPException(status_code=403, detail="Not authorized")
    job.employer_id = current_user.id
    return crud.create_job(db=db, job=job, employer_id=current_user.id)

# def get_jobs(db: Session = Depends(get_db), filters: dict = None):
@app.get("/jobs")
def get_jobs(db: Session = Depends(get_db), industry: Optional[str] = None,
    skills: Optional[List[str]] = None,
    location: Optional[str] = None,
    salary_range: Optional[str] = None,
    employer_id: Optional[str] = None,
    id: Optional[str] = None):
    # print(filters)
    filters = {}
    if industry:
        filters["industry"] = industry
    if skills:
        filters["skills"] = skills
    if location:
        filters["location"] = location
    if salary_range:
        filters["salary_range"] = salary_range
    if employer_id:
        filters["employer_id"] = employer_id
    if id:
        filters["id"] = id
    
    print(filters)
    return crud.get_jobs(db=db, filters=filters)

@app.delete("/jobs/{id}")
def delete_job(id: str, db: Session = Depends(get_db)):
    filters = {}
    filters["id"] = id
    job = crud.get_jobs(db, filters=filters)
    if not job:
        raise HTTPException(status_code=404, detail="Job not found")

    # Delete the job
    crud.delete_job(db, id=id)
    return {"message": "Job deleted successfully"}

@app.post("/applications")
def apply_job(application: schemas.ApplicationCreate, db: Session = Depends(get_db)):
    return crud.apply_for_job(db=db, application=application)

@app.get("/applications")
def get_applications(user_id: str = None, job_id: str = None, db: Session = Depends(get_db)):
    return crud.get_user_applications(db=db, user_id=user_id, job_id=job_id)
