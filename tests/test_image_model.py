import pytest
from sqlmodel import select

from models.image import ImageModel


class TestImageModel:

    @pytest.fixture
    def image_data(self):
        return {
            "title": "Test title",
            "short_description": "Simple description for image model test",
            "description": "I can not keep up long text\n" * 16,
        }

    def test_create_image_model(self, session, image_data):
        image = ImageModel(**image_data)
        session.add(image)
        session.commit()
        session.refresh(image)

        assert image.guid is not None
        assert image.title == image_data["title"]

    def test_bulk_create_images(self, session):
        images = [
            ImageModel(
                title="Test title 1", short_description="short", description="desc"
            ),
            ImageModel(
                title="Another title", short_description="short", description="desc"
            ),
            ImageModel(
                title="Test title 3", short_description="short", description="desc"
            ),
        ]
        session.add_all(images)
        session.commit()

        result = session.exec(select(ImageModel)).all()
        assert len(result) == 3

    def test_select_image_model_by_title(self, session):
        session.add_all(
            [
                ImageModel(
                    title="Test title 1", short_description="desc", description="..."
                ),
                ImageModel(
                    title="Special image", short_description="desc", description="..."
                ),
            ]
        )
        session.commit()

        from sqlalchemy import func

        stmt = select(ImageModel).where(func.lower(ImageModel.title).like("%title%"))
        results = session.exec(stmt).all()

        assert any("title" in img.title.lower() for img in results)

    def test_update_image_model(self, session):
        image = ImageModel(
            title="Old Title", short_description="desc", description="..."
        )
        session.add(image)
        session.commit()

        image.title = "New Title"
        session.add(image)
        session.commit()

        updated = session.exec(
            select(ImageModel).where(ImageModel.guid == image.guid)
        ).first()
        assert updated.title == "New Title"

    def test_delete_image_model(self, session):
        image = ImageModel(
            title="Delete Me", short_description="desc", description="..."
        )
        session.add(image)
        session.commit()

        session.delete(image)
        session.commit()

        deleted = session.exec(
            select(ImageModel).where(ImageModel.guid == image.guid)
        ).first()
        assert deleted is None

    def test_repr_and_str(self, session):
        image = ImageModel(title="Nice", short_description="short", description="long")
        assert "Nice" in str(image)
