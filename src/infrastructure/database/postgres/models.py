import uuid
from datetime import datetime

from sqlalchemy import Integer, BigInteger, String, DateTime, Text, ForeignKey, Boolean, UUID
from sqlalchemy.orm import declarative_base, Mapped, mapped_column

Base = declarative_base()


class BaseCategory(Base):
    """Базовые категории на что будет классификация"""
    __tablename__ = 'base_y'

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    name: Mapped[str] = mapped_column(String, nullable=False, unique=True)

class ArticleTable(Base):
    __tablename__ = 'articles'

    id: Mapped[uuid] = mapped_column(UUID, primary_key=True)

    ad_url: Mapped[str] = mapped_column(String, nullable=False, unique=True)
    can_load: Mapped[bool] = mapped_column(Boolean, default=True)

    ad_create_ad: Mapped[datetime] = mapped_column(DateTime, nullable=True)  # дата публикации с сайта
    create_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.now)
    text: Mapped[str] = mapped_column(Text, nullable=True)
    title: Mapped[str] = mapped_column(String, nullable=True)

    category: Mapped[str] = mapped_column(String, nullable=True)
    base_category_id: Mapped[int] = mapped_column(ForeignKey(BaseCategory.id, ondelete='SET NULL'), nullable=True)

    page: Mapped[int] = mapped_column(Integer, nullable=True)

