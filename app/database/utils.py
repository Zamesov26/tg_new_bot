from app.database.sqlalchemy_base import BaseModel


def resolve_model_by_name(name: str):
    try:
        return BaseModel.custom_registry[name.lower()]
    except KeyError:
        raise ValueError(f"Unknown model name: {name}")