from typing import Optional
from pydantic import BaseModel


class ApplicationCreate(BaseModel):
    name: str
    description: Optional[str] = None
    team_id: int


class ApplicationRead(BaseModel):
    id: int
    name: str
    description: Optional[str] = None
    team_id: int

    class Config:
        from_attributes = True


class ApplicationUpdate(BaseModel):
    name: str
    description: Optional[str] = None
    team_id: int
