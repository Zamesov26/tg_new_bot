from hashlib import sha256

from sqlalchemy.orm import Mapped, mapped_column

from app.database.sqlalchemy_base import BaseModel


def hash_password(password):
    return sha256(password.encode()).hexdigest()


def admin_from_session(session):
    return AdminModel(
        id=session["admin"]["id"], email=session["admin"]["email"]
    )


class AdminModel(BaseModel):
    __tablename__ = "admins"

    id: Mapped[int] = mapped_column(primary_key=True)
    email: Mapped[str]
    password: Mapped[str]

    def to_dict(self):
        return {"id": self.id, "email": self.email, "password": self.password}
