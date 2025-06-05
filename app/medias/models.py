import enum

from sqlalchemy import Column, Enum, Integer, String, Text

from app.database.sqlalchemy_base import BaseModel


class MediaType(enum.Enum):
    photo = "photo"


class Media(BaseModel):
    __tablename__ = "media"

    id = Column(Integer, primary_key=True)
    title = Column(String(256), nullable=False)
    file_id = Column(String(256), nullable=True, unique=True)
    url = Column(String(512), nullable=True)
    file_path = Column(String(512), nullable=True)

    type = Column(Enum(MediaType), default=MediaType.photo)
    caption = Column(Text, nullable=True)
