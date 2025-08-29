# models/__init__.py
from sqlalchemy.orm import declarative_base, Mapped, mapped_column
from sqlalchemy import DateTime, func, Integer
from typing import Type, TypeVar, List, Any, Optional

Base = declarative_base()
T = TypeVar("T", bound="CRUDMixin")


class TimestampMixin:
    """Mixin adding created_at / updated_at timestamps."""

    _created_at_col: Mapped[Any] = mapped_column(
        "created_at",
        DateTime,
        server_default=func.now(),
        nullable=False
    )
    _updated_at_col: Mapped[Any] = mapped_column(
        "updated_at",
        DateTime,
        server_default=func.now(),
        onupdate=func.now(),
        nullable=False
    )

    @property
    def created_at(self) -> Any:
        return self._created_at_col

    @property
    def updated_at(self) -> Any:
        return self._updated_at_col


class CRUDMixin:
    """Basic CRUD helpers with a private id column."""

    _id_col: Mapped[int] = mapped_column("id", Integer, primary_key=True)

    @property
    def id(self) -> int:
        return self._id_col

    @classmethod
    def create(cls: Type[T], session, **kwargs) -> T:
        obj = cls(**kwargs)
        session.add(obj)
        session.commit()
        session.refresh(obj)
        return obj

    def delete(self, session) -> None:
        session.delete(self)
        session.commit()

    @classmethod
    def get_all(cls: Type[T], session) -> List[T]:
        return session.query(cls).all()

    @classmethod
    def find_by_id(cls: Type[T], session, obj_id: int) -> Optional[T]:
        # Must use filter() with attribute comparison, not filter_by()
        return session.query(cls).filter(cls._id_col == obj_id).first()

    @classmethod
    def find_by_attribute(cls: Type[T], session, **kwargs) -> List[T]:
        return session.query(cls).filter_by(**kwargs).all()
