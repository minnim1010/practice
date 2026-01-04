from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship

from app.database import Base


class Team(Base):
    __tablename__ = "teams"

    id = Column(Integer, primary_key=True, index=True)
    squad_name = Column(String(100), index=True)
    squad_lead = Column(String(100))
    tribe = Column(String(100))
    tribe_lead = Column(String(100))
    product_line = Column(String(100))
    dh_slack_group = Column(String(100))

    applications = relationship("Application", back_populates="team", lazy="raise_on_sql")
