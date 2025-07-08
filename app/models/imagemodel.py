import datetime
import uuid

from config import tzinfo
from sqlmodel import Field, SQLModel


class ImageModel(SQLModel, table=True):
    guid: uuid.UUID = Field(default_factory=uuid.uuid4, primary_key=True)
    image: str
    name: str = Field(index=True)
    short_description: str
    description: str
    # tags: list[str] = Field(index=True)
    created_at: datetime.datetime = Field(
        default_factory=lambda: datetime.datetime.now(tzinfo)
    )
    updated_at: datetime.datetime = Field(
        default_factory=lambda: datetime.datetime.now(tzinfo)
    )
