import uuid

from pydantic import EmailStr
from sqlmodel import Field, SQLModel


class UserModel(SQLModel, table=True):
    __tablename__ = "user_model"

    guid: uuid.UUID = Field(
        default_factory=uuid.uuid4, primary_key=True, nullable=False
    )

    first_name: str
    middle_name: str
    last_name: str

    email: EmailStr = Field(nullable=True)
    phone: str
    password: str

    is_active: bool = Field(True, nullable=False)
    is_superuser: bool = Field(False, nullable=False)
    is_verified: bool = Field(False, nullable=False)

    model_config = {"arbitrary_types_allowed": True}
