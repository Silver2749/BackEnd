"""FastAPI Application Package"""
from app.factory import create_app, engine, SessionLocal


def get_db():
    """Database session dependency"""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


__all__ = ["create_app", "get_db", "engine", "SessionLocal"]
