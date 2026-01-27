from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship

Base = declarative_base()


class User(Base):
    __tablename__ = "user"

    id = Column(Integer, primary_key=True, index=True)
    email = Column(String(120), unique=True, nullable=False, index=True)
    password = Column(String(200), nullable=False)
    role = Column(String(20), default="USER")

    tasks = relationship("Task", back_populates="owner")


class Task(Base):
    __tablename__ = "task"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String(100))
    description = Column(String(200))
    user_id = Column(Integer, ForeignKey("user.id"))

    owner = relationship("User", back_populates="tasks")
