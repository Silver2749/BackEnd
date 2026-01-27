from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from config import Config
import os


engine = create_engine(Config.SQLALCHEMY_DATABASE_URI)        # databaseee
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


def create_app():
    app = FastAPI(title="Task Management API")

   
    app.add_middleware(              # add middleware.
        CORSMiddleware,
        allow_origins=["*"],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    
    from app.models import Base      #import db

    Base.metadata.create_all(bind=engine)

    
    from app.routes.auth import auth_router  #make auth routes

    app.include_router(auth_router, prefix="/api/auth", tags=["auth"])

   
    from app.routes.task import task_router        #register task routes

    app.include_router(task_router, prefix="/api/tasks", tags=["tasks"])

   
    base_dir = os.path.dirname(os.path.dirname(__file__))      #frontend path
    frontend_path = os.path.join(base_dir, "frontend")

   
    if os.path.exists(frontend_path):                  #static files 
        app.mount("/static", StaticFiles(directory=frontend_path), name="static")

   
    @app.get("/")
    async def root():
        if os.path.exists(frontend_path):
            index_file = os.path.join(frontend_path, "index.html")
            if os.path.exists(index_file):
                return FileResponse(index_file, media_type="text/html")
        return {"message": "Task Management API", "visit": "/docs"}


    @app.get("/dashboard")         #dashboard route 
    async def dashboard():
        if os.path.exists(frontend_path):
            dashboard_file = os.path.join(frontend_path, "dashboard.html")
            if os.path.exists(dashboard_file):
                return FileResponse(dashboard_file, media_type="text/html")
        return {"message": "Task Management API", "visit": "/docs"}

    return app
