from sqlalchemy import Column, Integer, String, ForeignKey, Date, Float
from sqlalchemy.orm import relationship
from database import Base

class User(Base):
    __tablename__ = "users"
    
    id = Column(String(50), primary_key=True, index=True)
    email = Column(String(50), unique=True, index=True)
    password = Column(String(150))
    role = Column(String(50))  # 'job_seeker' or 'employer'
    location = Column(String(50))

class Job(Base):
    __tablename__ = "jobs"
    
    id = Column(String(50), primary_key=True, index=True)
    title = Column(String(50))
    description = Column(String(50))
    employer_id = Column(String(50), ForeignKey("users.id"))
    employer = relationship("User", back_populates="jobs")
    industry = Column(String(50))
    required_skills = Column(String(100))  # JSON field
    location = Column(String(50))
    salary_range = Column(String(50))
    deadline = Column(Date)

class Application(Base):
    __tablename__ = "applications"
    
    id = Column(String(50), primary_key=True, index=True)
    job_id = Column(String(50), ForeignKey("jobs.id"))
    seeker_id = Column(String(50), ForeignKey("users.id"))
    status = Column(String(50))  # 'pending', 'accepted', 'rejected'
    application_date = Column(Date)

# Relationship definitions
User.jobs = relationship("Job", back_populates="employer")
