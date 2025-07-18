from sqlmodel import Session, SQLModel, create_engine

from models import ImageModel

engine = create_engine("sqlite:///db.sqlite3")
SQLModel.metadata.create_all(engine)

with Session(engine) as session:
    image = ImageModel(
        title="Sample Image",
        short_description="This is simple short description.",
        description="The interpreter might be using UUID of your actual field uuid instead of the imported package. So, you can change the code as follows. ",
    )
    session.add(image)
    session.commit()
