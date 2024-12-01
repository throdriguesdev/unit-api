from sqlalchemy import Column, Integer, String
from app.database import Base


class Asset(Base):
    __tablename__ = "assets"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    name = Column(String, index=True, nullable=False)
    description = Column(String, nullable=True)
    category = Column(String, nullable=False)  
    status = Column(String, nullable=False)  