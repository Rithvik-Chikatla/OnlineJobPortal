from fastapi import FastAPI, Depends
from fastapi.middleware.cors import CORSMiddleware
from .routers import auth, jobs, applications
from .models import database

app = FastAPI(title="Job Portal API")

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:8501"],  # Streamlit default port
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Create database tables
database.Base.metadata.create_all(bind=database.engine)

# Include routers
app.include_router(auth.router, prefix="/api", tags=["Authentication"])
app.include_router(jobs.router, prefix="/api/jobs", tags=["Jobs"])
app.include_router(applications.router, prefix="/api/applications", tags=["Applications"])

@app.get("/")
async def root():
    return {"message": "Welcome to Job Portal API"}
