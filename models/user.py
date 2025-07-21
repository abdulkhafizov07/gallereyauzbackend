from pydantic import EmailStr
from sqlmodel import Field
from .time_stamped_uuid import TimeStampedUUIDModel


class UserModel(TimeStampedUUIDModel, table=True):
    __tablename__ = "user_model"

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
