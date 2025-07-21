from .time_stamped_uuid import TimeStampedUUIDModel


class CategoryModel(TimeStampedUUIDModel, table=True):
    __tablename__ = "category_model"

    title: str
