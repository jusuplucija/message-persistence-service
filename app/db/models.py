from sqlalchemy import Boolean, DateTime, Enum, Text
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column

from app.db.base import Base
from app.schemas.message import RoleEnum


class Message(Base):
    __tablename__ = "messages"

    message_id: Mapped[str] = mapped_column(UUID(as_uuid=True), primary_key=True)
    chat_id: Mapped[str] = mapped_column(UUID(as_uuid=True), nullable=False, index=True)
    content: Mapped[str] = mapped_column(Text, nullable=False)
    rating: Mapped[bool] = mapped_column(Boolean, nullable=False)
    sent_at: Mapped[DateTime] = mapped_column(DateTime(timezone=True), nullable=False)
    role: Mapped[RoleEnum] = mapped_column(Enum(RoleEnum), nullable=False)