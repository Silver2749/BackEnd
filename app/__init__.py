
from app.factory import create_app, engine, SessionLocal


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


__all__ = ["create_app", "get_db", "engine", "SessionLocal"]
