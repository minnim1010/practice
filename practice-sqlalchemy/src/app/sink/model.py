from sqlalchemy import Column, Integer, String
from app.database import Base


class Sink(Base):
    __tablename__ = "sinks"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100), index=True)
