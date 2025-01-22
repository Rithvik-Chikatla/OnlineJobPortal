from sqlalchemy import Boolean, Column, ForeignKey, Integer, String, JSON, DateTime, Table
from sqlalchemy.orm import relationship
from .database import Base

# Association tables for many-to-many relationships
job_skills = Table('job_skills', Base.metadata,
    Column('job_id', Integer, ForeignKey('jobs.id')),
    Column('skill_id', Integer, ForeignKey('skills.id'))
)

user_skills = Table('user_skills', Base.metadata,
    Column('user_id', Integer, ForeignKey('users.id')),
    Column('skill_id', Integer, ForeignKey('skills.id'))
)

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, index=True)
    name = Column(String)
    hashed_password = Column(String)
    role = Column(String)  # job_seeker or employer
    location = Column(String)
    
    # Relationships
    posted_jobs = relationship("Job", back_populates="employer")
    applications = relationship("Application", back_populates="seeker")
    skills = relationship("Skill", secondary=user_skills)

class Job(Base):
    __tablename__ = "jobs"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, index=True)
    description = Column(String)
    employer_id = Column(Integer, ForeignKey("users.id"))
    industry_id = Column(Integer, ForeignKey("industries.id"))
    location = Column(String)
    salary_min = Column(Integer)
    salary_max = Column(Integer)
    deadline = Column(DateTime)
    is_active = Column(Boolean, default=True)

    # Relationships
    employer = relationship("User", back_populates="posted_jobs")
    applications = relationship("Application", back_populates="job")
    skills = relationship("Skill", secondary=job_skills)
    industry = relationship("Industry")

class Application(Base):
    __tablename__ = "applications"

    id = Column(Integer, primary_key=True, index=True)
    job_id = Column(Integer, ForeignKey("jobs.id"))
    seeker_id = Column(Integer, ForeignKey("users.id"))
    status = Column(String)  # pending, accepted, rejected
    application_date = Column(DateTime)

    # Relationships
    job = relationship("Job", back_populates="applications")
    seeker = relationship("User", back_populates="applications")

class Industry(Base):
    __tablename__ = "industries"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, unique=True, index=True)

class Skill(Base):
    __tablename__ = "skills"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, unique=True, index=True)
