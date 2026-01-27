"""Application factory module - creates FastAPI app with all routes and middleware"""
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from config import Config
import os

# Database setup
engine = create_engine(Config.SQLALCHEMY_DATABASE_URI)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


def create_app():
    """Create and configure FastAPI application"""
    app = FastAPI(title="Task Management API")

    # Add CORS middleware
    app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    # Import and create database tables
    from app.models import Base
    Base.metadata.create_all(bind=engine)

    # Register auth routes
    from app.routes.auth import auth_router
    app.include_router(auth_router, prefix="/api/auth", tags=["auth"])

    # Register task routes
    from app.routes.task import task_router
    app.include_router(task_router, prefix="/api/tasks", tags=["tasks"])

    # Get frontend path
    base_dir = os.path.dirname(os.path.dirname(__file__))
    frontend_path = os.path.join(base_dir, 'frontend')
    
    # Mount static files
    if os.path.exists(frontend_path):
        app.mount("/static", StaticFiles(directory=frontend_path), name="static")
    
    # Root route - serve index.html
    @app.get("/")
    async def root():
        if os.path.exists(frontend_path):
            index_file = os.path.join(frontend_path, 'index.html')
            if os.path.exists(index_file):
                return FileResponse(index_file, media_type="text/html")
        return {"message": "Task Management API", "visit": "/docs"}

    # Dashboard route
    @app.get("/dashboard")
    async def dashboard():
        if os.path.exists(frontend_path):
            dashboard_file = os.path.join(frontend_path, 'dashboard.html')
            if os.path.exists(dashboard_file):
                return FileResponse(dashboard_file, media_type="text/html")
        return {"message": "Task Management API", "visit": "/docs"}

    return app
