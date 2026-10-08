from datetime import datetime, timezone

from sqlalchemy import DateTime, String
from sqlalchemy.orm import mapped_column, Mapped

from app.models.base import Base


class User(Base):

    __tablename__ = "users"

    id: Mapped[int] = mapped_column(primary_key=True)

    username: Mapped[str] = mapped_column(String(100), unique=True, nullable=False)

    first_name: Mapped[str] = mapped_column(String(100), nullable=False)

    last_name: Mapped[str | None] = mapped_column(String(100), nullable=True)

    age: Mapped[int] = mapped_column(nullable=False)

    gender: Mapped[str] = mapped_column(String(20), nullable=False)

    email: Mapped[str] = mapped_column(
        String(150), unique=True, nullable=False, index=True
    )

    hashed_password: Mapped[str] = mapped_column(String(255), nullable=False)

    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        nullable=False,
        default=lambda: datetime.now(timezone.utc),
    )
