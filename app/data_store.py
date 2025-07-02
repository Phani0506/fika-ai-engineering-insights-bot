import os
from sqlalchemy import create_engine, Column, Integer, String, Float, DateTime
from sqlalchemy.orm import sessionmaker, declarative_base
import datetime

# Define the base for our models
Base = declarative_base()
DB_PATH = os.path.join('data', 'dev_metrics.db')

class Commit(Base):
    __tablename__ = 'commits'
    id = Column(Integer, primary_key=True)
    commit_hash = Column(String, unique=True, nullable=False)
    author = Column(String, nullable=False)
    timestamp = Column(DateTime, nullable=False)
    additions = Column(Integer)
    deletions = Column(Integer)
    files_changed = Column(Integer)

class PullRequest(Base):
    __tablename__ = 'pull_requests'
    id = Column(Integer, primary_key=True)
    pr_id = Column(Integer, unique=True, nullable=False)
    author = Column(String, nullable=False)
    created_at = Column(DateTime, nullable=False)
    merged_at = Column(DateTime)
    cycle_time_hours = Column(Float) # Time from first commit to merge

def get_engine():
    """Initializes and returns the SQLAlchemy engine."""
    # The database will be created in the `data` directory at the project root
    return create_engine(f'sqlite:///{DB_PATH}')

def get_session():
    """Returns a new database session."""
    engine = get_engine()
    Base.metadata.create_all(engine) # Create tables if they don't exist
    Session = sessionmaker(bind=engine)
    return Session()

print("✅ Data store module initialized.")