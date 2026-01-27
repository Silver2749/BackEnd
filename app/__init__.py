from fastapi import FastAPI
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from config import Config

engine = create_engine(Config.SQLALCHEMY_DATABASE_URI)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


def create_app():
    """Application factory"""
    app = FastAPI(title="Task Management API")

    # Import models to create tables
    from app.models import Base

    Base.metadata.create_all(bind=engine)

    # Register routes
    from app.routes.task import task_router

    app.include_router(task_router, prefix="/api/tasks", tags=["tasks"])

    return app
