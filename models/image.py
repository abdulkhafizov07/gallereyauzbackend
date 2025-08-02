from .time_stamped_uuid import TimeStampedUUIDModel


class ImageModel(TimeStampedUUIDModel, table=True):
    __tablename__ = "image_model"

    image: str
    title: str
    short_description: str
    description: str
