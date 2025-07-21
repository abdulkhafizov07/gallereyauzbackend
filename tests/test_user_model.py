import uuid
import pytest
from sqlmodel import select
from models.user import UserModel


class TestUserModel:

    @pytest.fixture
    def user_data(self):
        return {
            "first_name": "John",
            "middle_name": "A.",
            "last_name": "Doe",
            "email": "test@example.com",
            "phone": "1234567890",
            "password": "hashedpassword123",
            "is_active": True,
            "is_superuser": False,
            "is_verified": True,
        }

    def test_create_user_model(self, session, user_data):
        user = UserModel(**user_data)
        session.add(user)
        session.commit()
        session.refresh(user)

        assert user.guid is not None
        assert isinstance(user.guid, uuid.UUID)
        assert user.email == user_data["email"]

    def test_bulk_create_users(self, session):
        users = [
            UserModel(
                first_name="User",
                middle_name="One",
                last_name="Example",
                email="user1@example.com",
                phone="1111111111",
                password="pass",
                is_active=True,
                is_superuser=False,
                is_verified=True,
            ),
            UserModel(
                first_name="User",
                middle_name="Two",
                last_name="Example",
                email="user2@example.com",
                phone="2222222222",
                password="pass",
                is_active=True,
                is_superuser=False,
                is_verified=True,
            ),
            UserModel(
                first_name="User",
                middle_name="Three",
                last_name="Example",
                email="user3@example.com",
                phone="3333333333",
                password="pass",
                is_active=False,
                is_superuser=False,
                is_verified=False,
            ),
        ]
        session.add_all(users)
        session.commit()

        result = session.exec(select(UserModel)).all()
        assert len(result) == 3

    def test_select_user_model_by_email(self, session):
        session.add_all([
            UserModel(
                first_name="Match",
                middle_name="One",
                last_name="Example",
                email="match1@example.com",
                phone="4444444444",
                password="x",
                is_active=True,
                is_superuser=False,
                is_verified=False,
            ),
            UserModel(
                first_name="Special",
                middle_name="One",
                last_name="Example",
                email="special@example.com",
                phone="5555555555",
                password="x",
                is_active=False,
                is_superuser=True,
                is_verified=True,
            ),
        ])
        session.commit()

        from sqlalchemy import func

        stmt = select(UserModel).where(func.lower(UserModel.email).like("%example.com"))
        results = session.exec(stmt).all()

        assert all("example.com" in user.email.lower() for user in results)

    def test_update_user_model(self, session, user_data):
        user = UserModel(**user_data)
        session.add(user)
        session.commit()

        user.email = "updated@example.com"
        session.add(user)
        session.commit()

        updated = session.exec(
            select(UserModel).where(UserModel.guid == user.guid)
        ).first()
        assert updated.email == "updated@example.com"

    def test_delete_user_model(self, session, user_data):
        user = UserModel(**user_data)
        session.add(user)
        session.commit()

        session.delete(user)
        session.commit()

        deleted = session.exec(
            select(UserModel).where(UserModel.guid == user.guid)
        ).first()
        assert deleted is None

    def test_repr_and_str(self, user_data):
        user = UserModel(**user_data)
        assert user.email in str(user)
