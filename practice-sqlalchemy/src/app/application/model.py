from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship

from app.database import Base


class Application(Base):
    __tablename__ = "applications"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100), index=True)
    description = Column(String(200))
    team_id = Column(Integer, ForeignKey("teams.id"))

    team = relationship("Team", back_populates="applications", lazy="raise_on_sql")
