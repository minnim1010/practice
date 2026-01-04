from pydantic import BaseModel


class SinkBase(BaseModel):
    name: str


class SinkCreate(SinkBase):
    pass


class SinkUpdate(SinkBase):
    pass


class SinkRead(SinkBase):
    id: int

    class Config:
        from_attributes = True
