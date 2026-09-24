from datetime import datetime, timezone

from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import String, Text
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column

class Base(DeclarativeBase):
    pass 
db = SQLAlchemy(model_class=Base)

class Note(db.Model): 
    id: Mapped[int] = mapped_column(primary_key=True, index=True, nullable=False)
    title: Mapped[str] = mapped_column(String(100), unique=True, nullable=False)
    content: Mapped[str] = mapped_column(Text, nullable=True)
    created_at: Mapped[datetime] = mapped_column(default=lambda: datetime.now(timezone.utc))
    updated_at: Mapped[datetime] = mapped_column( default=lambda: datetime.now(timezone.utc), onupdate=lambda: datetime.now(timezone.utc))