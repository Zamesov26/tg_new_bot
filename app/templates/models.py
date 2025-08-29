import enum

from sqlalchemy import Column, Integer, String, Enum, UniqueConstraint, Text

from app.database.sqlalchemy_base import BaseModel


class TemplateType(str, enum.Enum):
    PAGE = "page"
    PAGINATE = "paginate"
    # TODO можно подумать о других типах шаблонов

class Template(BaseModel):
    __tablename__ = "templates"
    __table_args__ = (
        UniqueConstraint("type", "model", name="uq_template_type_model"),
    )

    id = Column(Integer, primary_key=True)
    type = Column(Enum(TemplateType), nullable=False)
    model = Column(String(128), nullable=False)
    list_template = Column(Text, nullable=False)
    list_image_path = Column(String(256), nullable=True)
    item_template = Column(Text, nullable=True)
    
    