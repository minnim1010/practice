from typing import Optional
from pydantic import BaseModel


class TeamCreate(BaseModel):
    squad_name: str
    squad_lead: str
    tribe: str
    tribe_lead: str
    product_line: str
    dh_slack_group: str


class TeamRead(BaseModel):
    id: int
    squad_name: Optional[str] = None
    squad_lead: Optional[str] = None
    tribe: Optional[str] = None
    tribe_lead: Optional[str] = None
    product_line: Optional[str] = None
    dh_slack_group: Optional[str] = None

    class Config:
        from_attributes = True


class TeamUpdate(BaseModel):
    squad_name: Optional[str] = None
    squad_lead: Optional[str] = None
    tribe: Optional[str] = None
    tribe_lead: Optional[str] = None
    product_line: Optional[str] = None
    dh_slack_group: Optional[str] = None
