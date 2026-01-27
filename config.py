import os


class Config:
    SECRET_KEY = "secret-key"
    SQLALCHEMY_DATABASE_URI = "sqlite:///./db.sqlite3"
    JWT_SECRET_KEY = "jwt-secret"
