from sqlalchemy.orm import DeclarativeBase


class BaseModel(DeclarativeBase):
    custom_registry = {}
    
    def __init_subclass__(cls, **kwargs):
        super().__init_subclass__(**kwargs)
        BaseModel.custom_registry[cls.__name__.lower()] = cls