from pydantic import BaseModel, PastDatetime


class Version(BaseModel):
    version: str
    date: PastDatetime
