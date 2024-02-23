from pydantic import BaseModel


class Context(BaseModel):
    name: str
    response: dict = dict()
