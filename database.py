import uuid
from contextlib import contextmanager
from typing import Any

import sqlalchemy
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

import config

Base = declarative_base()


class Quiz(Base):
    __tablename__ = "quiz"

    id = sqlalchemy.Column(sqlalchemy.Integer, primary_key=True)
    key = sqlalchemy.Column(sqlalchemy.TEXT, unique=True, nullable=False)
    name = sqlalchemy.Column(sqlalchemy.TEXT, unique=False, nullable=False)
    quiz_xml = sqlalchemy.Column(sqlalchemy.TEXT, unique=False, nullable=False)


class Database:
    def __init__(self):
        self.engine = sqlalchemy.create_engine(f"sqlite:///{config.DATABASE_PATH}")

        Base.metadata.create_all(self.engine)

        self.Session = sessionmaker(bind=self.engine)

    @contextmanager
    def session_scope(self):
        session = self.Session()
        try:
            yield session
            session.commit()  # Commit if no errors
        except Exception as e:
            session.rollback()  # Rollback in case of error
            raise e
        finally:
            session.close()  # Always close the session

    @staticmethod
    def generate_unique_uuid(session):
        """Generate a unique UUID that is not already in the database."""
        while True:
            new_uuid = str(uuid.uuid4())  # Generate a new UUID
            # Check if the generated UUID already exists in the 'key' field
            existing_entry = session.query(Quiz).filter_by(key=new_uuid).first()
            if not existing_entry:  # If no existing entry is found, it's unique
                return new_uuid

    def add_new_quiz(self, name: str, quiz_xml: str) -> str:
        with self.session_scope() as session:
            unique_key = self.generate_unique_uuid(session)
            new_entry = Quiz(key=unique_key, name=name, quiz_xml=quiz_xml)
            session.add(new_entry)
        return unique_key

    def get_quiz_by_key(self, key: str) -> dict[str, Any] | None:
        with self.session_scope() as session:
            result = session.query(Quiz).filter_by(key=key).first()
            if result:
                return {
                    "name": result.name,
                    "quiz_xml": result.quiz_xml
                }
            return None
