from fastapi import FastAPI,Depends,HTTPException
from sqlmodel import SQLModel,Session,select
from database import engine
from routes import candidate,recruiter,job,tag,skill
import auth
from fastapi.middleware.cors import CORSMiddleware
from fastapi_pagination import add_pagination
    
app = FastAPI()
add_pagination(app)

app.include_router(auth.router)
app.include_router(candidate.router)
app.include_router(recruiter.router)
app.include_router(job.router)
app.include_router(tag.router)
app.include_router(skill.router)

@app.on_event('startup')
def startup():
    SQLModel.metadata.create_all(engine)
    
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"], # In production, change this to your frontend URL
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)