from models.image import ImageModel


def test_create_image_model(session):
    for i in range(16):
        image = ImageModel(title=f"Test title {i}", short_description="Simple description for image model test", description="I can not keep up long text\n"*16)

        session.add(image)
        session.commit()

def test_select_image_model(session):
    search_title_contains_1 = session.exec(ImageModel.select().where(ImageModel.ilike("%title 1%"))).all()
    assert len(search_title_contains_1) == 3

