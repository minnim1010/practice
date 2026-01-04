from pydantic import BaseModel


class SourceBase(BaseModel):
    name: str


class SourceCreate(SourceBase):
    pass


class SourceUpdate(SourceBase):
    pass


class SourceRead(SourceBase):
    id: int

    class Config:
        from_attributes = True
