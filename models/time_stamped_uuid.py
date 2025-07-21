from nanoid import generate
from datetime import datetime
from sqlmodel import SQLModel, Field


class TimeStampedUUIDModel(SQLModel):
    uid: str = Field(
        default_factory=generate,
        primary_key=True,
        index=True,
        nullable=False
    )
    created_at: datetime = Field(
        default_factory=datetime.utcnow,
        nullable=False
    )
    updated_at: datetime = Field(
        default_factory=datetime.utcnow,
        nullable=False
    )
