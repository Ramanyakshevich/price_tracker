from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column
from sqlalchemy import BigInteger, ForeignKey, String

class Base(DeclarativeBase):
    pass

class User(Base):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(primary_key=True)
    tg_id: Mapped[int] = mapped_column(BigInteger, unique=True, index=True)
    username: Mapped[str] = mapped_column(String(50), nullable=True)

class TrackedItem(Base):
    __tablename__ = "tracked_items"

    id: Mapped[int] = mapped_column(primary_key=True)
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"))
    city_from: Mapped[str] = mapped_column(String(50))
    city_to: Mapped[str] = mapped_column(String(50))
    target_price: Mapped[int] = mapped_column()