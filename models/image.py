from sqlmodel import SQLModel, Field
import uuid


class ImageModel(SQLModel, table=True):
    guid: uuid.UUID = Field(default_factory=uuid.uuid4, primary_key=True, index=True, nullable=False)
    title: str
    short_description: str
    description: str
