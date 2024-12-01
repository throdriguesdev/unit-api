from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, clear_mappers
DATABASE_URL = "postgresql://user:password@postgres_db:5432/assets_db"
engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()
clear_mappers()
Base.metadata.clear()
Base.metadata.create_all(bind=engine)
