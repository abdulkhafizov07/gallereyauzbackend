import uuid

from sqlmodel import Field, SQLModel


class ImageModel(SQLModel, table=True):
    __tablename__ = "image_model"

    guid: uuid.UUID = Field(
        default_factory=uuid.uuid4, primary_key=True, index=True, nullable=False
    )
    title: str
    short_description: str
    description: str
