from .time_stamped_uuid import TimeStampedUUIDModel


class ImageModel(TimeStampedUUIDModel, table=True):
    __tablename__ = "image_model"

    title: str
    short_description: str
    description: str
